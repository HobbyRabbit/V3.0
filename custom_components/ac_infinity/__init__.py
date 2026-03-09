from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import ACInfinityCoordinator


async def async_setup(hass: HomeAssistant, config: dict):
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):

    coordinator = ACInfinityCoordinator(
        hass,
        entry.data["address"]
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        ["fan", "sensor"]
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        ["fan", "sensor"]
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
