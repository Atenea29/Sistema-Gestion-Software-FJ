"""Simula 35 operaciones (válidas e inválidas) del sistema de Software FJ."""

from datetime import date, timedelta  # Fechas relativas a hoy

from cliente import Cliente
from entidad import Entidad
from excepciones import ErrorReservas  # Excepción base del sistema
from logger_config import obtener_logger
from reserva import Reserva
from servicio import Servicio
from servicio_asesoria import AsesoriaEspecializada
from servicio_equipo import AlquilerEquipo
from servicio_sala import ReservaSala
from sistema_reservas import SistemaReservas

log = obtener_logger()  # Mismo logger que usa el sistema


def ejecutar(numero, descripcion, funcion, resultados):
    """Ejecuta una operación sin permitir que un error detenga el programa."""
    log.info("--- Simulación %02d: %s ---", numero, descripcion)
    try:
        resultado = funcion()  # Corre la simulación
    except ErrorReservas as error:
        if not error.registrado:  # Si aún no está en el log, se registra aquí
            log.error("Error controlado: %s", error, exc_info=bool(error.__cause__))
        estado, detalle = "ERROR CONTROLADO", str(error)  # Registra error de dominio controlado
    except Exception as error:  # Red de seguridad para errores no previstos
        log.critical("Error inesperado en simulación %02d", numero, exc_info=True)
        estado, detalle = "ERROR INESPERADO", f"{type(error).__name__}: {error}"  # Expone tipo y mensaje del fallo
    else:
        estado = "OK"  # Operación completada sin excepciones
        if isinstance(resultado, Reserva):
            detalle = resultado.describir()
        elif isinstance(resultado, Entidad):
            detalle = resultado.describir()
        else:
            detalle = "Operación exitosa"
    finally:
        log.info("--- Fin simulación %02d ---", numero)  # Cierra el bloque de traza de la simulación
    resultados.append((numero, descripcion, estado))  # Guarda resumen para el conteo final
    print(f"{numero:02d}. {descripcion:<50} -> {estado}: {detalle}")


def instanciar_abstracta():
    """Intenta crear un Servicio directamente: Python lo impide por ser abstracta."""
    try:
        Servicio(99, "Servicio genérico", 1000)  # TypeError: clase abstracta
    except TypeError as error:
        raise ErrorReservas("Servicio es abstracta y no se puede instanciar") from error  # Convierte y encadena el error


def main():
    """Prepara el sistema y corre todas las simulaciones."""
    sistema = SistemaReservas()  # Instancia principal del sistema en memoria
    sistema.registrar_cliente(Cliente(1, "Ana Pérez", "10203040", "ana@correo.com", "3001234567"))
    sistema.registrar_cliente(Cliente(2, "Luis Gómez", "55667788", "luis@correo.com", "3109876543"))
    sala = ReservaSala(1, "Sala de juntas A", 40000, capacidad=10)  # $40.000 por hora
    equipo = AlquilerEquipo(2, "Portátil", 25000, stock=5)  # $25.000 por día y unidad
    asesoria = AsesoriaEspecializada(3, "Asesoría en Python", 90000)  # $90.000 por hora
    apagado = ReservaSala(4, "Sala B (en mantenimiento)", 30000, capacidad=6, disponible=False)  # Servicio no disponible
    remota = AsesoriaEspecializada(5, "Asesoría externa", 80000)  # Proveedor caído
    for servicio in (sala, equipo, asesoria, apagado, remota):
        sistema.registrar_servicio(servicio)
    sistema.proveedores_caidos.add(5)  # Simula caída del proveedor del servicio 5

    hoy = date.today()
    f1, f2, f3, f4 = [(hoy + timedelta(days=d)).isoformat() for d in (1, 2, 3, 4)]  # Fechas futuras válidas
    ayer = (hoy - timedelta(days=1)).isoformat()  # Fecha pasada para probar rechazo
    cr = sistema.crear_reserva  # Atajo: crear_reserva(cliente, servicio, fecha, duracion, *opciones)

    simulaciones = [
        # --- Clientes (casos válidos y errores de validación/duplicidad) ---
        ("Registrar cliente válido (Carlos Ruiz)",
         lambda: sistema.registrar_cliente(Cliente(3, "Carlos Ruiz", "99887766", "carlos@correo.com", "3201112233"))),
        ("Cliente con nombre inválido ('A1')", lambda: Cliente(4, "A1", "123456", "a@b.com", "3001112233")),
        ("Cliente con correo inválido", lambda: Cliente(4, "Marta Díaz", "123456", "sin-arroba", "3001112233")),
        ("Cliente con teléfono inválido", lambda: Cliente(4, "Marta Díaz", "123456", "m@b.com", "12345")),
        ("Cliente con documento inválido", lambda: Cliente(4, "Marta Díaz", "12ab", "m@b.com", "3001112233")),
        ("Registrar cliente con id repetido",
         lambda: sistema.registrar_cliente(Cliente(1, "Otra Persona", "11223344", "o@b.com", "3001112233"))),
        # --- Servicios (casos válidos, errores de datos y clase abstracta) ---
        ("Crear servicio válido (Proyector)",
         lambda: sistema.registrar_servicio(AlquilerEquipo(6, "Proyector", 40000, stock=3))),
        ("Crear servicio con tarifa negativa", lambda: ReservaSala(7, "Sala C", -100, capacidad=5)),
        ("Crear servicio con nombre vacío", lambda: AsesoriaEspecializada(8, "   ", 50000)),
        ("Crear servicio con tarifa como texto", lambda: AlquilerEquipo(9, "Tablet", "barata", stock=2)),
        ("Instanciar la clase abstracta Servicio", instanciar_abstracta),
        # --- Reservas exitosas (las tres formas de sobrecarga) ---
        ("Sala: 2 horas (1 argumento)", lambda: cr(1, 1, f1, 2)),
        ("Sala: 3 h con 10 % descuento (2 argumentos)", lambda: cr(2, 1, f2, 3, 0.10)),
        ("Sala: 4 h, 10 % desc. e IVA 19 % (3 argumentos)", lambda: cr(1, 1, f3, 4, 0.10, 0.19)),
        ("Equipo: 3 días, 2 unidades, con seguro", lambda: cr(1, 2, f1, 3, 2, True)),
        ("Asesoría: 2 h, nivel experto, urgente", lambda: cr(2, 3, f1, 2, "experto", True)),
        # --- Parámetros inválidos (deben provocar errores controlados) ---
        ("Sala: horas negativas", lambda: cr(1, 1, f4, -2)),
        ("Sala: más de 12 horas", lambda: cr(1, 1, f4, 15)),
        ("Sala: descuento fuera de rango (150 %)", lambda: cr(1, 1, f4, 2, 1.5)),
        ("Sala: 4 argumentos (sobrecarga inexistente)", lambda: cr(1, 1, f4, 2, 0.1, 0.19, 5)),
        ("Sala: horas como texto ('dos')", lambda: cr(1, 1, f4, "dos")),
        ("Equipo: stock insuficiente (10 de 5)", lambda: cr(1, 2, f4, 2, 10)),
        ("Asesoría: nivel desconocido ('gurú')", lambda: cr(1, 3, f4, 2, "gurú")),
        # --- Reservas fallidas por otras reglas (fechas, existencia, disponibilidad y duplicados) ---
        ("Fecha con formato incorrecto", lambda: cr(1, 1, "31/12/2026", 2)),
        ("Fecha pasada", lambda: cr(1, 1, ayer, 2)),
        ("Servicio inexistente (id 99)", lambda: cr(1, 99, f4, 2)),
        ("Cliente no registrado (id 77)", lambda: cr(77, 1, f4, 2)),
        ("Servicio fuera de servicio", lambda: cr(1, 4, f4, 2)),
        ("Proveedor externo caído", lambda: cr(1, 5, f4, 2)),
        ("Reserva duplicada (Ana, sala, mismo día)", lambda: cr(1, 1, f1, 2)),
        # --- Cancelaciones y fallo inesperado ---
        ("Cancelar reserva existente (#1)", lambda: sistema.cancelar_reserva(1)),
        ("Cancelar reserva inexistente (#42)", lambda: sistema.cancelar_reserva(42)),
        ("Cancelar reserva ya cancelada (#1)", lambda: sistema.cancelar_reserva(1)),
        ("Reserva nueva tras cancelar (misma sala y día)", lambda: cr(1, 1, f1, 1)),
        ("Fallo inesperado (división por cero)", lambda: 1 / 0),  # Provoca error no controlado para probar captura
    ]

    print("=== SIMULACIONES ===")
    resultados = []
    for numero, (descripcion, funcion) in enumerate(simulaciones, start=1):
        ejecutar(numero, descripcion, funcion, resultados)  # Ejecuta y registra cada simulación

    ok = sum(1 for _, _, e in resultados if e == "OK")  # Cuenta simulaciones exitosas
    print(f"\nTotal: {len(resultados)} | Exitosas: {ok} | Con error: {len(resultados) - ok}")
    print(f"Clientes: {len(sistema.clientes)} | Servicios: {len(sistema.servicios)} | "
          f"Reservas en lista: {len(sistema.reservas)}")
    print("La aplicación terminó de forma estable. Revisa logs/sistema.log")


if __name__ == "__main__":  # Punto de entrada del programa
    main()