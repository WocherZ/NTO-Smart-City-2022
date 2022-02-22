import sqlite3
def sql_auth_doct(records):
    sqlite_connection = sqlite3.connect('db.sqlite3')
    cursor = sqlite_connection.cursor()

    sqlite_select_query = """SELECT login, password from app_doctor"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    return (records)

def sql_auth_pat(records):
    sqlite_connection = sqlite3.connect('db.sqlite3')
    cursor = sqlite_connection.cursor()

    sqlite_select_query = """SELECT login, password from app_patient"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    return (records)