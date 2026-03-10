from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            ACInfinityTemp(coordinator),
            ACInfinityHumidity(coordinator),
        ]
    )


class ACInfinityTemp(CoordinatorEntity, SensorEntity):

    def __init__(self, coordinator):

        super().__init__(coordinator)

        self._attr_name = "AC Infinity Temperature"
        self._attr_unique_id = f"{coordinator.mac}_temp"
        self._attr_native_unit_of_measurement = "°C"

    @property
    def native_value(self):
        return self.coordinator.data["temperature"]


class ACInfinityHumidity(CoordinatorEntity, SensorEntity):

    def __init__(self, coordinator):

        super().__init__(coordinator)

        self._attr_name = "AC Infinity Humidity"
        self._attr_unique_id = f"{coordinator.mac}_humidity"
        self._attr_native_unit_of_measurement = "%"

    @property
    def native_value(self):
        return self.coordinator.data["humidity"]
