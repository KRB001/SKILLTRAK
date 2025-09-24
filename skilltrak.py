# SKILLTRAK v0.0.3

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

# query for all skills in db
skills = fetch_skills_formatted(db)

print("╔═══════════════════════════════════════════════════╗")

for skill in skills:
    print(skill)

print("╚═══════════════════════════════════════════════════╝")


# close connection to db
print("\nTerminating connection to database...")
db.close()
print("Connection closed.")