
from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    switches = []

    for port in range(1, 9):

        switches.append(
            ACInfinityPortSwitch(coordinator, port)
        )

    async_add_entities(switches)


class ACInfinityPortSwitch(SwitchEntity):

    def __init__(self, coordinator, port):

        self.coordinator = coordinator
        self.port = port
        self._attr_name = f"AC Infinity Port {port}"

    @property
    def is_on(self):

        return False
