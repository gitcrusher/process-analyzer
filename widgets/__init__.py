# widgets/__init__.py

# Import all widget classes to make them accessible via the package
from .gear_card import GearCard
from .progress_group import ProgressGroup
from .image_progress import ImageProgress  # Remove duplicate ImageProgressCard import
from .icon_text import IconText  # Rename IconTextCard to IconText to match home.py import
from .error_card import ErrorCard
from .toggle_card import ToggleCard
from .circular_progress import CircularProgressBar

# Define __all__ to control what gets imported with "from widgets import *"
__all__ = [
    "GearCard",
    "ProgressGroup",
    "ImageProgress",  # Match the corrected import
    "IconText",      # Match the corrected import
    "ErrorCard",
    "ToggleCard",
    "CircularProgressBar"
]