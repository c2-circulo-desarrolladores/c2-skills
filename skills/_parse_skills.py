import re
from pathlib import Path

from skills._models import MemberSkills, Skill, SkillSection


def parse_markdown(md_path: Path) -> list[SkillSection]:
    """Parse markdown file y extrae secciones con sus skills"""
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    sections = []
    current_section = None

    for line in content.split("\n"):
        # Detectar títulos de sección (# Title)
        if line.startswith("# "):
            if current_section:
                sections.append(current_section)
            title = line.replace("# ", "").strip()
            current_section = SkillSection(title=title, skills=[])

        # Detectar skills (- [ ] o - [X])
        elif line.strip().startswith("- ["):
            match = re.match(r"- \[([ xX])\] (.+)", line.strip())
            if match:
                checked = match.group(1).lower() == "x"
                skill_name = match.group(2).strip()
                if current_section:
                    current_section.skills.append(Skill(skill_name, checked))

    # Agregar última sección
    if current_section:
        sections.append(current_section)

    return sections


def parse_skills_all(miembros_path: Path) -> list[MemberSkills]:
    """Parse todos los miembros y sus skills"""
    all_members = []

    for miembro_carpeta in miembros_path.iterdir():
        if not miembro_carpeta.is_dir():
            continue

        member_name = miembro_carpeta.name
        fundamentals = []
        profiles = []

        for md_file in miembro_carpeta.iterdir():
            if md_file.name == "FUNDAMENTALS.md":
                fundamentals = parse_markdown(md_file)
            elif md_file.name == "PERFIL.md":
                profiles = parse_markdown(md_file)

        if fundamentals or profiles:
            all_members.append(MemberSkills(member_name, fundamentals, profiles))

    return all_members
