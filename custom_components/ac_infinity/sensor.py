from homeassistant.components.sensor import SensorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        ACInfinityTemp(coordinator),
        ACInfinityHumidity(coordinator),
    ]

    async_add_entities(sensors)


class ACInfinityTemp(SensorEntity):

    def __init__(self, coordinator):

        self.coordinator = coordinator
        self._attr_name = "AC Infinity Temperature"


class ACInfinityHumidity(SensorEntity):

    def __init__(self, coordinator):

        self.coordinator = coordinator
        self._attr_name = "AC Infinity Humidity"
