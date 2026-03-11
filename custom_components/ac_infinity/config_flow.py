from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_MAC
from homeassistant.core import callback

from .const import DOMAIN


class ACInfinityConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AC Infinity."""

    VERSION = 1

    async def async_step_user(self, user_input=None):

        errors = {}

        if user_input is not None:

            return self.async_create_entry(
                title=user_input[CONF_MAC],
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_MAC): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):

        return ACInfinityOptionsFlow(config_entry)


class ACInfinityOptionsFlow(config_entries.OptionsFlow):

    def __init__(self, config_entry):

        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):

        return self.async_create_entry(title="", data={})
