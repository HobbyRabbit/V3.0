from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([ACInfinityFan(coordinator)])


class ACInfinityFan(CoordinatorEntity, FanEntity):

    _attr_supported_features = FanEntityFeature.SET_SPEED
    _attr_speed_count = 10

    def __init__(self, coordinator):

        super().__init__(coordinator)

        self._attr_name = "AC Infinity Fan"
        self._attr_unique_id = f"{coordinator.mac}_fan"

    @property
    def percentage(self):
        return self.coordinator.data["fan_speed"] * 10

    async def async_set_percentage(self, percentage):

        speed = int(percentage / 10)

        await self.coordinator.set_speed(speed)
