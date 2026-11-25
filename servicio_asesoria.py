"""Servicio especializado para asesorías técnicas de Software FJ."""

from math import isfinite  # Permite detectar horas no finitas como NaN o infinito.

from excepciones import DatosInvalidosError, ParametroInvalidoError
from servicio import Servicio  # Clase abstracta de la que hereda este servicio.


class AsesoriaEspecializada(Servicio):
    """Ofrece asesorías por horas, con tarifa según el nivel y recargo de urgencia."""

    MAX_HORAS = 8  # Duración máxima de una asesoría.
    NIVELES = {"basico": 1.0, "avanzado": 1.5, "experto": 2.0}
    RECARGO_URGENTE = 0.25  # Una asesoría urgente cuesta 25 % más.

    def __init__(self, identificador, nombre, tarifa_hora, disponible=True):
        # La tarifa debe ser numérica, positiva y finita antes de llamar al padre.
        self._validar_numero_finito(tarifa_hora, "tarifa_hora", DatosInvalidosError)
        super().__init__(identificador, nombre, tarifa_hora, disponible)

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

    def validar_parametros(self, *args):
        """Valida las formas (horas), (horas, nivel) y (horas, nivel, urgente)."""
        self._revisar_cantidad(args, 1, 3)

        # La cantidad de horas debe ser positiva, finita y no superar el máximo.
        self._validar_numero_finito(args[0], "horas", ParametroInvalidoError)
        horas = self._numero(args[0], "horas", self.MAX_HORAS)

        nivel = "basico"  # El nivel básico se usa si el usuario no especifica otro.
        if len(args) >= 2:
            if not isinstance(args[1], str):
                raise ParametroInvalidoError(
                    f"'nivel' debe ser texto; llegó {type(args[1]).__name__}"
                )
            nivel_recibido = args[1].strip().lower()
            if nivel_recibido not in self.NIVELES:
                raise ParametroInvalidoError(
                    f"Nivel {args[1]!r} no existe; use {', '.join(self.NIVELES)}"
                )
            nivel = nivel_recibido

        urgente = False  # Por defecto, la asesoría no tiene recargo de urgencia.
        if len(args) == 3:
            if not isinstance(args[2], bool):
                raise ParametroInvalidoError(
                    f"'urgente' debe ser True o False, llegó {args[2]!r}"
                )
            urgente = args[2]

        return horas, nivel, urgente

    def calcular_costo(self, *args):
        """Calcula el costo en sus tres variantes de argumentos:

        calcular_costo(horas)                 -> nivel básico sin urgencia.
        calcular_costo(horas, nivel)          -> nivel indicado sin urgencia.
        calcular_costo(horas, nivel, urgente) -> nivel indicado y posible recargo.
        """
        horas, nivel, urgente = self.validar_parametros(*args)
        subtotal = self.tarifa_base * horas * self.NIVELES[nivel]
        if urgente:
            subtotal *= 1 + self.RECARGO_URGENTE
        return round(subtotal, 2)

    def describir(self):
        """Devuelve una descripción del servicio de asesoría."""
        return f"Asesoria: {super().describir()}"
