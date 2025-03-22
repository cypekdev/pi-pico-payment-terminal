from machine import Pin
from time import ticks_ms

class Keyboard:
    R1 = Pin(10, Pin.OUT)
    R2 = Pin(9, Pin.OUT)
    R3 = Pin(8, Pin.OUT)
    R4 = Pin(7, Pin.OUT)
    C1 = Pin(6, Pin.IN, Pin.PULL_DOWN)
    C2 = Pin(5, Pin.IN, Pin.PULL_DOWN)
    C3 = Pin(4, Pin.IN, Pin.PULL_DOWN)
    HOLD_TIME = 1000

    def __init__(self):        
        self._previousClickedButton = None
        self._clickedTime = None
        self._justClickedButton = None
        self.pressedButton = None

    def _register_btn_click(self, btn):
        self._justClickedButton = btn
        if self._justClickedButton != self._previousClickedButton: self._clickedTime = ticks_ms()

    def get_clicked(self):
        if self._justClickedButton == None:
            return self._previousClickedButton
        return None

    def get_pressed(self):
        if self._clickedTime != None:
            if (ticks_ms() - self._clickedTime) >= self.HOLD_TIME: 
                return self._justClickedButton

    def process(self):
        self._previousClickedButton = self._justClickedButton

        if self._clickedTime != None:
            if ticks_ms() - self._clickedTime >= self.HOLD_TIME: 
                self.pressedButton = self._justClickedButton
            else:
                self.pressedButton = None
        
        self.R1.on()
        if self.C1.value(): self._register_btn_click('1'); return
        if self.C2.value(): self._register_btn_click('2'); return
        if self.C3.value(): self._register_btn_click('3'); return
        self.R1.off()
        self.R2.on()
        if self.C1.value(): self._register_btn_click('4'); return
        if self.C2.value(): self._register_btn_click('5'); return
        if self.C3.value(): self._register_btn_click('6'); return
        self.R2.off()
        self.R3.on()
        if self.C1.value(): self._register_btn_click('7'); return
        if self.C2.value(): self._register_btn_click('8'); return
        if self.C3.value(): self._register_btn_click('9'); return
        self.R3.off()
        self.R4.on()
        if self.C1.value(): self._register_btn_click('*'); return
        if self.C2.value(): self._register_btn_click('0'); return
        if self.C3.value(): self._register_btn_click('#'); return
        self.R4.off()

        self._justClickedButton = None
        self._clickedTime = None