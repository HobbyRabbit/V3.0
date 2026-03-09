from homeassistant.components.fan import FanEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, PORT_COUNT


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    fans = []

    for port in range(1, PORT_COUNT + 1):

        fans.append(ACInfinityFan(coordinator, entry.entry_id, port))

    async_add_entities(fans)


class ACInfinityFan(CoordinatorEntity, FanEntity):

    def __init__(self, coordinator, entry_id, port):

        super().__init__(coordinator)

        self.port = port

        self._attr_unique_id = f"{entry_id}_fan_{port}"

        self._attr_name = f"AC Infinity Port {port}"

    @property
    def percentage(self):

        return self.coordinator.data["ports"].get(self.port)

    async def async_set_percentage(self, percentage):

        await self.coordinator.set_port_speed(self.port, percentage)

    async def async_turn_on(self, percentage=None, preset_mode=None, **kwargs):

        if percentage is None:
            percentage = 100

        await self.coordinator.set_port_speed(self.port, percentage)

    async def async_turn_off(self, **kwargs):

        await self.coordinator.set_port_speed(self.port, 0)
