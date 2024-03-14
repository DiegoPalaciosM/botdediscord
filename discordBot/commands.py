import ctypes
import logging
import threading


class CustomFormatter(logging.Formatter):
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


fmt = '%(asctime)s | %(levelname)s | %(message)s'
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(CustomFormatter(fmt))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(stdout_handler)


logger.info('Iniciando Logger')

def singleton(cls):
    """
    Un decorador que garantiza que sólo se crea una instancia de una clase.

    Este decorador utiliza un diccionario para almacenar instancias de la clase, cuya clave es el tipo de clase.
    Si aún no existe una instancia de la clase, se crea utilizando los argumentos proporcionados.
    Las siguientes llamadas a la función decorada devolverán la instancia existente.

    Args:
        cls (tipo): La clase a decorar.

    Devuelve
        tipo: La clase decorada.

    """

    instances = {}

    def wrap(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrap
