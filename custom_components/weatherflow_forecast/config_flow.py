"""Config flow to configure WeatherFlow Forecast component."""
from __future__ import annotations

import logging
import voluptuous as vol
from typing import Any
from homeassistant import config_entries
from homeassistant.const import CONF_ID
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from pyweatherflow_forecast import WeatherFlow, WeatherFlowStationData

from .const import (
    DOMAIN,
    CONF_API_TOKEN,
    CONF_STATION_ID,
)

_LOGGER = logging.getLogger(__name__)

class WeatherFlowForecastHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config Flow for WeatherFlow Forecast."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        """Get the options flow for WeatherFlow Forecast."""
        return WeatherFlowForecastOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle a flow initialized by the user."""

        if user_input is None:
            return await self._show_setup_form(user_input)

        errors = {}
        session = async_create_clientsession(self.hass)

        try:
            weatherflow_api = WeatherFlow(user_input[CONF_STATION_ID],
                                          user_input[CONF_API_TOKEN], session=session)

            station_data: WeatherFlowStationData = await weatherflow_api.async_get_station()

        except:
            return await self._show_setup_form(errors)

        await self.async_set_unique_id(user_input[CONF_STATION_ID])
        self._abort_if_unique_id_configured

        return self.async_create_entry(
            title=station_data.station_name,
            data={
                CONF_ID: station_data.station_name,
                CONF_STATION_ID: user_input[CONF_STATION_ID],
                CONF_API_TOKEN: user_input[CONF_API_TOKEN],
            }

        )

    async def _show_setup_form(self, errors=None):
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_STATION_ID): int,
                    vol.Required(CONF_API_TOKEN): str,
                }
            ),
            errors=errors or {},
        )

class WeatherFlowForecastOptionsFlowHandler(config_entries.OptionsFlow):
    """Options Flow for WeatherFlow Forecast component."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize the WeatherFlow Forecast Options Flows."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Configure Options for WeatherFlow Forecast."""

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_STATION_ID, default=self._config_entry.options.get(CONF_STATION_ID, 0)): int,
                    vol.Required(CONF_API_TOKEN, default=self._config_entry.options.get(CONF_API_TOKEN, "")): str,
                }
            )
        )
