"""Support for WeatherFlow Forecast weather service."""
from __future__ import annotations

from typing import Any

from homeassistant.components.weather import (
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_TIME,
    ATTR_WEATHER_DEW_POINT,
    ATTR_WEATHER_HUMIDITY,
    ATTR_WEATHER_PRESSURE,
    ATTR_WEATHER_TEMPERATURE,
    ATTR_WEATHER_WIND_BEARING,
    ATTR_WEATHER_WIND_GUST_SPEED,
    ATTR_WEATHER_WIND_SPEED,
    DOMAIN as WEATHER_DOMAIN,
    Forecast,
    SingleCoordinatorWeatherEntity,
    WeatherEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_NAME,
    UnitOfPrecipitationDepth,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.unit_system import METRIC_SYSTEM

from . import WeatherFlowForecastDataUpdateCoordinator
from .const import DOMAIN, CONF_API_TOKEN, CONF_STATION_ID

DEFAULT_NAME = "WeatherFlow Forecast"

async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Add a weather entity from a config_entry."""
    coordinator: WeatherFlowForecastDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    entity_registry = er.async_get(hass)

    entities = [WeatherFlowWeather(coordinator, config_entry.data,
                                   hass.config.units is METRIC_SYSTEM, False)]

    async_add_entities(entities)

class WeatherFlowWeather(SingleCoordinatorWeatherEntity[WeatherFlowForecastDataUpdateCoordinator]):
    """Implementation of a WeatherFlow weather condition."""

    _attr_attribution = (
        "Weather Forecast from Better Forecast delivered by WeatherFlow"
    )
    _attr_has_entity_name = True
    _attr_native_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_native_precipitation_unit = UnitOfPrecipitationDepth.MILLIMETERS
    _attr_native_pressure_unit = UnitOfPressure.HPA
    _attr_native_wind_speed_unit = UnitOfSpeed.METERS_PER_SECOND
    _attr_supported_features = (
        WeatherEntityFeature.FORECAST_DAILY | WeatherEntityFeature.FORECAST_HOURLY
    )
