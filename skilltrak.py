# SKILLTRAK v0.2.0

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

    # remove a skill
    if(user_in[0:3] == "rm " or user_in[0:7] == "remove "):
        rm_in = user_in.split(" ")
        # only 1 argument is valid
        if(len(rm_in) == 2):
            # call remove skill injection function from dbutil
            try:
                remove_skill(db, rm_in[1])
                print("Removed skill " + rm_in[1] + "!")
            # raised if query returns no rows deleted
            except NameError as e:
                print(RED + str(e) + RESET)
        # num of args other than 2
        else:
            print(RED + "Invalid number of arguments for command rm!" + RESET)
    
    # add a new skill
    elif(user_in[0:4] == "add "):
        add_in = user_in.split(" ")
        # only 1 argument is valid
        if(len(add_in) == 2):
            # call add skill injection function from dbutil
            try:
                add_skill(db, add_in[1])
                print("Added new skill " + add_in[1] + "!")
            # add raises an exception (can only happen if name violates uniqueness condition)
            except NameError as e:
                print(RED + str(e) + RESET)
        # num of args other than 2
        else:
            print(RED + "Invalid number of arguments for command add!" + RESET)
        
    elif(user_in[0:4] == "log "):
        log_in = user_in.split(" ")
        # 2 arguments valid
        if(len(log_in) == 3):
            mins = log_in[1]
            skill = log_in[2]
            try:
                skill = int(skill)
                skill = fetch_skill_by_index(db, skill)
                print(skill[1])
            except (TypeError, ValueError):
                print(skill)
            except IndexError:
                print(RED + "Index " + str(skill) + " is out of range!" + RESET)
        else:
            print(RED + "Invalid number of arguments for command log!" + RESET)

    else:
        if(user_in != ""):
            print(RED + "Invalid command!" + RESET)

    # query for all skills in db
    # refreshes every command
    skills = fetch_skills_formatted(db)

    print("  YOUR SKILLS:")
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