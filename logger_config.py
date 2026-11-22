"""Configuración del logging: todos los eventos y errores van a logs/sistema.log."""

import logging  # Módulo estándar de Python para registrar eventos y errores
import os  # Permite crear el directorio de logs si aún no existe


def obtener_logger(nombre="reservas", archivo="logs/sistema.log"):
    """Devuelve un logger configurado hacia archivo, sin duplicar manejadores ni ocultar errores."""
    os.makedirs(os.path.dirname(archivo), exist_ok=True)  # Crea la carpeta logs/ si no existe
    logger = logging.getLogger(nombre)  # Recupera o crea el logger identificado por nombre
    if logger.handlers:  # Evita agregar manejadores repetidos si ya está inicializado
        return logger
    logger.setLevel(logging.DEBUG)  # Captura todos los niveles desde DEBUG hasta CRITICAL
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(funcName)s | %(message)s"
    )  # Estructura cada línea con fecha/hora, nivel, función origen y mensaje
    manejador = logging.FileHandler(archivo, encoding="utf-8")  # Envía los registros al archivo en UTF-8
    manejador.setFormatter(formato)  # Asigna el formato de salida al manejador
    logger.addHandler(manejador)  # Registra el manejador en el logger
    return logger  # Devuelve la instancia lista para registrar eventos y errores