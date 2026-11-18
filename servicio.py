"""Clase abstracta Servicio: base de los tres servicios especializados de Software FJ."""

from abc import abstractmethod  # Para declarar métodos abstractos

from entidad import Entidad  # Clase abstracta general
from excepciones import DatosInvalidosError, ParametroInvalidoError


class Servicio(Entidad):
    """Servicio reservable. No se puede instanciar: las subclases deben implementar
    calcular_costo(), validar_parametros() y describir()."""

    def __init__(self, identificador, nombre, tarifa_base, disponible=True):
        super().__init__(identificador)  # Valida el id
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio")
        if isinstance(tarifa_base, bool) or not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatosInvalidosError(f"Tarifa base inválida: {tarifa_base!r}")
        self._nombre = nombre.strip()  # Atributos protegidos (encapsulación)
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

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
        self._disponible = bool(valor)  # Permite activar o desactivar el servicio

    @abstractmethod
    def validar_parametros(self, *args):
        """Valida y normaliza los parámetros de la reserva. Cada servicio define los suyos."""

    @abstractmethod
    def calcular_costo(self, *args):
        """Cálculo de costo SOBRECARGADO: cada subclase acepta 1, 2 o 3 argumentos."""

    # ---- utilidades de validación compartidas por las subclases ---------
    @staticmethod
    def _revisar_cantidad(args, minimo, maximo):
        """Simula la sobrecarga: valida cuántos argumentos se recibieron."""
        if not minimo <= len(args) <= maximo:
            raise ParametroInvalidoError(
                f"Se esperaban entre {minimo} y {maximo} argumentos y llegaron {len(args)}"
            )

    @staticmethod
    def _numero(valor, nombre, maximo=None):
        """Valida que el valor sea un número mayor que cero (y menor o igual a un máximo)."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ParametroInvalidoError(f"'{nombre}' debe ser numérico, llegó {valor!r}")
        if valor <= 0:
            raise ParametroInvalidoError(f"'{nombre}' debe ser mayor que cero, llegó {valor}")
        if maximo is not None and valor > maximo:
            raise ParametroInvalidoError(f"'{nombre}' no puede superar {maximo}, llegó {valor}")
        return valor

    @staticmethod
    def _porcentaje(valor, nombre):
        """Valida un porcentaje expresado entre 0 y 1 (por ejemplo 0.10 = 10 %)."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ParametroInvalidoError(f"'{nombre}' debe ser numérico, llegó {valor!r}")
        if not 0 <= valor <= 1:
            raise ParametroInvalidoError(f"'{nombre}' debe estar entre 0 y 1, llegó {valor}")
        return valor

    def describir(self):
        """Descripción general; las subclases la amplían (método sobrescrito)."""
        estado = "disponible" if self.disponible else "fuera de servicio"
        return f"{self.nombre} (tarifa base ${self.tarifa_base:,.0f}, {estado})"
