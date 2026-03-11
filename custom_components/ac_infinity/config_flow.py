from __future__ import annotations

from homeassistant import config_entries
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak
from homeassistant.const import CONF_MAC

from .const import DOMAIN


class ACInfinityConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_bluetooth(
        self,
        discovery_info: BluetoothServiceInfoBleak,
    ):

        address = discovery_info.address

        await self.async_set_unique_id(address)
        self._abort_if_unique_id_configured()

        self.context["title_placeholders"] = {
            "name": discovery_info.name or address
        }

        return await self.async_step_confirm()

    async def async_step_confirm(self, user_input=None):

        if user_input is not None:

            return self.async_create_entry(
                title=self.context["title_placeholders"]["name"],
                data={"mac": self.unique_id},
            )

        return self.async_show_form(step_id="confirm")
