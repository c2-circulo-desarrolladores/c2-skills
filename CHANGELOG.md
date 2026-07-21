## [0.4.0] - 2026-07-21

### 🚀 Features

- **(cuestionario)** Agregar preguntas a encuesta principal

### 🐛 Bug Fixes

- **(io)** Corrije títulos de secciones a parsear; agregar error personalizado
- **(miembros)** Actualiza títulos de secciones de encuestas

### ⚙️ Miscellaneous Tasks

- Actualiza dependencias dev y agrega pre-commit

## [0.3.0] - 2026-07-12

### 🚀 Features

- **(ranking)** Añadir heatmap de miembros x encuesta ([#29](https://github.com/c2-circulo-desarrolladores/c2-cli/issues/29))
- **(mentoria)** Añade nueva pestaña de mentoria

### 🐛 Bug Fixes

- **(ranking)** Cambia width=content -> width=stretch

### 🚜 Refactor

- **(ranking)** Se usa funciones para renderizar la pestaña y reorganizar visuales; mueve 'temas débiles' a otra pestaña

### ⚙️ Miscellaneous Tasks

- Actualizar release workflow
- Fixes cliff.toml to skip version bumps
- Adds pre-commit as dev dependency
- Adds .vscode/ to .gitignore
- Just run executes streamlit on auto-rerun by default
- Adds pre-commit

## [0.2.0] - 2026-07-11

### 🚀 Features

- **(dashboard)** Añade pestaña de ranking del equipo

### 🐛 Bug Fixes

- **(individual)** Utiliza fn seleccionar_y_filtrar para consistencia
- **(io)** Corregir error en el mapeo de columnas
- **(general)** Corregir nombres de columnas
- **(individual)** Corregir nombres de columnas

### 🚜 Refactor

- Mover utilidades, colores y figuras a módulos propios dentro de shared/
- **(dashboard)** Mueve lógica repetida entre general e individual a shared/utils
- Cambia proyecto a src layout

### ⚙️ Miscellaneous Tasks

- Fixes release.yml
- Actualiza dependencias dev y añade cliff.toml
- Removes ruff 'line too long' rule
- Renombra pestaña overview -> general
- Añade commit_preprocessors para generar enlaces al poner 'closes #'
- Agregar commitizen como dependencia dev

## [0.1.1] - 2026-07-01

### 🚀 Features

- **(encuesta)** Se lee encuestas desde yaml

### 🐛 Bug Fixes

- **(encuesta)** Corregir orden de los headers
- **(encuesta)** Actualizar encuesta final de fundamentos

### 📚 Documentation

- **(encuesta)** Añadir docstrings a encuesta_parser.py

### ⚙️ Miscellaneous Tasks

- Añadir pull request template
- Limpiar repositorio
- **(cuestionario)** Añadir versión del cuestionario en yml
- Añadir pyyaml como dependencia
- Actualizar justfile
- Deletes fundamentals.xlsx
- Añade commitizen config a pyproject.toml

## [0.1.0] - 2026-07-01

### 🚀 Features

- Add josue info

### ⚙️ Miscellaneous Tasks

- Fixes uv.lock and adds commitizen
- Añadir release.yml

