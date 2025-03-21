from machine import Pin
from time import ticks_ms

class Buzzer:
    def __init__(self):
        self._pin = Pin(2, Pin.OUT)
        self.turn_off()

    def turn_off(self):
        self._state = 0
        self._lastStateChange = ticks_ms()

    def on_card_reading(self):
        self._state = 1
        self._lastStateChange = ticks_ms()

    def on_payment_rejected(self):
        self._state = 2
        self._lastStateChange = ticks_ms()

    def render(self):
        if self._state == 0:
            self._pin.off()
        elif self._state == 1:
            elapsed = ticks_ms() - self._lastStateChange
            if elapsed < 1000:
                self._pin.on()
            else:
                self._pin.off()
                self.turn_off()
        elif self._state == 2:
            elapsed = ticks_ms() - self._lastStateChange
            if elapsed < 100:
                self._pin.on()
            elif elapsed < 200:
                self._pin.off()
            elif elapsed < 300:
                self._pin.on()
            elif elapsed < 400:
                self._pin.off()
            elif elapsed < 500:
                self._pin.on()
            else:
                self._pin.off()
                self.turn_off()


