"""Constants for WeatherFlow Forecast component."""

ATTR_ATTRIBUTION = "Weather data delivered by WeatherFlow"
ATTR_DESCRIPTION = "description"

BATTERY_MODE_DESCRIPTION = [
    "All sensors enabled and operating at full performance. Wind sampling interval every 3 seconds",
    "Wind sampling interval set to 6 seconds",
    "Wind sampling interval set to one minute",
    "Wind sampling interval set to 5 minutes. All other sensors sampling interval set to 5 minutes. Haptic Rain sensor disabled from active listening",
]

CONCENTRATION_GRAMS_PER_CUBIC_METER = "g/m³"
CONF_ADD_SENSORS = "add_sensors"
CONF_API_TOKEN = "api_token"
CONF_DEVICE_ID = "device_id"
CONF_FIRMWARE_REVISION = "firmware_revision"
CONF_SERIAL_NUMBER = "serial_number"
CONF_STATION_ID = "station_id"

DEFAULT_ADD_SENSOR = False
DEFAULT_NAME = "WeatherFlow Forecast"
DOMAIN = "weatherflow_forecast"

MANUFACTURER = "WeatherFlow"
MODEL = "Rest API"

TIMESTAMP_SENSORS = [
    "lightning_strike_last_epoch",
    "timestamp",
]
