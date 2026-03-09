from homeassistant.components.fan import FanEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([ACInfinityFan(coordinator)])


class ACInfinityFan(CoordinatorEntity, FanEntity):

    def __init__(self, coordinator):

        super().__init__(coordinator)

        self._attr_name = "AC Infinity Fan"

    @property
    def percentage(self):

        return self.coordinator.data.get("speed", 0) * 10
