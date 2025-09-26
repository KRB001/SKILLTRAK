# SKILLTRAK v0.0.4

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
    print(RED + "Could not connect to database, was database initialized?")
    exit(0)
print("Connected!")

# main title
print("\n\n\n")
print("▄▖▖▖▄▖▖ ▖ ▄▖▄▖▄▖▖▖\n▚ ▙▘▐ ▌ ▌ ▐ ▙▘▌▌▙▘\n▄▌▌▌▟▖▙▖▙▖▐ ▌▌▛▌▌▌")
print("\n")

user_in = ""

# dialogue loop
while(user_in.lower() != "q" and user_in.lower() != "quit"):

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