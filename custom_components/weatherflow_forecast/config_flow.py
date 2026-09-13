"""Config flow to configure WeatherFlow Forecast component."""

from __future__ import annotations

import logging
import voluptuous as vol
from typing import Any, cast
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from pyweatherflow_forecast import (
    WeatherFlow,
    WeatherFlowStationData,
    WeatherFlowSensorData,
    WeatherFlowForecastBadRequest,
    WeatherFlowForecastInternalServerError,
    WeatherFlowForecastUnauthorized,
    WeatherFlowForecastWongStationId,
)
from . import async_migrate_station_id
from .const import (
    DEFAULT_ADD_SENSOR,
    DEFAULT_FORECAST_HOURS,
    DOMAIN,
    CONF_ADD_SENSORS,
    CONF_API_TOKEN,
    CONF_DEVICE_ID,
    CONF_FIRMWARE_REVISION,
    CONF_FORECAST_HOURS,
    CONF_SERIAL_NUMBER,
    CONF_STATION_ID,
)

_LOGGER = logging.getLogger(__name__)


class WeatherFlowForecastHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config Flow for WeatherFlow Forecast."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        """Get the options flow for WeatherFlow Forecast."""
        return WeatherFlowForecastOptionsFlowHandler(config_entry)

    async def _async_validate_and_fetch(
        self, station_id: str, api_token: str, add_sensors: bool
    ) -> tuple[WeatherFlowStationData | None, str | None]:
        """Validate a Station ID/API Token pair against the WeatherFlow API.

        Returns a tuple of (station_data, error_key). On success error_key is
        None; on failure station_data is None and error_key names the
        translation key to show on the form.
        """
        session = async_create_clientsession(self.hass)

        try:
            weatherflow_api = await self.hass.async_add_executor_job(
                lambda: WeatherFlow(
                    station_id,
                    api_token,
                    session=session,
                )
            )

            station_data = cast(
                WeatherFlowStationData, await weatherflow_api.async_get_station()
            )
            if add_sensors:
                sensor_data = cast(
                    WeatherFlowSensorData,
                    await weatherflow_api.async_fetch_sensor_data(),
                )
                if not sensor_data.data_available:
                    return None, "offline_error"
        except WeatherFlowForecastWongStationId as err:
            _LOGGER.debug(err)
            return None, "wrong_station_id"
        except WeatherFlowForecastBadRequest as err:
            _LOGGER.debug(err)
            return None, "bad_request"
        except WeatherFlowForecastInternalServerError as err:
            _LOGGER.debug(err)
            return None, "server_error"
        except WeatherFlowForecastUnauthorized as err:
            _LOGGER.debug("401 Error: %s", err)
            return None, "wrong_token"

        return station_data, None

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle a flow initialized by the user."""

        if user_input is None:
            return await self._show_setup_form()

        station_data, error = await self._async_validate_and_fetch(
            user_input[CONF_STATION_ID],
            user_input[CONF_API_TOKEN],
            user_input[CONF_ADD_SENSORS],
        )
        if error:
            return await self._show_setup_form({"base": error})

        await self.async_set_unique_id(str(user_input[CONF_STATION_ID]))
        self._abort_if_unique_id_configured(error="unique_id")

        return self.async_create_entry(
            title=station_data.station_name,
            data={
                CONF_NAME: station_data.station_name,
                CONF_STATION_ID: user_input[CONF_STATION_ID],
                CONF_API_TOKEN: user_input[CONF_API_TOKEN],
                CONF_DEVICE_ID: station_data.device_id,
                CONF_FIRMWARE_REVISION: station_data.firmware_revision,
                CONF_SERIAL_NUMBER: station_data.serial_number,
            },
            options={
                CONF_FORECAST_HOURS: user_input[CONF_FORECAST_HOURS],
                CONF_ADD_SENSORS: user_input[CONF_ADD_SENSORS],
            },
        )

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None):
        """Handle reconfiguration, e.g. when a station has been replaced.

        Lets the user point the existing config entry at a new Station ID
        (and API Token) without losing the entities, history and
        customizations already set up for it.
        """
        reconfigure_entry = self._get_reconfigure_entry()

        if user_input is None:
            return self._show_reconfigure_form(reconfigure_entry)

        add_sensors = reconfigure_entry.options.get(
            CONF_ADD_SENSORS, DEFAULT_ADD_SENSOR
        )
        station_data, error = await self._async_validate_and_fetch(
            user_input[CONF_STATION_ID], user_input[CONF_API_TOKEN], add_sensors
        )
        if error:
            return self._show_reconfigure_form(reconfigure_entry, {"base": error})

        new_station_id = str(user_input[CONF_STATION_ID])
        existing_entry = self.hass.config_entries.async_entry_for_domain_unique_id(
            DOMAIN, new_station_id
        )
        if existing_entry and existing_entry.entry_id != reconfigure_entry.entry_id:
            return self._show_reconfigure_form(reconfigure_entry, {"base": "unique_id"})

        old_station_id = str(reconfigure_entry.data[CONF_STATION_ID])
        await async_migrate_station_id(
            self.hass, reconfigure_entry, old_station_id, new_station_id
        )

        return self.async_update_reload_and_abort(
            reconfigure_entry,
            unique_id=new_station_id,
            title=station_data.station_name,
            data={
                **reconfigure_entry.data,
                CONF_NAME: station_data.station_name,
                CONF_STATION_ID: new_station_id,
                CONF_API_TOKEN: user_input[CONF_API_TOKEN],
                CONF_DEVICE_ID: station_data.device_id,
                CONF_FIRMWARE_REVISION: station_data.firmware_revision,
                CONF_SERIAL_NUMBER: station_data.serial_number,
            },
        )

    async def _show_setup_form(self, errors=None):
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_STATION_ID): str,
                    vol.Required(CONF_API_TOKEN): str,
                    vol.Optional(
                        CONF_FORECAST_HOURS, default=DEFAULT_FORECAST_HOURS
                    ): vol.All(vol.Coerce(int), vol.Range(min=12, max=96)),
                    vol.Optional(CONF_ADD_SENSORS, default=DEFAULT_ADD_SENSOR): bool,
                }
            ),
            errors=errors or {},
        )

    def _show_reconfigure_form(
        self, reconfigure_entry: config_entries.ConfigEntry, errors=None
    ):
        """Show the reconfigure form, pre-filled with the current values."""
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_STATION_ID,
                        default=reconfigure_entry.data[CONF_STATION_ID],
                    ): str,
                    vol.Required(
                        CONF_API_TOKEN,
                        default=reconfigure_entry.data[CONF_API_TOKEN],
                    ): str,
                }
            ),
            errors=errors or {},
        )


class WeatherFlowForecastOptionsFlowHandler(config_entries.OptionsFlow):
    """Options Flow for WeatherFlow Forecast component."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize the WeatherFlow Forecast Options Flows."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Configure Options for WeatherFlow Forecast."""

        if user_input is not None:
            self.hass.config_entries.async_update_entry(
                self._config_entry,
                data={
                    **self._config_entry.data,
                    CONF_API_TOKEN: user_input[CONF_API_TOKEN],
                },
            )
            return self.async_create_entry(
                title="",
                data={
                    CONF_FORECAST_HOURS: user_input[CONF_FORECAST_HOURS],
                    CONF_ADD_SENSORS: user_input[CONF_ADD_SENSORS],
                },
            )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_API_TOKEN,
                        default=self._config_entry.data.get(CONF_API_TOKEN, ""),
                    ): str,
                    vol.Optional(
                        CONF_FORECAST_HOURS,
                        default=self._config_entry.options.get(
                            CONF_FORECAST_HOURS, DEFAULT_FORECAST_HOURS
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=12, max=96)),
                    vol.Optional(
                        CONF_ADD_SENSORS,
                        default=self._config_entry.options.get(
                            CONF_ADD_SENSORS, DEFAULT_ADD_SENSOR
                        ),
                    ): bool,
                }
            ),
        )
