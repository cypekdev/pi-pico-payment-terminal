from machine import Pin
from rgb_indicators import RGB_indicators
from wlan_config import URL, SECRET
from terminal_wlan import TermialWLAN
from keyboard import Keyboard
from terminal_lcd import TermianlLCD
from terminal_communication import TerminalCommunication
from mfrc522 import MFRC522
from buzzer import Buzzer

builtinLedPin = Pin("LED", Pin.OUT)
cardPresencePin = Pin(3, Pin.IN, Pin.PULL_UP)
rgb_indicators = RGB_indicators()
terminal_WLAN = TermialWLAN()
keyboard = Keyboard()
buzzer = Buzzer()
terminal_LCD = TermianlLCD()
termianl_communication = TerminalCommunication()
insertable_card_reader = MFRC522(sck=18,mosi=19,miso=16,rst=22,cs=17)
proximity_card_reader = MFRC522(sck=14,mosi=15,miso=12,rst=11,cs=13,spi_id=1)
state = 0
ammount = ""
blik_code = ""
card_id = None
card_code = None
require_card_pin = None
payment_type = None # 0 - blik, 1 - card


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

def get_card_id(mfrc: MFRC522) -> int|None:
    mfrc.init()
    (stat, tagtype) = mfrc.request(mfrc.REQIDL)
    if stat == mfrc.OK:
        (stat, uid) = mfrc.SelectTagSN()
        if stat == mfrc.OK:
            card = int.from_bytes(bytes(uid),'little')
            return card
    return None

def process():
    global state
    global ammount
    global blik_code
    global require_card_pin
    global payment_type
    global card_id
    global card_code

    terminal_WLAN.process()
    if terminal_WLAN.isTryingToConnect:
        rgb_indicators.scan_network()
        terminal_LCD.connecting()
    else:
        rgb_indicators.turn_off()
        
        keyboard.process()

        clicked = keyboard.get_clicked()
        pressed = keyboard.get_pressed()
        if clicked != None: print(clicked)
        if pressed != None: print(pressed + " pressed")

        if state == 0: # waiting for action
            terminal_LCD.awaiting_for_action()
            if clicked != None:
                if clicked == '*':
                    state = 1
                    payment_type = 0
                    terminal_LCD.entering_amount_blik()
                elif clicked == '#':
                    state = 2
                    payment_type = 1
                    terminal_LCD.entering_amount_card()

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
                        require_card_pin = float(ammount) >= 100
                        state = 4
                        terminal_LCD.waiting_for_card()
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
                    terminal_LCD.entering_amount_blik()
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
            card_id = None
            if Pin(cardPresencePin).value():                
                card_id = get_card_id(insertable_card_reader)
            else:
                card_id = get_card_id(proximity_card_reader)
            if card_id:
                buzzer.on_card_reading()
                if require_card_pin:
                    state = 5
                else:
                    state = 6

        elif state == 5: # enter card pin
            pass

        elif state == 6: # processing payment
            response = None
            if payment_type == 0:
                response = termianl_communication.blik_transfer(int(blik_code), float(ammount))
            elif payment_type == 1:
                if card_id != None:
                    if not require_card_pin and card_code != None: 
                        response = termianl_communication.card_transfer(card_id, float(ammount), int(card_code))
                    else:
                        response = termianl_communication.card_transfer(card_id, float(ammount))
            if response != None:
                type(response) 

def render():
    rgb_indicators.render()
    terminal_LCD.render()
    buzzer.render()


while True:
    builtinLedPin.toggle()
    process()
    render()
    # sleep(0.5)
