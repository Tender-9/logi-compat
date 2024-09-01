import evdev

EV_KEY = evdev.ecodes.EV_KEY
EV_ABS = evdev.ecodes.EV_ABS

class Device:
    def __init__(self, name):
        self.name = name
        self.events = None
        self.keys = []
        self.axes = []
        self.virtual_device = None
        self.input_device   = None
        
    def virtual_device_init(self):
        keyinfo = self.keys
        absinfo = [axis.get_abs_info() for axis in self.axes]
        events = {
            evdev.ecodes.EV_KEY : keyinfo,
            evdev.ecodes.EV_ABS : absinfo
        }
        self.virtual_device = evdev.UInput(name = self.name, events = events)

    def input_device_init(self): 
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()] 
        self.input_device = next((device for device in devices if self.name in device.name), None)
        if self.input_device == None: raise ValueError(f"{self.name} not found")

    def sync(self):
        if self.virtual_device == None:
            raise ValueError(f"No virtual device initiated for {self.name}")
        self.virtual_device.syn()

    def read_loop(self):
        if self.input_device == None:
            raise ValueError(f"No input device initiated for {self.name}")
        for event in self.input_device.read_loop():
            
            if event.code in self.keys:
                index = self.keys.index(event.code)
                self.keys[index].write(event.value)

            elif event.code in self.axes:
                index = self.axes.index(event.code)
                self.axes[index].write(event.value)
            
            yield event
    
    def close(self): 
        if self.virtual_device == None:
            raise ValueError(f"No virtual device initiated for {self.name}")
        self.virtual_device.close()


class Axis:
    def __init__(self, device:Device, id, min, max, rest, fuzz=0, flat=0, resolution=0):
        self.device = device
        self.id = id
        self.min = min
        self.max = max
        self.fuzz = fuzz
        self.rest = rest
        self.flat = flat
        self.resolution = resolution
        self.state = 0

        self.device.axes.append(self)

    def __repr__(self) -> str:
        return f"{self.id}"
    
    def __int__(self):
        return self.id

    def __eq__(self, other):
        if isinstance(other, int):
            return self.id == other
        return NotImplemented
    
    def __index__(self):
        return self.id

    def get_abs_info(self):
        abs_info = evdev. AbsInfo(value=self.rest, min=self.min, 
                                  max=self.max,    fuzz=self.fuzz,
                                  flat=self.flat,  resolution=self.resolution)
        
        return (self, abs_info)
    
    def write(self, value):
        if self.state == value: return
        if self.device.virtual_device != None:
            self.device.virtual_device.write(EV_ABS, self, value)
        self.state = value


class Key:
    def __init__(self, device:Device, id, value=0):
        self.device = device
        self.id = id
        self.state = value
        self.device.keys.append(self)

    def __repr__(self):
        return f"{self.id}"

    def __int__(self):
        return self.id

    def __index__(self):
        return self.id

    def __eq__(self, other):
        if isinstance(other, int):
            return self.id == other
        return NotImplemented
    
    def write(self, value):
        if value == self.state: return
        if self.device.virtual_device != None:
            self.device.virtual_device.write(EV_KEY, self.id, value)
        self.state = value
