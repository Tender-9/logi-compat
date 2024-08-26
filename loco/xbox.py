from evdev import AbsInfo, ecodes

# Keys #
A      = ecodes.BTN_SOUTH
B      = ecodes.BTN_EAST
X      = ecodes.BTN_WEST
Y      = ecodes.BTN_NORTH
LB     = ecodes.BTN_TL
RB     = ecodes.BTN_TR
LTH    = ecodes.BTN_THUMBL
RTH    = ecodes.BTN_THUMBR
VIEW   = ecodes.BTN_SELECT
MENU   = ecodes.BTN_START
XBOX   = ecodes.KEY_MODE  
SHARE  = ecodes.KEY_RECORD 
DPAD_U = ecodes.BTN_DPAD_UP
DPAD_D = ecodes.BTN_DPAD_DOWN
DPAD_L = ecodes.BTN_DPAD_LEFT
DPAD_R = ecodes.BTN_DPAD_RIGHT


# ABS #
LT      = ecodes.ABS_Z
RT      = ecodes.ABS_RZ
DHAT_X  = ecodes.ABS_HAT0X
DHAT_Y  = ecodes.ABS_HAT0Y
LEFT_X  = ecodes.ABS_X
LEFT_Y  = ecodes.ABS_Y
RIGHT_X = ecodes.ABS_RX
RIGHT_Y = ecodes.ABS_RY


_key_info = [
    A,
    B, 
    X,
    Y,
    LB,
    RB,
    LTH,
    RTH,
    VIEW,
    MENU, 
    XBOX,  
    SHARE,
    DPAD_U,
    DPAD_D,
    DPAD_L,
    DPAD_R
]

_abs_info = [
    (LT,
     AbsInfo(min = 0,   max = 255,
             value = 0, fuzz = 0,
             flat = 0,  resolution = 0)),
    (RT,
     AbsInfo(min = 0,   max = 255,
             value = 0, fuzz = 0,
             flat = 0,  resolution = 0)),
    (LEFT_X,
     AbsInfo(min = 0,   max = 1023,
             value = 0, fuzz = 0,
             flat = 0,  resolution = 0)),
    (LEFT_Y,
     AbsInfo(min = 0,   max = 1023,
             value = 0, fuzz = 0,
             flat = 0,  resolution = 0)),
    (RIGHT_X,
     AbsInfo(min = 0,   max = 1023,
             value = 0, fuzz = 0,
             flat = 0,  resolution = 0)),
    (RIGHT_Y,
     AbsInfo(min = 0, max = 1023,
             value = 0, fuzz = 0,
             flat = 0,  resolution = 0)),
    (DHAT_X,
     AbsInfo(min = -1,   max = 1,
             value = 0, fuzz = 0,
             flat = 0,  resolution = 0)),
    (DHAT_Y,
     AbsInfo(min = -1,   max = 1,
             value = 0, fuzz = 0,
             flat = 0,  resolution = 0))
]

name = "Custom Controller"
events = {
    ecodes.EV_KEY : _key_info,
    ecodes.EV_ABS : _abs_info
}
