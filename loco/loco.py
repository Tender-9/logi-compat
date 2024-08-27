import random
import evdev
import logi
import xbox

EV_KEY = evdev.ecodes.EV_KEY
EV_ABS = evdev.ecodes.EV_ABS

class ControllerManager:
    def __init__(self, virtual_device):
        self.virtual_device = virtual_device
        self.view     = ViewController(self, virtual_device)
        self.throttle = ThrottleController(self, virtual_device)
        self.pitch    = PitchController(self, virtual_device)
        self.roll     = RollController(self, virtual_device)
        self.yaw      = YawController(self, virtual_device)
        self.key      = KeyController(self, virtual_device)
        self.running = 0
        self.zero_all()
    
    def toggle(self, event):
        if event.value == 1:
            return
        elif self.running == 0: 
            print("Running...")
            self.running = 1
        elif self.running == 1:
            self.zero_all()
            self.running = 0
            print("Paused...")
    
    def zero_all(self):
        self.throttle.zero()
        self.pitch.zero()
        self.roll.zero()
        self.yaw.zero()
        self.view.zero()
        self.virtual_device.syn()

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
        self.virtual_device.syn()


class Controller:
    def __init__(self, controller_manager, virtual_device):
        self.controller_manager = controller_manager
        self.virtual_device = virtual_device

class ViewController(Controller):
    def __init__(self, controller_manager, virtual_device):
        super().__init__(controller_manager, virtual_device)
    
    def update(self, event): 
        if event.code == logi.HATX: 
            axis = xbox.RIGHT_X
        elif event.code == logi.HATY:
            axis = xbox.RIGHT_Y
        else: return

        if event.value < 0: 
            self.virtual_device.write(EV_ABS, axis, 0)
        elif event.value == 0:
            self.virtual_device.write(EV_ABS, axis, 512)
        elif event.value > 0:
            self.virtual_device.write(EV_ABS, axis, 1023)
    
    def zero(self):
        self.virtual_device.write(EV_ABS, xbox.RIGHT_X, 512)
        self.virtual_device.write(EV_ABS, xbox.RIGHT_Y, 512)

class ThrottleController(Controller):
    def __init__(self, controller_manager, virtual_device):
        super().__init__(controller_manager, virtual_device)
        self.rev_state = 0
        self.state = 0

    def update(self, event): 
        if event.type == EV_ABS: self.state = 255 - event.value
        elif event.type == EV_KEY: self.rev_state = event.value

        if self.rev_state == 0:
            self.virtual_device.write(EV_ABS, xbox.LT, 0)
            self.virtual_device.write(EV_ABS, xbox.RT, self.state)

        elif self.rev_state == 1:
            self.virtual_device.write(EV_ABS, xbox.LT, self.state)
            self.virtual_device.write(EV_ABS, xbox.RT, 0)

    def zero(self):
        self.virtual_device.write(EV_ABS, xbox.LT, 0)
        self.virtual_device.write(EV_ABS, xbox.RT, 0)

class PitchController(Controller):
    def __init__(self, controller_manager, virtual_device):
        super().__init__(controller_manager, virtual_device)
    def update(self, event):
        self.virtual_device.write(EV_ABS, xbox.LEFT_Y, event.value)
    def zero(self):
        self.virtual_device.write(EV_ABS, xbox.LEFT_Y, 512)

class RollController(Controller):
    def __init__(self, controller_manager, virtual_device):
        super().__init__(controller_manager, virtual_device)
    def update(self, event):
        self.virtual_device.write(EV_ABS, xbox.LEFT_X, event.value) 
    def zero(self):
        self.virtual_device.write(EV_ABS, xbox.LEFT_X, 512)

class YawController(Controller):
    def __init__(self, controller_manager, virtual_device):
        super().__init__(controller_manager, virtual_device)
        self.nullzone = 100
    def update(self, event):
        if event.value <= (255/2 - self.nullzone/2):
            self.virtual_device.write(EV_KEY, xbox.LB, 1)
            self.virtual_device.write(EV_KEY, xbox.RB, 0)
        elif event.value >= (255/2 + self.nullzone/2):
            self.virtual_device.write(EV_KEY, xbox.LB, 0)
            self.virtual_device.write(EV_KEY, xbox.RB, 1)
        else: self.zero()
    def zero(self):
        self.virtual_device.write(EV_KEY, xbox.LB, 0)
        self.virtual_device.write(EV_KEY, xbox.RB, 0)

class KeyController(Controller):
    def __init__(self, controller_manager, virtual_device):
        super().__init__(controller_manager, virtual_device)
    
    def update(self, event):
        if event.code == logi.TRIGGER:
            self.virtual_device.write(EV_KEY, xbox.A, event.value)
        elif event.code == logi.THUMB:
            self.virtual_device.write(EV_KEY, xbox.DPAD_R, event.value)
        elif event.code == logi.BTN3:
            self.virtual_device.write(EV_KEY, xbox.X, event.value)
        elif event.code == logi.BTN7:
            self.controller_manager.toggle(event)
        elif event.code == logi.BTN9:
            self.virtual_device.write(EV_KEY, xbox.LTH, event.value)
        elif event.code == logi.BTN10:
            self.controller_manager.throttle.update(event)

def main(): 
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    physical_device = next((device for device in devices if device.name == logi.name), None)
    if physical_device == None: print("Logitech controller not found"); exit()

    # I have been needing to salt the VC for gta to recognize it more than once
    chars = "abcdefghijklmnopqrstuvwxyz"
    salt = "".join(chars[random.randrange(len(chars))] for _ in range(4))
    virtual_device = evdev.UInput(name = f"{xbox.name}_{salt}", events = xbox.events)

    manager = ControllerManager(virtual_device)
    try:
        print(f"Monitoring {physical_device.name}...")
        for event in physical_device.read_loop():
            manager.handle_event(event)
    except KeyboardInterrupt:
        print("Closing...")
        virtual_device.close()
