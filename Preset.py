import sqlite3

conn = sqlite3.connect('search_engine.db')
cur = conn.cursor()

cur.execute('''UPDATE Ranking SET rank=1.0''')
conn.commit()

cur.close()

print("All pages set to a rank of 1.0")
