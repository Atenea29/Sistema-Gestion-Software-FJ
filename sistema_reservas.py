"""Lógica del sistema de reservas con manejo robusto de excepciones."""

from dataclasses import dataclass  # Para definir clases de datos de forma corta
from datetime import date, datetime  # Manejo de fechas

from excepciones import (  # Excepciones personalizadas del proyecto
    DatosInvalidosError,
    ErrorReservas,
    ReservaInvalidaError,
    ReservaNoEncontradaError,
    ServicioNoDisponibleError,
)
from logger_config import obtener_logger  # Logger que escribe en archivo

log = obtener_logger()  # Logger compartido por todo el módulo


@dataclass
class Servicio:
    """Servicio que se puede reservar (restaurante, spa, tour, etc.)."""

    id: int  # Identificador único
    nombre: str  # Nombre del servicio
    capacidad: int  # Máximo de personas por reserva
    disponible: bool = True  # False si el servicio está fuera de operación


@dataclass
class Reserva:
    """Reserva realizada por un cliente."""

    id: int  # Identificador único de la reserva
    cliente: str  # Nombre del cliente
    servicio_id: int  # Servicio reservado
    fecha: date  # Fecha de la reserva
    personas: int  # Cantidad de personas
    estado: str = "CONFIRMADA"  # CONFIRMADA o CANCELADA


class SistemaReservas:
    """Gestiona servicios y reservas sin detenerse ante errores."""

    def __init__(self, servicios):
        self.servicios = {s.id: s for s in servicios}  # Diccionario id -> Servicio
        self.reservas = {}  # Diccionario id -> Reserva
        self._siguiente_id = 1  # Contador para asignar ids de reserva
        self.intentos = 0  # Cantidad de intentos de reserva realizados
        self.proveedores_caidos = set()  # Ids de servicios cuyo proveedor no responde
        log.info("Sistema iniciado con %d servicios", len(self.servicios))

    # ------------------------------------------------------------------
    # Métodos auxiliares (validaciones)
    # ------------------------------------------------------------------
    def _validar_datos(self, cliente, personas, fecha_texto):
        """Valida y convierte los datos. Encadena excepciones con 'raise ... from'."""
        if not isinstance(cliente, str) or not cliente.strip():  # Nombre vacío o no texto
            raise DatosInvalidosError("El nombre del cliente es obligatorio")
        try:
            personas = int(personas)  # Intenta convertir a entero
        except (ValueError, TypeError) as error:
            # Encadenamiento: el error original queda como causa (__cause__)
            raise DatosInvalidosError(
                f"Número de personas inválido: {personas!r}"
            ) from error
        if personas <= 0:  # Debe haber al menos una persona
            raise DatosInvalidosError("El número de personas debe ser mayor que cero")
        try:
            # Formato esperado: AAAA-MM-DD
            fecha = datetime.strptime(fecha_texto, "%Y-%m-%d").date()
        except (ValueError, TypeError) as error:
            raise DatosInvalidosError(
                f"Fecha inválida: {fecha_texto!r} (use AAAA-MM-DD)"
            ) from error
        return cliente.strip(), personas, fecha  # Datos limpios y convertidos

    def _obtener_servicio(self, servicio_id):
        """Busca un servicio; si no existe, lanza una excepción propia encadenada."""
        try:
            return self.servicios[servicio_id]  # Búsqueda directa en el diccionario
        except KeyError as error:
            raise ServicioNoDisponibleError(
                f"El servicio {servicio_id} no existe"
            ) from error

    def _llamar_proveedor(self, servicio):
        """Simula la consulta a un proveedor externo que puede estar caído."""
        if servicio.id in self.proveedores_caidos:  # Proveedor sin respuesta
            raise ConnectionError(f"Sin respuesta del proveedor de '{servicio.nombre}'")

    # ------------------------------------------------------------------
    # Operaciones principales
    # ------------------------------------------------------------------
    def crear_reserva(self, cliente, personas, fecha_texto, servicio_id):
        """Crea una reserva. Usa try/except/else/finally y registra todo en el log."""
        self.intentos += 1  # Cuenta el intento aunque falle
        try:
            # 1) Validar y convertir los datos de entrada
            cliente, personas, fecha = self._validar_datos(cliente, personas, fecha_texto)
            # 2) Verificar que el servicio exista y esté activo
            servicio = self._obtener_servicio(servicio_id)
            if not servicio.disponible:
                raise ServicioNoDisponibleError(f"'{servicio.nombre}' está fuera de servicio")
            # 3) Consultar al proveedor externo (puede fallar con ConnectionError)
            try:
                self._llamar_proveedor(servicio)
            except ConnectionError as error:
                raise ServicioNoDisponibleError(
                    f"Proveedor de '{servicio.nombre}' no disponible"
                ) from error  # Encadena el ConnectionError original
            # 4) Reglas de negocio
            if fecha < date.today():  # No se permiten fechas pasadas
                raise ReservaInvalidaError(f"La fecha {fecha} ya pasó")
            if personas > servicio.capacidad:  # No se puede superar la capacidad
                raise ReservaInvalidaError(
                    f"{personas} personas superan la capacidad ({servicio.capacidad}) de '{servicio.nombre}'"
                )
            for r in self.reservas.values():  # Evita reservas duplicadas
                if (r.cliente, r.servicio_id, r.fecha, r.estado) == (
                    cliente, servicio_id, fecha, "CONFIRMADA",
                ):
                    raise ReservaInvalidaError(f"{cliente} ya tiene una reserva ese día en '{servicio.nombre}'")
        except ErrorReservas as error:
            # Se registra el error (con traceback si hay causa encadenada) y se propaga
            log.error("Reserva rechazada: %s", error, exc_info=bool(error.__cause__))
            raise  # El llamador decide cómo continuar; la app no se cae
        else:
            # Solo se ejecuta si NO hubo excepciones: se confirma la reserva
            reserva = Reserva(self._siguiente_id, cliente, servicio_id, fecha, personas)
            self.reservas[reserva.id] = reserva  # Guarda la reserva
            self._siguiente_id += 1  # Prepara el siguiente id
            log.info("Reserva #%d creada: %s en '%s' el %s (%d pers.)",
                     reserva.id, cliente, servicio.nombre, fecha, personas)
            return reserva
        finally:
            # Se ejecuta SIEMPRE, haya o no error
            log.debug("Intento de reserva #%d finalizado", self.intentos)

    def cancelar_reserva(self, reserva_id):
        """Cancela una reserva existente."""
        try:
            reserva = self.reservas[reserva_id]  # Busca la reserva
            if reserva.estado == "CANCELADA":  # No se puede cancelar dos veces
                raise ReservaInvalidaError(f"La reserva #{reserva_id} ya estaba cancelada")
        except KeyError as error:
            log.error("Cancelación fallida: reserva #%s no existe", reserva_id)
            raise ReservaNoEncontradaError(
                f"La reserva #{reserva_id} no existe"
            ) from error  # Encadena el KeyError original
        except ReservaInvalidaError as error:
            log.error("Cancelación rechazada: %s", error)
            raise
        else:
            reserva.estado = "CANCELADA"  # Cambia el estado
            log.info("Reserva #%d cancelada", reserva_id)
            return reserva
        finally:
            log.debug("Operación de cancelación sobre #%s finalizada", reserva_id)
