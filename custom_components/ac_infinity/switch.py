from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, PORT_COUNT


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    switches = []

    for port in range(1, PORT_COUNT + 1):

        switches.append(ACInfinitySwitch(coordinator, entry.entry_id, port))

    async_add_entities(switches)


class ACInfinitySwitch(CoordinatorEntity, SwitchEntity):

    def __init__(self, coordinator, entry_id, port):

        super().__init__(coordinator)

        self.port = port

        self._attr_unique_id = f"{entry_id}_power_{port}"
        self._attr_name = f"AC Infinity Port {port} Power"

    @property
    def is_on(self):
        return self.coordinator.data["ports"].get(self.port, 0) > 0

    async def async_turn_on(self, **kwargs):
        await self.coordinator.set_port_power(self.port, True)

    async def async_turn_off(self, **kwargs):
        await self.coordinator.set_port_power(self.port, False)
