"""Servicio especializado 2: alquiler de equipos."""

from excepciones import ParametroInvalidoError, ReservaInvalidaError
from servicio import Servicio  # Clase abstracta padre


class AlquilerEquipo(Servicio):
    """Alquiler de equipos (portátiles, proyectores, etc.). La tarifa base es por día y por unidad."""

    MAX_DIAS = 30  # Máximo de días por alquiler
    PORCENTAJE_SEGURO = 0.10  # El seguro cuesta 10 % del subtotal

    def __init__(self, identificador, nombre, tarifa_dia, stock, disponible=True):
        super().__init__(identificador, nombre, tarifa_dia, disponible)
        self._stock = int(self._numero(stock, "stock"))  # Unidades en inventario

    def validar_parametros(self, *args):
        """Acepta (dias), (dias, cantidad) o (dias, cantidad, con_seguro). Devuelve los 3 valores."""
        self._revisar_cantidad(args, 1, 3)
        dias = self._numero(args[0], "dias", self.MAX_DIAS)
        cantidad = 1  # Por defecto, una unidad
        if len(args) >= 2:
            cantidad = self._numero(args[1], "cantidad")
            if cantidad != int(cantidad):  # No existe "media unidad" de un equipo
                raise ParametroInvalidoError(f"'cantidad' debe ser entera, llegó {cantidad}")
            if cantidad > self._stock:  # Regla de negocio: no se alquila más de lo que hay
                raise ReservaInvalidaError(
                    f"Stock insuficiente de '{self.nombre}': piden {int(cantidad)}, hay {self._stock}"
                )
        con_seguro = False
        if len(args) == 3:
            if not isinstance(args[2], bool):  # El seguro debe ser True o False
                raise ParametroInvalidoError(f"'con_seguro' debe ser True/False, llegó {args[2]!r}")
            con_seguro = args[2]
        return dias, cantidad, con_seguro

    def calcular_costo(self, *args):
        """Método sobrecargado (3 formas):
        calcular_costo(dias)                        -> 1 unidad
        calcular_costo(dias, cantidad)              -> varias unidades
        calcular_costo(dias, cantidad, con_seguro)  -> varias unidades con seguro (bool)
        """
        dias, cantidad, con_seguro = self.validar_parametros(*args)
        costo = self.tarifa_base * dias * cantidad
        if con_seguro:
            costo *= 1 + self.PORCENTAJE_SEGURO
        return round(costo, 2)

    def describir(self):
        return f"Equipo: {super().describir()}, stock {self._stock}"
