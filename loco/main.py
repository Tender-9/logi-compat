# main.py
from evdev.events import EV_ABS, EV_KEY
from device_info import LogiController, XboxController

import random
chars = "abcdefghijklmnopqrstuvwxyz"
salt = "".join(chars[random.randrange(len(chars))] for _ in range(4))

logi = LogiController()
xbox = XboxController(name = "Xbox_" + salt)

class ControllerManager:
    def __init__(self) -> None:
        self.running  = 0
        self.view     = ViewController()
        self.throttle = ThrottleController()
        self.pitch    = PitchController()
        self.roll     = RollController()
        self.yaw      = YawController()
        self.key      = KeyController(self)
   
    def toggle(self, event):
        if event.value == 1: return
        if self.running == 0:
            print("Running...")
            self.running = 1 
        elif self.running == 1:
            print("Paused...")
            self.zero_all()
            self.running = 0
    
    def zero_all(self):
        self.view.zero()
        self.throttle.zero()
        self.pitch.zero()
        self.roll.zero()
        self.yaw.zero()

    def handle_event(self, event):
        if self.running == 0 and event.code != logi.BTN7: return
        if event.type == EV_ABS:
            if event.code == logi.THROTTLE: self.throttle.update(event)
            elif event.code == logi.PITCH: self.pitch.update(event)
            elif event.code == logi.ROLL: self.roll.update(event)
            elif event.code == logi.YAW: self.yaw.update(event)
            elif event.code == logi.HATX: self.view.update(event)
            elif event.code == logi.HATY: self.view.update(event)
        elif event.type == EV_KEY: self.key.update(event)
        xbox.sync()
        pass

class ViewController():
    def __init__(self) -> None: pass
    
    def update(self, event) -> None:
        if event.code == logi.HATX: axis = xbox.RIGHT_X
        elif event.code == logi.HATY: axis = xbox.RIGHT_Y
        else: return 
        if event.value < 0: axis.write(axis.min)
        elif event.value == 0: axis.write(axis.rest)
        elif event.value > 0: axis.write(axis.max)
    
    def zero(self) -> None:
        xbox.RIGHT_X.write(xbox.RIGHT_X.rest)
        xbox.RIGHT_Y.write(xbox.RIGHT_Y.rest)

class ThrottleController():
    def __init__(self) -> None:
        self.throt_rev_key = logi.BTN10
        self.input = logi.THROTTLE
        self.prev_input = 0

    def update(self, event) -> None:
        if event.code == self.throt_rev_key: 
            value = self.prev_input
        else: value = self.input.max - event.value
        
        if self.throt_rev_key.state == 0:
            xbox.LT.write(xbox.LT.min)
            xbox.RT.write(value)
        elif self.throt_rev_key.state == 1: 
            xbox.LT.write(value)
            xbox.RT.write(xbox.RT.min)
        
        self.prev_input = value
    
    def zero(self) -> None:
        xbox.LT.write(xbox.LT.min)
        xbox.RT.write(xbox.RT.min)

class PitchController():
    def __init__(self) -> None:
        self.input  = logi.PITCH
        self.output = xbox.LEFT_Y
        self.accel_coeff = 2
    
    def update(self, event) -> None:
        value = self.accel(event.value)
        value = self.translate(value)
        self.output.write(value)

    def accel(self, value):
        c = self.accel_coeff
        a = (c - 1) / 524288
        b = (3 - 3*c) / 1024
        return a*value**3 + b*value**2 + c*value
    
    def translate(self, value):
        position = (value - self.input.min) / (self.input.max - self.input.min)
        target = self.output.min + position * (self.output.max - self.output.min)
        return int(round(target))
    
    def zero(self):
        self.output.write(self.output.rest)

class RollController():
    def __init__(self) -> None:
        self.input  = logi.ROLL
        self.output = xbox.LEFT_X
        self.accel_coeff = 2
    
    def update(self, event) -> None:
        value = self.accel(event.value)
        value = self.translate(value)
        self.output.write(value)

    def accel(self, value):
        c = self.accel_coeff
        a = (c - 1) / 524288
        b = (3 - 3*c) / 1024
        return a*value**3 + b*value**2 + c*value
    
    def translate(self, value):
        position = (value - self.input.min) / (self.input.max - self.input.min)
        target = self.output.min + position * (self.output.max - self.output.min)
        return int(round(target))
    
    def zero(self):
        self.output.write(self.output.rest)

class YawController():
    def __init__(self) -> None:
        self.nullzone = 160 # I know I know magic numbers...

    def update(self, event):
        if event.value <= logi.YAW.rest - (self.nullzone/2):
            xbox.LB.write(1)
            xbox.RB.write(0)
        elif event.value >= logi.YAW.rest + (self.nullzone/2):
            xbox.LB.write(0)
            xbox.RB.write(1)
        else: self.zero()

    def zero(self):
        xbox.LB.write(0)
        xbox.RB.write(0)

class KeyController():
    def __init__(self, controller_manager:ControllerManager) -> None:
        self.manager = controller_manager

    def update(self, event):
        code = event.code
        value = event.value
        
        if code == logi.TRIGGER: xbox.A.write(value)
        elif code == logi.THUMB: xbox.DPAD_R.write(value)
        elif code == logi.BTN3:  xbox.R3.write(value)
        elif code == logi.BTN4:  xbox.Y.write(value)
        elif code == logi.BTN7:  self.manager.toggle(event)
        elif code == logi.BTN9:  xbox.L3.write(value) 
        elif code == logi.BTN10: self.manager.throttle.update(event)



def main():
    logi.input_device_init()
    xbox.virtual_device_init()
    
    manager = ControllerManager()
    
    try:
        print(f"Monitoring {logi.name}...")
        for event in logi.read_loop():
            manager.handle_event(event)
    
    except KeyboardInterrupt:
        print("\rClosing...")
        xbox.close()
