import db

db.curr.execute("""
CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL
);
""")

db.curr.execute("""
CREATE TABLE IF NOT EXISTS chats(
    id SERIAL PRIMARY KEY,
    user_id INTEGER references users(id),
    alias VARCHAR NOT NULL
);
""")

db.curr.execute("""
CREATE TABLE IF NOT EXISTS messages(
    id SERIAL PRIMARY KEY,
    chat_id INTEGER REFERENCES chats(id),
    content VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);
""")

db.curr.execute("""
CREATE TABLE IF NOT EXISTS um_bridge(
    id SERIAL PRIMARY KEY,
    user_id INTEGER references users(id),
    message_id INTEGER references messages(id)
)
""")

db.conn.commit()
db.curr.close()
db.conn.close()