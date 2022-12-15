from micropython import const

from trezor.ui import rgb

# backlight brightness
BACKLIGHT_NORMAL = const(150)
BACKLIGHT_LOW = const(45)
BACKLIGHT_DIM = const(5)
BACKLIGHT_NONE = const(2)
BACKLIGHT_MAX = const(255)

# color palette
GREEN = rgb(0x00, 0xAE, 0x0B)
BLACK = rgb(0x00, 0x00, 0x00)
WHITE = rgb(0xFA, 0xFA, 0xFA)

# common color styles
BG = BLACK

# icons
ICON_CHECK = "trezor/res/check.toif"
