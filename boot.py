from machine import Pin
from rgb_indicators import RGB_indicators
from wlan_config import URL, SECRET
from terminal_wlan import TermialWLAN
from keyboard import Keyboard
from terminal_lcd import TermianlLCD
# import urequests

builtinLedPin = Pin("LED", Pin.OUT)
rgb_indicators = RGB_indicators(20)
terminal_WLAN = TermialWLAN()
keyboard = Keyboard()
terminal_LCD = TermianlLCD()

def process():
    keyboard.process()
    terminal_WLAN.process()
    if terminal_WLAN.isTryingToConnect:
        rgb_indicators.scan_network()
    else:
        rgb_indicators.turn_off() 
    terminal_LCD.process()

def render():
    rgb_indicators.render()
    terminal_LCD.render()


while True:
    builtinLedPin.toggle()
    process()
    render()
    # sleep(0.5)
