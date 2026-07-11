set shell := ["powershell.exe", "-Command"] # Windows
# set shell := ["bash", "-c"] # Linux/Mac

run:
    uv run streamlit run src/skills/app/general.py