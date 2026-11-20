"""Clase abstracta Servicio: base de los tres servicios especializados de Software FJ."""

from abc import abstractmethod
from math import isfinite

from entidad import Entidad
from excepciones import DatosInvalidosError, ParametroInvalidoError


class Servicio(Entidad):
    """Servicio reservable. Las subclases implementan sus reglas y cálculos."""

    def __init__(self, identificador, nombre, tarifa_base, disponible=True):
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio")

        tarifa = self._validar_numero_positivo(tarifa_base, "tarifa_base")
        if not isinstance(disponible, bool):
            raise DatosInvalidosError("'disponible' debe ser True o False")

        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa)
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise DatosInvalidosError("'disponible' debe ser True o False")
        self._disponible = valor

    @abstractmethod
    def validar_parametros(self, *args):
        """Valida y normaliza los parámetros específicos de cada servicio."""

    @abstractmethod
    def calcular_costo(self, *args):
        """Calcula el costo según los parámetros admitidos por cada subclase."""

    @staticmethod
    def _revisar_cantidad(args, minimo, maximo):
        """Comprueba la cantidad de argumentos de las variantes de cálculo."""
        if not minimo <= len(args) <= maximo:
            raise ParametroInvalidoError(
                f"Se esperaban entre {minimo} y {maximo} argumentos y llegaron {len(args)}"
            )

    @staticmethod
    def _validar_numero_positivo(valor, nombre, maximo=None):
        """Valida un número real, finito y positivo, con máximo opcional."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ParametroInvalidoError(f"'{nombre}' debe ser numérico, llegó {valor!r}")
        if not isfinite(valor):
            raise ParametroInvalidoError(f"'{nombre}' debe ser un número finito, llegó {valor!r}")
        if valor <= 0:
            raise ParametroInvalidoError(f"'{nombre}' debe ser mayor que cero, llegó {valor}")
        if maximo is not None and valor > maximo:
            raise ParametroInvalidoError(f"'{nombre}' no puede superar {maximo}, llegó {valor}")
        return valor

    @staticmethod
    def _numero(valor, nombre, maximo=None):
        """Alias compatible con los servicios especializados existentes."""
        return Servicio._validar_numero_positivo(valor, nombre, maximo)

    @staticmethod
    def _porcentaje(valor, nombre):
        """Valida porcentajes entre 0 y 1, incluidos ambos extremos."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ParametroInvalidoError(f"'{nombre}' debe ser numérico, llegó {valor!r}")
        if not isfinite(valor):
            raise ParametroInvalidoError(f"'{nombre}' debe ser un número finito, llegó {valor!r}")
        if not 0 <= valor <= 1:
            raise ParametroInvalidoError(f"'{nombre}' debe estar entre 0 y 1, llegó {valor}")
        return float(valor)

    def describir(self):
        estado = "disponible" if self.disponible else "fuera de servicio"
        return f"{self.nombre} (tarifa base ${self.tarifa_base:,.2f}, {estado})"
