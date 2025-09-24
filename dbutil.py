import psycopg2

def fetch_skills(db):
    with db.cursor() as cur:
        cur.execute("""
                SELECT * FROM skills;
                """)
        return cur.fetchall()