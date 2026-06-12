import os
import subprocess
from io import StringIO

import pandas as pd
import requests

DATA_URL = (
    "https://docs.google.com/spreadsheets/d/1SccaMN39OepYrvrGIlyjQTCetxj19noNeLaW-55WS7o/export?format=csv&id=1SccaMN39OepYrvrGIlyjQTCetxj19noNeLaW-55WS7o&gid=1447091477",
)


def load_dataframe() -> pd.DataFrame:
    """Carga el DataFrame desde URL o archivo local."""
    response = requests.get(DATA_URL, timeout=30)

    if DATA_URL.endswith(".csv") or "text/csv" in response.headers.get(
        "Content-Type", ""
    ):
        df = pd.read_csv(StringIO(response.text))
    else:
        from io import BytesIO

        df = pd.read_excel(BytesIO(response.content))
    return df


def run(cmd: str, check=True) -> subprocess.CompletedProcess:
    """Ejecuta un comando shell, imprime y retorna resultado."""
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.stdout.strip():
        print(f"    {result.stdout.strip()}")
    if result.stderr.strip():
        print(f"    STDERR: {result.stderr.strip()}")
    if check and result.returncode != 0:
        raise RuntimeError(f"Comando falló (rc={result.returncode}): {cmd}")
    return result


def branch_exists_remote(branch: str) -> bool:
    result = run(f"git ls-remote --heads origin {branch}", check=False)
    return branch in result.stdout


def branch_exists_local(branch: str) -> bool:
    result = run(f"git branch --list {branch}", check=False)
    return branch.strip() in result.stdout.strip()


def setup_git_config():
    """Configura git user si estamos en CI (GitHub Actions)."""
    if os.getenv("GITHUB_ACTIONS"):
        run('git config user.email "github-actions[bot]@users.noreply.github.com"')
        run('git config user.name "github-actions[bot]"')


def process_user(user: str, user_row: pd.Series, all_columns: list):
    """Crea branch, escribe CSV con la fila del usuario y hace push."""
    # 1. Volver a main antes de crear/cambiar branch
    run("git checkout main")

    # 2. Crear branch si no existe (local ni remote)
    if branch_exists_remote(user):
        if not branch_exists_local(user):
            run(f"git checkout -b {user} origin/{user}")
        else:
            run(f"git checkout {user}")
            run(f"git pull origin {user} --ff-only", check=False)
    else:
        print(f"    Creando nueva branch '{user}'...")
        run(f"git checkout -b {user}")

    # 3. Crear carpeta data/ si no existe
    os.makedirs("data", exist_ok=True)

    # 4. Escribir CSV con solo la fila del usuario
    csv_path = os.path.join("data", f"{user}.csv")
    row_df = pd.DataFrame([user_row], columns=all_columns)
    row_df.to_csv(csv_path, index=False)
    print(f"    CSV escrito: {csv_path}")

    # 5. Git add + commit + push
    run(f"git add {csv_path}")

    # Commit solo si hay cambios staged
    status = run("git status --porcelain", check=False)
    if status.stdout.strip():
        run(f'git commit -m "data: add/update {user}.csv"')
        run(f"git push -u origin {user}")
        print(f"    [OK] Push exitoso → origin/{user}")
    else:
        print(f"    Sin cambios nuevos para {user}, skip push.")


def main():
    setup_git_config()
    GITHUB_COL = "user_github"

    # Carga datos
    df = load_dataframe()

    # Limpia: drop nulos y espacios en user_github
    df[GITHUB_COL] = df[GITHUB_COL].astype(str).str.strip()
    df = df[df[GITHUB_COL].notna() & (df[GITHUB_COL] != "") & (df[GITHUB_COL] != "nan")]

    users = df[GITHUB_COL].unique()
    print(f"\n[+] Usuarios encontrados ({len(users)}): {list(users)}")

    errors = []
    for user in users:
        # Si hay duplicados, toma la última fila (más reciente en el form)
        user_row = df[df[GITHUB_COL] == user].iloc[-1]
        try:
            process_user(user, user_row, list(df.columns))
        except Exception as e:
            print(f"    [ERROR] {user}: {e}")
            errors.append((user, str(e)))


# if __name__ == "__main__":
#     main()
