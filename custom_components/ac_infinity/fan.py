from homeassistant.components.fan import FanEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([ACInfinityFan(coordinator)])


class ACInfinityFan(FanEntity):

    def __init__(self, coordinator):

        self.coordinator = coordinator
        self._attr_name = "AC Infinity Fan"

    @property
    def is_on(self):

        return False
