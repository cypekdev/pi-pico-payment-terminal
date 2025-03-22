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
ammount = ''

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def add_to_ammount(char):
    global ammount

    if char == '.' and '.' not in ammount:
        ammount += '.'
    if char.isdecimal():
        if '.' in ammount:
            if (ammount.find(".") - len(ammount) + 3) > 0:
                ammount += char
        else:
            ammount += char

def process():
    global state
    global ammount

    terminal_WLAN.process()
    if terminal_WLAN.isTryingToConnect:
        rgb_indicators.scan_network()
    else:
        rgb_indicators.turn_off() 
        keyboard.process()

        clicked = keyboard.get_clicked()
        pressed = keyboard.get_pressed()
        
        if state == 0:
            if clicked == '*':
                state = 1
            elif clicked == '#':
                state = 2
        elif state == 1:
            if clicked != None:
                if pressed == '*':
                    state = 0
                elif clicked == '*':
                    ammount = ammount[:len(ammount) - 1]
                elif pressed == "#":
                    if is_float(ammount):
                        pass # todo
                elif clicked == '#':
                    add_to_ammount('.')
                else: add_to_ammount(clicked)

            

            

def render():
    rgb_indicators.render()
    terminal_LCD.render()


while True:
    builtinLedPin.toggle()
    process()
    render()
    # sleep(0.5)
