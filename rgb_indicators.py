from neopixel import Neopixel
from machine import Pin
from time import ticks_ms

class RGB_indicators:
    COLOR_BLUE = (0, 0, 255)
    COLOR_WHITE = (255, 255, 255)
    COLOR_NONE = (0, 0, 0)

    def __init__(self, pin):
        self.strip = Neopixel(4, 0, pin)
        self.turn_off()

    def turn_off(self):
        self.state = 0
        self.last_state_change = ticks_ms()

    def start_scanning_network(self):
        self.state = 1
        self.last_state_change = ticks_ms()

    def scan_network(self):
        if self.state != 1:
            self.start_scanning_network()

    def _set_colors(self, first = COLOR_NONE, second = COLOR_NONE, third = COLOR_NONE, fourth = COLOR_NONE):
        if self.strip.get_pixel(0) != first:  self.strip.set_pixel(0, first)
        if self.strip.get_pixel(1) != second: self.strip.set_pixel(1, second)
        if self.strip.get_pixel(2) != third:  self.strip.set_pixel(2, third)
        if self.strip.get_pixel(3) != fourth: self.strip.set_pixel(3, fourth)
        self.strip.show()

    def render(self):
        if self.state == 0:
            pass
        elif self.state == 1:
            period = (ticks_ms() - self.last_state_change) % 1500
            
            if period < 250:
                self._set_colors(first = self.COLOR_BLUE)
                return
            elif period < 500:
                self._set_colors(second = self.COLOR_BLUE)
                return
            elif period < 750:
                self._set_colors(third = self.COLOR_BLUE)
                return
            elif period < 1000:
                self._set_colors(fourth = self.COLOR_BLUE)
                return
            elif period < 1250:
                self._set_colors(third = self.COLOR_BLUE)
                return
            elif period < 1500:
                self._set_colors(second = self.COLOR_BLUE)
                return