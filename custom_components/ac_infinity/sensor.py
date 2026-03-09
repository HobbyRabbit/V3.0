from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        ACTemperature(coordinator, entry.entry_id),
        ACHumidity(coordinator, entry.entry_id),
        ACVPD(coordinator, entry.entry_id),
    ])


class ACTemperature(CoordinatorEntity, SensorEntity):

    _attr_device_class = "temperature"
    _attr_native_unit_of_measurement = "°C"

    def __init__(self, coordinator, entry_id):

        super().__init__(coordinator)

        self._attr_unique_id = f"{entry_id}_temp"
        self._attr_name = "AC Infinity Temperature"

    @property
    def native_value(self):

        return self.coordinator.data["temperature"]


class ACHumidity(CoordinatorEntity, SensorEntity):

    _attr_device_class = "humidity"
    _attr_native_unit_of_measurement = "%"

    def __init__(self, coordinator, entry_id):

        super().__init__(coordinator)

        self._attr_unique_id = f"{entry_id}_humidity"
        self._attr_name = "AC Infinity Humidity"

    @property
    def native_value(self):

        return self.coordinator.data["humidity"]


class ACVPD(CoordinatorEntity, SensorEntity):

    _attr_native_unit_of_measurement = "kPa"

    def __init__(self, coordinator, entry_id):

        super().__init__(coordinator)

        self._attr_unique_id = f"{entry_id}_vpd"
        self._attr_name = "AC Infinity VPD"

    @property
    def native_value(self):

        t = self.coordinator.data["temperature"]
        h = self.coordinator.data["humidity"]

        if t is None or h is None:
            return None

        svp = 0.6108 * (2.71828 ** ((17.27 * t) / (t + 237.3)))

        vpd = svp * (1 - h / 100)

        return round(vpd, 2)
