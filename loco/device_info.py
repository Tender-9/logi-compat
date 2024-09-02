# device_info.py
from devices import Device, Axis, Key
from evdev import ecodes

class LogiController(Device):
    def __init__(self, name = "Logitech Extreme 3D pro") -> None:
        super().__init__(name)
        self.TRIGGER = Key(self, ecodes.BTN_TRIGGER)
        self.THUMB   = Key(self, ecodes.BTN_THUMB)
        self.BTN3    = Key(self, ecodes.BTN_THUMB2)
        self.BTN4    = Key(self, ecodes.BTN_TOP)
        self.BTN5    = Key(self, ecodes.BTN_TOP2)
        self.BTN6    = Key(self, ecodes.BTN_PINKIE)
        self.BTN7    = Key(self, ecodes.BTN_BASE)
        self.BTN8    = Key(self, ecodes.BTN_BASE2)
        self.BTN9    = Key(self, ecodes.BTN_BASE3)
        self.BTN10   = Key(self, ecodes.BTN_BASE4)
        self.BTN11   = Key(self, ecodes.BTN_BASE5)
        self.BTN12   = Key(self, ecodes.BTN_BASE6)

        self.THROTTLE = Axis(self, ecodes.ABS_THROTTLE, 0, 255, 255)
        self.PITCH    = Axis(self, ecodes.ABS_Y, 0, 1023, 512)
        self.ROLL     = Axis(self, ecodes.ABS_X, 0, 1023, 512)
        self.YAW      = Axis(self, ecodes.ABS_RZ, 0, 255, 128)
        self.HATX     = Axis(self, ecodes.ABS_HAT0X, -1, 1, 0)
        self.HATY     = Axis(self, ecodes.ABS_HAT0Y, -1, 1, 0)



class XboxController(Device):
    def __init__(self, name = "Xbox Controller"):
        super().__init__(name)
        self.A      = Key(self, ecodes.BTN_SOUTH)
        self.B      = Key(self, ecodes.BTN_EAST)
        self.X      = Key(self, ecodes.BTN_WEST)
        self.Y      = Key(self, ecodes.BTN_NORTH)
        self.LB     = Key(self, ecodes.BTN_TL)
        self.RB     = Key(self, ecodes.BTN_TR)
        self.L3     = Key(self, ecodes.BTN_THUMBL)
        self.R3     = Key(self, ecodes.BTN_THUMBR)
        self.VIEW   = Key(self, ecodes.BTN_SELECT)
        self.MENU   = Key(self, ecodes.BTN_START)
        self.XBOX   = Key(self, ecodes.KEY_MODE)
        self.SHARE  = Key(self, ecodes.KEY_RECORD)
        self.DPAD_U = Key(self, ecodes.BTN_DPAD_UP)
        self.DPAD_D = Key(self, ecodes.BTN_DPAD_DOWN)
        self.DPAD_L = Key(self, ecodes.BTN_DPAD_LEFT)
        self.DPAD_R = Key(self, ecodes.BTN_DPAD_RIGHT)

        # ABS #
        self.LT      = Axis(self, ecodes.ABS_Z, 0, 255, 0)
        self.RT      = Axis(self, ecodes.ABS_RZ, 0, 255, 0)
        self.DHAT_X  = Axis(self, ecodes.ABS_HAT0X, -1, 1, 0)
        self.DHAT_Y  = Axis(self, ecodes.ABS_HAT0Y, -1, 1, 0)
        self.LEFT_X  = Axis(self, ecodes.ABS_X, -32768, 32767, 0)
        self.LEFT_Y  = Axis(self, ecodes.ABS_Y, -32768, 32767, 0)
        self.RIGHT_X = Axis(self, ecodes.ABS_RX, -32768, 32767, 0) 
        self.RIGHT_Y = Axis(self, ecodes.ABS_RY, -32768, 32767, 0)
