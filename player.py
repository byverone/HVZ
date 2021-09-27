import sqlite3


conn = sqlite3.connect('player.db')

c = conn.cursor()

c.execute("""CREATE TABLE players (
            username text,
            code text,
            status text
            )""")

conn.commit()

conn.close()


