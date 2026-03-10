import logging
from datetime import timedelta

from bleak import BleakClient
from bleak_retry_connector import establish_connection

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from homeassistant.components.bluetooth import async_ble_device_from_address

from .const import *

_LOGGER = logging.getLogger(__name__)


class ACInfinityCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, mac, name):

        super().__init__(
            hass,
            _LOGGER,
            name=name,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

        self.mac = mac
        self.client = None

        self.state = {
            "temperature": None,
            "humidity": None,
            "ports": [False] * 8,
            "fan_speed": 0,
        }

        self.learning_mode = False

    async def _ensure_connected(self):

        if self.client and self.client.is_connected:
            return

        ble_device = async_ble_device_from_address(self.hass, self.mac)

        if not ble_device:
            raise UpdateFailed(f"Device {self.mac} not found")

        try:

            self.client = await establish_connection(
                BleakClient,
                ble_device,
                self.name,
            )

            await self.client.start_notify(
                NOTIFY_UUID,
                self._notification_handler,
            )

        except Exception as err:
            raise UpdateFailed(f"BLE connect failed: {err}") from err

    def _notification_handler(self, sender, data):

        if self.learning_mode:
            _LOGGER.warning("LEARNING PACKET: %s", data.hex())

        try:

            if len(data) > 10:

                temp = data[8]
                hum = data[9]

                self.state["temperature"] = float(temp)
                self.state["humidity"] = float(hum)

        except Exception as e:
            _LOGGER.debug("Parse error %s", e)

    async def _async_update_data(self):

        await self._ensure_connected()

        try:

            await self.client.write_gatt_char(
                WRITE_UUID,
                bytes([0xA1, 0x01, 0x00]),
                response=True,
            )

        except Exception as err:
            raise UpdateFailed(err)

        return self.state

    async def set_port(self, port, state):

        cmd = bytes([0xA2, port, 1 if state else 0])

        await self.client.write_gatt_char(
            WRITE_UUID,
            cmd,
            response=True,
        )

        self.state["ports"][port - 1] = state
        self.async_set_updated_data(self.state)

    async def set_speed(self, speed):

        cmd = bytes([0xA3, speed])

        await self.client.write_gatt_char(
            WRITE_UUID,
            cmd,
            response=True,
        )

        self.state["fan_speed"] = speed
        self.async_set_updated_data(self.state)
