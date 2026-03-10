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

        self.write_char = None
        self.notify_char = None

        self.decoder = ACInfinityDecoder()
        self.logger = PacketLogger()

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

        await self._discover_characteristics()

        await self.client.start_notify(
            self.notify_char,
            self._notification_handler
        )

        _LOGGER.debug("AC Infinity BLE connected")

    async def _discover_characteristics(self):

        services = await self.client.get_services()

        for service in services:

            for char in service.characteristics:

                props = char.properties

                if "write" in props and not self.write_char:
                    self.write_char = char.uuid

                if "notify" in props and not self.notify_char:
                    self.notify_char = char.uuid

        _LOGGER.debug("Write char: %s", self.write_char)
        _LOGGER.debug("Notify char: %s", self.notify_char)

    def _notification_handler(self, sender, data):

        self.logger.log("notify", data)

        state = self.decoder.decode(data)

        self.async_set_updated_data(state)

    async def _async_update_data(self):

        await self._ensure_connected()

        packet = status_request()

        self.logger.log("write", packet)

        await self.client.write_gatt_char(
            self.write_char,
            packet,
            response=True
        )

        return self.decoder.state

    async def set_port(self, port, state):

        packet = set_port(port, state)

        self.logger.log("write", packet)

        await self.client.write_gatt_char(
            self.write_char,
            packet,
            response=True
        )

    async def set_speed(self, speed):

        packet = set_speed(speed)

        self.logger.log("write", packet)

        await self.client.write_gatt_char(
            self.write_char,
            packet,
            response=True
        )
