from machine import Pin
from utime import sleep
from rgb_indicators import RGB_indicators
import wlan_config
from network import WLAN, STA_IF
# import urequests

builtinLedPin = Pin("LED", Pin.OUT)
rgb_indicators = RGB_indicators(20)
wlan = WLAN(STA_IF)
wlan.active(True)
reconnect = True

def process():
    global reconnect
    if not wlan.isconnected(): 
        if reconnect:
            wlan.connect(wlan_config.SSID, wlan_config.PWD)
            print("Próba nawiązania połączenia")
            reconnect = False
            rgb_indicators.start_scanning_network()
    else:
        reconnect = True
        rgb_indicators.turn_off()
    

def render():
    rgb_indicators.render()


while True:
    builtinLedPin.toggle()
    # print("asd")
    process()
    render()
    sleep(0.5)
