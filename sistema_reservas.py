"""Gestión de clientes, servicios y reservas con listas internas (sin base de datos)."""

from datetime import date, datetime  # Manejo de fechas

from cliente import Cliente
from excepciones import (
    ClienteNoEncontradoError,
    DatosInvalidosError,
    ErrorReservas,
    ReservaInvalidaError,
    ReservaNoEncontradaError,
    ServicioNoDisponibleError,
)
from logger_config import obtener_logger
from reserva import Reserva
from servicio import Servicio

log = obtener_logger()  # Logger compartido por todo el módulo


class SistemaReservas:
    """Sistema integral de Software FJ. Ningún error detiene la aplicación."""

    def __init__(self):
        self.clientes = []  # Lista de objetos Cliente
        self.servicios = []  # Lista de objetos Servicio (cualquier subclase)
        self.reservas = []  # Lista de objetos Reserva
        self._siguiente_id = 1  # Contador de ids de reserva
        self.intentos = 0  # Intentos de reserva realizados
        self.proveedores_caidos = set()  # Ids de servicios cuyo proveedor no responde
        log.info("Sistema iniciado")

    # ---- registro -------------------------------------------------------
    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Solo se pueden registrar objetos Cliente")
        if any(c.id == cliente.id for c in self.clientes):  # Id repetido
            raise DatosInvalidosError(f"Ya existe un cliente con id {cliente.id}")
        self.clientes.append(cliente)
        log.info("Cliente registrado: %s", cliente)
        return cliente

    def registrar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Solo se pueden registrar objetos Servicio")
        if any(s.id == servicio.id for s in self.servicios):
            raise DatosInvalidosError(f"Ya existe un servicio con id {servicio.id}")
        self.servicios.append(servicio)
        log.info("Servicio registrado: %s", servicio)
        return servicio

    # ---- auxiliares -----------------------------------------------------
    def _obtener_cliente(self, cliente_id):
        try:
            return next(c for c in self.clientes if c.id == cliente_id)  # Busca en la lista
        except StopIteration as error:
            raise ClienteNoEncontradoError(f"El cliente {cliente_id} no está registrado") from error

    def _obtener_servicio(self, servicio_id):
        try:
            return next(s for s in self.servicios if s.id == servicio_id)
        except StopIteration as error:
            raise ServicioNoDisponibleError(f"El servicio {servicio_id} no existe") from error

    @staticmethod
    def _convertir_fecha(fecha_texto):
        try:
            return datetime.strptime(fecha_texto, "%Y-%m-%d").date()  # Formato AAAA-MM-DD
        except (ValueError, TypeError) as error:
            raise DatosInvalidosError(f"Fecha inválida: {fecha_texto!r} (use AAAA-MM-DD)") from error

    def _llamar_proveedor(self, servicio):
        """Simula la consulta a un proveedor externo que puede estar caído."""
        if servicio.id in self.proveedores_caidos:
            raise ConnectionError(f"Sin respuesta del proveedor de '{servicio.nombre}'")

    # ---- operaciones ----------------------------------------------------
    def crear_reserva(self, cliente_id, servicio_id, fecha_texto, duracion, *opciones):
        """Crea y procesa una reserva. 'duracion' y 'opciones' se pasan al cálculo de costo."""
        self.intentos += 1  # Cuenta el intento aunque falle
        try:
            cliente = self._obtener_cliente(cliente_id)  # 1) Cliente registrado
            servicio = self._obtener_servicio(servicio_id)  # 2) Servicio existente
            fecha = self._convertir_fecha(fecha_texto)  # 3) Fecha válida
            if not servicio.disponible:  # 4) Servicio activo
                raise ServicioNoDisponibleError(f"'{servicio.nombre}' está fuera de servicio")
            try:
                self._llamar_proveedor(servicio)  # 5) Proveedor externo
            except ConnectionError as error:
                raise ServicioNoDisponibleError(
                    f"Proveedor de '{servicio.nombre}' no disponible"
                ) from error
            if fecha < date.today():  # 6) No se permiten fechas pasadas
                raise ReservaInvalidaError(f"La fecha {fecha} ya pasó")
            if any(r.cliente.id == cliente.id and r.servicio.id == servicio.id
                   and r.fecha == fecha and r.estado == "CONFIRMADA" for r in self.reservas):
                raise ReservaInvalidaError(  # 7) Evita duplicados
                    f"{cliente.nombre} ya tiene una reserva ese día en '{servicio.nombre}'")
            reserva = Reserva(self._siguiente_id, cliente, servicio, fecha, duracion, *opciones)
            reserva.procesar()  # 8) Confirma: valida parámetros y calcula costo
        except ErrorReservas as error:
            if not error.registrado:  # Evita duplicar entradas del log
                log.error("Reserva rechazada: %s", error, exc_info=bool(error.__cause__))
                error.registrado = True
            raise
        else:
            self.reservas.append(reserva)  # Solo las reservas exitosas entran a la lista
            self._siguiente_id += 1
            return reserva
        finally:
            log.debug("Intento de reserva #%d finalizado", self.intentos)

    def cancelar_reserva(self, reserva_id):
        """Busca la reserva en la lista y la cancela."""
        try:
            reserva = next(r for r in self.reservas if r.id == reserva_id)
        except StopIteration as error:
            nuevo = ReservaNoEncontradaError(f"La reserva #{reserva_id} no existe")
            log.error("Cancelación fallida: %s", nuevo)
            nuevo.registrado = True
            raise nuevo from error  # Encadena el StopIteration original
        reserva.cancelar()
        return reserva
