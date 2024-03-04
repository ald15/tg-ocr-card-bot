import os
import sqlite3
import pandas as pd

# Процедура создания БД
def createDb(db_name = './sqlite_python1.db'):
    if not os.path.isfile(db_name):
        conn = sqlite3.connect(db_name)
        query = '''
                    CREATE TABLE edit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT
                    );
                '''
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        if conn: conn.close()


# Процедура добавления данных в БД
def insertDb(data_inp, db_name = './sqlite_python1.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query  ='''
                INSERT INTO edit (
                    data
                    ) VALUES (?);
            '''
    cursor.execute(query, (data_inp,))
    conn.commit()
    cursor.close()
    if conn: conn.close()
    return lastIdInDb()

def selectrowDb(key_id, db_name = './sqlite_python1.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = f"SELECT * FROM edit WHERE id = {key_id};"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    if conn: conn.close()
    return data
    
# Функция для получения id последней записи в БД
def lastIdInDb(db_name = './sqlite_python1.db'):
    conn = sqlite3.connect(db_name)
    query = '''
                SELECT id FROM edit
                ORDER BY id DESC
                LIMIT 1;
            '''
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    if len(data) == 0: return -1
    data = data[0][0]
    cursor.close()
    if conn: conn.close()
    return str(data)

# Тестирование
#d = ("Test company", "Ivanov Ivan Ivanovich", "Manager", "+71234567890", "+70123654789", "example@example.ru", "www.example.com")   
#createDb()
#insertDb(d)
#selectDb(1) 
#excelDb()
#print(lastIdInDb())
