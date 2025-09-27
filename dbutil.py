import psycopg2
from math import floor
from valsutil import *

def fetch_skills(db):
    with db.cursor() as cur:
        cur.execute("""
                SELECT * FROM skills;
                """)
        return cur.fetchall()

def fetch_skill_by_index(db, ndx):
    skills = fetch_skills(db)
    try:
        skill = skills[ndx]
        return skill
    except:
        raise IndexError
    
def add_skill(db, skill_name):
    with db.cursor() as cur:
        try:
            cur.execute("""
                        INSERT INTO skills (name, mins, lvl, prestige)
                        VALUES ('{name}', 0, 0, 0);
                        """.format(name=skill_name))
            db.commit()
        except:
            db.rollback()
            raise NameError("A skill named {name} already exists!".format(name=skill_name))
        return

def remove_skill(db, skill_name):
    with db.cursor() as cur:
        cur.execute("""
                    DELETE FROM skills WHERE
                    name='{name}';
                    """.format(name=skill_name))
        db.commit()
        if(cur.statusmessage == "DELETE 0"):
            raise NameError("No skill named {name} could be found!".format(name=skill_name))
        return
        
    
def fetch_skills_formatted(db):
    skills_raw = fetch_skills(db)
    skills = []
    ndx = 0

    for skill in skills_raw:
        # string builder
        skill_string = "║ ["
        skill_string += str(ndx)
        skill_string += "]\t"
        skill_string += skill[1]
        
        for i in range(MAX_NAME_LEN - len(skill[1])):
            skill_string += " "
        skill_string += " ["

        # progress bar builder
        skill_progress = floor((skill[2] / (MINUTES * (1 + skill[4]))) * BAR_LEN)
        for i in range(skill_progress):
            skill_string += "*"
        for i in range(BAR_LEN - skill_progress):
            skill_string += " "

        # pad level marker if <10
        skill_string += "] LVL"
        if(skill[3] < 10):
            skill_string += "0"
        skill_string += str(skill[3])

        # prestige bar builder
        skill_string += BRIGHT_YELLOW
        for i in range(skill[4]):
            skill_string += "✦"
        for i in range(5 - skill[4]):
            skill_string += " "
        skill_string += RESET

        skill_string += " ║"

        skills.append(skill_string)

        ndx += 1

    return skills