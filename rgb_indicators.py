from neopixel import Neopixel
from machine import Pin
from time import ticks_ms

class RGB_indicators:
    COLOR_RED = (255, 0, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_BLUE = (0, 0, 255)
    COLOR_WHITE = (255, 255, 255)
    COLOR_NONE = (0, 0, 0)


    def __init__(self):
        self._strip = Neopixel(4, 0, 20, mode="GRB")
        self.turn_off()

    def turn_off(self):
        self._state = 0
        self._last_state_change = ticks_ms()

    def start_scanning_network(self):
        self._state = 1
        self._last_state_change = ticks_ms()

    def scan_network(self):
        if self._state != 1:
            self.start_scanning_network()

    def start_on_connected(self):
        self._state = 2
        self._last_state_change = ticks_ms()

    def start_payment_rejected(self):
        self._state = 3
        self._last_state_change = ticks_ms()

    def ready_to_read(self):
        self._state = 4
        self._set_colors(self.COLOR_WHITE)

    def card_reading(self):
        self._state = 5
        self._set_colors(self.COLOR_WHITE, self.COLOR_WHITE)

    def request_processing(self):
        self._state = 6
        self._set_colors(self.COLOR_WHITE, self.COLOR_WHITE, self.COLOR_WHITE)

    def start_request_accepted(self):
        self._state = 7

    def _set_colors(self, first = COLOR_NONE, second = COLOR_NONE, third = COLOR_NONE, fourth = COLOR_NONE):
        if self._strip.get_pixel(0) != first:  self._strip.set_pixel(0, first)
        if self._strip.get_pixel(1) != second: self._strip.set_pixel(1, second)
        if self._strip.get_pixel(2) != third:  self._strip.set_pixel(2, third)
        if self._strip.get_pixel(3) != fourth: self._strip.set_pixel(3, fourth)
        self._strip.show()

    def render(self):
        if self._state == 0:
            self._set_colors()
        elif self._state == 1:
            period = (ticks_ms() - self._last_state_change) % 1500
            if period < 250:
                self._set_colors(first = self.COLOR_BLUE)
            elif period < 500:
                self._set_colors(second = self.COLOR_BLUE)
            elif period < 750:
                self._set_colors(third = self.COLOR_BLUE)
            elif period < 1000:
                self._set_colors(fourth = self.COLOR_BLUE)
            elif period < 1250:
                self._set_colors(third = self.COLOR_BLUE)
            elif period < 1500:
                self._set_colors(second = self.COLOR_BLUE)
        elif self._state == 2:
            period = ticks_ms() - self._last_state_change
            if period < 125:
                self._set_colors(self.COLOR_BLUE, self.COLOR_BLUE, self.COLOR_BLUE, self.COLOR_BLUE)
            elif period < 250:
                self._set_colors()
            elif period < 375:
                self._set_colors(self.COLOR_BLUE, self.COLOR_BLUE, self.COLOR_BLUE, self.COLOR_BLUE)
            else:
                self.turn_off()
        elif self._state == 3:
            elapsed = (ticks_ms() - self._last_state_change) % 500
            if elapsed < 250:
                self._set_colors(self.COLOR_RED, self.COLOR_RED, self.COLOR_RED, self.COLOR_RED)
            else:
                self._set_colors()
        elif self._state == 7:
            elapsed = ticks_ms() - self._last_state_change
            if elapsed < 125:
                self._set_colors(self.COLOR_GREEN, self.COLOR_GREEN, self.COLOR_GREEN, self.COLOR_GREEN)
            elif elapsed < 250:
                self._set_colors()
            elif elapsed < 375:
                self._set_colors(self.COLOR_GREEN, self.COLOR_GREEN, self.COLOR_GREEN, self.COLOR_GREEN)
            else:
                self.turn_off()