import sqlite3
import os

print(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'project.db'))
conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'project.db'))
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS contacts(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   name TEXT,
   phone INTEGER,
   address TEXT,
   email TEXT,
   birthday TEXT);
""")
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS notes(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   tag TEXT,
   note TEXT);
""")
conn.commit()
