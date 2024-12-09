from flask import current_app
import sqlite3 as sql


# Code snippet for logging a message
# current_app.logger.critical("message")


def check_login(email, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM TLD91_USERS WHERE email == ? AND password == ?",
        (email, password),
    )
    result = cur.fetchone()
    con.close()
    if result is None:
        return False
    else:
        return True
