import psycopg2
from math import floor
from valsutil import *

def fetch_skills(db):
    with db.cursor() as cur:
        cur.execute("""
                SELECT * FROM skills;
                """)
        return cur.fetchall()
    
def fetch_skills_formatted(db):
    skills_raw = fetch_skills(db)
    skills = []

    for skill in skills_raw:
        # string builder
        skill_string = "║ "
        skill_string += skill[1]
        for i in range(15 - len(skill[1])):
            skill_string += " "
        skill_string += " ["

        # progress bar builder
        skill_progress = floor((skill[2] / (MINUTES * (1 + skill[4]))) * 20)
        for i in range(skill_progress):
            skill_string += "*"
        for i in range(20 - skill_progress):
            skill_string += " "

        # pad level marker
        skill_string += "] LVL"
        if(skill[3] < 10):
            skill_string += "0"
        skill_string += str(skill[3])

        # prestige bar builder
        for i in range(skill[4]):
            skill_string += "✦"
        for i in range(5 - skill[4]):
            skill_string += " "

        skill_string += " ║"

        skills.append(skill_string)

    return skills