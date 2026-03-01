# metadata
__title__ = "minchin.pelican.readers.tasknotes"
__version__ = "0.1.2-dev"
__description__ = "Tasknotes for Pelican"
__author__ = "W. Minchin"
__email__ = "w_minchin@hotmail.com"
__url__ = "https://blog.minchin.ca/label/tasknotes-pelican/"
__license__ = "MIT License"

# Configuration Defaults
LOG_PREFIX = "[TaskNotes]"

DEFAULT_TASKNOTES_CATEGORY = "tasks"

DEFAULT_IN_PROGRESS_STATUS = [
    "in-progress",
    "in progress",
    "20-in-progress",
]
DEFAULT_CANCELLED_STATUS = [
    "cancelled",
    "canceled",
    "50-cancelled",
]
DEFAULT_DUPLICATE_STATUS = [
    "duplicate",
    "60-duplicate",
]
DEFAULT_DONE_STATUS = [
    "done",
    "30-done",
]
