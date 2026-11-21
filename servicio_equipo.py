"""Servicio especializado para el alquiler de equipos de Software FJ."""

from math import isfinite  # Permite rechazar NaN e infinito en datos numéricos.

from excepciones import DatosInvalidosError, ParametroInvalidoError, ReservaInvalidaError
from servicio import Servicio  # Clase abstracta de la que hereda este servicio.


class AlquilerEquipo(Servicio):
    """Alquila equipos por días y unidades, con opción de agregar un seguro."""

    MAX_DIAS = 30  # Límite de días que puede durar un alquiler.
    PORCENTAJE_SEGURO = 0.10  # El seguro equivale al 10 % del subtotal.

    def __init__(self, identificador, nombre, tarifa_dia, stock, disponible=True):
        # La tarifa debe ser numérica, positiva y finita antes de llamar al padre.
        self._validar_numero_finito(tarifa_dia, "tarifa_dia", DatosInvalidosError)
        super().__init__(identificador, nombre, tarifa_dia, disponible)

        # El inventario representa unidades completas; no se truncan valores decimales.
        self._validar_numero_finito(stock, "stock", ParametroInvalidoError)
        if stock <= 0 or int(stock) != stock:
            raise ParametroInvalidoError(
                f"'stock' debe ser un entero mayor que cero, llegó {stock!r}"
            )
        self._stock = int(stock)

    @staticmethod
    def _validar_numero_finito(valor, nombre, tipo_error):
        """Comprueba tipo numérico y finitud para evitar NaN, infinito y booleanos."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise tipo_error(f"'{nombre}' debe ser numérico, llegó {valor!r}")
        try:
            finito = isfinite(valor)
        except OverflowError:
            finito = False
        if not finito:
            raise tipo_error(f"'{nombre}' debe ser un número finito, llegó {valor!r}")

    @property
    def stock(self):
        """Cantidad de unidades disponibles registrada para el equipo."""
        return self._stock

    def validar_parametros(self, *args):
        """Valida las formas (días), (días, cantidad) y (días, cantidad, con_seguro)."""
        self._revisar_cantidad(args, 1, 3)

        # La duración debe ser positiva, finita y no superar el máximo permitido.
        self._validar_numero_finito(args[0], "dias", ParametroInvalidoError)
        dias = self._numero(args[0], "dias", self.MAX_DIAS)

        cantidad = 1  # Cuando no se indica cantidad, se alquila una unidad.
        if len(args) >= 2:
            self._validar_numero_finito(args[1], "cantidad", ParametroInvalidoError)
            cantidad = self._numero(args[1], "cantidad")
            if int(cantidad) != cantidad:
                raise ParametroInvalidoError(
                    f"'cantidad' debe ser un número entero, llegó {cantidad!r}"
                )
            if cantidad > self.stock:
                raise ReservaInvalidaError(
                    f"Stock insuficiente de '{self.nombre}': piden {int(cantidad)}, hay {self.stock}"
                )

        con_seguro = False  # El seguro es opcional y por defecto no se agrega.
        if len(args) == 3:
            if not isinstance(args[2], bool):
                raise ParametroInvalidoError(
                    f"'con_seguro' debe ser True o False, llegó {args[2]!r}"
                )
            con_seguro = args[2]

        return dias, int(cantidad), con_seguro

    def calcular_costo(self, *args):
        """Calcula el costo en sus tres variantes de argumentos:

        calcular_costo(dias)                        -> una unidad sin seguro.
        calcular_costo(dias, cantidad)              -> varias unidades sin seguro.
        calcular_costo(dias, cantidad, con_seguro)  -> varias unidades con/sin seguro.
        """
        dias, cantidad, con_seguro = self.validar_parametros(*args)
        subtotal = self.tarifa_base * dias * cantidad
        if con_seguro:
            subtotal *= 1 + self.PORCENTAJE_SEGURO
        return round(subtotal, 2)

    def describir(self):
        """Devuelve la descripción polimórfica del servicio y su inventario."""
        return f"Equipo: {super().describir()}, stock {self.stock} unidades"
