from dataclasses import dataclass


@dataclass
class Skill:
    name: str
    checked: bool


@dataclass
class SkillSection:
    title: str
    skills: list[Skill]


@dataclass
class MemberSkills:
    name: str
    fundamentals: list[SkillSection]
    profiles: list[SkillSection]
