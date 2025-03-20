from machine import Pin
from rgb_indicators import RGB_indicators
from wlan_config import URL, SECRET
from terminal_wlan import TermialWLAN
# import urequests

builtinLedPin = Pin("LED", Pin.OUT)
rgb_indicators = RGB_indicators(20)
terminal_WLAN = TermialWLAN()

def process():
    terminal_WLAN.process()
    if terminal_WLAN.isTryingToConnect:
        rgb_indicators.scan_network()
    else:
        rgb_indicators.turn_off() 

def render():
    rgb_indicators.render()


while True:
    builtinLedPin.toggle()
    process()
    render()
    # sleep(0.5)
