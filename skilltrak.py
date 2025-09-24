# SKILLTRAK v0.0.2

import psycopg2
from math import floor
from dbutil import *

# useful ANSI codes
RESET = "\033[0m"
RED = "\033[31m"

# no magic numbers
MINUTES = 60



# clear terminal window
for i in range(20):
    print("\n")

# attempt connection to db
print("Connecting to database...")
try:
    db = psycopg2.connect(database = "skilltrak",
                      host = "localhost",
                      port = 5432)
except:
    print(RED + "Could not connect to database, was database initialized?")
    exit(0)
print("Connected!")

# main title
print("\n\n\n")
print("▄▖▖▖▄▖▖ ▖ ▄▖▄▖▄▖▖▖\n▚ ▙▘▐ ▌ ▌ ▐ ▙▘▌▌▙▘\n▄▌▌▌▟▖▙▖▙▖▐ ▌▌▛▌▌▌")
print("\n")

# query for all skills in db
skills = fetch_skills(db)

print("╔═══════════════════════════════════════════════════╗")

for skill in skills:
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

    print(skill_string)

print("╚═══════════════════════════════════════════════════╝")


# close connection to db
print("\nTerminating connection to database...")
db.close()
print("Connection closed.")