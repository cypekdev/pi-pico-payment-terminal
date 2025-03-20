from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd

class TermianlLCD:
    def __init__(self) -> None:
        i2c = I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)
        self._lcd = I2cLcd(i2c, 0x27, 2, 16)
        self._renderedTextFirstRow = ""
        self._renderedTextSecondRow = ""
        self._textFirstRow = ""
        self._textSecondRow = ""
        self._status = 0

    def process(self):
        if self._status == 0:
            self._textFirstRow = "      Z$10"
            self._textSecondRow = "      Bank"

    def render(self):
        if self._textFirstRow != self._renderedTextFirstRow or self._textFirstRow != self._renderedTextFirstRow:
            self._lcd.clear()
            self._lcd.putstr(self._textFirstRow)
            self._lcd.move_to(0, 1)
            self._lcd.putstr(self._textSecondRow)
            self._renderedTextFirstRow = self._textFirstRow
            self._renderedTextSecondRow = self._textSecondRow

