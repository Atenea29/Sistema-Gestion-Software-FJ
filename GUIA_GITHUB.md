# Guía de GitHub para el equipo (5 integrantes)

Objetivo de la rúbrica (30 pts): repositorio organizado, **una rama por integrante**,
**commits frecuentes y descriptivos**, **pull requests**, **issues asignados**, **README**
y colaboración equilibrada.

---

## PARTE A – Lo hace UNA persona (el que crea el repositorio)

1. En github.com: **New repository** → nombre sugerido `sistema-reservas-excepciones`
   → público o privado (agregar al profesor y a los 4 compañeros como *collaborators*
   en Settings → Collaborators).
2. En la carpeta del proyecto (la que tiene los `.py`), en la terminal:

```bash
git init
git add main.py sistema_reservas.py excepciones.py logger_config.py README.md .gitignore
git commit -m "Commit inicial: estructura base del proyecto"
git branch -M main
git remote add origin https://github.com/USUARIO/sistema-reservas-excepciones.git
git push -u origin main
```

3. Crear los **6 issues** de la sección C (Issues → New issue → asignar a cada persona).
4. Compartir el enlace del repositorio en el foro de la actividad.

## PARTE B – Lo hace CADA integrante (4 pasos)

```bash
# 1. Clonar el repositorio (solo la primera vez)
git clone https://github.com/USUARIO/sistema-reservas-excepciones.git
cd sistema-reservas-excepciones

# 2. Crear SU rama (usar la de la tabla de abajo)
git checkout -b feature/nombre-de-su-rama

# 3. Hacer cambios y guardar con commits pequeños y descriptivos
git add archivo_modificado.py
git commit -m "Descripción clara de lo que cambió"
git push -u origin feature/nombre-de-su-rama

# 4. En GitHub: botón "Compare & pull request" → pedir revisión a un compañero
```

Después de que el pull request sea aprobado y fusionado, cada integrante actualiza su copia:

```bash
git checkout main
git pull
```

### Buenos mensajes de commit (ejemplos)

- `Agregar excepción DatosInvalidosError con código propio`
- `Validar formato de fecha y encadenar ValueError`
- `Registrar en el log el intento de reserva dentro de finally`
- `Agregar simulación de proveedor caído`
- `Documentar en el README la tabla de simulaciones`

Evitar mensajes como `cambios`, `update` o `arreglo`.

---

## C – Reparto de tareas, ramas e issues

| # | Integrante | Rama | Issue | Aporte concreto (que debe hacer con sus manos) |
|---|---|---|---|---|
| 1 | Integrante 1 | `feature/excepciones` | #1 Crear excepciones personalizadas | Escribir `excepciones.py`: clase base y 4 subclases, con comentarios. |
| 2 | Integrante 2 | `feature/logging` | #2 Configurar logging a archivo | Escribir `logger_config.py` y revisar que `logs/sistema.log` se genere. |
| 3 | Integrante 3 | `feature/validaciones` | #3 Validaciones y encadenamiento | Métodos `_validar_datos`, `_obtener_servicio`, `_llamar_proveedor`. |
| 4 | Integrante 4 | `feature/reservas` | #4 Crear y cancelar reservas | `crear_reserva` y `cancelar_reserva` con `try/except/else/finally`. |
| 5 | Integrante 5 | `feature/simulaciones` | #5 Simulaciones y pruebas | `main.py` con las 16 simulaciones y verificación del log. |
| Todos | — | — | #6 Documento PDF final | Portada, introducción, enlace, conclusiones y referencias APA. |

### Texto sugerido para cada issue (copiar y pegar)

**#1 Crear excepciones personalizadas** — Crear `excepciones.py` con la clase base
`ErrorReservas` y las subclases `DatosInvalidosError`, `ServicioNoDisponibleError`,
`ReservaInvalidaError` y `ReservaNoEncontradaError`. Criterio: cada una con código propio
y comentarios explicativos. *Asignado a: Integrante 1.*

**#2 Configurar logging a archivo** — Crear `logger_config.py` para que todos los eventos
y errores se escriban en `logs/sistema.log` con fecha, nivel, función y mensaje.
Criterio: el archivo se genera al ejecutar el programa. *Asignado a: Integrante 2.*

**#3 Validaciones y encadenamiento de excepciones** — Implementar la validación de nombre,
personas y fecha; la búsqueda de servicio y la consulta al proveedor. Criterio: usar
`raise ... from error` para conservar la causa original. *Asignado a: Integrante 3.*

**#4 Crear y cancelar reservas** — Implementar `crear_reserva` y `cancelar_reserva` con
`try/except/else/finally`, reglas de negocio (fecha pasada, capacidad, duplicadas) y
registro en el log. *Asignado a: Integrante 4.*

**#5 Simulaciones y pruebas** — Implementar `main.py` con mínimo 10 simulaciones (válidas
e inválidas) y una red de seguridad para errores inesperados. Criterio: el programa
termina sin caerse y el log registra todo. *Asignado a: Integrante 5.*

**#6 Documento PDF final** — Elaborar el PDF con portada, introducción, enlace del
repositorio, conclusiones y referencias en APA. *Asignado a: todos.*

---

## D – Para que el nivel sea "Alto" en la rúbrica

- [ ] Los 5 integrantes tienen **commits propios** (revisar en Insights → Contributors).
- [ ] Hay **una rama por integrante** y cada una se fusionó con un **pull request**.
- [ ] Cada pull request tiene **al menos una revisión** de otro compañero.
- [ ] Los **6 issues** están asignados y se cierran al fusionar (escribir `Closes #1` en la
      descripción del pull request).
- [ ] El **README** está completo y los nombres de los integrantes están escritos.
- [ ] `logs/sistema.log` está en el repositorio (o un fragmento en el README) como evidencia.
- [ ] Se conservan los comentarios línea por línea en el código.

## E – Advertencia importante

Si dos personas editan el mismo archivo (por ejemplo, los integrantes 3 y 4 en
`sistema_reservas.py`) puede aparecer un **conflicto de fusión**. Es normal y de hecho
sirve como evidencia de trabajo colaborativo: se resuelve en VS Code eligiendo
"Accept Both Changes" o editando a mano, y luego se hace un nuevo commit.

Cada integrante debe hacer sus propios commits desde su propia cuenta: la rúbrica evalúa
que la colaboración sea real y equilibrada, y el historial de GitHub lo muestra.
