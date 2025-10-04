import psycopg2
from math import floor
from valsutil import *
from datetime import datetime

### FETCHES

def fetch_skills(db):
    with db.cursor() as cur:
        cur.execute("""
                SELECT * FROM skills
                ORDER BY prestige DESC, mins DESC;
                """)
        return cur.fetchall()

def fetch_skill_by_index(db, ndx):
    skills = fetch_skills(db)
    try:
        skill = skills[ndx]
        return skill
    except:
        raise IndexError
    
def fetch_skill_id_by_name(db, skill_name):
    with db.cursor() as cur:
        cur.execute("""
                        SELECT id FROM skills
                        WHERE name = '{name}';
                        """.format(name=skill_name))
        try:
            return cur.fetchone()[0]
        except:
            return None
        
    
### ADD FUNCTIONS

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

def log(db, skill_name, mins):
    with db.cursor() as cur:

        # fetch skill id and datetime block
        skill_id = fetch_skill_id_by_name(db, skill_name)

        if skill_id == None:
            raise NameError("A skill named {name} does not exist!".format(name=skill_name))
        
        curr_datetime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S+00")

        # log in entries table block

        try:
            cur.execute("""
                         INSERT INTO entries(date, mins, skillID) 
                         VALUES ('{date}', {mins}, {skill_id});
                        """.format(date=curr_datetime,mins=mins,skill_id=skill_id))
            db.commit()
        except:
            db.rollback()
            raise RuntimeError("Was unable to log {mins} minutes for skill [{skill}]".format(mins=mins,skill=skill_name))
        
        # level logic block

        try:
            cur.execute("""
                        SELECT mins,lvl,prestige FROM skills
                        WHERE name = '{name}';
                        """.format(name=skill_name))
            
            curr_dat = cur.fetchone()
            curr_mins = int(curr_dat[0])
            curr_lvl = int(curr_dat[1])
            curr_pres = int(curr_dat[2])

            new_mins = curr_mins + int(mins)

            new_lvl = floor(new_mins / (60 * (curr_pres + 1)))

            new_pres = curr_pres
            if new_lvl > 99:
                new_mins = new_mins % (99 * 60 * (new_pres + 1))
                new_pres += new_lvl // 99
                new_lvl = floor(new_mins / (60 * (new_pres + 1)))
                print(YELLOW + "-*<>*-*<>*-*<>*-*<>*-*<>*-*<>*-*<>*-*<>*-*<>*-*<>*-*<>*-" + RESET + "\n")
                print("Your prestige for [" + skill_name + "] has increased to " + BRIGHT_YELLOW + "[" + str(new_pres) + "]" + RESET + " and your level has been reset!\n")
                print(YELLOW + "-*<>*-*<>*-*<>*-*<>*-*<>*-*<>*-*<>*-*<>*-*<>*-*<>*-*<>*-" + RESET + "\n")

            if new_lvl > curr_lvl:
                print("" + get_level_color(new_lvl) + ">>>>>>>>" + RESET)
                print("Your LEVEL for [" + skill_name + "] has increased to " + get_level_color(new_lvl) + "[" + str(new_lvl) + "]!" + RESET)
                print("" + get_level_color(new_lvl) + ">>>>>>>>\n" + RESET)

            cur.execute("""
                        UPDATE skills SET 
                        mins={new_mins},lvl={new_lvl},prestige={new_pres} 
                        WHERE name = '{name}';
                        """.format(new_mins=new_mins,new_lvl=new_lvl,new_pres=new_pres,name=skill_name))
            db.commit()
        except:
            db.rollback()
            raise RuntimeError("Was able to log an entry of {mins} minutes, " \
            "but was unable to add to total for [{skill}]".format(mins=mins,skill=skill_name))


### REMOVE FUNCTIONS

def remove_skill(db, skill_name):
    with db.cursor() as cur:
        cur.execute("""
                    DELETE FROM entries WHERE
                    skillID={skill_id};
                    """.format(skill_id=int(fetch_skill_id_by_name(db, skill_name))))
        cur.execute("""
                    DELETE FROM skills WHERE
                    name='{name}';
                    """.format(name=skill_name))
        db.commit()
        if(cur.statusmessage == "DELETE 0"):
            raise NameError("No skill named {name} could be found!".format(name=skill_name))
        return
        
    
### STRING FORMATTED FETCHES

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

        skill_color = get_level_color(skill[3])

        # progress bar builder
        skill_progress = floor(((skill[2] % (60 * (skill[4] + 1))) / (MINUTES * (1 + skill[4]))) * BAR_LEN)
        # I will explain the line above cuz it looks kinda stupid :))
        # skill_progress gets the current progress to the next level by:
        # 1. getting the number of minutes (skill[2])
        # 2. moduloing that by 60 * prestige+1 (skill[4]) to get the 'current' level progress minus all levels that were passed
        # 3. dividing that by 60 (MINUTES) * prestige+1 * BAR_LEN to get the number of stars to go in the progress bar
        
        skill_string += skill_color

        for i in range(skill_progress):
            skill_string += "*"
        for i in range(BAR_LEN - skill_progress):
            skill_string += " "

        skill_string += RESET

        # pad level marker if <10
        skill_string += "] LVL"

        skill_string += skill_color
        if(skill[3] < 10):
            skill_string += "0"
        skill_string += str(skill[3])
        skill_string += RESET

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

### MISC

def get_level_color(lvl):
    return LEVEL_COLORS[floor(lvl / 20)]