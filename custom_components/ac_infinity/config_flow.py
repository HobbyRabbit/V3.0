import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components.bluetooth import async_discovered_service_info
from .const import DOMAIN


class ACInfinityConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input=None):

        devices = async_discovered_service_info(self.hass)

        choices = {
            d.address: f"{d.name} ({d.address})"
            for d in devices
            if "AC Infinity" in (d.name or "")
        }

        if user_input is not None:

            mac = user_input["mac"]

            return self.async_create_entry(
                title=mac,
                data={"mac": mac},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("mac"): vol.In(choices)
                }
            ),
        )
