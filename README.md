# WeatherFlow Better Forecast integration for Home Assistant
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

This integration adds support for retrieving only the Forecast and Current condition data from [WeatherFlow](https://shop.weatherflow.com/products/tempest). There are other integrations that both create realtime sensor data and forecast data, but this new integration only focusses on the Forecast.

For this integration you **must own a WeatherFlow weather station** and you must create a personal API Token that work with your weather station. [See this link](https://weatherflow.github.io/Tempest/api/) for a description on how to retrieve the API Token.

#### This integration will set up the following platforms.

Platform | Description
-- | --
`weather` | A Home Assistant `weather` entity, with current data, daily- and hourly forecast data.

Minimum required version of Home Assistant is **2023.9.0** as this integration uses the new Weather entity forecast types and it does **not** create Forecast Attributes.

## Installation through HACS (Recommended Method)

This Integration is not yet part of the default HACS store, but can still be installed through HACS.

- Open HACS, click integrations, and then in the upper right corner click on the three dots.
- Select *Custom Repositories* and in the bottom add `https://github.com/briis/weatherflow_forecast` to the *Repository* field and under *Category* select *Integration*.
- Close the dialog box, and you should now see the WeatherFlow Forecast integration show up in HACS as a new integration.
- Click on it and select the DOWNLOAD button in the lower right corner.

After the installation of the files, you must restart Home Assistant, or else you will not be able to add WeatherFlow Weather from the Integration Page.

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
  | `Station ID` | Yes | None | The Station ID for your weathwer station. |
  | `API Token` | Yes | None | The personal API Token you created as per instructions above. |

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
