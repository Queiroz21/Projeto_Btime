import logging
import os
from datetime import datetime

def get_logger(name: str) -> logging.Logger:
    """
    Configura e retorna um logger centralizado.
    Pode ser utilizado por qualquer módulo do projeto.
    """
    #padronização de nome de arquivo e caminho,para que o arquivo não se perca
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logs")
    os.makedirs(log_dir, exist_ok=True)

    log_filename = f"log_{datetime.now().strftime('%d_%m_%Y')}.log"
    log_path = os.path.join(log_dir, log_filename)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Evita adicionar múltiplos handlers ao mesmo logger
    if not logger.handlers:
        #Comandos CONSOLE usados apenas para fins de testes no terminal
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        #console_handler = logging.StreamHandler()
        #definindo o formato base do log
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        #console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        #logger.addHandler(console_handler)

    return logger
