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

    getState()
Show current state of mower

    getMowed()
Show percentage of lawn mowed

    getPosition()
Get position of mower (relative on map)

    getRuntimeTotal()
Get total runtime and charge time from mower

    getRuntimeSession()
Get session rutime and charge time from mower

    getAlerts()
Get number of alerts from mower

    getAlertsDescription()
Get detailed list of alerts from mower

    getNextPredicitiveCutting()
NOT WORKING!
Get next scheduled cutting session from mover (seems to be a problem with this function, dates are from the past)

    getName()
Get the mower name

    getSerial()
Get the mower serial

    getServiceCounter()
Get service counter for mower knives

    getNeedsService()
Get the change knives flag from mover

    getMowingMode()
Get the mowing mode from the mower

    getModel()
Get the mower model

    getFirmware()
Get the mower firmware version

    getLocation()
Get garden location (GPS coordinates?)

    getPredicitiveCalendar()
Get the mower calender for predicted cutting sessions

    getUserAdjustment()
Get the user adjustment of the cutting frequency

    getCalendar()
Get the mover calendar for allowed cutting times

    getSecurity()
Get the security settings for the mover

    getAutomaticUpdate()
Get the automatic update settings

    getUpdateAvailable()
Check if there is an update available for the mower

    putCommand(command)
Send commands to the mower. Accepted commands:

Command     |Description         
------------|--------------------
mow         |Start mowing        
pause       |Pause mower         
returnToDock|Return mower to dock