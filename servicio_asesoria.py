"""Servicio especializado 3: asesorías especializadas."""

from excepciones import ParametroInvalidoError
from servicio import Servicio  # Clase abstracta padre


class AsesoriaEspecializada(Servicio):
    """Asesoría técnica por horas. El nivel del asesor multiplica la tarifa."""

    MAX_HORAS = 8  # Máximo de horas por asesoría
    NIVELES = {"basico": 1.0, "avanzado": 1.5, "experto": 2.0}  # Multiplicador por nivel
    RECARGO_URGENTE = 0.25  # Una asesoría urgente cuesta 25 % más

    def validar_parametros(self, *args):
        """Acepta (horas), (horas, nivel) o (horas, nivel, urgente). Devuelve los 3 valores."""
        self._revisar_cantidad(args, 1, 3)
        horas = self._numero(args[0], "horas", self.MAX_HORAS)
        nivel = "basico"  # Por defecto, nivel básico
        if len(args) >= 2:
            if args[1] not in self.NIVELES:  # Nivel desconocido
                raise ParametroInvalidoError(
                    f"Nivel {args[1]!r} no existe; use {', '.join(self.NIVELES)}"
                )
            nivel = args[1]
        urgente = False
        if len(args) == 3:
            if not isinstance(args[2], bool):
                raise ParametroInvalidoError(f"'urgente' debe ser True/False, llegó {args[2]!r}")
            urgente = args[2]
        return horas, nivel, urgente

    def calcular_costo(self, *args):
        """Método sobrecargado (3 formas):
        calcular_costo(horas)                    -> nivel básico
        calcular_costo(horas, nivel)             -> nivel: 'basico', 'avanzado' o 'experto'
        calcular_costo(horas, nivel, urgente)    -> con recargo si urgente es True
        """
        horas, nivel, urgente = self.validar_parametros(*args)
        costo = self.tarifa_base * horas * self.NIVELES[nivel]
        if urgente:
            costo *= 1 + self.RECARGO_URGENTE
        return round(costo, 2)

    def describir(self):
        return f"Asesoría: {super().describir()}"
