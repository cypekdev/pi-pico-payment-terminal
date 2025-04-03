from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd
from time import ticks_ms

class TermianlLCD:
    def _get_2f_amount(self) -> str:
        return f"{float(self.amount):.2f}"

    def __init__(self) -> None:
        i2c = I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)
        self._lcd = I2cLcd(i2c, 0x27, 2, 16)
        self.empty()

    def _rjust(self, s: str, n: int):
        return "".join((" "*(n - len(s)), s))

    def start_awaiting_for_action(self):
        self._status = 0
        self._last_status_change = ticks_ms()
        self._lcd.hide_cursor()
        self._lcd.clear()
        self._lcd.move_to(0, 0)
        self._lcd.putstr("Blik")
        self._lcd.move_to(6, 0)
        self._lcd.putstr("Z$10")
        self._lcd.move_to(12, 0)
        self._lcd.putstr("Card")
        self._lcd.move_to(1, 1)
        self._lcd.putchar('*')
        self._lcd.move_to(6, 1)
        self._lcd.putstr("Bank")
        self._lcd.move_to(14, 1)
        self._lcd.putchar('#')
        self._blinker_state = False

    def awaiting_for_action(self):
        if self._status != 0: self.start_awaiting_for_action()

    def entering_amount_blik(self):
        self._status = 1
        self.amount = ""
        self._previous_amount = self.amount
        self._lcd.clear()
        self._lcd.move_to(0, 0)
        self._lcd.putstr("To Pay:")
        self._lcd.move_to(12, 0)
        self._lcd.putstr("Blik")
        self._lcd.move_to(13, 1)
        self._lcd.putstr("PLN")
        self._lcd.move_to(12, 1)
        self._lcd.show_cursor()
        self._lcd.blink_cursor_on()

    def entering_amount_card(self):
        self._status = 2
        self.amount = ""
        self._previous_amount = self.amount
        self._lcd.clear()
        self._lcd.move_to(0, 0)
        self._lcd.putstr("To Pay:")
        self._lcd.move_to(12, 0)
        self._lcd.putstr("Card")
        self._lcd.move_to(13, 1)
        self._lcd.putstr("PLN")
        self._lcd.move_to(12, 1)
        self._lcd.show_cursor()
        self._lcd.blink_cursor_on()

    def entering_blik_code(self):
        self._status = 3
        self.blik_code = ""
        self._previous_blik_code = self.blik_code
        self._lcd.clear()
        self._lcd.move_to(0, 0)
        self._lcd.putstr(self._get_2f_amount())
        self._lcd.move_to(13, 0)
        self._lcd.putstr("PLN")
        self._lcd.move_to(0, 1)
        self._lcd.putstr("Blik:")
        self._lcd.move_to(10, 1)
        self._lcd.putstr("______")
        self._lcd.move_to(10, 1)
        self._lcd.show_cursor()
        self._lcd.blink_cursor_on()

    def waiting_for_card(self):
        self._status = 4
        self._lcd.hide_cursor()
        self._lcd.clear()
        self._lcd.move_to(0, 0)
        self._lcd.putstr("To Pay:")
        self._lcd.move_to(12, 0)
        self._lcd.putstr("Card")
        self._lcd.move_to(13, 1)
        self._lcd.putstr("PLN")
        amount_to_display = self._get_2f_amount()
        self._lcd.move_to(12 - len(amount_to_display), 1)
        self._lcd.putstr(amount_to_display[-12:])

    def start_entering_card_pin(self):
        self._status = 5
        self.card_pin_length = 0
        self._previous_card_pin_length = self.card_pin_length
        self._lcd.hide_cursor()
        self._lcd.clear()
        self._lcd.move_to(3, 0)
        self._lcd.putstr("Enter pin:")
        self._lcd.move_to(5, 1)
        self._lcd.putstr("____")        

    def start_payment_accepted(self):
        self._status = 6
        self.paymentId = ""

    def start_payment_error(self):
        self._last_status_change = ticks_ms()
        self._status = 7
        self.error = ""

    def start_connecting(self):
        self._status = 8
        self._last_status_change = ticks_ms()
        self._lcd.hide_cursor()
        self._lcd.clear()
        self._lcd.move_to(2, 0)
        self._lcd.putstr("Connecting.")

    def start_processin_payment(self):
        self._status = 9
        self._lcd.hide_cursor()
        self._lcd.clear()
        self._lcd.move_to(3, 0)
        self._lcd.putstr("Processing")
        self._lcd.move_to(4, 1)
        self._lcd.putstr("Payment")

    def connecting(self):
        if self._status != 8: self.start_connecting()

    def empty(self):
        self._status = 9
        self._lcd.hide_cursor()
        self._lcd.clear()

    def render(self):
        if self._status == 0:
            elapsed = (ticks_ms() - self._last_status_change) % 2000
            if elapsed < 1000:
                if self._blinker_state:
                    self._lcd.move_to(0, 1)
                    self._lcd.putchar(' ')
                    self._lcd.move_to(2, 1)
                    self._lcd.putchar(' ')
                    self._lcd.move_to(13, 1)
                    self._lcd.putchar(' ')
                    self._lcd.move_to(15, 1)
                    self._lcd.putchar(' ')
                    self._blinker_state = False
            else:
                if not self._blinker_state:
                    self._lcd.move_to(0, 1)
                    self._lcd.putchar('>')
                    self._lcd.move_to(2, 1)
                    self._lcd.putchar('<')
                    self._lcd.move_to(13, 1)
                    self._lcd.putchar('>')
                    self._lcd.move_to(15, 1)
                    self._lcd.putchar('<')
                    self._blinker_state = True

        elif self._status == 1 or self._status == 2 or self._status == 4:
            if self._previous_amount != self.amount:
                amount_to_display = ""
                full_len = len(self.amount)
                if full_len >= 12:
                    amount_to_display = self.amount
                else:
                    amount_to_display = "".join((' ' * (12 - len(self.amount)), self.amount[-12:]))
                self._lcd.move_to(0, 1)
                self._lcd.putstr(amount_to_display)
                self._lcd.move_to(12, 1)
                self._previous_amount = self.amount

        elif self._status == 3:
            if self._previous_blik_code != self.blik_code:
                self._lcd.move_to(10, 1)
                self._lcd.putstr(self.blik_code + ''.join(('_'*(6 - len(self.blik_code)))))
                self._lcd.move_to(10 + len(self.blik_code), 1)
                self._previous_blik_code = self.blik_code

        elif self._status == 5:
            if self._previous_card_pin_length != self.card_pin_length:
                self._lcd.move_to(5, 1)
                self._textSecondRow = "".join(('*' * self.card_pin_length, '_' * (4 - self.card_pin_length)))
                self._previous_card_pin_length = self.card_pin_length

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
        
        elif self._status == 8:
            elapsed = (ticks_ms() - self._last_status_change) % 1500
            if elapsed < 500:
                self._lcd.move_to(13, 0)
                self._lcd.putstr("  ")
            elif elapsed < 1000:
                self._lcd.move_to(13, 0)
                self._lcd.putstr(". ")
            else:
                self._lcd.move_to(13, 0)
                self._lcd.putstr("..")