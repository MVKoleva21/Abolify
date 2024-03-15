import db

db.curr.execute("SELECT * FROM users")
print(db.curr.fetchall())