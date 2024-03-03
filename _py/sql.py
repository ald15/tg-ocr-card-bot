import os
import sqlite3
import pandas as pd

# Процедура создания БД
def createDb(db_name = './sqlite_python.db'):
    if not os.path.isfile(db_name):
        conn = sqlite3.connect(db_name)
        query = '''
                    CREATE TABLE cards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT,
                    name TEXT,
                    post TEXT,
                    tel1 TEXT,
                    tel2 TEXT,
                    email TEXT,
                    site TEXT,
                    comment TEXT
                    );
                '''
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        if conn: conn.close()


# Процедура добавления данных в БД
def insertDb(data, db_name = './sqlite_python.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query  = '''
                INSERT INTO cards (
                    company,
                    name,
                    post,
                    tel1,
                    tel2,
                    email,
                    site,
                    comment
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            '''
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    if conn: conn.close()

# Процедура обновления данных в БД
def updateDb(key, val, column, db_name = './sqlite_python.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query  = f'''
                UPDATE cards
                    SET {column} = ?
                    WHERE id = ?;
            '''
    data = (val, key)
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    if conn: conn.close()


# Функция получения данных из БД
def selectDb(p = 0, db_name = './sqlite_python.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = "SELECT * FROM cards"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    if conn: conn.close()
    if p:
        for row in data: print(data)
    return data
    if conn: conn.close()
    

# Процедура преобразования данных в .xlsx
def excelDb(out_file = "./out.xlsx", db_name = './sqlite_python.db'):
    d = {
            "id": [],
            "Компания": [],
            "ФИО": [],
            "Должность": [],
            "Тел. №1": [],
            "Тел. №2": [],
            "E-mail": [],
            "Сайт": [],
            "Комментарий": []
        }
    data = selectDb(0, db_name)
    temp_data = [[] for i in range(len(d.keys()))]
    for row in data:
        i = 0
        for key in d.keys():
            d[key].append(row[i])
            i += 1
    df = pd.DataFrame(d)
    df.to_excel(out_file)


# Функция для получения id последней записи в БД
def lastIdInDb(db_name = './sqlite_python.db'):
    conn = sqlite3.connect(db_name)
    query = '''
                SELECT id FROM cards
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
