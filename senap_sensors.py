import time
from dth import DTH #  Jurassic Port, https://github.com/JurassicPork/DHT_PyCom/tree/pulses_get
from machine import ADC
from machine import Pin

# Sensor variable names
DHT_TEMPERATURE_VAR_NAME = 'Temperature'
DHT_HUMIDITY_VAR_NAME = 'Humidity'
LDR_LIGHT_VAR_NAME = 'Light'
SENSOR_STATUS_VAR_NAME = 'Status'
SENSOR_INDEX_PREFIX = '_S'

# Sensor base class
class Sensor:
    def __init__(self, pin_id, sensor_id):
        self.sensor_id = sensor_id
        self.pin_id = pin_id
        self.vars = []
        self.first_cycle = True

        # Sensors currently reported status. Functional=True or Failed=False  
        self.reported_status = False

        # Automatically register status variable
        self.status_var_name = self._register_var(SENSOR_STATUS_VAR_NAME)
        
    def get_vars(self):
        return self.vars

    # Attempt to read sensor
    def read(self, max_attempts, attempt_delay, sensor_data):
        result = True

        # Attempt max (config.CFG_SENSOR_MAX_ATTEMPTS) times, then trigger alarm
        for x in range(max_attempts):

            result = self.try_read(sensor_data)

            # Break if valid
            if result:
                break
            
            # Else sleep and retry...
            time.sleep(attempt_delay)   

        # Report status change (alwats report on first cycle)
        if result != self.reported_status or self.first_cycle: 
            self.reported_status = result
            sensor_data[self.status_var_name] = 1 if result else 0 
        
        self.first_cycle = False
        return result   


    # Read sensor and collect sensor data
    def try_read(self, sensordata):
        pass

    # Register variable, automatically append sensor-id and return variable index
    def _register_var(self, name):

        # Mangle name, append and return  
        varname = name + SENSOR_INDEX_PREFIX + str(self.sensor_id)
        self.vars.append(varname)
        return varname

# LDR Sensor class
class SensorLDR(Sensor):
    
    def __init__(self, pin_id, sensor_id):

        # Superclass init
        Sensor.__init__(self, pin_id, sensor_id)

        self.sensor_pin = Pin(self.pin_id, mode=Pin.IN)       
        self.adc = ADC(bits=12) 
        self.channel = self.adc.channel(attn=ADC.ATTN_11DB, pin=self.pin_id)  
        
        # Light variable index, assigned in init
        self.light_var = self._register_var(LDR_LIGHT_VAR_NAME)

    # Collect sensor data
    def try_read(self, sensor_data):
        
        result = self.channel()

        # Store reading in dictionary
        sensor_data[self.light_var] = result

        # No error handling for this sensor, always report successful read
        return True


TH_SENSOR_DHT111 = 0
TH_SENSOR_DHT222 = 1

# LDR Sensor class
class SensorDHT(Sensor):

    def __init__(self, pin, id):
        Sensor.__init__(self, pin, id)
        
        self.th = DTH(pin, TH_SENSOR_DHT111)

        self.humidity_var = self._register_var(DHT_HUMIDITY_VAR_NAME)
        self.temperature_var = self._register_var(DHT_TEMPERATURE_VAR_NAME)
        

    # Collect sensor data
    def try_read(self, sensor_data):
        
        result = self.th.read()

        # Store data in case sensor was read without error
        # Use the manged variable names as keys in sensor_data dictionary
        if result.is_valid():
            sensor_data[self.temperature_var] = result.temperature
            sensor_data[self.humidity_var] = result.humidity
        
        # Break if valid
        return result.is_valid()