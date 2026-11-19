"""Excepciones personalizadas del sistema de Software FJ."""


class ErrorReservas(Exception):
    """Excepción base: todas las excepciones del sistema heredan de ella."""

    def __init__(self, mensaje, codigo="ERR_GENERAL"):
        super().__init__(mensaje)  # Guarda el mensaje en la clase Exception
        self.mensaje = mensaje  # Mensaje legible para el usuario
        self.codigo = codigo  # Código corto para identificar el tipo de error
        self.registrado = False  # Indica si ya se escribió en el log (evita duplicados)

    def __str__(self):
        # Formato uniforme para consola y log: [CODIGO] mensaje
        return f"[{self.codigo}] {self.mensaje}"


class DatosInvalidosError(ErrorReservas):
    """Datos erróneos de un cliente o de una fecha (nombre, correo, teléfono, etc.)."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="DATOS_INVALIDOS")


class ParametroInvalidoError(ErrorReservas):
    """Parámetros incorrectos al calcular un costo (tipo, rango o cantidad de argumentos)."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="PARAMETRO_INVALIDO")


class ServicioNoDisponibleError(ErrorReservas):
    """El servicio no existe, está inactivo o su proveedor no responde."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="SERVICIO_NO_DISPONIBLE")


class ReservaInvalidaError(ErrorReservas):
    """La reserva incumple una regla de negocio (fecha pasada, stock, duplicada)."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="RESERVA_INVALIDA")


class ReservaNoEncontradaError(ErrorReservas):
    """Se intenta operar sobre una reserva que no existe."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="RESERVA_NO_ENCONTRADA")


class OperacionNoPermitidaError(ErrorReservas):
    """Se intenta una operación que el estado actual no permite (ej. confirmar una reserva cancelada)."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="OPERACION_NO_PERMITIDA")


class CalculoInconsistenteError(ErrorReservas):
    """El cálculo de un costo produjo un resultado imposible (infinito, NaN, cero o negativo)."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="CALCULO_INCONSISTENTE")


class ClienteNoEncontradoError(ErrorReservas):
    """Se intenta operar con un cliente que no está registrado."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="CLIENTE_NO_ENCONTRADO")
class ClienteInvalidoError(DatosInvalidosError):
    """Datos personales inválidos de un cliente (nombre, documento, correo o teléfono).

    Hereda de DatosInvalidosError: cualquier 'except DatosInvalidosError' también la captura,
    pero su código propio (CLIENTE_INVALIDO) permite distinguirla en el log."""

    def __init__(self, mensaje):
        super().__init__(mensaje)  # Reutiliza la inicialización de DatosInvalidosError
        self.codigo = "CLIENTE_INVALIDO"  # Código propio para identificarla en el log
