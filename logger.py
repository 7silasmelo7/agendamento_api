from logging.config import dictConfig
import logging
import os

# Caminho seguro para logs (fora do OneDrive)
LOG_DIR = "C:/temp/agendamento_logs/"

# Cria o diretório se não existir
os.makedirs(LOG_DIR, exist_ok=True)

dictConfig({
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)-4s %(funcName)s() L%(lineno)-4d %(message)s",
        },
        "detailed": {
            "format": "[%(asctime)s] %(levelname)-4s %(funcName)s() L%(lineno)-4d %(message)s - file=%(pathname)s",
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },

        # Arquivo de erros (sem rotação para evitar WinError 32)
        "error_file": {
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "filename": os.path.join(LOG_DIR, "error.log"),
            "encoding": "utf-8"
        },

        # Arquivo detalhado (sem rotação)
        "detailed_file": {
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "filename": os.path.join(LOG_DIR, "detailed.log"),
            "encoding": "utf-8"
        }
    },

    "loggers": {
        "gunicorn.error": {
            "handlers": ["console", "error_file"],
            "level": "INFO",
            "propagate": False,
        }
    },

    "root": {
        "handlers": ["console", "detailed_file"],
        "level": "INFO",
    }
})

logger = logging.getLogger(__name__)
