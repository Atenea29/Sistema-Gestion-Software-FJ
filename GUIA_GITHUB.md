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
git add *.py README.md .gitignore
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

| # | Integrante | Rama | Issue | Aporte concreto |
|---|---|---|---|---|
| 1 | Integrante 1 | `feature/entidad-excepciones` | #1 Clase abstracta general y excepciones | `entidad.py` y `excepciones.py` |
| 2 | Integrante 2 | `feature/cliente` | #2 Clase Cliente | `cliente.py`: atributos privados, propiedades y validaciones |
| 3 | Integrante 3 | `feature/servicio-sala` | #3 Servicio abstracto y reserva de salas | `servicio.py` y `servicio_sala.py` con costo sobrecargado |
| 4 | Integrante 4 | `feature/equipo-asesoria` | #4 Alquiler de equipos y asesorías | `servicio_equipo.py` y `servicio_asesoria.py` |
| 5 | Integrante 5 | `feature/reserva-sistema` | #5 Reserva, sistema, logging y simulaciones | `reserva.py`, `sistema_reservas.py`, `logger_config.py`, `main.py` |
| Todos | — | — | #6 Documento PDF final | Portada, introducción, enlace, conclusiones y referencias APA. |

### Texto sugerido para cada issue (copiar y pegar)

**#1** — Crear la clase abstracta `Entidad` y la jerarquía de excepciones personalizadas.
**#2** — Crear `Cliente` con encapsulación y validaciones de nombre, documento, correo y teléfono.
**#3** — Crear la clase abstracta `Servicio` y `ReservaSala` con `calcular_costo` sobrecargado.
**#4** — Crear `AlquilerEquipo` y `AsesoriaEspecializada` con `calcular_costo` sobrecargado.
**#5** — Crear la clase `Reserva` (confirmar, cancelar, procesar), el sistema con listas internas, el logging y mínimo 10 simulaciones.

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
