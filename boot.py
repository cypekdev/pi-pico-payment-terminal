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
blik_code = ''

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def add_to_ammount(char: str):
    global ammount

    if char == '.': 
        if len(ammount) == 0:
            ammount = '0'
        if '.' not in ammount:
            ammount += '.'

    if char.isdigit():
        if '.' in ammount:
            if (ammount.find(".") - len(ammount) + 3) > 0:
                ammount += char
        else:
            ammount += char
        if len(ammount) >= 2 and ammount[0] == '0' and ammount[1] != '.':
            ammount = ammount[1:len(ammount)]

def add_to_blik_code(char: str):
    global blik_code

    if len(blik_code) < 6 and char.isdigit():
        blik_code += char

def process_blik_payment():
    pass

def process_card_payment():
    pass

def process():
    global state
    global ammount
    global blik_code

    terminal_WLAN.process()
    if terminal_WLAN.isTryingToConnect:
        rgb_indicators.scan_network()
    else:
        rgb_indicators.turn_off() 
        keyboard.process()

        clicked = keyboard.get_clicked()
        pressed = keyboard.get_pressed()

        if state == 0: # waiting for action
            if clicked == '*':
                state = 1
                terminal_LCD.entering_amount_blik()
            elif clicked == '#':
                state = 2

        elif state == 1: # blik enter ammount
            if pressed != None:
                if pressed == '*':
                    state = 0
                elif pressed == '#':
                    if is_float(ammount):
                        state = 3
                        terminal_LCD.entering_blik_code()
            elif clicked != None:
                if clicked == '*':
                    ammount = ammount[:len(ammount) - 1]

                elif clicked == '#':
                    add_to_ammount('.')
                else: add_to_ammount(clicked)
                terminal_LCD.amount = ammount

        elif state == 2: # card enter ammount
            if pressed != None:
                if pressed == '*':
                    state = 0
                elif pressed == '#':
                    if is_float(ammount):
                        state = 3
                        terminal_LCD.entering_amount_card()
            elif clicked != None:
                if clicked == '*':
                    ammount = ammount[:len(ammount) - 1]

                elif clicked == '#':
                    add_to_ammount('.')
                else: add_to_ammount(clicked)
                terminal_LCD.amount = ammount

        elif state == 3: # blik enter code
            if pressed != None:
                if pressed == '*':
                    state = 1
            elif clicked != None:
                if clicked == '*':
                    blik_code = blik_code[:len(blik_code) - 1]
                elif clicked == '#':
                    pass
                    process_blik_payment()
                else:
                    add_to_blik_code(clicked)
                terminal_LCD.blik_code = blik_code


        elif state == 4: # waiting for card
            pass

        elif state == 5: # enter card pin
            pass





def render():
    rgb_indicators.render()
    terminal_LCD.render()


while True:
    builtinLedPin.toggle()
    process()
    render()
    # sleep(0.5)
