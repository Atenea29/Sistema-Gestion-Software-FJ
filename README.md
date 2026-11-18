# Software FJ – Sistema de Reservas con Manejo de Excepciones

**Curso:** Programación (213023) · Universidad Nacional Abierta y a Distancia (UNAD)
**Actividad:** Fase 4 – Componente práctico (Prácticas simuladas)

Aplicación en Python orientada a objetos que gestiona reservas y demuestra un manejo
robusto de excepciones: excepciones personalizadas, `try/except/else/finally`,
encadenamiento de excepciones y registro de eventos y errores en un archivo de logs.
La aplicación nunca se detiene ante un error.

## Estructura del proyecto

| Archivo | Descripción |
|---|---|
| `main.py` | Punto de entrada. Ejecuta 35 simulaciones (válidas e inválidas). |
| `entidad.py` | Clase abstracta general `Entidad` (id y `describir()`). |
| `cliente.py` | Clase `Cliente` con atributos privados, propiedades y validaciones. |
| `servicio.py` | Clase abstracta `Servicio` con `validar_parametros()`, `calcular_costo()` y `describir()`. |
| `servicio_sala.py` | `ReservaSala`: costo sobrecargado (horas / descuento / IVA). |
| `servicio_equipo.py` | `AlquilerEquipo`: costo sobrecargado (días / cantidad / seguro). |
| `servicio_asesoria.py` | `AsesoriaEspecializada`: costo sobrecargado (horas / nivel / urgente). |
| `reserva.py` | Clase `Reserva`: cliente, servicio, duración y estado; `confirmar()`, `cancelar()` y `procesar()`. |
| `sistema_reservas.py` | Gestión con listas internas de clientes, servicios y reservas (sin base de datos). |
| `excepciones.py` | Jerarquía de excepciones personalizadas. |
| `logger_config.py` | Configuración del logging hacia `logs/sistema.log`. |
| `logs/sistema.log` | Archivo de logs generado en cada ejecución. |

## Programación orientada a objetos

- **Sin base de datos:** toda la información vive en objetos y listas; los archivos se usan solo para el log.
- **Abstracción:** `Entidad` y `Servicio` son clases abstractas (no se pueden instanciar).
- **Herencia:** `Cliente` y `Servicio` heredan de `Entidad`; las tres clases de servicio heredan de `Servicio`.
- **Encapsulación:** `Cliente` usa atributos privados con propiedades que validan al asignar.
- **Polimorfismo:** `calcular_costo()` y `describir()` se comportan distinto en cada servicio.
- **Sobrecarga:** Python no la trae nativa; se simula con argumentos variables (`*args`) y validación
  de cantidad y tipo, de modo que cada servicio acepta 1, 2 o 3 argumentos.

## Requisitos y ejecución

- Python 3.10 o superior (solo usa la biblioteca estándar, no hay que instalar nada).

```bash
python main.py
```

Al terminar, revise `logs/sistema.log`.

## Conceptos de excepciones aplicados

- **Excepciones personalizadas:** `ErrorReservas` (base), `DatosInvalidosError`,
  `ServicioNoDisponibleError`, `ReservaInvalidaError`, `ReservaNoEncontradaError`.
- **`try/except`:** captura de errores esperados en validaciones y simulaciones.
- **`try/except/else`:** la reserva solo se confirma si no hubo errores.
- **`try/finally`:** el cierre de cada intento se registra siempre.
- **Encadenamiento:** `raise ... from error` conserva la causa original
  (`ValueError`, `KeyError`, `ConnectionError`).
- **Logging:** niveles DEBUG, INFO, ERROR y CRITICAL en archivo.

## Simulaciones incluidas

Hay 35 simulaciones en `main.py`: registro válido e inválido de clientes (nombre, correo, teléfono, documento, id repetido), creación correcta e incorrecta de servicios (tarifa negativa, nombre vacío, tarifa como texto, clase abstracta), 5 reservas exitosas con las tres formas de sobrecarga de cada servicio, parámetros de costo erróneos, stock insuficiente, fechas inválidas o pasadas, cliente o servicio inexistente, servicio fuera de servicio, proveedor caído, reserva duplicada, cancelaciones y un fallo inesperado. Todo queda registrado en `logs/sistema.log`.

## Equipo de trabajo

| Integrante | Rama | Responsabilidad |
|---|---|---|
| Integrante 1 (nombre) | `feature/entidad-excepciones` | `entidad.py`, `excepciones.py` |
| Integrante 2 (nombre) | `feature/cliente` | `cliente.py` (encapsulación y validaciones) |
| Integrante 3 (nombre) | `feature/servicio-sala` | `servicio.py` y `servicio_sala.py` |
| Integrante 4 (nombre) | `feature/equipo-asesoria` | `servicio_equipo.py` y `servicio_asesoria.py` |
| Integrante 5 (nombre) | `feature/reserva-sistema` | `reserva.py`, `sistema_reservas.py`, `main.py`, `logger_config.py` |

## Flujo de trabajo en GitHub

1. Cada integrante trabaja en su propia rama (`feature/...`).
2. Los commits son frecuentes y descriptivos.
3. Los cambios llegan a `main` solo mediante *pull request* revisado por un compañero.
4. Cada tarea está asignada mediante un *issue*.
