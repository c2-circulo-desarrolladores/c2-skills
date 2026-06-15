# c2_skills

Repositorio para visualizar las habilidades del equipo Open Source y generar un dashboard de perfiles técnicos.

Si eres nuevo, completa tu encuesta de fundamentos siguiendo la plantilla disponible en [encuestas_finales/fundamentals_template.md](encuestas_finales/fundamentals_template.md).

## Índice

- Encuesta
- Dashboard

## Encuesta

### Cómo responder la encuesta

1. Crea una nueva carpeta dentro de `miembros/` con tu nombre (por ejemplo `miembros/michael`).
2. Dentro de esa carpeta, crea un archivo llamado `fundamentals.md`.
3. Copia y adapta la plantilla de [encuestas_finales/fundamentals_template.md](encuestas_finales/fundamentals_template.md) en tu `fundamentals.md`
4. Completa la encuesta según las instrucciones.

### Estructura esperada

- Carpeta: `miembros/<nombre>/`
- Archivo: `fundamentals.md` (basado en la plantilla de `encuestas_finales/`)

## Cómo funciona el dashboard

- El dashboard recoge todos los archivos `fundamentals.md` dentro de `miembros/` y actualiza las vistas del equipo.
- Al agregar o modificar `miembros/<nombre>/fundamentals.md`, el dashboard incorporará los cambios en la próxima carga.

## Correr el dashboard localmente

- Requisitos: Python 3.8+, entornos virtuales y dependencias listadas en `pyproject.toml`.
- Pasos básicos:

```bash
uv sync
uv run streamlit run skills/app/overview.py
```