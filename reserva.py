"""Clase Reserva: integra cliente, servicio, duración y estado."""

from datetime import date  # Tipo de la fecha de la reserva

from cliente import Cliente
from excepciones import DatosInvalidosError, ErrorReservas, ReservaInvalidaError
from logger_config import obtener_logger
from servicio import Servicio

log = obtener_logger()  # Logger compartido


class Reserva:
    """Reserva de un servicio. Estados: PENDIENTE -> CONFIRMADA -> CANCELADA (o FALLIDA)."""

    def __init__(self, identificador, cliente, servicio, fecha, duracion, *opciones):
        # Validaciones de tipo: la reserva solo integra objetos del dominio
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("La reserva requiere un objeto Cliente")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("La reserva requiere un objeto Servicio")
        if not isinstance(fecha, date):
            raise DatosInvalidosError("La fecha de la reserva debe ser de tipo date")
        self._id = identificador  # Atributos privados (encapsulación)
        self._cliente = cliente
        self._servicio = servicio
        self._fecha = fecha
        self._duracion = duracion  # Horas o días, según el servicio
        self._opciones = opciones  # Parámetros opcionales (descuento, IVA, seguro, nivel...)
        self._estado = "PENDIENTE"  # Estado inicial
        self._costo = None  # Se calcula al confirmar

    # ---- propiedades de solo lectura ------------------------------------
    @property
    def id(self):
        return self._id

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def fecha(self):
        return self._fecha

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    # ---- operaciones ------------------------------------------------------
    def confirmar(self):
        """Confirma la reserva: valida el estado y calcula el costo (polimorfismo del servicio)."""
        try:
            if self._estado != "PENDIENTE":  # Solo se confirman reservas pendientes
                raise ReservaInvalidaError(f"La reserva #{self._id} está {self._estado}, no se puede confirmar")
            costo = self._servicio.calcular_costo(self._duracion, *self._opciones)
        except ErrorReservas as error:
            log.error("Confirmación fallida de reserva #%s: %s", self._id, error,
                      exc_info=bool(error.__cause__))
            error.registrado = True
            raise
        else:  # Solo si no hubo excepciones
            self._costo = costo
            self._estado = "CONFIRMADA"
            log.info("Reserva #%s confirmada: %s en '%s' el %s, costo $%s", self._id,
                     self._cliente.nombre, self._servicio.nombre, self._fecha, f"{costo:,.2f}")
        finally:
            log.debug("Confirmación de reserva #%s finalizada", self._id)  # Siempre se ejecuta

    def cancelar(self):
        """Cancela una reserva confirmada o pendiente."""
        try:
            if self._estado == "CANCELADA":
                raise ReservaInvalidaError(f"La reserva #{self._id} ya estaba cancelada")
        except ReservaInvalidaError as error:
            log.error("Cancelación rechazada: %s", error)
            error.registrado = True
            raise
        else:
            self._estado = "CANCELADA"
            log.info("Reserva #%s cancelada", self._id)
        finally:
            log.debug("Cancelación de reserva #%s finalizada", self._id)

    def procesar(self):
        """Procesa la reserva completa: confirma y, si falla, la marca como FALLIDA
        y encadena el error original con 'raise ... from'."""
        try:
            self.confirmar()
        except ErrorReservas as error:
            self._estado = "FALLIDA"
            nuevo = ReservaInvalidaError(f"No se pudo procesar la reserva #{self._id}: {error.mensaje}")
            log.error("Procesamiento fallido de reserva #%s", self._id)
            nuevo.registrado = True
            raise nuevo from error  # Conserva la causa original (__cause__)
        return self

    def describir(self):
        costo = f"${self._costo:,.0f}" if self._costo is not None else "sin calcular"
        return (f"Reserva #{self._id} [{self._estado}] {self._cliente.nombre} - "
                f"{self._servicio.nombre} - {self._fecha} - duración {self._duracion} - {costo}")

    def __str__(self):
        return self.describir()
