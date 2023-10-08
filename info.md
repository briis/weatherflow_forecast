# WeatherFlow Forecast and Sensor integration for Home Assistant
Home Assistant integration for WeatherFlow Forecast

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![Community Forum][forum-shield]][forum]

<p align="center">
  <img width="384" height="128" src="https://github.com/briis/weatherflow_forecast/blob/main/images/logo@2x.png?raw=true">
</p>

This integration adds support for retrieving the Forecast, Current condition and optionally realtime data from [WeatherFlow](https://shop.weatherflow.com/products/tempest). It replaces [WeatherFlow Weather for Home Assistant](https://github.com/briis/hass-weatherflow) that will soon be deprecated.

For this integration you **must own a WeatherFlow weather station** and you must create a personal API Token that work with your weather station. [See this link](https://weatherflow.github.io/Tempest/api/) for a description on how to retrieve the API Token.

#### This integration will set up the following platforms.

Platform | Description
-- | --
`weather` | A Home Assistant `weather` entity, with current data, daily- and hourly forecast data.
`sensor` | A Home Assistant `sensor` entity, with all available sensors from the API, plus a few local calculated.

Minimum required version of Home Assistant is **2023.9.0** as this integration uses the new Weather entity forecast types and it does **not** create Forecast Attributes.


## Configuration

To add WeatherFlow Forecast to your installation, do the following:

- Go to Configuration and Integrations
- Click the + ADD INTEGRATION button in the lower right corner.
- Search for *WeatherFlow Forecast** and click the integration.
- When loaded, there will be a configuration box, where you must enter:

  | Parameter | Required | Default Value | Description |
  | --------- | -------- | ------------- | ----------- |
  | `Station ID` | Yes | None | The Station ID for your weathwer station. |
  | `API Token` | Yes | None | The personal API Token you created as per instructions above. |
  | `Add Sensors` | No | False | Mark the box if you want to have all the available sensors from the Rest API add to Home Assistant |

- Click on SUBMIT to save your data. If all goes well you should now have a new Weather entity with data from WeatherFlow Forecast

You can configure more than 1 instance of the Integration by using a different Station ID and new API Token.


***

[commits-shield]: https://img.shields.io/github/commit-activity/y/briis/weatherflow_forecast.svg?style=flat-square
[commits]: https://github.com/briis/weatherflow_forecast/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=flat-square
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/briis/weatherflow_forecast.svg?style=flat-square
[maintenance-shield]: https://img.shields.io/badge/maintainer-Bjarne%20Riis%20%40briis-blue.svg?style=flat-square
[releases-shield]: https://img.shields.io/github/release/briis/weatherflow_forecast.svg?style=flat-square
[releases]: https://github.com/briis/weatherflow_forecast/releases
