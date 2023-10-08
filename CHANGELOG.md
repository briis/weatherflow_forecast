## Release 0.2.0

Date: `NOT RELEASED`

### Changes

- Added option to add all the sensors to the Integration. If upgrading select configure button, to add the sensors.
- If sensors are enabled, the Weather Entity will use sensor data as the Current Data, to get a more realtime view.
- Integration images are added to Home Assistant Brand icons - It is the same images as the `core` integration uses, as these are the official WeatherFlow images.


### TODO
- Add the remaining Calculated sensors that are currently available in the 'old' integration (Some have already been included.)
- If sensors have been installed, and the user selectes to remove them again, ensure they are deleted from Home Assistant. Currently they must be manually remnoved.
- Migrate parts of the language files from the 'old' integration. I will still need people to do some translations.
- If Station ID and API Token do not match, a wrong error message is displayed.
- Add the Integration to the Default HACS store.
- Add sensor description to the README file
