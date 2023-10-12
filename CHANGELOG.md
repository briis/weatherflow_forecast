## Release 0.2.3

Date: `NOT RELEASED`

### Changes
- Changed icon for Cloud Base
- Add the Integration to the Default HACS store. (Not merged on release of this version)
- Bump pyweatherflow-forecast to 0.5.0
- Added `Voltage` sensor. This sensor will only be available for Tempest devices. There will be no implementation for AIR and SKY as these are deprecated devices.
- Added `Battery` sensor. This sensor is derived from the Voltage sensor above and shows the % full based on voltage amount.

### TODO
- If sensors have been installed, and the user selectes to remove them again, ensure they are deleted from Home Assistant. Currently they must be manually removed.
- Migrate parts of the language files from the 'old' integration. I will still need people to do some translations.
- If Station ID and API Token do not match, a wrong error message is displayed.

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

