set shell := ["powershell.exe", "-Command"] # Windows
# set shell := ["bash", "-c"] # Linux/Mac

# Update pre-commit hooks
update:
    pre-commit autoupdate
     
# Format files
format-py:
    # 🧹 Removes unused imports and variables
    uv run autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r . --exclude "__init__.py"

    # 🧭 Orders imports
    uv run isort . --profile black

    # 🐶 Formats code
    uv run ruff check --fix . --exit-zero

run:
    uv run streamlit run skills/app/overview.py
