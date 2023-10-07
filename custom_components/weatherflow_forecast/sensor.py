"""Support for WeatherFlow sensor data."""
from __future__ import annotations

import logging

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_NAME,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    LIGHT_LUX,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from . import WeatherFlowForecastDataUpdateCoordinator
from .const import (
    ATTR_ATTRIBUTION,
    CONF_STATION_ID,
    CONFIG_URL,
    DOMAIN,
    MANUFACTURER,
    MODEL
)

@dataclass
class WeatherFlowSensorEntityDescription(SensorEntityDescription):
    """Describes WeatherFlow sensor entity."""


SENSOR_TYPES: tuple[WeatherFlowSensorEntityDescription, ...] = (
    WeatherFlowSensorEntityDescription(
        key="air_density",
        name="Air Density",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    WeatherFlowSensorEntityDescription(
        key="air_temperature",
        name="Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    WeatherFlowSensorEntityDescription(
        key="barometric_pressure",
        name="Barometric Pressure",
        native_unit_of_measurement=UnitOfPressure.HPA,
        device_class=SensorDeviceClass.ATMOSPHERIC_PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    WeatherFlowSensorEntityDescription(
        key="brightness",
        name="Illuminance",
        native_unit_of_measurement=LIGHT_LUX,
        device_class=SensorDeviceClass.ILLUMINANCE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    WeatherFlowSensorEntityDescription(
        key="delta_t",
        name="Delta T",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,

    ),
    WeatherFlowSensorEntityDescription(
        key="dew_point",
        name="Dew Point",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    WeatherFlowSensorEntityDescription(
        key="feels_like",
        name="Apparent Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    WeatherFlowSensorEntityDescription(
        key="heat_index",
        name="Heat Index",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    WeatherFlowSensorEntityDescription(
        key="wind_gust",
        name="Wind Gust",
        native_unit_of_measurement=UnitOfSpeed.METERS_PER_SECOND,
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """WeatherFlow sensor platform."""
    coordinator: WeatherFlowForecastDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    if coordinator.data.sensor_data == {}:
        return

    entities: list[WeatherFlowSensor[Any]] = [
        WeatherFlowSensor(coordinator, description, config_entry)
        for description in SENSOR_TYPES
    ]

    async_add_entities(entities, False)

class WeatherFlowSensor(CoordinatorEntity[DataUpdateCoordinator], SensorEntity):
    """A WeatherFlow sensor."""

    entity_description: WeatherFlowSensorEntityDescription

    def __init__(self,
                 coordinator: WeatherFlowForecastDataUpdateCoordinator,
                 description: WeatherFlowSensorEntityDescription,
                 config: MappingProxyType[str, Any]
                 ) -> None:
        """Initialize a WeatherFlow sensor."""
        super().__init__(coordinator)
        self.entity_description = description

        self._attr_attribution = ATTR_ATTRIBUTION
        self._attr_name = f"{config.data[CONF_NAME]} {description.name}"
        self._attr_unique_id = f"{config.data[CONF_STATION_ID]} {description.key}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        assert self.platform.config_entry and self.platform.config_entry.unique_id
        return DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, self.platform.config_entry.unique_id)},
            manufacturer=MANUFACTURER,
            model=MODEL,
            name="Sensors",
            configuration_url=CONFIG_URL,
        )

    @property
    def native_value(self) -> StateType:
        """Return state of the sensor."""

        return (
            getattr(self.coordinator.data.sensor_data, self.entity_description.key)
            if self.coordinator.data.sensor_data else None
        )
