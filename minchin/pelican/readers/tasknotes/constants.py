# metadata
__title__ = "minchin.pelican.readers.tasknotes"
__version__ = "1.0.0"
__description__ = "Tasknotes for Pelican"
__author__ = "W. Minchin"
__email__ = "w_minchin@hotmail.com"
__url__ = "https://blog.minchin.ca/label/tasknotes-pelican/"
__license__ = "MIT License"

# Configuration Defaults
LOG_PREFIX = "[TaskNotes]"

DEFAULT_TASKNOTES_FOLDERS: list[str] = [
    "tasks",
]
DEFAULT_TASKNOTES_CATEGORY: str = "tasks"

DEFAULT_IN_PROGRESS_STATUS: list[str] = [
    "in-progress",
    "in progress",
    "20-in-progress",
]
DEFAULT_CANCELLED_STATUS: list[str] = [
    "cancelled",
    "canceled",
    "50-cancelled",
]
DEFAULT_DUPLICATE_STATUS: list[str] = [
    "duplicate",
    "60-duplicate",
]
DEFAULT_DONE_STATUS: list[str] = [
    "done",
    "30-done",
]
