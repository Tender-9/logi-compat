from evdev import AbsInfo, ecodes

class Axis:
    def __init__(self, id, min, max, rest, fuzz=0, flat=0, resolution=0):
        self.id = id
        self.min = min
        self.max = max
        self.fuzz = fuzz
        self.rest = rest
        self.flat = flat
        self.resolution = resolution

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
        abs_info = AbsInfo(value=self.rest, min=self.min, 
                           max=self.max,     fuzz=self.fuzz,
                           flat=self.flat,   resolution=self.resolution)
        
        return (self, abs_info)

class Key:
    def __init__(self, id, value=0):
        self.id = id
        self.value = value

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

class LogiController:
    def __init__(self) -> None:
        self.TRIGGER = Key(ecodes.BTN_TRIGGER)
        self.THUMB   = Key(ecodes.BTN_THUMB)
        self.BTN3    = Key(ecodes.BTN_THUMB2)
        self.BTN4    = Key(ecodes.BTN_TOP)
        self.BTN5    = Key(ecodes.BTN_TOP2)
        self.BTN6    = Key(ecodes.BTN_PINKIE)
        self.BTN7    = Key(ecodes.BTN_BASE)
        self.BTN8    = Key(ecodes.BTN_BASE2)
        self.BTN9    = Key(ecodes.BTN_BASE3)
        self.BTN10   = Key(ecodes.BTN_BASE4)
        self.BTN11   = Key(ecodes.BTN_BASE5)
        self.BTN12   = Key(ecodes.BTN_BASE6)

        self.THROTTLE = Axis(ecodes.ABS_THROTTLE, min = 0, max = 255, rest = 255)
        self.PITCH    = Axis(ecodes.ABS_Y, min = 0, max = 1023, rest = 512)
        self.ROLL     = Axis(ecodes.ABS_X, min = 0, max = 1023, rest = 512)
        self.YAW      = Axis(ecodes.ABS_RZ, min = 0, max = 255, rest = 128)
        self.HATX     = Axis(ecodes.ABS_HAT0X, min = -1, max = 1, rest = 0)
        self.HATY     = Axis(ecodes.ABS_HAT0Y, min = -1, max = 1, rest = 0)

        self.name   = "Logitech Extreme 3D pro"
        self.events = self.get_events()
    
    def get_events(self):
        key_info = [
            self.TRIGGER,
            self.THUMB,
            self.BTN3,
            self.BTN4,
            self.BTN5,
            self.BTN6,
            self.BTN7,
            self.BTN8,
            self.BTN9,
            self.BTN10,
            self.BTN11,
            self.BTN12
        ]
        abs_info = [
            self.THROTTLE.get_abs_info(),
            self.PITCH.get_abs_info(),
            self.ROLL.get_abs_info(),
            self.YAW.get_abs_info(),
            self.HATX.get_abs_info(),
            self.HATY.get_abs_info(),
        ]
        events = {
            ecodes.EV_KEY : key_info,
            ecodes.EV_ABS : abs_info
        }
        return events


class XboxController:
    def __init__(self) -> None:
        # Keys #
        self.A      = Key(ecodes.BTN_SOUTH)
        self.B      = Key(ecodes.BTN_EAST)
        self.X      = Key(ecodes.BTN_WEST)
        self.Y      = Key(ecodes.BTN_NORTH)
        self.LB     = Key(ecodes.BTN_TL)
        self.RB     = Key(ecodes.BTN_TR)
        self.L3     = Key(ecodes.BTN_THUMBL)
        self.R3     = Key(ecodes.BTN_THUMBR)
        self.VIEW   = Key(ecodes.BTN_SELECT)
        self.MENU   = Key(ecodes.BTN_START)
        self.XBOX   = Key(ecodes.KEY_MODE)
        self.SHARE  = Key(ecodes.KEY_RECORD)
        self.DPAD_U = Key(ecodes.BTN_DPAD_UP)
        self.DPAD_D = Key(ecodes.BTN_DPAD_DOWN)
        self.DPAD_L = Key(ecodes.BTN_DPAD_LEFT)
        self.DPAD_R = Key(ecodes.BTN_DPAD_RIGHT)

        # ABS #
        self.LT      = Axis(ecodes.ABS_Z, min = 0, max = 255, rest = 0)
        self.RT      = Axis(ecodes.ABS_RZ, min = 0, max = 255, rest = 0)
        self.DHAT_X  = Axis(ecodes.ABS_HAT0X, min = -1, max = 1, rest = 0)
        self.DHAT_Y  = Axis(ecodes.ABS_HAT0Y, min = -1, max = 1, rest = 0)
        self.LEFT_X  = Axis(ecodes.ABS_X, min = -32768, max = 32767, rest = 0)
        self.LEFT_Y  = Axis(ecodes.ABS_Y, min = -32768, max = 32767, rest = 0)
        self.RIGHT_X = Axis(ecodes.ABS_RX, min = -32768, max = 32767, rest = 0) 
        self.RIGHT_Y = Axis(ecodes.ABS_RY, min = -32768, max = 32767, rest = 0)
        
        self.name = "Custom Xbox Controller"
        self.events = self.get_events()

    def get_events(self):
        key_info = [
            self.A,
            self.B, 
            self.X,
            self.Y,
            self.LB,
            self.RB,
            self.L3,
            self.R3,
            self.VIEW,
            self.MENU, 
            self.XBOX,  
            self.SHARE,
            self.DPAD_U,
            self.DPAD_D,
            self.DPAD_L,
            self.DPAD_R
        ]

        abs_info = [
            self.LT.get_abs_info(),
            self.RT.get_abs_info(),
            self.DHAT_X.get_abs_info(),
            self.DHAT_Y.get_abs_info(),
            self.LEFT_X.get_abs_info(),
            self.LEFT_Y.get_abs_info(),
            self.RIGHT_X.get_abs_info(),
            self.RIGHT_Y.get_abs_info(),
        ]

        events = {
            ecodes.EV_KEY : key_info,
            ecodes.EV_ABS : abs_info
        }

        return events
