from machine import Pin
from time import ticks_ms, sleep_ms

class Keyboard:
    HOLD_TIME = 1000

    def __init__(self):        
        self._previousPressedBtn = None
        self._previousClickedButton = None
        self._clickedTime = None
        self._justClickedButton = None
        self.pressedButton = None
        self._rowsMap = [(Pin(10, Pin.OUT, value=0), ['1', '2', '3']),
                        (Pin(9, Pin.OUT, value=0), ['4', '5', '6']),
                        (Pin(8, Pin.OUT, value=0), ['7', '8', '9']),
                        (Pin(7, Pin.OUT, value=0), ['*', '0', '#'])]
        self._collumns = [Pin(6, Pin.IN, Pin.PULL_DOWN),
                        Pin(5, Pin.IN, Pin.PULL_DOWN),
                        Pin(4, Pin.IN, Pin.PULL_DOWN)]

    def _register_btn_click(self, btn: str | None = None):
        self._justClickedButton = btn
        if self._justClickedButton == None:
            self._previousPressedBtn = None
            self._clickedTime = None
        else:
            if self._justClickedButton != self._previousClickedButton: self._clickedTime = ticks_ms()

    def get_clicked(self):
        if self._justClickedButton == None:
            return self._previousClickedButton
        return None

    def get_pressed(self):
        if self._clickedTime != None:
            if (ticks_ms() - self._clickedTime) >= self.HOLD_TIME: 
                if self._previousPressedBtn != self._justClickedButton:
                    self._previousPressedBtn = self._justClickedButton
                    return self._justClickedButton 

        return None

    def process(self):
        self._previousClickedButton = self._justClickedButton

        if self._clickedTime != None:
            if ticks_ms() - self._clickedTime >= self.HOLD_TIME: 
                self.pressedButton = self._justClickedButton
            else:
                self.pressedButton = None
        

        for row, labels in self._rowsMap:
            row.high()
            # print(row)
            for coll in range(3):
               
                if self._collumns[coll].value() == 1:
                    row.low()
                    self._register_btn_click(labels[coll])
                    return
            
            row.low()

        self._register_btn_click(None)
