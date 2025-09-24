# SKILLTRAK v0.0.1

import psycopg2

# useful ANSI codes
RESET = "\033[0m"
RED = "\033[31m"

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


# close connection to db
print("Terminating connection to database...")
db.close()
print("Connection closed.")