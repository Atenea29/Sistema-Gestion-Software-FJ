"""Gestión de clientes, servicios y reservas con listas internas (sin base de datos)."""

from datetime import date, datetime  # Manejo y parseo de fechas para validar reservas

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

log = obtener_logger()  # Logger compartido para registrar eventos y errores del módulo


class SistemaReservas:
    """Sistema integral de Software FJ; valida condiciones y lanza errores ante fallos."""

    def __init__(self):
        """Inicializa listas internas, contadores y registro de proveedores caídos."""
        self.clientes = []  # Lista de objetos Cliente registrados
        self.servicios = []  # Lista de objetos Servicio (incluye subclases)
        self.reservas = []  # Lista de objetos Reserva creadas
        self._siguiente_id = 1  # Correlativo autoincremental para nuevas reservas
        self.intentos = 0  # Contador de intentos de reserva realizados
        self.proveedores_caidos = set()  # IDs de servicios cuyo proveedor externo está caído
        log.info("Sistema iniciado")

    # ---- registro -------------------------------------------------------
    def registrar_cliente(self, cliente):
        """Registra un cliente verificando tipo y unicidad del ID."""
        if not isinstance(cliente, Cliente):
            # Condición: solo se aceptan instancias de Cliente
            raise DatosInvalidosError("Solo se pueden registrar objetos Cliente")
        if any(c.id == cliente.id for c in self.clientes):
            # Condición: no permitir dos clientes con el mismo ID
            raise DatosInvalidosError(f"Ya existe un cliente con id {cliente.id}")
        self.clientes.append(cliente)  # Agrega el cliente válido a la lista interna
        log.info("Cliente registrado: %s", cliente)
        return cliente

    def registrar_servicio(self, servicio):
        """Registra un servicio verificando tipo y unicidad del ID."""
        if not isinstance(servicio, Servicio):
            # Condición: solo se aceptan instancias de Servicio o sus subclases
            raise DatosInvalidosError("Solo se pueden registrar objetos Servicio")
        if any(s.id == servicio.id for s in self.servicios):
            # Condición: no permitir dos servicios con el mismo ID
            raise DatosInvalidosError(f"Ya existe un servicio con id {servicio.id}")
        self.servicios.append(servicio)  # Agrega el servicio válido a la lista interna
        log.info("Servicio registrado: %s", servicio)
        return servicio

    # ---- auxiliares -----------------------------------------------------
    def _obtener_cliente(self, cliente_id):
        """Busca un cliente por ID o lanza ClienteNoEncontradoError."""
        try:
            return next(c for c in self.clientes if c.id == cliente_id)  # Busca coincidencia por ID
        except StopIteration as error:
            # Condición: el cliente debe existir previamente en self.clientes
            raise ClienteNoEncontradoError(f"El cliente {cliente_id} no está registrado") from error

    def _obtener_servicio(self, servicio_id):
        """Busca un servicio por ID o lanza ServicioNoDisponibleError."""
        try:
            return next(s for s in self.servicios if s.id == servicio_id)  # Busca coincidencia por ID
        except StopIteration as error:
            # Condición: el servicio debe existir previamente en self.servicios
            raise ServicioNoDisponibleError(f"El servicio {servicio_id} no existe") from error

    @staticmethod
    def _convertir_fecha(fecha_texto):
        """Convierte fecha_texto (AAAA-MM-DD) a date o lanza DatosInvalidosError."""
        try:
            return datetime.strptime(fecha_texto, "%Y-%m-%d").date()  # Valida formato AAAA-MM-DD
        except (ValueError, TypeError) as error:
            # Condición: la fecha debe tener formato válido y tipo compatible
            raise DatosInvalidosError(f"Fecha inválida: {fecha_texto!r} (use AAAA-MM-DD)") from error

    def _llamar_proveedor(self, servicio):
        """Simula consulta a proveedor externo; lanza ConnectionError si está caído."""
        if servicio.id in self.proveedores_caidos:
            # Condición: el proveedor del servicio no debe estar marcado como caído
            raise ConnectionError(f"Sin respuesta del proveedor de '{servicio.nombre}'")

    # ---- operaciones ----------------------------------------------------
    def crear_reserva(self, cliente_id, servicio_id, fecha_texto, duracion, *opciones):
        """Valida todas las condiciones de reserva, procesa el costo y propaga errores."""
        self.intentos += 1  # Registra el intento sin importar si la reserva procede o falla
        try:
            cliente = self._obtener_cliente(cliente_id)  # 1) Condición: cliente registrado
            servicio = self._obtener_servicio(servicio_id)  # 2) Condición: servicio existente
            fecha = self._convertir_fecha(fecha_texto)  # 3) Condición: fecha con formato válido

            if not servicio.disponible:
                # 4) Condición: el servicio debe estar disponible operativamente
                raise ServicioNoDisponibleError(f"'{servicio.nombre}' está fuera de servicio")

            try:
                self._llamar_proveedor(servicio)  # 5) Condición: proveedor externo responde
            except ConnectionError as error:
                # Convierte el fallo de conexión en error de dominio encadenando la causa
                raise ServicioNoDisponibleError(
                    f"Proveedor de '{servicio.nombre}' no disponible"
                ) from error

            if fecha < date.today():
                # 6) Condición: no se permiten fechas anteriores a la fecha actual
                raise ReservaInvalidaError(f"La fecha {fecha} ya pasó")

            if any(
                r.cliente.id == cliente.id
                and r.servicio.id == servicio.id
                and r.fecha == fecha
                and r.estado == "CONFIRMADA"
                for r in self.reservas
            ):
                # 7) Condición: evitar reservas CONFIRMADA duplicadas para mismo cliente, servicio y día
                raise ReservaInvalidaError(
                    f"{cliente.nombre} ya tiene una reserva ese día en '{servicio.nombre}'"
                )

            reserva = Reserva(self._siguiente_id, cliente, servicio, fecha, duracion, *opciones)
            reserva.procesar()  # 8) Condición: valida parámetros y calcula costo de la reserva
        except ErrorReservas as error:
            if not error.registrado:
                # Registra el error una sola vez en el log antes de dejar que aparezca arriba
                log.error("Reserva rechazada: %s", error, exc_info=bool(error.__cause__))
                error.registrado = True
            raise  # Propaga la excepción para que el error sea visible y manejado afuera
        else:
            # Solo se guarda y avanza el ID si todas las condiciones y el procesamiento pasaron
            self.reservas.append(reserva)
            self._siguiente_id += 1
            return reserva
        finally:
            # Deja trazabilidad en debug del cierre de cada intento de reserva
            log.debug("Intento de reserva #%d finalizado", self.intentos)

    def cancelar_reserva(self, reserva_id):
        """Busca una reserva por ID, la cancela o lanza ReservaNoEncontradaError."""
        try:
            reserva = next(r for r in self.reservas if r.id == reserva_id)  # Busca la reserva por ID
        except StopIteration as error:
            # Condición: la reserva debe existir en self.reservas para poder cancelarse
            nuevo = ReservaNoEncontradaError(f"La reserva #{reserva_id} no existe")
            log.error("Cancelación fallida: %s", nuevo)
            nuevo.registrado = True
            raise nuevo from error  # Propaga el error encadenado para que aparezca
        reserva.cancelar()  # Cambia el estado de la reserva a cancelada
        return reserva