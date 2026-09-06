print("... About to initialize CredAgent Logger...")

from .InitLogger import InitLogger

# Shared logger instance for the whole system
logger = InitLogger.get_logger()

print("CredAgent Logger initialized successfully.")
