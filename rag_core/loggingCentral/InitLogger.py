import logging
from logging.handlers import TimedRotatingFileHandler
import os

class InitLogger:
    @staticmethod
    def get_logger(name="Cred_FinTech_Agent"):
        os.makedirs("logs", exist_ok=True)

        handler = TimedRotatingFileHandler(
            "logs/Cred_FinTech_AgentS.log",
            when="midnight",
            interval=1,
            backupCount=30,
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d | %(levelname)s | %(module)s |  %(funcName)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)

        #logger = logging.getLogger(name)
        logger = logging.getLogger(__name__)

        logger.setLevel(logging.INFO)

        if not logger.handlers:
            logger.addHandler(handler)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger

   