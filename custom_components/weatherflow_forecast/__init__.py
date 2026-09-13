"""WeatherFlow Forecast Platform."""

from __future__ import annotations

from datetime import timedelta
import logging
from random import randrange
from types import MappingProxyType
from typing import Any, Self, cast

from pyweatherflow_forecast import (
    WeatherFlow,
    WeatherFlowForecastData,
    WeatherFlowForecastDaily,
    WeatherFlowForecastHourly,
    WeatherFlowForecastUnauthorized,
    WeatherFlowForecastBadRequest,
    WeatherFlowForecastInternalServerError,
    WeatherFlowForecastWongStationId,
    WeatherFlowSensorData,
    WeatherFlowStationData,
)

from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import (
    HomeAssistantError,
    ConfigEntryNotReady,
    Unauthorized,
)
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.loader import async_get_integration

from .const import (
    DEFAULT_ADD_SENSOR,
    DEFAULT_FORECAST_HOURS,
    DOMAIN,
    CONF_ADD_SENSORS,
    CONF_API_TOKEN,
    CONF_FORECAST_HOURS,
    CONF_STATION_ID,
    STARTUP,
)

PLATFORMS = [Platform.WEATHER, Platform.SENSOR, Platform.BINARY_SENSOR]

_LOGGER = logging.getLogger(__name__)


def _get_platforms(config_entry: ConfigEntry) -> bool:
    val = config_entry.options.get(CONF_ADD_SENSORS)
    return DEFAULT_ADD_SENSOR if val is None else bool(val)


def _get_forecast_hours(config_entry: ConfigEntry) -> int:
    val = config_entry.options.get(CONF_FORECAST_HOURS)
    return DEFAULT_FORECAST_HOURS if val is None else int(val)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up WeatherFlow Forecast as config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Coerce legacy non-string unique_id to a string. Entries created before the
    # config flow started casting the station id (commit 73213aa) stored it as an
    # int, which Home Assistant now flags on every load. There is no migration for
    # those existing entries, so fix them up in place here.
    if config_entry.unique_id is not None and not isinstance(
        config_entry.unique_id, str
    ):
        hass.config_entries.async_update_entry(
            config_entry, unique_id=str(config_entry.unique_id)
        )

    integration = await async_get_integration(hass, DOMAIN)
    _LOGGER.info(STARTUP, integration.version, str(config_entry.data[CONF_STATION_ID]))

    add_sensors = _get_platforms(config_entry)
    forecast_hours = _get_forecast_hours(config_entry)

    coordinator = WeatherFlowForecastDataUpdateCoordinator(
        hass, config_entry, add_sensors, forecast_hours
    )
    if config_entry.state == ConfigEntryState.SETUP_IN_PROGRESS:
        await coordinator.async_config_entry_first_refresh()
    else:
        await coordinator.async_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    config_entry.async_on_unload(config_entry.add_update_listener(async_update_entry))

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    if not add_sensors:
        await cleanup_old_device(hass, str(config_entry.data[CONF_STATION_ID]))

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )

    hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok


async def async_update_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Reload WeatherFlow Forecast component when options changed."""
    await hass.config_entries.async_reload(config_entry.entry_id)


async def cleanup_old_device(hass: HomeAssistant, station_id) -> None:
    """Cleanup device without proper device identifier."""
    device_reg = dr.async_get(hass)
    device = device_reg.async_get_device(identifiers={(DOMAIN, station_id)})  # type: ignore[arg-type]
    if device:
        _LOGGER.debug("Removing deselected sensors: %s", device.name)
        device_reg.async_remove_device(device.id)
    device = device_reg.async_get_device(identifiers={(DOMAIN, f"{station_id}_binary")})  # type: ignore[arg-type]
    if device:
        _LOGGER.debug("Removing deselected sensors: %s", device.name)
        device_reg.async_remove_device(device.id)


async def async_migrate_station_id(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    old_station_id: str,
    new_station_id: str,
) -> None:
    """Move entities and devices from an old Station ID to a new one.

    Used when a physical station is replaced and WeatherFlow issues a new
    Station ID for it. Entity/device unique IDs and device identifiers are
    built with the Station ID as a prefix (see sensor.py, binary_sensor.py
    and weather.py), so they are rewritten here to keep the existing
    entity_ids, names, history and customizations intact instead of
    Home Assistant treating the reconfigured station as brand new hardware.
    """
    if old_station_id == new_station_id:
        return

    entity_reg = er.async_get(hass)
    for entry in er.async_entries_for_config_entry(entity_reg, config_entry.entry_id):
        if not entry.unique_id.startswith(old_station_id):
            continue
        new_unique_id = new_station_id + entry.unique_id[len(old_station_id) :]
        entity_reg.async_update_entity(entry.entity_id, new_unique_id=new_unique_id)

    device_reg = dr.async_get(hass)
    for device in dr.async_entries_for_config_entry(device_reg, config_entry.entry_id):
        new_identifiers = set()
        changed = False
        for identifier in device.identifiers:
            if len(identifier) != 2 or identifier[0] != DOMAIN:
                new_identifiers.add(identifier)
                continue
            ident = identifier[1]
            if ident == old_station_id:
                new_identifiers.add((DOMAIN, new_station_id))
                changed = True
            elif ident == f"{old_station_id}_binary":
                new_identifiers.add((DOMAIN, f"{new_station_id}_binary"))
                changed = True
            else:
                new_identifiers.add(identifier)
        if changed:
            device_reg.async_update_device(device.id, new_identifiers=new_identifiers)


class CannotConnect(HomeAssistantError):
    """Unable to connect to the web site."""


class WeatherFlowForecastDataUpdateCoordinator(
    DataUpdateCoordinator["WeatherFlowForecastWeatherData"]
):
    """Class to manage fetching WeatherFlow data."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        add_sensors: bool,
        forecast_hours: int,
    ) -> None:
        """Initialize global WeatherFlow forecast data updater."""
        self.weather = WeatherFlowForecastWeatherData(
            hass, config_entry.data, add_sensors, forecast_hours
        )
        self.weather.initialize_data()
        self.hass = hass
        self.config_entry = config_entry
        self.add_sensors = add_sensors
        self.forecast_hours = forecast_hours

        if add_sensors:
            update_interval = timedelta(minutes=randrange(1, 5))
        else:
            update_interval = timedelta(minutes=randrange(25, 35))

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
            config_entry=config_entry,
        )

    async def _async_update_data(self) -> WeatherFlowForecastWeatherData:
        """Fetch data from WeatherFlow Forecast."""
        try:
            return await self.weather.fetch_data()
        except Exception as err:
            raise UpdateFailed(f"Update failed: {err}") from err


class WeatherFlowForecastWeatherData:
    """Keep data for WeatherFlow Forecast entity data."""

    def __init__(
        self,
        hass: HomeAssistant,
        config: MappingProxyType[str, Any],
        add_sensors: bool,
        forecast_hours: int,
    ) -> None:
        """Initialise the weather entity data."""
        self.hass = hass
        self._config = config
        self._add_sensors = add_sensors
        self._forecast_hours = forecast_hours
        self._weather_data: WeatherFlow
        self.current_weather_data: WeatherFlowForecastData | None = None
        self.daily_forecast: list[WeatherFlowForecastDaily] = []
        self.hourly_forecast: list[WeatherFlowForecastHourly] = []
        self.sensor_data: WeatherFlowSensorData | None = None
        self.station_data: WeatherFlowStationData | None = None

    def initialize_data(self) -> bool:
        """Establish connection to API."""

        self._weather_data = WeatherFlow(
            int(self._config[CONF_STATION_ID]),
            self._config[CONF_API_TOKEN],
            elevation=self.hass.config.elevation,
            session=async_get_clientsession(self.hass),
            forecast_hours=self._forecast_hours,
        )

        return True

    async def fetch_data(self) -> Self:
        """Fetch data from API - (current weather and forecast)."""

        try:
            forecast_data = cast(
                WeatherFlowForecastData, await self._weather_data.async_get_forecast()
            )
        except WeatherFlowForecastWongStationId as unauthorized:
            _LOGGER.debug(unauthorized)
            raise Unauthorized from unauthorized
        except WeatherFlowForecastBadRequest as err:
            _LOGGER.debug(err)
            raise UpdateFailed(str(err)) from err
        except WeatherFlowForecastUnauthorized as unauthorized:
            _LOGGER.debug(unauthorized)
            raise Unauthorized from unauthorized
        except WeatherFlowForecastInternalServerError as notreadyerror:
            _LOGGER.debug(notreadyerror)
            raise ConfigEntryNotReady from notreadyerror

        if not forecast_data:
            raise CannotConnect()
        self.current_weather_data = forecast_data
        self.daily_forecast = cast(
            list[WeatherFlowForecastDaily], forecast_data.forecast_daily
        )
        self.hourly_forecast = cast(
            list[WeatherFlowForecastHourly], forecast_data.forecast_hourly
        )

        if self._add_sensors:
            try:
                sensor_data = cast(
                    WeatherFlowSensorData,
                    await self._weather_data.async_fetch_sensor_data(),
                )
                station_info = cast(
                    WeatherFlowStationData,
                    await self._weather_data.async_get_station(),
                )
            except WeatherFlowForecastWongStationId as unauthorized:
                _LOGGER.debug(unauthorized)
                raise Unauthorized from unauthorized
            except WeatherFlowForecastBadRequest as err:
                _LOGGER.debug(err)
                raise UpdateFailed(str(err)) from err
            except WeatherFlowForecastUnauthorized as unauthorized:
                _LOGGER.debug(unauthorized)
                raise Unauthorized from unauthorized
            except WeatherFlowForecastInternalServerError as notreadyerror:
                _LOGGER.debug(notreadyerror)
                raise ConfigEntryNotReady from notreadyerror

            if not sensor_data or not station_info:
                raise CannotConnect()
            self.sensor_data = sensor_data
            self.station_data = station_info
            if not self.sensor_data.data_available:
                _LOGGER.warning(
                    "Weather Station either is offline or no recent observations from station. Remove Sensors to avoid this warning."
                )

        return self
