from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant

from .const import UPDATE_INTERVAL
from .ble_device import ACInfinityBLE

_LOGGER = logging.getLogger(__name__)


class ACInfinityCoordinator(DataUpdateCoordinator):

    def __init__(self, hass: HomeAssistant, address: str):

        self.ble = ACInfinityBLE(address)

        super().__init__(
            hass,
            _LOGGER,
            name="ac_infinity",
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self):

        if not self.ble.connected:
            await self.ble.connect()

        data = await self.ble.get_status()

        return data
