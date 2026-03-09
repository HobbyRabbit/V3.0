from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        ACTemperature(coordinator),
        ACHumidity(coordinator)
    ])


class ACTemperature(CoordinatorEntity, SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "AC Infinity Temperature"

    @property
    def native_value(self):
        return self.coordinator.data.get("temperature")


class ACHumidity(CoordinatorEntity, SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "AC Infinity Humidity"

    @property
    def native_value(self):
        return self.coordinator.data.get("humidity")
