"""Servicio especializado 1: reserva de salas."""

from servicio import Servicio  # Clase abstracta padre


class ReservaSala(Servicio):
    """Reserva de salas de reuniones. La tarifa base es por hora."""

    MAX_HORAS = 12  # Máximo de horas por reserva

    def __init__(self, identificador, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        self._capacidad = int(self._numero(capacidad, "capacidad"))  # Personas que caben

    def validar_parametros(self, *args):
        """Acepta (horas), (horas, descuento) o (horas, descuento, iva). Devuelve los 3 valores."""
        self._revisar_cantidad(args, 1, 3)  # Solo se aceptan 1, 2 o 3 argumentos
        horas = self._numero(args[0], "horas", self.MAX_HORAS)
        descuento = self._porcentaje(args[1], "descuento") if len(args) >= 2 else 0.0
        iva = self._porcentaje(args[2], "iva") if len(args) == 3 else 0.0
        return horas, descuento, iva

    def calcular_costo(self, *args):
        """Método sobrecargado (3 formas):
        calcular_costo(horas)                     -> costo simple
        calcular_costo(horas, descuento)          -> con descuento (0 a 1)
        calcular_costo(horas, descuento, iva)     -> con descuento e IVA (0 a 1)
        """
        horas, descuento, iva = self.validar_parametros(*args)
        return round(self.tarifa_base * horas * (1 - descuento) * (1 + iva), 2)

    def describir(self):
        return f"Sala: {super().describir()}, capacidad {self._capacidad} personas"
