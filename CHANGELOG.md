## Release 1.0.7

Date: `2024-01-22`

### Changes

- Even though the Station has not transmitted data to WeatherFlow, the device itself, often does, so we are able to post the Voltage, Battery and Power Save Mode from the device itself.
- New binary sensor `Data Available` is added to the system. If WeatherFlow reports an empty dataset, this is set to False, and you should check your hub and see if it is still online.
- Added better error handling if user types in the wrong Station ID upon configuration. The error is now trapped, and a more detailed error message supplied.
- Bump dependency module pyweatherflow-forecast to 1.0.10


## Release 1.0.6

Date: `2024-01-20`

### Changes

This release is all about error handling. Most issues I get reported are caused by the station being offline for some reason or the sensors not reporting correctly. These two are, of course, sometimes related, but often the missing update of sensor data is caused by the Tempest device being underpowered. For a person like myself who live in the Northern Hemisphere, this always happens in the winther when there is not enough daylight to charge the battery. So after sometime the device will reduce the reporting intervals and the sensors it reports, until the time when the power is so low that it stops sending any data.

- As of this release the system will write a warning to the logfile if it detects that there is no data. It will continue working, but there will be no data in the sensors until the station comes back online.
- Also at the time of setup, if you try to add the sensors, an error will be shown if there are no sensor data, and you cannot add the sensors until the issue is resolved. The forecast can always be added.
- Finally, if you discover that sensor data is not being updated or only some of them, check the `power_save_mode` sensor. Any number here greater than 0 will mean reduced updating of sensors. You can read more about the Power Save Mode [here](https://help.weatherflow.com/hc/en-us/articles/360048877194-Solar-Power-Rechargeable-Battery)
- Bump dependency pyweatherflow-forecast to 1.0.8 (Failed setup, will retry #70 and Error while setting up weatherflow_forecast platform for sensor #69)


## Release 1.0.5

Date: `2024-01-06`

### Changes

- Fixing issue [#59](https://github.com/briis/weatherflow_forecast/issues/59). As I could not find a way to provoke the error, I cannot fully guarantee that this fix will work. If not please open a new issue with detailed logfiles.

## Release 1.0.4

Date: `2024-01-04`

### Changes

- This integration is now part of the Default HACS store. So you can delete the pointer to the Github library under *Custom Repositories*
- Added `wind_gust_speed` to daily forecast, closing [#58](https://github.com/briis/weatherflow_forecast/issues/58)


## Release 1.0.3

Date: `2023-12-23`

### Changes

- If sensors have been installed, and the user selectes to remove them again, ensure they are deleted from Home Assistant.
- Added new sensor `Precip Type` exposing an integer with the type of precipitation. Possible values are: 0 = none, 1 = rain, 2 = hail and 3 = rain+hail (Experimental)

## Release 1.0.2

Date: `2023-12-16`

### Changes

- @baylanger updated the French Translation.

## Release 1.0.1

Date: `2023-12-03`

This release is now V1.0, as all the relevant entities from the previous release are now implemented. Unfortunately my PR for getting this in to Default HACS is not merged yet, but I hope that this will happen soon, and when this does the previous integration will be removed.

### Changes

- @zuper83 updated the Swedish Translation.
- Added new sensor `Precip Intensity` that express the intensity of rain in text. (Can be translated). Closing [#41](https://github.com/briis/weatherflow_forecast/issues/41)
- Fixing wrong value and unit for the `Air Density` sensor when using the Imperial Unit System. **WARNING** When digging in to this, the Unit for the Metric system was also wrong and is changed from µg/m³ to kg/m³. You can correct the unit under the _Developer Tools_ and then _STATISTICS_ if you get a warning during startup. Closing #40


## Release 1.0.0

Date: `2023-11-18`

This release is now V1.0, as all the relevant entities from the previous release are now implemented. Unfortunately my PR for getting this in to Default HACS is not merged yet, but I hope that this will happen soon, and when this does the previous integration will be removed.

### Changes

- Bump pyweatherflow-forecast to 1.0.0
- Added new sensor `Power Save Mode` that shows the Power Mode of a Tempest device. Attributes of the sensor gives a textual explanation. For more information [read here](https://help.weatherflow.com/hc/en-us/articles/360048877194-Solar-Power-Rechargeable-Battery) Closes (#27)
- Added new sensor `Beaufort Description`, detailing the current Beaufort value with a descriptive text (For translated values please update the language file in the *translations* directory) Closes (#27)
- Added new sensor `UV Description`, detailing the current UV value (For translated values please update the language file in the *translations* directory) Closes (#27)
- Added new sensor `Staton Name`, detailing data about the Tempest Station (For translated values please update the language file in the *translations* directory) Closes (#27)
- Added new Binary Sensor `Is Freezing`. On when the Celcius temperature is below 0. (Closes #26)
- Added new Binary Sensor `Is Lightning`. On when Lightning strikes are detected. (Closes #26)
- Added new Binary Sensor `Is Raining`. On when the rain rate is above 0mm. (Closes #26)

## Release 0.3.3

Date: `2023-11-18`

### Changes

- Added new sensor `Power Save Mode` that shows the Power Mode of a Tempest device. Attributes of the sensor gives a textual explanation. For more information [read here](https://help.weatherflow.com/hc/en-us/articles/360048877194-Solar-Power-Rechargeable-Battery)
- Bump pyweatherflow-forecast to 0.6.4.

## Release 0.3.2

Date: `2023-10-17`

### Changes

- Bump pyweatherflow-forecast to 0.6.3, with a fix that ensures none of the calculated sensors fail if the sensors used to do the calculations are None.
- French translation is updated. Thank you @baylanger


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

