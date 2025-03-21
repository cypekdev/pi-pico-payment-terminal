from machine import Pin
from rgb_indicators import RGB_indicators
from wlan_config import URL, SECRET
from terminal_wlan import TermialWLAN
from keyboard import Keyboard
from terminal_lcd import TermianlLCD
from terminal_communication import TerminalCommunication

builtinLedPin = Pin("LED", Pin.OUT)
cardPresencePin = Pin(3, Pin.IN, Pin.PULL_UP)
rgb_indicators = RGB_indicators()
terminal_WLAN = TermialWLAN()
keyboard = Keyboard()
terminal_LCD = TermianlLCD()
termianl_communication = TerminalCommunication()
state = 0



def process():
    global state

    terminal_WLAN.process()
    if terminal_WLAN.isTryingToConnect:
        rgb_indicators.scan_network()
    else:
        rgb_indicators.turn_off() 

        previousPressed = keyboard.pressedButtons
        keyboard.process()
        justClicked = [btn for btn in keyboard.pressedButtons if btn not in previousPressed]

        if state == 0:
            if '*' in justClicked:
                state = 1

    terminal_LCD.process()

def render():
    rgb_indicators.render()
    terminal_LCD.render()


while True:
    builtinLedPin.toggle()
    process()
    render()
    # sleep(0.5)
