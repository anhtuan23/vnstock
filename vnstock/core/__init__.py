# Use local stub instead of vnai to disable ads/telemetry
from vnstock.core.vnai_stub import *
from .utils.parser import *
from .utils.logger import *
from .utils.env import *

# Note: vnai.setup() is called in vnstock/__init__.py after all imports are complete
# to avoid circular import issues
