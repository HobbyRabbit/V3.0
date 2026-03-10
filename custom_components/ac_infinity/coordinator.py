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
from .protocol import *
from .decoder import ACInfinityDecoder
from .packet_logger import PacketLogger

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

        self.decoder = ACInfinityDecoder()
        self.logger = PacketLogger()

        self.learning_mode = True

    async def _ensure_connected(self):

        if self.client and self.client.is_connected:
            return

        ble_device = async_ble_device_from_address(self.hass, self.mac)

        if not ble_device:
            raise UpdateFailed("BLE device not found")

        self.client = await establish_connection(
            BleakClient,
            ble_device,
            self.name
        )

        await self.client.start_notify(
            NOTIFY_UUID,
            self._notification_handler
        )

    def _notification_handler(self, sender, data):

        if self.learning_mode:
            self.logger.log("notify", data)

        state = self.decoder.decode(data)

        self.async_set_updated_data(state)

    async def _async_update_data(self):

        await self._ensure_connected()

        packet = build_status_request()

        self.logger.log("write", packet)

        await self.client.write_gatt_char(
            WRITE_UUID,
            packet,
            response=True
        )

        return self.decoder.state

    async def set_port(self, port, state):

        packet = build_set_port(port, state)

        self.logger.log("write", packet)

        await self.client.write_gatt_char(
            WRITE_UUID,
            packet,
            response=True
        )

    async def set_speed(self, speed):

        packet = build_set_speed(speed)

        self.logger.log("write", packet)

        await self.client.write_gatt_char(
            WRITE_UUID,
            packet,
            response=True
        )
