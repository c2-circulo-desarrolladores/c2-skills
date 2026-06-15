# c2_skills

Repositorio para visualizar las habilidades del Círculo Open Source y generar un dashboard de perfiles técnicos.

## Encuesta

### Encuestas disponibles

- [Encuesta de fundamentos](encuestas_finales/fundamentals.md).

### Cómo responder las encuestas

1. Clona el repositorio.
2. Crea una nueva carpeta dentro de `miembros/` con tu nombre (por ejemplo `miembros/michael`).
3. Copia el archivo [templates/fundamentals.md](templates/fundamentals.md) dentro de tu nueva carpeta.
4. Completa la encuesta según las instrucciones.
5. Crea una rama con tu nombre.
6. Sube tus cambios a tu rama y manda tu Pull Request.

## Dashboard
### Cómo funciona el dashboard

El dashboard utiliza el módulo [encuesta_parser](skills/io/encuesta_parser.py) para recoger todos los archivos `fundamentals.md` dentro de `miembros/` y convertirlos a un DataFrame de Polars, que se utilizará como insumo para los datos.
- Al agregar o modificar `miembros/<nombre>/fundamentals.md`, el dashboard incorporará los cambios en la próxima carga.

### Correr el dashboard localmente

Con uv:

```bash
uv sync
uv run streamlit run skills/app/overview.py
```

Con just instalado, también puedes correr el dashboard así:

```bash
just run
```
