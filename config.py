"""Global configuration for the desktop pet."""

# Window
WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200
FPS = 30

# Pet behavior
WALK_INTERVAL_MIN = 15   # seconds min between random walks
WALK_INTERVAL_MAX = 60   # seconds max between random walks
WALK_DURATION_MIN = 3    # seconds min walk duration
WALK_DURATION_MAX = 8    # seconds max walk duration
WALK_SPEED = 80          # pixels per second

# Status decay (per second)
HUNGER_DECAY = 0.0067    # ~2 per 5 minutes
MOOD_DECAY = 0.0017      # ~1 per 10 minutes
ENERGY_DECAY = 0.02      # drained by activities
ENERGY_RECOVER = 0.5     # recovered per second when sleeping

# Status limits
STATUS_MAX = 100
STATUS_MIN = 0
STATUS_LOW = 30          # threshold for "unhappy" behavior
AUTO_SLEEP_THRESHOLD = 15  # energy below this triggers auto-sleep

# Interaction effects
CLICK_MOOD_BOOST = 5
FEED_HUNGER_BOOST = 40
PLAY_MOOD_BOOST = 30
PLAY_ENERGY_COST = 20

# Menu
MENU_FONT_SIZE = 14
MENU_BG = (50, 50, 60)
MENU_TEXT = (240, 240, 240)
MENU_HOVER = (70, 70, 90)

# Speech bubble
BUBBLE_BG = (255, 255, 255, 220)
BUBBLE_TEXT = (40, 40, 40)
BUBBLE_SHOW_SECONDS = 5
