# logging_config.py

import logging

# Configurar el logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("events.log"),
        logging.StreamHandler()
    ]
)

# Crear un logger específico para nuestro módulo
logger = logging.getLogger('my_logger')


