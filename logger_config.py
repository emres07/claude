"""Logging configuration for agent team."""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional


def setup_agent_logging(agent_name: str, log_dir: str = ".agent_logs") -> logging.Logger:
    """Setup logging for an agent."""
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    log_file = log_path / f"{agent_name}.log"

    # Create logger
    logger = logging.getLogger(agent_name)
    logger.setLevel(logging.DEBUG)

    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
    )
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get logger for a name."""
    return logging.getLogger(name)
