from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    for port in range(1, 9):
        entities.append(
            ACInfinityPortSwitch(coordinator, port)
        )

    async_add_entities(entities)


class ACInfinityPortSwitch(CoordinatorEntity, SwitchEntity):

    def __init__(self, coordinator, port):

        super().__init__(coordinator)

        self.port = port
        self._attr_name = f"AC Infinity Port {port}"
        self._attr_unique_id = f"{coordinator.mac}_port_{port}"

    @property
    def is_on(self):
        return self.coordinator.data["ports"][self.port - 1]

    async def async_turn_on(self, **kwargs):
        await self.coordinator.set_port(self.port, True)

    async def async_turn_off(self, **kwargs):
        await self.coordinator.set_port(self.port, False)
