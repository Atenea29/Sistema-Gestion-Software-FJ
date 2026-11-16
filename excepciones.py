"""Excepciones personalizadas del sistema de reservas."""


class ErrorReservas(Exception):
    """Excepción base: todas las excepciones del sistema heredan de ella."""

    def __init__(self, mensaje, codigo="ERR_GENERAL"):
        super().__init__(mensaje)  # Guarda el mensaje en la clase Exception
        self.mensaje = mensaje  # Mensaje legible para el usuario
        self.codigo = codigo  # Código corto para identificar el tipo de error

    def __str__(self):
        # Formato uniforme para consola y log: [CODIGO] mensaje
        return f"[{self.codigo}] {self.mensaje}"


class DatosInvalidosError(ErrorReservas):
    """Se lanza cuando los datos ingresados (nombre, fecha, personas) son erróneos."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="DATOS_INVALIDOS")


class ServicioNoDisponibleError(ErrorReservas):
    """Se lanza cuando el servicio no existe, está inactivo o su proveedor no responde."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="SERVICIO_NO_DISPONIBLE")


class ReservaInvalidaError(ErrorReservas):
    """Se lanza cuando la reserva incumple una regla de negocio (fecha pasada, cupo, duplicada)."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="RESERVA_INVALIDA")


class ReservaNoEncontradaError(ErrorReservas):
    """Se lanza cuando se intenta operar sobre una reserva que no existe."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="RESERVA_NO_ENCONTRADA")
