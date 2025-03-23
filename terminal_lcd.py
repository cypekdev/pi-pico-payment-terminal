from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd
from time import ticks_ms

class TermianlLCD:
    def __init__(self) -> None:
        i2c = I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)
        self._lcd = I2cLcd(i2c, 0x27, 2, 16)
        self._renderedTextFirstRow = ""
        self._renderedTextSecondRow = ""
        self._textFirstRow = ""
        self._textSecondRow = ""
        self.start_awaiting_for_action()

    def _rjust(self, s: str, n: int):
        return "".join((" "*(n - len(s)), s))

    def start_awaiting_for_action(self):
        self._status = 0
        self._last_status_change = ticks_ms()

    def entering_amount_blik(self):
        self._status = 1
        self.amount = ""
        self._lcd.show_cursor()
        self._lcd.blink_cursor_on()

    def entering_amount_card(self):
        self._status = 2
        self.amount = ""

    def entering_blik_code(self):
        self._status = 3
        self.blik_code = ""
        self._lcd.show_cursor()
        self._lcd.blink_cursor_on()

    def waiting_for_card(self):
        self._status = 4

    def start_entering_card_pin(self):
        self._status = 5
        self.card_pin_length = 0

    def start_payment_accepted(self):
        self._status = 6
        self.paymentId = ""

    def start_payment_error(self):
        self._last_status_change = ticks_ms()
        self._status = 7
        self.error = ""

    def render(self):
        if self._status == 0:
            elapsed = (ticks_ms() - self._last_status_change) % 2000
            self._textFirstRow = "Blik  Z$10  Card"
            if elapsed < 1000:
                self._textSecondRow = ">*<   Bank   >#<"
            else:
                self._textSecondRow = " *    Bank    #"

        elif self._status == 1:
            self._textFirstRow = "To Pay:     Blik"
            self._textSecondRow = f"{self._rjust(self.amount, 12)} PLN"
            self._lcd.move_to(12, 1)
            
        elif self._status == 2 or self._status == 4:
            self._textFirstRow = "To Pay:     Card"
            self._textSecondRow = f"{self._rjust(self.amount, 12)} PLN"

        elif self._status == 3:
            ammount_text = self._rjust(f"{float(self.amount):.2f}", 12)
            self._textFirstRow = f"{ammount_text} PLN"
            self._textSecondRow = f"Blik:     {self.blik_code + ''.join(('_'*(6 - len(self.blik_code))))}"
            self._lcd.move_to(10 + len(self.blik_code), 1)

        elif self._status == 5:
            self._textFirstRow = "Enter pin:".center(16)
            self._textSecondRow = "".rjust(self.card_pin_length, '*').ljust(4, '_').center(16)

        elif self._status == 6:
            elapsed = ticks_ms() - self._last_status_change
            if elapsed < 3000:
                self._textFirstRow = f"Payment {str(self.paymentId)}".center(16)
                self._textSecondRow = "Accepted".center(16)
            else:
                self.start_awaiting_for_action()

        elif self._status == 7:
            self._textFirstRow = "Payment REJECTED"
          
            errorLength = len(self.error)
            if errorLength > 16:
                elapsed_scrolling_cycle = (ticks_ms() - self._last_status_change) % (500 * (errorLength - 15))
                character_shift = int(elapsed_scrolling_cycle / 500)

                self._textSecondRow = self.error[character_shift:(17+character_shift)]
            else:
                self._textSecondRow = self.error.center(16)

        if self._textFirstRow != self._renderedTextFirstRow or self._textSecondRow != self._renderedTextSecondRow:
            self._lcd.clear()
            self._lcd.putstr(self._textFirstRow)
            self._lcd.move_to(0, 1)
            self._lcd.putstr(self._textSecondRow)
            self._renderedTextFirstRow = self._textFirstRow
            self._renderedTextSecondRow = self._textSecondRow
