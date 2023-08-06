# pypi
""" API for Bosch API server for Indego lawn mower """
import requests
import json
from requests.auth import HTTPBasicAuth
import logging

DEFAULT_URL = "https://api.indego.iot.bosch-si.com:443/api/v1/"
# CONST TAKEN FROM homeassistant.const
CONTENT_TYPE_JSON = "application/json"
#const taken from aiohttp.hdrs
CONTENT_TYPE = "Content-Type"

logging.basicConfig(filename='pyindego.log',level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("---------------------------------")
_LOGGER.debug("Start")

MOWER_STATE_DESCRIPTION = {
    '0'    : 'Reading status',
    '257'  : 'Charging',
    '258'  : 'Docked',
    '259'  : 'Docked - Software update',
    '260'  : 'Docked',
    '261'  : 'Docked',
    '262'  : 'Docked - Loading map',
    '263'  : 'Docked - Saving map',
    '513'  : 'Mowing',
    '514'  : 'Relocalising',
    '515'  : 'Loading map',
    '516'  : 'Learning lawn',
    '517'  : 'Paused',
    '518'  : 'Border cut',
    '519'  : 'Idle in lawn',
    '769'  : 'Returning to Dock',
    '770'  : 'Returning to Dock',
    '771'  : 'Returning to Dock - Battery low',
    '772'  : 'Returning to dock - Calendar timeslot ended',
    '773'  : 'Returning to dock - Battery temp range',
    '774'  : 'Returning to dock - requested by user/app',
    '775'  : 'Returning to dock - Lawn complete',
    '776'  : 'Returning to dock - Relocalising',
    '1025' : 'Diagnostic mode',
    '1026' : 'End of life',
    '1281' : 'Software update',
    '1537' : 'Stuck on lawn, help needed',
    '64513': 'Sleeping'
}

MOWER_MODEL_DESCRIPTION = {
    '3600HA2300':'Indego 1000 Connect',
    '3600HA2301': 'Indego 1200 Connect',
    '3600HA2302': 'Indego 1100 Connect',
    '3600HA2303': 'Indego 13C',
    '3600HA2304': 'Indego 10C',
    '3600HB0100': 'Indego 350 Connect',
    '3600HB0101': 'Indego 400 Connect'
    '3600HB0102': 'Indego S+ 350 Connect'
}

MOWING_MODE_DESCRIPTION = {
    'smart':    'SmartMowing',
    'calendar': 'Calendar',
    'manual':   'Manual'
}

class IndegoAPI():
    """Wrapper for Indego's API."""
    def __init__(self, username=None, password=None, serial=None):
        """Initialize Indego API and set headers needed later."""
        _LOGGER.debug("Init Indego API class __init__")
        # Declaring variables in case that they are read before initialized

        self.api_url = DEFAULT_URL
        # Log in settings
        self.username = username
        self.password = password
        self.headers = {CONTENT_TYPE: CONTENT_TYPE_JSON}
        self.body = {'device': '', 'os_type': 'Android', 'os_version': '4.0', 'dvc_manuf': 'unknown', 'dvc_type': 'unknown'}
        self.jsonBody = json.dumps(self.body)
        #Properties for cached values
        self._serial = serial
        self.devices = {}
        self.status = None
        self._mower_state = None
        self._model = None
        self.mowed = None
        self._runtime = None

        _LOGGER.debug(">>>API-call: %s", '{}{}'.format(self.api_url, 'authenticate'))
        _LOGGER.debug("Call self login")
        self.login = requests.post(
            '{}{}'.format(self.api_url, 'authenticate'), data=self.jsonBody, headers=self.headers,
            auth=HTTPBasicAuth(username, password), timeout=30)
        _LOGGER.debug("JSON Response: " + str(self.login.json()))
        
        logindata = json.loads(self.login.content)
        self._contextid = logindata['contextId']
        _LOGGER.debug("self._contextid: " + self._contextid)
        self._userid = logindata['userId']
        _LOGGER.debug("self._userId: " + logindata['userId'])
        _LOGGER.debug("self._serial: " + self._serial)
        _LOGGER.debug("End Indego API class __init__")
        self.update()

    def authenticate(self):
        _LOGGER.debug("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        _LOGGER.debug("Authenticate start")
        try:
            _LOGGER.debug("authenticate called")
            _LOGGER.debug(">>>API: " + self.api_url +  'authenticate')
            #self.login = requests.post(
            #    '{}{}'.format(self.api_url, 'authenticate'), data=self.jsonBody, headers=self.headers,
            #    auth=HTTPBasicAuth(self.username, self.password), timeout=30, verify=False)
            self.login = requests.post(
                '{}{}'.format(self.api_url, 'authenticate'), data=self.jsonBody, headers=self.headers,
                auth=HTTPBasicAuth(self.username, self.password), timeout=30)
            _LOGGER.debug("Response: " + str(self.login.content))
            _LOGGER.debug("JSON Response: " + str(self.login.json()))
            # This can be removed later, only used for debugging and setting initial state of properties
            # maye kept for sensors that only should be read at startup, until I have figured out how to make sensors update with longer interval
            self.update()
            _LOGGER.debug("Authenticate end")

        except requests.exceptions.ConnectionError as conn_exc:
            _LOGGER.debug("Failed to update Indego status. Error: " + str(conn_exc))
            _LOGGER.debug("Authenticate end")
            _LOGGER.debug("--------------------------------------------------------")
            raise

    def update(self):
        """Update cached response."""
        _LOGGER.debug("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        _LOGGER.debug("Update start")
    
        ### States of self properties
        # getState
        # Updates often!
        self._mower_state = 'Not updated yet'
        _LOGGER.debug(f"self._mower_state: {self._mower_state}")
        self._map_update_available = 'Not updated yet'
        _LOGGER.debug(f"self._map_update_available: {self._map_update_available}")
        self._mowed = 'Not updated yet'
        _LOGGER.debug(f"self._mowed: {self._mowed}")
        self._mowmode = 'Not updated yet'
        _LOGGER.debug(f"self._mowmode: {self._mowmode}")
        self._xPos = 'Not updated yet'
        _LOGGER.debug(f"self._xPos: {self._xPos}")
        self._yPos = 'Not updated yet'
        _LOGGER.debug(f"self._yPos: {self._yPos}")
        self._runtime = 'Not updated yet'
        _LOGGER.debug(f"self._runtime: {self._runtime}")
        self._mapsvgcache_ts = 'Not updated yet'
        _LOGGER.debug(f"self._mapsvgcache_ts: {self._mapsvgcache_ts}")
        self._svg_xPos = 'Not updated yet'
        _LOGGER.debug(f"self._svg_xPos: {self._svg_xPos}")
        self._svg_yPos = 'Not updated yet'
        _LOGGER.debug(f"self._svg_yPos: {self._svg_yPos}")                
        # User friendly state of mower
        self._mower_state_description = 'Not updated yet'
        _LOGGER.debug(f"self._mower_state_description: {self._mower_state_description}")
        # User friendly total runtime
        self._total_operation = 'Not updated yet'
        _LOGGER.debug(f"self._total_operation: {self._total_operation}")
        self._total_cut = 'Not updated yet'
        _LOGGER.debug(f"self._total_cut: {self._total_cut}")
        self._total_charge = 'Not updated yet'
        _LOGGER.debug(f"self._total_charge: {self._total_charge}")
        # User friendly session runtime
        self._session_operation = 'Not updated yet'
        _LOGGER.debug(f"self._session_operation: {self._session_operation}")
        self._session_cut = 'Not updated yet'
        _LOGGER.debug(f"self._session_cut: {self._session_cut}")
        self._session_charge = 'Not updated yet'
        _LOGGER.debug(f"self._session_charge: {self._session_charge}")
        # User friendly mowing mode description
        self._mowingmode_description = 'Not updated yet'
        _LOGGER.debug(f"self._mowingmode_description: {self._mowingmode_description}")

        # getUsers
        # This one only needs to run at startup
        self._email = 'Not updated yet'
        self._display_name = 'Not updated yet'
        self._language = 'Not updated yet'
        self._country = 'Not updated yet'
        self._optin = 'Not updated yet'
        self._optinapp = 'Not updated yet'

        # getGenericData
        # Updates at startup (may change in future releases)
        #_LOGGER.debug(f"self.alm_sn ignored: {self._alm_sn}")
        self._alm_name = 'Not updated yet'
        _LOGGER.debug(f"self._alm_name: {self._alm_name}")
        self._service_counter = 'Not updated yet'
        _LOGGER.debug(f"self._service_counter: {self._service_counter}")
        self._needs_service = 'Not updated yet'
        _LOGGER.debug(f"self._needs_service: {self._needs_service}")
        self._alm_mode = 'Not updated yet'
        _LOGGER.debug(f"self._alm_mode: {self._alm_mode}")
        self._bareToolnumber = 'Not updated yet'
        _LOGGER.debug(f"self._bareToolnumber: {self._bareToolnumber}")
        self._alm_firmware_version = 'Not updated yet'
        _LOGGER.debug(f"self._alm_firmware_version: {self._alm_firmware_version}")

        # getUpdates
        # Updates only at startup (may change in future releases)
        self._firmware_available = 'Not updated yet'
        _LOGGER.debug(f"self._firmware_available: {self._firmware_available}")


        # getOperatingData
        # Updates often
        self._battery = 'Not updated yet'
        _LOGGER.debug(f"battery: {self._battery}")
        self._battery_percent = 'Not updated yet'
        _LOGGER.debug(f"self._battery_percent: {self._battery_percent}")
        self._battery_voltage = 'Not updated yet'
        _LOGGER.debug(f"self._battery_voltage: {self._battery_voltage}")
        self._battery_cycles = 'Not updated yet'
        _LOGGER.debug(f"self._battery_cycles: {self._battery_cycles}")
        self._battery_discharge = 'Not updated yet'
        _LOGGER.debug(f"self._battery_discharge: {self._battery_discharge}")
        self._battery_ambient_temp = 'Not updated yet'
        _LOGGER.debug(f"self._battery_ambient_temp: {self._battery_ambient_temp}")
        self._battery_temp = 'Not updated yet'
        _LOGGER.debug(f"self._battery_temp: {self._battery_temp}")

        self._garden = 'Not updated yet'
        _LOGGER.debug(f"garden: {self._garden}")
        self._hmikeys = 'Not updated yet'
        _LOGGER.debug(f"hmiKeys: {self._hmikeys}")

        # Other API calls to update
        self._model = 'Not updated yet'
        _LOGGER.debug(f"self._model: {self._model}")

        try:
            _LOGGER.debug("Try on initial update (only once at startup)")

            #self.getState()
            self.getUsers()
            self.getGenericData()
            self.ModelDescription()
            self.MowingModeDescription()
            self.getUpdates()

        except requests.exceptions.ConnectionError:
            _LOGGER.debug("Failed to update status - exception already logged in self.post")
            raise

        _LOGGER.debug("Update end")
        _LOGGER.debug("--------------------------------------------------------")
        return(self.status)

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def refresh_devices(self):
        _LOGGER.debug("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        _LOGGER.debug("Refresh devices start")

        _LOGGER.debug("Catched from authenticate")
        _LOGGER.debug(f"self._contextid: {self._contextid}")
        _LOGGER.debug(f"self._userid: {self._userid}")
        _LOGGER.debug(f"self._serial: {self._serial}")

        _LOGGER.debug("self.getState API call")
        self.getState()
        _LOGGER.debug(f"self._mower_state: {self._mower_state}")
        _LOGGER.debug(f"self._map_update_available: {self._map_update_available}")
        _LOGGER.debug(f"self._mowed: {self._mowed}")
        _LOGGER.debug(f"self._mowmode: {self._mowmode}")
        _LOGGER.debug(f"self._xPos: {self._xpos}")
        _LOGGER.debug(f"self._yPos: {self._ypos}")
        _LOGGER.debug(f"self._runtime: {self._runtime}")
        _LOGGER.debug(f"self._mapsvgcache_ts: {self._mapsvgcache_ts}")
        _LOGGER.debug(f"self._svg_xPos: {self._svg_xPos}")
        _LOGGER.debug(f"self._svg_yPos: {self._svg_yPos}")                

        # User-friendly mower state
        self.MowerStateDescription()
        _LOGGER.debug(f"self._mower_state_description = {self._mower_state_description}")

        # split runtime into total        
        self.RuntimeTotal()
        _LOGGER.debug(f"self._total_operation: {self._total_operation}")
        _LOGGER.debug(f"self._total_charge: {self._total_charge}")
        _LOGGER.debug(f"self._total_cut: {self._total_cut}")

        # split runtime into session
        self.RuntimeSession()
        _LOGGER.debug(f"self._session_operation: {self._session_operation}")
        _LOGGER.debug(f"self._session_charge: {self._session_charge}")
        _LOGGER.debug(f"self._session_cut: {self._session_cut}")

        #self.getUsers()
        _LOGGER.debug("self.getUsers API call")
        _LOGGER.debug(f"self._email: {self._email}")                
        _LOGGER.debug(f"self._display_name: {self._display_name}")                
        _LOGGER.debug(f"self._language: {self._language}")                
        _LOGGER.debug(f"self._country = {self._country}")
        _LOGGER.debug(f"self._optIn = {self._optin}")
        _LOGGER.debug(f"self._optInApp = {self._optinapp}")

        #self.getGenericData()
        _LOGGER.debug("self.getGenericData API call")
        #_LOGGER.debug(f"self.alm_sn ignored: {self._alm_sn}")
        _LOGGER.debug(f"self._alm_name: {self._alm_name}")
        _LOGGER.debug(f"self._service_counter: {self._service_counter}")
        _LOGGER.debug(f"self._needs_service: {self._needs_service}")
        _LOGGER.debug(f"self._alm_mode: {self._alm_mode}")
        _LOGGER.debug(f"self._bareToolnumber: {self._bareToolnumber}")
        _LOGGER.debug(f"self._alm_firmware_version: {self._alm_firmware_version}")

        # User-friendly mower model
        _LOGGER.debug(f"self._model_description = {self._model_description}")

        #self.getOperationalData()
        _LOGGER.debug("self.getOperatingData API call")
        self.getOperatingData()
        _LOGGER.debug(f"battery: {self._battery}")
        _LOGGER.debug(f"garden: {self._garden}")
        _LOGGER.debug(f"hmiKeys: {self._hmikeys}")
        self.BatteryPercent()        
        _LOGGER.debug(f"self._battery_percent: {self._battery_percent}")
        self.BatteryVoltage()
        _LOGGER.debug(f"self._battery_voltage: {self._battery_voltage}")
        self.BatteryCycles()
        _LOGGER.debug(f"self._battery_cycles: {self._battery_cycles}")
        self.BatteryDischarge()
        _LOGGER.debug(f"self._battery_discharge: {self._battery_discharge}")
        self.BatteryAmbientTemp()
        _LOGGER.debug(f"self._battery_ambient_temp: {self._battery_ambient_temp}")
        self.BatteryTemp()
        _LOGGER.debug(f"self._battery_temp: {self._battery_temp}")

        #self.getUpdates()
        _LOGGER.debug(f"self._firmware_available: {self._firmware_available}")
        
        #self.getNextCutting()

        # Not updated in the getState API call
        #_LOGGER.debug("Not updated in the getState API call")        
        #_LOGGER.debug(f"self._model = {self._model}")

        _LOGGER.debug("Refresh Devices end")
        _LOGGER.debug("--------------------------------------------------------")
        ### >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Update API calls:
# complete_url = 'alms/' + self._serial + '/state'
# complete_url = 'users/' + self._userid
# complete_url = 'alms/' + self._serial
# complete_url = 'alms/' + self._serial + '/operatingData'
# complete_url = 'alms/' + self._serial + '/updates'
# complete_url = 'alms/' + self._serial + '/predictive/nextcutting?withReason=true'
# complete_url = 'alerts'
#
#
#

###########################################################
### Updating classes that updates cached data
###########################################################
    def getState(self):
        # FInished with all properties as get-calls
        # GET core Update all self values in STATE API call
        _LOGGER.debug("---")    
        _LOGGER.debug("getState: Update State API call values")    
        complete_url = 'alms/' + self._serial + '/state'
        _LOGGER.debug("URL: " + complete_url)
        tmp_json = self.get(complete_url)
        self._mower_state = tmp_json['state']
        _LOGGER.debug(f"self._mower_state: {self._mower_state}")
        self._map_update_available = tmp_json['map_update_available']
        _LOGGER.debug(f"self.map_update_available: {self._map_update_available}")    
        self._mowed = tmp_json['mowed']
        _LOGGER.debug(f"self._mowed: {self._mowed}")    
        self._mowmode = tmp_json['mowmode']
        _LOGGER.debug(f"self._mowmode: {self._mowmode}")    
        self._xpos = tmp_json['xPos']
        _LOGGER.debug(f"self._xPos: {self._xpos}")    
        self._ypos = tmp_json['yPos']
        _LOGGER.debug(f"self._yPos: {self._ypos}")    
        self._runtime = tmp_json['runtime']
        _LOGGER.debug(f"self._runtime: {self._runtime}")    
        self._mapsvgcache_ts = tmp_json['mapsvgcache_ts']
        _LOGGER.debug(f"self._mapsvgcache_ts: {self._mapsvgcache_ts}")    
        self._svg_xPos = tmp_json['svg_xPos']
        _LOGGER.debug(f"self._svg_xPos: {self._svg_xPos}")    
        self._svg_yPos = tmp_json['svg_yPos']
        _LOGGER.debug(f"self._svg_yPos: {self._svg_yPos}")    

        _LOGGER.debug("getState end")    
        _LOGGER.debug("---")    
        return tmp_json

    def getUsers(self):
        # Finished
        # GET Core Update all self values in USERS API call
        _LOGGER.debug("---")  
        _LOGGER.debug("getUsers: ")
        complete_url = 'users/' + self._userid
        _LOGGER.debug(">>>API Call: " + complete_url)
        tmp_json = self.get(complete_url)
        self._email = tmp_json['email']
        _LOGGER.debug(f"email = {self._email}")
        self._display_name = tmp_json['display_name']
        _LOGGER.debug(f"display_name = {self._display_name}")
        self._language = tmp_json['language']
        _LOGGER.debug(f"language = {self._language}")
        self._country = tmp_json['country']
        _LOGGER.debug(f"country = {self._country}")
        self._optin = tmp_json['optIn']
        _LOGGER.debug(f"optIn = {self._optin}")
        self._optinapp = tmp_json['optInApp']
        _LOGGER.debug(f"optInApp = {self._optinapp}")
        _LOGGER.debug(f"Value User = {tmp_json}")
        _LOGGER.debug("getUsers end")
        _LOGGER.debug("---")  
        return tmp_json
        #PUT https://api.indego.iot.bosch-si.com/api/v1/users/{{userId}}
        #{New_display_name: "New name"}

    def getGenericData(self):
        # Finished
        # GET Core Update all self values in SERIAL API call
        _LOGGER.debug("---")  
        _LOGGER.debug("getGenericData start")
        complete_url = 'alms/' + self._serial
        _LOGGER.debug(f">>>API call: {complete_url}")
        tmp_json = self.get(complete_url)
        #value = tmp_json['alm_mode']
        _LOGGER.debug(f"self.alm_sn ignored: {tmp_json['alm_sn']}")
        self._alm_name = tmp_json['alm_name']
        _LOGGER.debug(f"self._alm_name: {self._alm_name}")
        self._service_counter = tmp_json['service_counter']
        _LOGGER.debug(f"self._service_counter: {self._service_counter}")
        self._needs_service = tmp_json['needs_service']
        _LOGGER.debug(f"self._needs_service: {self._needs_service}")
        self._alm_mode = tmp_json['alm_mode']
        _LOGGER.debug(f"self._alm_mode: {self._alm_mode}")
        self._bareToolnumber = tmp_json['bareToolnumber']
        _LOGGER.debug(f"self._bareToolnumber: {self._bareToolnumber}")
        self._alm_firmware_version = tmp_json['alm_firmware_version']
        _LOGGER.debug(f"self._alm_firmware_version: {self._alm_firmware_version}")
        _LOGGER.debug("getGenericData end")
        _LOGGER.debug("---")  
        return tmp_json

    def getOperatingData(self):
        # Finished
        # GET core Update all self values in state get API call
        _LOGGER.debug("---")  
        _LOGGER.debug("getOperatingData start")
        complete_url = 'alms/' + self._serial + '/operatingData'
        _LOGGER.debug(">>>API Call: " + complete_url)
        tmp_json = self.get(complete_url)
        ### Dont pay attention to runtime values as they are collected in the STATE call also
        _LOGGER.debug(f"runtime: {tmp_json['runtime']}")
        self._battery = tmp_json['battery']
        _LOGGER.debug(f"battery: {self._battery}")
        self._garden = tmp_json['garden']
        _LOGGER.debug(f"garden: {self._garden}")
        self._hmikeys = tmp_json['hmiKeys']
        _LOGGER.debug(f"hmiKeys: {self._hmikeys}")
        _LOGGER.debug("getOperatingData end")
        _LOGGER.debug("---")  
        return tmp_json

    def getUpdates(self):
        # Finished
        _LOGGER.debug("---")  
        _LOGGER.debug("getUpdates start")  
        # Need to better this class with better error handling for timeout
        # Takes time as the mower has to wake up for this control to be perfomed
        complete_url = 'alms/' + self._serial + '/updates'
        tmp_json = self.get(complete_url)
        self._firmware_available = tmp_json['available']
        _LOGGER.debug("getUpdates end")
        _LOGGER.debug("---")  
        return tmp_json

    def getNextCutting(self):
        _LOGGER.debug("---")  
        _LOGGER.debug("getNextCutting start")
        #https://api.indego.iot.bosch-si.com/api/v1/alms/{{alm_sn}}/predictive/nextcutting?withReason=true]
        complete_url = 'alms/' + self._serial + '/predictive/nextcutting?withReason=true'
        _LOGGER.debug("Complete URL: " + complete_url)
        tmp_json = self.get(complete_url)
        self.nextcutting = tmp_json
        _LOGGER.debug(f"NextCutting = {tmp_json}")
        _LOGGER.debug("getNextCutting end")
        _LOGGER.debug("---")  
        return tmp_json

# Depricated in Bosch API??? Gives no answer from API call
#    def getNextPredicitiveCutting(self):
#        # Not working
#        _LOGGER.debug("---")
#        _LOGGER.debug("getNetPRedicitveCutting")
#        complete_url = 'alms/' + self._serial + '/predictive/nextcutting?last=YYYY-MM-DDTHH:MM:SS%2BHH:MM'
#        Runtime_temp = self.get(complete_url)
#        value = Runtime_temp
#        return value

    def getAlerts(self):
        _LOGGER.debug("---")  
        _LOGGER.debug("getAlerts start")
        complete_url = 'alerts'
        _LOGGER.debug(">>>API Call: " + complete_url)
        tmp_json = self.get(complete_url)
        self.alerts = tmp_json
        _LOGGER.debug("getAlerts end")
        _LOGGER.debug("---")  
        return tmp_json

###################################################
### Functions for getting data from STATE cache

    def MowerState(self):
        # Fixed
        _LOGGER.debug("---")
        _LOGGER.debug(f"MowerState: {self._mower_state}")
        return self._mower_state

    def Mowed(self):
        # Fixed
        _LOGGER.debug("---")
        _LOGGER.debug(f"Moved new method: {self.mowed}")
        return self.mowed

    def MapUpdateAvailable(self):
        # Fixed
        _LOGGER.debug("---")
        _LOGGER.debug(f"MapUpdateAvailable method: {self.map_update_available}")
        return self.map_update_available

    def MowMode(self):
        # Fixed
        _LOGGER.debug("---")
        _LOGGER.debug(f"MowMode method: {self.mowmode}")
        return self.mowmode

    def XPos(self):
        # Fixed
        _LOGGER.debug("---")
        _LOGGER.debug(f"XPos method: {self.xpos}")
        return self.xpos

    def YPos(self):
        # Fixed
        _LOGGER.debug("---")
        _LOGGER.debug(f"YPos method: {self.ypos}")
        return self.ypos

    def Runtime(self):
        return self._runtime

    def RuntimeTotal(self):
        _LOGGER.debug("---")
        tmp = self.Runtime()
        tmp = tmp['total']
        if tmp:
            self._total_operation = round(tmp['operate']/100)
            self._total_charge = round(tmp['charge']/100)
            self._total_cut = round(self._total_operation - self._total_charge)
            return None
        else:
            _LOGGER.debug("RuntimeTotal: None")
            return None

    def RuntimeSession(self):
        tmp = self.Runtime()
        tmp = tmp['session']
        if tmp:
            self._session_operation = round(tmp['operate'])
            self._session_charge = round(tmp['charge'])
            self._session_cut = round(self._session_operation - self._session_charge)
            return None
        else:
            _LOGGER.debug("RuntimeSession: None")
            return None

    def MapSvgCacheTs(self):
        # Fixed
        _LOGGER.debug("---")
        _LOGGER.debug(f"MapSvgCache_Ts: {self.mapsvgcache_ts}")
        return self.mapsvgcache_ts

    def SvgxPos(self):
        # Fixed
        _LOGGER.debug("---")
        _LOGGER.debug(f"SvgxPos: {self.svg_xPos}")
        return self.svg_xPos

    def SvgyPos(self):
        # Fixed
        _LOGGER.debug("---")
        _LOGGER.debug(f"SvgyPos: {self.svg_yPos}")
        return self.svg_yPos

### --- User readable get functions

    def MowerStateDescription(self):
        # Fixed
        _LOGGER.debug("--- Fixed!")
        _LOGGER.debug("MowerStateDescription: Get Mower State from cached value")
        if str(self._mower_state) in MOWER_STATE_DESCRIPTION.keys():
            _LOGGER.debug(f"Value in dict = {self._mower_state}")
            #tmp_description = MOWER_STATE_DESCRIPTION.get(str(self._mower_state))
            self._mower_state_description = MOWER_STATE_DESCRIPTION.get(str(self._mower_state))
            _LOGGER.debug(f"Mower state description: {self._mower_state_description}")
        else:
            _LOGGER.debug(f"Value not in dict = {self._mower_state}")
            #tmp_description = "Value not in database: " + str(self._mower_state)
            self._mower_state_description = "Value not in database: " + str(self._mower_state)
        #return tmp_description
        return self._mower_state_description

    def MowingModeDescription(self):
        # Fixed
        _LOGGER.debug("MowingModeDescription: Get Mowing Mode Description from cached value")
        if str(self._alm_mode) in MOWING_MODE_DESCRIPTION.keys():
            _LOGGER.debug(f"Value in dict = {self._alm_mode}")
            #tmp_description = MOWER_STATE_DESCRIPTION.get(str(self._mower_state))
            self._mowingmode_description = MOWING_MODE_DESCRIPTION.get(str(self._alm_mode))
            _LOGGER.debug(f"Mowingmode description: {self._mowingmode_description}")
        else:
            _LOGGER.debug(f"Value not in dict = {self._alm_mode}")
            #tmp_description = "Value not in database: " + str(self._mower_state)
            self._mowingmode_description = "Value not in database: " + str(self._alm_mode)
        #return tmp_description
        return self._mowingmode_description

###################################################
### Functions for getting data from USERS cache

    def Email(self):
        _LOGGER.debug("---")  
        _LOGGER.debug(f"Email: {self.email}")
        return self.email

    def DisplayName(self):
        _LOGGER.debug("---")  
        _LOGGER.debug(f"DisplayName: {self.display_name}")
        return self.display_name

    def Language(self):
        _LOGGER.debug("---")  
        _LOGGER.debug(f"Language: {self.language}")
        return self.language

    def Country(self):
        _LOGGER.debug("---")  
        _LOGGER.debug(f"Country: {self.country}")
        return self.country

    def OptIn(self):
        _LOGGER.debug("---")  
        _LOGGER.debug(f"OptIn: {self.optin}")
        return self.optin

    def OptInApp(self):
        _LOGGER.debug("---")  
        _LOGGER.debug(f"OptInApp: {self.optinapp}")
        return self.optinapp

#########################################################
### Functions for getting data from SERIAL API call cache

    def Serial(self):
        # Fixed
        _LOGGER.debug("---")  
        _LOGGER.debug("Serial")
        return self._serial

    def AlmName(self):
        # Fixed
        _LOGGER.debug("---")  
        _LOGGER.debug("AlmName")
        return self._alm_name

    def ServiceCounter(self):
        # Fixed
        _LOGGER.debug("---")  
        _LOGGER.debug("ServiceCounter")
        return self._service_counter

    def NeedsService(self):
        # Fixed
        _LOGGER.debug("---")  
        _LOGGER.debug("NeedsService")
        return self._needs_service

    def AlmMode(self):
        # Fixed
        _LOGGER.debug("---")  
        _LOGGER.debug("AlmMode")
        return self._alm_mode

    def BareToolNumber(self):
        # Fixed
        _LOGGER.debug("---")  
        _LOGGER.debug("BareToolNumber")
        return self._bareToolnumber

    def AlmFirmwareVersion(self):
        # Fixed
        _LOGGER.debug("---")  
        _LOGGER.debug("Firmware")
        return self._alm_firmware_version

### --- User readable get functions

    def ModelDescription(self):
        # Fixed
        _LOGGER.debug("---")  
        _LOGGER.debug("ModelDescription")
        if str(self._bareToolnumber) in MOWER_MODEL_DESCRIPTION.keys():  
            _LOGGER.debug(f"Value in dict = {self._bareToolnumber}")  
            tmp_description = MOWER_MODEL_DESCRIPTION.get(str(self._bareToolnumber))
            self._model_description = MOWER_MODEL_DESCRIPTION.get(str(self._bareToolnumber))
        else:
            _LOGGER.debug(f"Value not in dict = {self._bareToolnumber}")  
            tmp_description = "Value not in database: " + str(self._bareToolnumber)
            self.model_description = "Value not in database: " + str(self._bareToolnumber)
        #return tmp_description
        return self._model_description

############################################################
### Functions for getting data from OPERATING API call cache

    def Battery(self):
        return self._battery

    def BatteryPercent(self):
        tmp = self.Battery()
        self._battery_percent = tmp['percent']
        return self._battery_percent

    def BatteryVoltage(self):
        tmp = self.Battery()
        self._battery_voltage = tmp['voltage']
        return self._battery_voltage

    def BatteryCycles(self):
        # Finished
        _LOGGER.debug("---")  
        _LOGGER.debug(f"Battery = {self._battery}")
        tmp = self.Battery()
        self._battery_cycles = tmp['cycles']
        return self._battery_cycles

    def BatteryDischarge(self):
        # Finished
        _LOGGER.debug("---")  
        _LOGGER.debug(f"self._battery_discharge = {self._battery_discharge}")
        tmp = self.Battery()
        self._battery_discharge = tmp['discharge']
        return self._battery_discharge

    def BatteryAmbientTemp(self):
        # Finished
        _LOGGER.debug("---")  
        _LOGGER.debug(f"self._battery_ambient_temp = {self._battery_ambient_temp}")
        tmp = self.Battery()
        self._battery_ambient_temp = tmp['ambient_temp']
        return self._battery_ambient_temp

    def BatteryTemp(self):
        # Finished
        _LOGGER.debug("---")  
        _LOGGER.debug(f"self._battery_temp = {self._battery_temp}")
        tmp = self.Battery()
        self._battery_temp = tmp['battery_temp']
        return self._battery_temp

    def Garden(self):
        # Finished
        _LOGGER.debug("---")  
        _LOGGER.debug(f"Garden = {self._garden}")
        return self._garden

    def HmiKeys(self):
        # Finished
        _LOGGER.debug("---")  
        _LOGGER.debug(f"HmiKeys = {self._hmikeys}")
        return self._hmikeys

############################################################
### Functions for getting data from UPDATES API call cache

    def FirmwareAvailable(self):
        # Finished
        _LOGGER.debug("---")  
        _LOGGER.debug(f"FirmwareAvailable = {self._firmware_available}")
        return self._firmware_available

############################################################
### Functions for getting data from NEXTCUTTING API call cache

    def NextCutting(self):
        # Finished
        _LOGGER.debug("---")
        _LOGGER.debug(f"NextCutting = {self.nextcutting}")
        return self.nextcutting

############################################################
### Functions for getting data from ALERTS API call cache

    def AlertsDescription(self):
        _LOGGER.debug("---")
        _LOGGER.debug("AlertsDescription: " + str(self.alerts))
        return self.alerts

### --- User readable get functions

    def AlertsCount(self):
        # Fixed
        _LOGGER.debug("---")
        self.alerts_count = len(self.alerts)
        _LOGGER.debug(f"AlertsCount: : {self.alerts_count}")
        return self.alerts_count

#######################################
### Sending commands to mower
####################################### 
    def putCommand(self, command):
        _LOGGER.debug("---")  
        _LOGGER.debug("postCommand: " + command)
        if command == "mow" or command == "pause" or command == "returnToDock":
            complete_url = "alms/" + self._serial + "/state"
            temp = self.put(complete_url, command)    
            return temp
        else:
            _LOGGER.debug("postCommand " + command + " not valid!")
            return "Wrong Command!"


###
# Not properly implemented yet
###


#    def getLocation(self):
#        _LOGGER.debug("---")
#        _LOGGER.debug("getLocation")
#        complete_url = 'alms/' + self._serial + '/predictive/location'
#        Runtime_temp = self.get(complete_url)
#        value = Runtime_temp
#        return value

#    def getPredicitiveCalendar(self):
#        _LOGGER.debug("---")
#        _LOGGER.debug("getPredicitveCalendar")
#        complete_url = 'alms/' + self._serial + '/predictive/calendar'
#        Runtime_temp = self.get(complete_url)
#        value = Runtime_temp
#        return value

#    def getUserAdjustment(self):
#        # No idea what this does?
#        _LOGGER.debug("---")
#        _LOGGER.debug("getUserAdjustment")
#        complete_url = 'alms/' + self._serial + '/predictive/useradjustment'
#        Runtime_temp = self.get(complete_url)
#        value = Runtime_temp
#        return value['user_adjustment']

#    def getCalendar(self):
#        _LOGGER.debug("---")
#        _LOGGER.debug("getCalendar")
#        complete_url = 'alms/' + self._serial + '/calendar'
#        Runtime_temp = self.get(complete_url)
#        value = Runtime_temp
#        return value

#    def getSecurity(self):
#        _LOGGER.debug("---")
#        _LOGGER.debug("getSecurity")
#        complete_url = 'alms/' + self._serial + '/security'
#        Runtime_temp = self.get(complete_url)
#        value = Runtime_temp
#        return value

#    def getAutomaticUpdate(self):
#        _LOGGER.debug("---")
#        _LOGGER.debug("getAutomaticUpdate")
#        complete_url = 'alms/' + self._serial + '/automaticUpdate'
#        Runtime_temp = self.get(complete_url)
#        value = Runtime_temp
#        return value

#    def getMap(self):
#        _LOGGER.debug("---")
#        print("getMap (Not implemented yet")
#        #complete_url = 'alms/' + self._serial + '/map'
#        #Runtime_temp = self.get(complete_url)
#        #value = Runtime_temp
#        value = "error"
#        return value

##########################################################################
### Basics for API calls
    def get(self, method):
        """Send a GET request and return the response as a dict."""
        _LOGGER.debug("---")  
        _LOGGER.debug("GET start")
        try:
            logindata = json.loads(self.login.content)
            contextId = logindata['contextId']
            _LOGGER.debug("   ContextID: " + contextId)
            headers = {CONTENT_TYPE: CONTENT_TYPE_JSON, 'x-im-context-id': contextId}
            url = self.api_url + method
            _LOGGER.debug("   >>>API CALL: " + url)
            #response = requests.get(url, headers=headers, timeout=30, verify=False)
            response = requests.get(url, headers=headers, timeout=30)
            _LOGGER.debug("   HTTP Status code: " + str(response.status_code))
            if response.status_code != 200:
                _LOGGER.debug("   need to call login again")
                self.authenticate()
                return
            else:
                _LOGGER.debug("   Json:" + str(response.json()))
                response.raise_for_status()
                _LOGGER.debug("GET end")
                return response.json()
        except requests.exceptions.ConnectionError as conn_exc:
            _LOGGER.debug("   Failed to update Indego status. Error: " + str(conn_exc))
            _LOGGER.debug("GET end")
            raise
    
    def put(self, url, method):
        """Send a PUT request and return the response as a dict."""
        _LOGGER.debug("---")  
        _LOGGER.debug("PUT start")
        try:
            logindata = json.loads(self.login.content)
            contextId = logindata['contextId']
            headers = {CONTENT_TYPE: CONTENT_TYPE_JSON, 'x-im-context-id': contextId}
            url = self.api_url + url
            data = '{"state":"' + method + '"}'
            _LOGGER.debug("   >>>API CALL: " + url)
            _LOGGER.debug("   headers: " + str(headers))
            _LOGGER.debug("   data: " + str(data))
            #response = requests.put(url, headers=headers, data=data, timeout=30, verify=False)
            response = requests.put(url, headers=headers, data=data, timeout=30)
            _LOGGER.debug("   HTTP Status code: " + str(response.status_code))
            if response.status_code != 200:
                _LOGGER.debug("   need to call login again")
                _LOGGER.debug("PUT end")
                self.authenticate()
                return
            else:
                _LOGGER.debug("   Status code: " + str(response))
                #response.raise_for_status()
                _LOGGER.debug("PUT end")
                #return response.json()
                return response.status_code                   #Not returning codes!!!

        except requests.exceptions.ConnectionError as conn_exc:
            _LOGGER.debug("   Failed to update Indego status. Error: " + str(conn_exc))
            _LOGGER.debug("PUT end")
            raise

#End PYPI __init__.py