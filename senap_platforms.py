import urequest as requests # https://github.com/jotathebest/micropython-lib/blob/master/urequests/urequests.py
import senap_auth 

UBIDOTS_API_URL = "https://industrial.api.ubidots.com/api/v1.6/devices/" 

# Base class for all platforms
class Platform:

    # Constructor
    def __init__(self):
        pass

    # Prepare API for specific platform
    def init_with_context(self, var_list):
        pass

    # Transmit dictionary of variable names and their values to platform
    def transmit(self, sensor_data):
        pass

    def report_battery_level(battery_level):
        pass


# Extended from reference/tutorial to handle list of values: 
# https://help.ubidots.com/en/articles/961994-connect-any-pycom-board-to-ubidots-using-wi-fi-over-http

UBIDOTS_BATTERY_VAR = "BatteryLevel"

# Ubidots platform connecting over WIFI and sending data using HTTP
class PlatformUbidots(Platform):

    # Constructor
    def __init__(self):
        Platform.__init__(self)

    # Prepare and initialize with context
    def init_with_context(self, var_list):
        pass
    
    # Builds the json to send the request from a dictionary of sensor inputs
    def build_json_from_dict(self, values:Dict):
        try:

            data = {}

            # Convert to json format
            for key in values.keys(): 
                data[key] = {"value": values[key]}
            
            return data
        except:
            return None
    
    # Sends the request. Please reference the REST API reference https://ubidots.com/docs/api/
    def transmit(self, values):
        try:

            url = UBIDOTS_API_URL + senap_auth.AUTH_DEVICE_NAME
            print("Post to " + url)
            headers = {"X-Auth-Token": senap_auth.AUTH_UBIDOTS_ACCESS_TOKEN, "Content-Type": "application/json"}
            
            # Build JSON
            data = self.build_json_from_dict(values)
            
            # No need to send in case no variables exist...
            if data is not None:
                print(data)
                req = requests.post(url=url, headers=headers, json=data)
                return req.json()
            else:
                pass
        except:
            pass

    # For Ubidots, just populate a dictionary with a battery level variable and transmit
    def report_battery_level(self, battery_level):
        battery_level_data = {}
        battery_level_data[UBIDOTS_BATTERY_VAR] = battery_level
        self.transmit(battery_level_data)