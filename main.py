"""Ejecuta 16 simulaciones (válidas e inválidas) sobre el sistema de reservas."""

from datetime import date, timedelta  # Para generar fechas relativas a hoy

from excepciones import ErrorReservas  # Excepción base del sistema
from logger_config import obtener_logger
from sistema_reservas import Servicio, SistemaReservas

log = obtener_logger()  # Mismo logger que usa el sistema


def ejecutar(numero, descripcion, funcion, resultados):
    """Ejecuta una simulación sin permitir que un error detenga el programa."""
    log.info("--- Simulación %02d: %s ---", numero, descripcion)
    try:
        funcion()  # Corre la simulación
    except ErrorReservas as error:
        estado, detalle = "ERROR CONTROLADO", str(error)  # Error esperado del sistema
    except Exception as error:  # Red de seguridad para errores no previstos
        log.critical("Error inesperado en simulación %02d", numero, exc_info=True)
        estado, detalle = "ERROR INESPERADO", f"{type(error).__name__}: {error}"
    else:
        estado, detalle = "OK", "Operación exitosa"
    finally:
        log.info("--- Fin simulación %02d ---", numero)
    resultados.append((numero, descripcion, estado))  # Guarda el resultado
    print(f"{numero:02d}. {descripcion:<45} -> {estado}: {detalle}")


def main():
    """Prepara el sistema y corre todas las simulaciones."""
    sistema = SistemaReservas([
        Servicio(1, "Restaurante", 10),
        Servicio(2, "Hotel", 6),
        Servicio(3, "Spa", 4),
        Servicio(4, "Cine", 50, disponible=False),  # Fuera de servicio
        Servicio(5, "Tour guiado", 15),  # Su proveedor estará caído
    ])
    sistema.proveedores_caidos.add(5)  # Simula caída del proveedor del tour
    hoy = date.today()
    manana = (hoy + timedelta(days=1)).isoformat()  # Fecha futura válida
    en_3 = (hoy + timedelta(days=3)).isoformat()
    ayer = (hoy - timedelta(days=1)).isoformat()  # Fecha pasada
    resultados = []

    simulaciones = [
        ("Reserva válida (restaurante)", lambda: sistema.crear_reserva("Ana", 2, manana, 1)),
        ("Reserva válida (hotel)", lambda: sistema.crear_reserva("Luis", 4, en_3, 2)),
        ("Reserva válida (spa)", lambda: sistema.crear_reserva("Marta", 1, en_3, 3)),
        ("Nombre de cliente vacío", lambda: sistema.crear_reserva("  ", 2, manana, 1)),
        ("Personas no numéricas ('abc')", lambda: sistema.crear_reserva("Pedro", "abc", manana, 1)),
        ("Fecha con formato incorrecto", lambda: sistema.crear_reserva("Pedro", 2, "31/12/2026", 1)),
        ("Fecha pasada", lambda: sistema.crear_reserva("Pedro", 2, ayer, 1)),
        ("Supera la capacidad del spa", lambda: sistema.crear_reserva("Pedro", 9, manana, 3)),
        ("Servicio inexistente (id 99)", lambda: sistema.crear_reserva("Pedro", 2, manana, 99)),
        ("Servicio fuera de servicio (cine)", lambda: sistema.crear_reserva("Pedro", 2, manana, 4)),
        ("Proveedor caído (tour)", lambda: sistema.crear_reserva("Pedro", 2, manana, 5)),
        ("Reserva duplicada (Ana)", lambda: sistema.crear_reserva("Ana", 2, manana, 1)),
        ("Cancelar reserva existente (#1)", lambda: sistema.cancelar_reserva(1)),
        ("Cancelar reserva inexistente (#42)", lambda: sistema.cancelar_reserva(42)),
        ("Cancelar reserva ya cancelada (#1)", lambda: sistema.cancelar_reserva(1)),
        ("Fallo inesperado (división por cero)", lambda: 1 / 0),
    ]

    print("=== SIMULACIONES ===")
    for numero, (descripcion, funcion) in enumerate(simulaciones, start=1):
        ejecutar(numero, descripcion, funcion, resultados)

    ok = sum(1 for _, _, e in resultados if e == "OK")
    print(f"\nTotal: {len(resultados)} | Exitosas: {ok} | Con error: {len(resultados) - ok}")
    print("La aplicación terminó de forma estable. Revisa logs/sistema.log")


if __name__ == "__main__":  # Punto de entrada del programa
    main()
