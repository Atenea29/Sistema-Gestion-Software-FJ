"""Configuración del logging: todos los eventos y errores van a logs/sistema.log."""

import logging  # Módulo estándar de Python para registrar eventos
import os  # Para crear la carpeta de logs si no existe


def obtener_logger(nombre="reservas", archivo="logs/sistema.log"):
    """Devuelve un logger que escribe en un archivo, sin duplicar handlers."""
    os.makedirs(os.path.dirname(archivo), exist_ok=True)  # Crea la carpeta logs/
    logger = logging.getLogger(nombre)  # Obtiene (o crea) el logger con ese nombre
    if logger.handlers:  # Si ya fue configurado, se reutiliza tal cual
        return logger
    logger.setLevel(logging.DEBUG)  # Registra desde DEBUG hasta CRITICAL
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(funcName)s | %(message)s"
    )  # Fecha | nivel | función que registra | mensaje
    manejador = logging.FileHandler(archivo, encoding="utf-8")  # Escribe al archivo
    manejador.setFormatter(formato)  # Aplica el formato definido
    logger.addHandler(manejador)  # Conecta el manejador al logger
    return logger
