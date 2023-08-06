# API for the Bosch Indego lawnmowers

## Usage with Home Assistant
See https://github.com/jm-73/Indego

## Basic information needed

Information | Description
----------- | -----------
your_username | Your username when using the BoschSmartMove app
your_password | Your password for the app
your_serial | Your Bosch Indego serial (found on the mover, in the mover menu or in the app)

The python library is written for the login method with username (email address) and password. Login with Facebook account is not supported.

## Call the API
Call the API:

    IndegoApi_Instance = IndegoAPI(username=your_mail@gmail.com, password=your_password, serial=your_serial)

## Functions

    getAlerts()
Get number of alerts

    getAlertsDescription()
Get detailed list of alerts

    getBatteryInformation()
Get detailed battery information

    getFirmware()
Get the mower firmware version

    getModel()
Get the mower model

    getMowed()
Show percentage of lawn mowed

    getMowingMode()
Get the mowing mode

    getNeedsService()
Get the change knives flag

    getOperateData()
Get the operating data such as runtime, battery status and temperature.

```python
{
    'runtime': {
        'total': {
            'operate': 84909, 
            'charge': 25556
            }, 
        'session': {
            'operate': 178, 
            'charge': 0
            }
        }, 
    'battery': {
        'voltage': 36.7, 
        'cycles': 1, 
        'discharge': 0.0, 
        'ambient_temp': 43, 
        'battery_temp': 43, 
        'percent': 367
        }, 
    'garden': {
        'id': 7, 
        'name': 1, 
        'signal_id': 1, 
        'size': 625, 
        'inner_bounds': 3, 
        'cuts': 25, 
        'runtime': 80773, 
        'charge': 24571, 
        'bumps': 4639, 
        'stops': 24, 
        'last_mow': 4}, 
    'hmiKeys': 1344
}
```
    getPosition()
Get position (relative on map)

    getRuntimeSession()
Get session rutime and charge time

    getRuntimeTotal()
Get total runtime and charge time

    getSerial()
Get the serial number

    getServiceCounter()
Get service counter for knives

    getState()
Show current state
```python
Response:
{
    'state': 771, 
    'map_update_available': True, 
    'mowed': 79, 
    'mowmode': 0, 
    'xPos': 34, 
    'yPos': 93, 
    'runtime': {
        'total': {
            'operate': 84818, 
            'charge': 25556
            }, 
        'session': {
            'operate': 87, 
            'charge': 0
            }
        }, 
    'mapsvgcache_ts': 1564741543919, 
    'svg_xPos': 1200, 
    'svg_yPos': 768
}
```

    getUpdateAvailable()
Check if there is an update available

    getUpdateAvailable()
Get the user data.

```python
Response:
{
    'email': 'mail@gmail.com', 
    'display_name': 'Indego', 
    'language': 'sv', 
    'country': 'SE', 
    'optIn': True, 
    'optInApp': True
}
```
    putCommand(command)
Send command. Accepted commands:

Command     |Description         
------------|--------------------
mow         |Start mowing        
pause       |Pause mower         
returnToDock|Return mower to dock


## Not working
    getName()
NOT WORKING (Not implemented by Bosch?)
Get the mower name

    getNextPredicitiveCutting()
NOT WORKING! (No data returned from API)
Get next scheduled cutting session

### Not properly implemented yet

    getLocation()
Get garden location (GPS coordinates?)

    getPredicitiveCalendar()
Get the calender for predicted cutting sessions

    getUserAdjustment()
Get the user adjustment of the cutting frequency

    getCalendar()
Get the calendar for allowed cutting times

    getSecurity()
Get the security settings

    getAutomaticUpdate()
Get the automatic update settings


# API CALLS
https://api.indego.iot.bosch-si.com:443/api/v1


```python
get
/authenticate
/alerts
/alms/<serial>
/alms/<serial>/automaticUpdate
/alms/<serial>/updates
/alms/<serial>/calendar
/alms/<serial>/map
/alms/<serial>/operatingData
/alms/<serial>/predictive/nextcutting?withReason=true
/alms/<serial>/predictive/nextcutting?last=YYYY-MM-DDTHH:MM:SS%2BHH:MM (Not working)
/alms/<serial>/predictive/location
/alms/<serial>/predictive/calendar
/alms/<serial>/predictive/useradjustment (What is this for?)
/alms/<serial>/security
/alms/<serial>/state

put
```