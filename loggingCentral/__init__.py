print("... About to initialize HFDC Logger...")

from .InitLogger import InitLogger

# Shared logger instance for the whole system
logger = InitLogger.get_logger()

print("HFDC Logger initialized successfully.")
