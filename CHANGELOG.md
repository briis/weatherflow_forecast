
## Release 0.3.2

Date: `2023-10-17`

### Changes

- Bump pyweatherflow-forecast to 0.6.3, with a fix that ensures none of the calculated sensors fail if the sensors used to do the calculations are None.
- French translation is updated. Thank you @baylanger

### TODO
- If sensors have been installed, and the user selectes to remove them again, ensure they are deleted from Home Assistant. Currently they must be manually removed.


## Release 0.3.1

Date: `2023-10-15`

### Changes

- Bump pyweatherflow-forecast to 0.6.1, which optimizes the number of calls to the WeatherFlow Rest API, by removing 1 call per cycle
- Bump pyweatherflow-forecast to 0.6.2, to ensure that AIR and SKY devices still can work with sensors, even without Voltage and Battery information.
- Added language file for the following language codes: **cs, de, it, nl, sv**. Please note that not all translations are complete in these files, so anyone with the knowledge of the languages, please fork this repo, change the text strings, and make a Pull Request.

## Release 0.3.0

Date: `2023-10-14`

### Changes
- **BREAKING**
  **Due to all the changes made in this release, I recommend that you remove the integration and re-add it. This will ensure all sensors are named correctly, and obsolete sensors are removed.**
  - Precipitation Minutes... sensors have been renamed. Please delete them manually if you do not follow the recommendation above.
  - Wet Bulb sensors have been renamed due to spelling error. You might need to delete the obsolete sensors manually.
- Changed icon for Cloud Base
- Add the Integration to the Default HACS store. (Not merged on release of this version)
- Bump pyweatherflow-forecast to 0.6.0
- Added `Voltage` sensor. This sensor will only be available for Tempest devices. There will be no implementation for AIR and SKY as these are deprecated devices.
- Added `Battery` sensor. This sensor is derived from the Voltage sensor above and shows the % full based on voltage amount.

## Release 0.2.2

Date: `2023-10-09`

### Changes

- **BREAKING** Removed sensor `precip` as this is only used for calculating precipitation rate - must be manually deleted.
- Sensor description added to README.md
- Fix issue [#6](https://github.com/briis/weatherflow_forecast/issues/6) wrong value in Absolute Humidity
- Added Beaufort sensor
- Added Freezing Altitude sensor

## Release 0.2.1

Date: `2023-10-08`

### Changes

- Added `visibility` sensor
- Added `cloud_base` sensor
- Added `precip_rate` sensor

## Release 0.2.0

Date: `2023-10-08`

### Changes

- Added option to add all the sensors to the Integration. If upgrading select configure button, to add the sensors.
- If sensors are enabled, the Weather Entity will use sensor data as the Current Data, to get a more realtime view.
- Integration images are added to Home Assistant Brand icons - It is the same images as the `core` integration uses, as these are the official WeatherFlow images.
- Updated the documentation

