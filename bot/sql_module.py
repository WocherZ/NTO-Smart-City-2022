import sqlite3

def read_sqlite_table(records):
    try:
        sqlite_connection = sqlite3.connect('db.sqlite3')
        cursor = sqlite_connection.cursor()

        sqlite_select_query = """SELECT id, first_name, last_name, login, password, age, height, weight, doctor_id, room_id, image_link, diagnosis, gender from  app_patient"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        return(records)

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def analisis(records):
    try:
        sqlite_connection = sqlite3.connect('db.sqlite3')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = """SELECT * from  app_analysis"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        return (records)

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()