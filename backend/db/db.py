import psycopg2

host = "abilify-db.postgres.database.azure.com"
dbname = "postgres"
user = "abilify"
password = "xUR}4LYE;zphk}n"
sslmode = "require"

conn: psycopg2.extensions.connection = psycopg2.connect(f"host={host} user={user} dbname={dbname} password={password} sslmode={sslmode}")
curr: psycopg2.extensions.cursor = conn.cursor()