from machine import Pin

class Keyboard:
    R1 = Pin(10, Pin.OUT)
    R2 = Pin(9, Pin.OUT)
    R3 = Pin(8, Pin.OUT)
    R4 = Pin(7, Pin.OUT)
    C1 = Pin(6, Pin.IN, Pin.PULL_DOWN)
    C2 = Pin(5, Pin.IN, Pin.PULL_DOWN)
    C3 = Pin(4, Pin.IN, Pin.PULL_DOWN)

    def __init__(self):
        self.pressedButtons = []

    def process(self):
        self.pressedButtons = []
        self.R1.on()
        if self.C1.value() == 1: self.pressedButtons.append('1')
        if self.C2.value() == 1: self.pressedButtons.append('2')
        if self.C3.value() == 1: self.pressedButtons.append('3')
        self.R1.off()
        self.R2.on()
        if self.C1.value() == 1: self.pressedButtons.append('4')
        if self.C2.value() == 1: self.pressedButtons.append('5')
        if self.C3.value() == 1: self.pressedButtons.append('6')
        self.R2.off()
        self.R3.on()
        if self.C1.value() == 1: self.pressedButtons.append('7')
        if self.C2.value() == 1: self.pressedButtons.append('8')
        if self.C3.value() == 1: self.pressedButtons.append('9')
        self.R3.off()
        self.R4.on()
        if self.C1.value() == 1: self.pressedButtons.append('*')
        if self.C2.value() == 1: self.pressedButtons.append('0')
        if self.C3.value() == 1: self.pressedButtons.append('#')
        self.R4.off()