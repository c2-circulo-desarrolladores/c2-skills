from dashboard.conf import MIEMBROS, TEMPLATES


def retrieve_skills() -> None:
    TEMPLATES / "FUNDAMENTALS.md"


def modify_skills_all() -> None:
    for miembro_carpeta in MIEMBROS.iterdir():
        for md_file in miembro_carpeta.iterdir():
            if md_file.name == "FUNDAMENTALS.md":
                pass
            elif md_file.name == "PERFIL.md":
                pass


if __name__ == "__main__":
    modify_skills_all()
