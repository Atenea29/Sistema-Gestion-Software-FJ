"""Servicio especializado 1: reserva de salas."""

from math import isfinite

from excepciones import CalculoInconsistenteError, ParametroInvalidoError, ServicioNoDisponibleError
from servicio import Servicio


class ReservaSala(Servicio):
    """Reserva de salas de reuniones. La tarifa base se cobra por hora."""

    MAX_HORAS = 12

    def __init__(self, identificador, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        capacidad_validada = self._numero(capacidad, "capacidad")
        if not float(capacidad_validada).is_integer():
            raise ParametroInvalidoError(
                f"'capacidad' debe ser un número entero de personas, llegó {capacidad!r}"
            )
        self._capacidad = int(capacidad_validada)

    @property
    def capacidad(self):
        """Cantidad máxima de personas permitida en la sala."""
        return self._capacidad

    def validar_parametros(self, *args):
        """Acepta (horas), (horas, descuento) o (horas, descuento, iva)."""
        self._revisar_cantidad(args, 1, 3)
        horas = self._numero(args[0], "horas", self.MAX_HORAS)
        descuento = self._porcentaje(args[1], "descuento") if len(args) >= 2 else 0.0
        iva = self._porcentaje(args[2], "iva") if len(args) == 3 else 0.0
        return horas, descuento, iva

    def calcular_costo(self, *args):
        """Calcula el costo con 1, 2 o 3 argumentos (horas, descuento e IVA)."""
        if not self.disponible:
            raise ServicioNoDisponibleError(f"La sala '{self.nombre}' no está disponible")

        horas, descuento, iva = self.validar_parametros(*args)
        try:
            costo = self.tarifa_base * horas * (1 - descuento) * (1 + iva)
        except (OverflowError, ArithmeticError) as exc:
            raise CalculoInconsistenteError("No fue posible calcular el costo de la sala") from exc

        if not isfinite(costo) or costo < 0:
            raise CalculoInconsistenteError("El cálculo produjo un costo no válido")
        return round(costo, 2)

    def describir(self):
        return f"Sala: {super().describir()}, capacidad {self._capacidad} personas"
