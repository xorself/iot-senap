from network import WLAN
import machine
import senap_auth
import pycom

def wifi_is_connected():
    wlan = WLAN(mode=WLAN.STA)
    return wlan.isconnected()

def wifi_enable(connect_timeout):

    # Enable wifi
    wlan = WLAN(mode=WLAN.STA)

    nets = wlan.scan()

    for net in nets:
        if net.ssid == senap_auth.AUTH_WIFI_SSID:
            print('Connect to network ' + senap_auth.AUTH_WIFI_SSID + '...')
            wlan.connect(net.ssid, auth=(net.sec, senap_auth.AUTH_WIFI_PWD), timeout=connect_timeout)
            
            # Check status and idle while not connected...
            while not wlan.isconnected():
                machine.idle()
                
            print('Connected to ' + senap_auth.AUTH_WIFI_SSID)
            print(wlan.ifconfig())
            break
