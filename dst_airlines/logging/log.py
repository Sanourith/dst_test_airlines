import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logger(
    name: str = "root",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    use_colors: bool = True,
) -> logging.Logger:
    """
    Configure un logger avec un format élégant et aéré.

    Args:
        name: Nom du logger (par défaut 'root')
        level: Niveau de log (par défaut INFO)
        log_file: Chemin vers le fichier de log (optionnel)
        max_bytes: Taille max des fichiers de log avant rotation
        backup_count: Nombre de fichiers de log à conserver
        use_colors: Activer les couleurs dans la console (si colorlog disponible)

    Returns:
        Le logger configuré
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Éviter les handlers multiples
    if logger.handlers:
        return logger

    # Formatter de base (pour fichier et console si colorlog non disponible)
    base_formatter = logging.Formatter(
        "\n%(asctime)s ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "▶ %(name)s.%(levelname)s\n"
        "▷ %(message)s\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler console avec gestion des couleurs
    console_handler = logging.StreamHandler(sys.stdout)

    if use_colors:
        try:
            from colorlog import ColoredFormatter

            color_formatter = ColoredFormatter(
                "%(log_color)s%(asctime)s ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "▶ %(name)s.%(levelname)s\n"
                "▷ %(message)s\n"
                "%(log_color)s━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━%(reset)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                reset=True,
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
            )
            console_handler.setFormatter(color_formatter)
        except ImportError:
            console_handler.setFormatter(base_formatter)
            logger.debug("colorlog non installé, utilisation du formatage standard")
    else:
        console_handler.setFormatter(base_formatter)

    logger.addHandler(console_handler)

    # Handler fichier (toujours sans couleurs)
    if log_file:
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setFormatter(base_formatter)
        logger.addHandler(file_handler)

    return logger
