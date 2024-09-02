import evdev
import random
import devices

EV_KEY = evdev.ecodes.EV_KEY
EV_ABS = evdev.ecodes.EV_ABS

logi = devices.LogiController()
xbox = devices.XboxController()

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
physical_device = next((device for device in devices if logi.name in device.name), None)
if physical_device == None: print("Logitech controller not found"); exit()

chars = "abcdefghijklmnopqrstuvwxyz"
salt = "".join(chars[random.randrange(len(chars))] for _ in range(4))
virtual_device = evdev.UInput(name = f"{xbox.name}_{salt}", events = xbox.events)


def works():
    for event in physical_device.read_loop():
        code = event.code 
        value = event.value
    
        print(f"code : {code}, value : {value}")

        if code == logi.HATX:
            if value == 1:
                print("Here")

        print(f"code : {code}, value : {value}")

def test():
    for event in physical_device.read_loop():
        code = event.code 
        value = event.value
    
        print(f"code : {code}, value : {value}")

        if code == logi.HATX:
            if value == 1:
                print("One")
    pass


test()
