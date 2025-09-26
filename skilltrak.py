# SKILLTRAK v0.1.0

import psycopg2
from dbutil import *
from valsutil import *

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
    print(RED + "Could not connect to database, was database initialized?" + RESET)
    exit(0)
print("Connected!")

# main title
print("\n\n\n")
print("▄▖▖▖▄▖▖ ▖ ▄▖▄▖▄▖▖▖\n▚ ▙▘▐ ▌ ▌ ▐ ▙▘▌▌▙▘\n▄▌▌▌▟▖▙▖▙▖▐ ▌▌▛▌▌▌")
print("\n")

user_in = ""

# dialogue loop
while(user_in.lower() != "q" and user_in.lower() != "quit"):

    # all valid commands have keywords >3 chars long (plus space)
    if(len(user_in) > 4):
        # add a new skill
        if(user_in[0:4] == "add "):
            add_in = user_in.split(" ")
            # only 1 argument is valid
            if(len(add_in) == 2):
                add_skill(db, add_in[1])
                print("Added new skill " + add_in[1] + "!")
            else:
                print(RED + "Invalid number of arguments for command add!" + RESET)
    # all other invalid commands
    else:
        if(user_in != ""):
            print(RED + "Invalid command!" + RESET)

    # query for all skills in db
    # refreshes every command
    skills = fetch_skills_formatted(db)

    print("YOUR SKILLS:")
    print("╔═════════════════════════════════════════════════════════╗")

    for skill in skills:
        print(skill)

    print("╚═════════════════════════════════════════════════════════╝")

    user_in = input(" > ")
    # clear terminal window
    for i in range(20):
        print("\n")



# close connection to db
print("\nTerminating connection to database...")
db.close()
print("Connection closed.")