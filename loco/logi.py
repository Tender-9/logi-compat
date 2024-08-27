from evdev import AbsInfo, ecodes

# KEY #
TRIGGER = ecodes.BTN_TRIGGER 
THUMB   = ecodes.BTN_THUMB
BTN3    = ecodes.BTN_THUMB2
BTN4    = ecodes.BTN_TOP
BTN5    = ecodes.BTN_TOP2
BTN6    = ecodes.BTN_PINKIE
BTN7    = ecodes.BTN_BASE
BTN8    = ecodes.BTN_BASE2
BTN9    = ecodes.BTN_BASE3
BTN10   = ecodes.BTN_BASE4
BTN11   = ecodes.BTN_BASE5
BTN12   = ecodes.BTN_BASE6

# ABS #
THROTTLE = ecodes.ABS_THROTTLE
PITCH    = ecodes.ABS_Y
ROLL     = ecodes.ABS_X
YAW      = ecodes.ABS_RZ
HATX     = ecodes.ABS_HAT0X
HATY     = ecodes.ABS_HAT0Y

_key_info = [
    TRIGGER,
    THUMB,
    BTN3,
    BTN4, 
    BTN5,
    BTN6,
    BTN7,
    BTN8,
    BTN9,
    BTN10,
    BTN11,
    BTN12
]

_abs_info = [
    (THROTTLE,
     AbsInfo(min=0, max=255,
             value=0, fuzz=0,
             flat=0, resolution=0)),
    (PITCH,
     AbsInfo(min=0, max=1023,
             value=0, fuzz=0,
             flat=0, resolution=0)),
    (ROLL,
     AbsInfo(min=0, max=1023,
             value=0, fuzz=0,
             flat=0, resolution=0)),
    (YAW,
     AbsInfo(min=0, max=255,
             value=0, fuzz=0,
             flat=0, resolution=0)),
    (HATX,
     AbsInfo(min=-1, max=1,
             value=0, fuzz=0,
             flat=0, resolution=0)),
    (HATY,
     AbsInfo(min=-1, max=1,
             value=0, fuzz=0,
             flat=0, resolution=0)),
]

name = "Logitech Extreme 3D pro"
events = {
    ecodes.EV_KEY : _key_info,
    ecodes.EV_ABS : _abs_info
}
