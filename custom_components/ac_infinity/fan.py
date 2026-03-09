import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .ble_device import ACInfinityBLE
from .const import DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class ACInfinityCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, entry):

        self.hass = hass

        self.address = entry.data["address"]

        self.ble = ACInfinityBLE(self.address)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self):

        await self.ble.connect()

        return await self.ble.request_state()

    async def set_port_speed(self, port, speed):

        await self.ble.set_speed(port, speed)

        await self.async_request_refresh()

    async def set_port_power(self, port, state):

        await self.ble.set_power(port, state)

        await self.async_request_refresh()
