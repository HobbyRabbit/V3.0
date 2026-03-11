import logging
from datetime import timedelta

from bleak import BleakClient
from bleak_retry_connector import establish_connection

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from homeassistant.components.bluetooth import async_ble_device_from_address

from .const import UPDATE_INTERVAL

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

    async def _ensure_connected(self):

        if self.client and self.client.is_connected:
            return

        device = async_ble_device_from_address(self.hass, self.mac)

        if not device:
            raise UpdateFailed("BLE device not found")

        self.client = await establish_connection(
            BleakClient,
            device,
            self.name,
        )

    async def _async_update_data(self):

        await self._ensure_connected()

        return {}
