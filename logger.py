import logging
import logging.handlers
import os
from pathlib import Path

def setup_logger():
    """Configure logging to file with rotation."""
    log_dir = Path(os.getenv('APPDATA')) / 'OctaveLights' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / 'app.log'

    logger = logging.getLogger('octavelights')
    logger.setLevel(logging.DEBUG)

    handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

logger = setup_logger()
