# WeatherFlow Forecast and Sensor integration for Home Assistant
Home Assistant integration for WeatherFlow Cloud Based Data using the REST API

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![Community Forum][forum-shield]][forum]

<a href="https://www.buymeacoffee.com/briis" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 40px !important;width: 145px !important;" ></a>

<p align="center">
  <img width="384" height="128" src="https://github.com/briis/weatherflow_forecast/blob/main/images/logo@2x.png?raw=true">
</p>

This integration adds support for retrieving the Forecast, Current condition and optionally realtime data from [WeatherFlow](https://shop.weatherflow.com/products/tempest). It replaces [WeatherFlow Weather for Home Assistant](https://github.com/briis/hass-weatherflow) that will soon be deprecated.

For this integration you **must own a WeatherFlow weather station** and you must create a **personal API Token** that work with your weather station. [See this link](https://weatherflow.github.io/Tempest/api/) for a description on how to retrieve the API Token.
**Note**: There are two types of authorization *oAuth* and *Personal API Token*. Make sure you use the later.

**Note**: All development is done using a *TEMPEST* device, so no testing of the code is done using the old AIR and SKY devices. It does not mean that it will not work with that setup, but some sensors will not be available and no testing is done.
Please do not add ask me to implement special features for these device, as it will not happen. This is open source, so you are welcome to create your own fork and implement as desired.

#### This integration will set up the following platforms.

Platform | Description
-- | --
`weather` | A Home Assistant `weather` entity, with current data, daily- and hourly forecast data.
`sensor` | A Home Assistant `sensor` entity, with all available sensor from the API, plus a few local calculated.
`binary_sensor` | A Home Assistant `binary_sensor` entity, with few local calculated binary sensors.

Minimum required version of Home Assistant is **2023.9.0** as this integration uses the new Weather entity forecast types and it does **not** create Forecast Attributes.

## Installation through HACS (Recommended Method)

This Integration is part of the default HACS store. Search for *WeatherFlow Forecast* under Integrations and install from there. After the installation of the files, you must restart Home Assistant, or else you will not be able to add WeatherFlow Forecast from the Integration Page.

If you are not familiar with HACS, or haven't installed it, I would recommend to [look through the HACS documentation](https://hacs.xyz/), before continuing. Even though you can install the Integration manually, I would recommend using HACS, as you would always be reminded when a new release is published.

## Manual Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `weatherflow_forecast`.
1. Download _all_ the files from the `custom_components/weatherflow_forecast/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "WeatherFlow Forecast"


## Configuration

To add WeatherFlow Forecast to your installation, do the following:

- Go to Configuration and Integrations
- Click the + ADD INTEGRATION button in the lower right corner.
- Search for *WeatherFlow Forecast** and click the integration.
- When loaded, there will be a configuration box, where you must enter:

  | Parameter | Required | Default Value | Description |
  | --------- | -------- | ------------- | ----------- |
  | `Station ID` | Yes | None | Each WeatherFlow Station you setup, will get a unique Station ID, this id is needed during configuration. To get your Station ID, [login with your account](https://tempestwx.com/settings/stations/), select the station on the list, and then click *Status*. Here you will find your Station ID. |
  | `API Token` | Yes | None | The WeatherFlow REST API requires a Token. Please [login with your account](https://tempestwx.com/settings/tokens) and create the token. Go to Settings and choose Data Authorizations (almost at the bottom). Create a personal access token and use that as Token (API key). |
  | `Forecast Hours` | No | 48 | Adjust the number of hours you want returned for the hourly forecast. Min is 12, max is 96 hours. |
  | `Add Sensors` | No | False | Mark the box if you want to have all the available sensors from the Rest API add to Home Assistant |

- Click on SUBMIT to save your data. If all goes well you should now have a new Weather entity with data from WeatherFlow Forecast
- **Please Note**: The Token you create here will ONLY work with Stations that are registered under the same Login.


You can configure more than 1 instance of the Integration by using a different Station ID.


## Available Sensors

Here is the list of sensors that the program generates. Calculated means, if No, then data comes directly from the Weather Station, if yes, it is a sensor that is derived from some of the other sensors. Not all sensors show up on all installations. It depends on where in the world your station is located.

### Binary Sensors
All entities are prefixed with `[STATION NAME]_binary_sensors_`

| Sensor Name | Description | Calculated |
| --- | --- | --- |
| Data Available | Will be Off if no sensor data is returned from WeatherFlow. This typically happens if the station has not transmitted data for a while and you should check the status of the Station or the attached device. | Yes |
| Is Freezing | On when the Celcius temperature is below 0 | Yes |
| Is Lightning | On when Lightning strikes are detected | Yes |
| Is Raining | On when the rain rate is above 0mm | Yes |

### Sensors
All entities are prefixed with `[STATION NAME]_sensors_`

| Sensor Name | Description | Calculated |
| --- | --- | --- |
| Absolute Humidity | The amount of water per volume of air | Yes |
| Air Density | The Air density | No |
| Apparent Temperature | The apparent temperature, a mix of Heat Index and Wind Chill | No |
| Barometric Pressure | The Barometric pressure | No |
| Battery | The % of charge on the Battery (Tempest device only) | Yes |
| Beaufort | Beaufort scale is an empirical measure that relates wind speed to observed conditions at sea or on land | Yes |
| Beaufort Description | A descriptive text of the Beaufort value | Yes |
| Cloud Base| The cloud height altitude above sea level | Yes |
| Data Updated | The time of the last data update. Disabled by default.  | No |
| Delta T | Difference between Air Temperature and Wet Bulb Temperature | No |
| Dew Point | Dewpoint in degrees | No |
| Distance last lightning strike | Distance of the last strike | No |
| Freezing Altitude| The altitude above sea level where snow is possible | Yes |
| Heat Index | How warm does it feel? | No |
| Humidity | Relative Humidity in % | No |
| Illuminance | How much the incident light illuminates the surface | No |
| Lightning Strikes | Number of lightning strikes in the last minute | No |
| Lightning Strikes last hour | Number of lightning strikes during the last hour | No |
| Lightning Strikes last 3 hours | Number of lightning strikes the last 3 hours | No |
| Power Save Mode | [Power Save Mode](https://help.weatherflow.com/hc/en-us/articles/360048877194-Solar-Power-Rechargeable-Battery) of a Tempest device | Yes |
| Precipitation duration today | Total rain minutes for the current day. (Reset at midnight) | No |
| Precipitation duration today Checked | Total rain minutes for the current day. (Reset at midnight). Only if Rain Check enabled and in the US | No |
| Precipitation duration yesterday | Total rain minutes yesterday | No |
| Precipitation duration yesterday Checked | Total rain minutes yesterday. Only if Rain Check enabled and in the US | No |
| Precipitation Intensity| A textual representation on the current rain rate | Yes |
| Precipitation last hour | Total rain accumulation for the last hour | No |
| Precipitation Rate | How much is it raining right now | Yes |
| Precipitation today | Total rain for the current day. (Reset at midnight) | No |
| Precipitation today Checked | Total rain for the current day. (Reset at midnight) Only if Rain Check enabled and in the US | No |
| Precipitation Type | Type of precipitation. Possible values are: 0 = none, 1 = rain, 2 = hail and 3 = rain+hail (Experimental) | No |
| Precipitation yesterday | Total rain for yesterday (Reset at midnight) | No |
| Precipitation yesterday Checked | Total rain for yesterday (Reset at midnight) Only if Rain Check enabled and in the US | No |
| Pressure Trend | Returns Steady, Falling or Rising determined by the rate of change over the past 3 hours| No |
| Sea Level Pressure | Preasure measurement at Sea Level | No |
| Solar Radiation | Electromagnetic radiation emitted by the sun | No |
| Staton Name | Station Name as state and more information about the station in the Attributes | Yes |
| Station Pressure | Pressure measurement where the station is located | No |
| Temperature | Outside Temperature | No |
| Time of last lightning strike | When the last lightning strike occurred | No |
| UV Description | A descriptive text of the UV Index | Yes |
| UV Index | The UV index | No |
| Voltage | The Voltage of the Tempest device | No |
| Visibility | Distance to the horizon | Yes |
| Wet Bulb Globe Temperature | (WBGT) is a specialised heat stress index which considers several environmental and personal factors. | No |
| Wet Bulb Temperature | Temperature of a parcel of air cooled to saturation (100% relative humidity) | No |
| Wind Cardinal | Current measured Wind bearing as text | Yes |
| Wind Chill | How cold does it feel? | No |
| Wind Direction | Current measured Wind bearing in degrees | No |
| Wind Gust | Highest wind speed for the last minute | No |
| Wind Lull | Lowest wind for the last minute | No |
| Wind Speed | Average wind speed for the last minute | No |

## Enable Debug Logging

If logs are needed for debugging or reporting an issue, use the following configuration.yaml:

```yaml
logger:
  default: error
  logs:
    pyweatherflow-forecast: debug
    custom_components.weatherflow_forecast: debug
```

***

[commits-shield]: https://img.shields.io/github/commit-activity/y/briis/weatherflow_forecast.svg?style=flat-square
[commits]: https://github.com/briis/weatherflow_forecast/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=flat-square
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=flat-square
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/briis/weatherflow_forecast.svg?style=flat-square
[maintenance-shield]: https://img.shields.io/badge/maintainer-Bjarne%20Riis%20%40briis-blue.svg?style=flat-square
[releases-shield]: https://img.shields.io/github/release/briis/weatherflow_forecast.svg?style=flat-square
[releases]: https://github.com/briis/weatherflow_forecast/releases
