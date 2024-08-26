from evdev import ecodes

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

THROTTLE = ecodes.ABS_THROTTLE
PITCH    = ecodes.ABS_Y
ROLL     = ecodes.ABS_X
YAW      = ecodes.ABS_RZ
HATX     = ecodes.ABS_HAT0X
HATY     = ecodes.ABS_HAT0Y


name = "Logitech Extreme 3D pro"

#############
# AXIS INFO #
#############

# THROTTLE: 
# min - 0   (North position)
# max - 255 (south position)

# PITCH:
# min - 0    (North position)
# max - 1023 (South position)

# ROLL
# min - 0    (West position)
# max - 1023 (East position)

# YAW
# min - 0   (West position)
# max - 255 (East position)

# HAT X
# -1 West
#  0 Neutral
#  1 East

# HAT Y
# -1 North
#  0 Neutral
#  1 South
