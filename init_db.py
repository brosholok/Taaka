import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)')
conn.commit()
conn.close()

