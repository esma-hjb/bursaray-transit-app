"""Uygulama genelinde kullanilan basit logger kurulumu."""

from __future__ import annotations

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """Verilen isimle yapilandirilmis bir logger dondurur.

    Ilk cagrida handler yoksa stderr'e yazan bir handler ekler.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%H:%M:%S"
            )
        )
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
