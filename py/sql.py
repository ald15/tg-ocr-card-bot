import sqlite3
import pandas as pd
import os

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
                    email text,
                    site text
                    );
                '''
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        if conn: conn.close()


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
                    site
                    ) VALUES (?, ?, ?, ?, ?, ?, ?);
            '''
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    if conn: conn.close()


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


def lastIdInDb(db_name = './sqlite_python.db'):
    conn = sqlite3.connect(db_name)
    query = '''
                SELECT id FROM cards
                ORDER BY id DESC
                LIMIT 1;
            '''
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()[0][0]
    cursor.close()
    if conn: conn.close()
    return str(data)


d = ("Roga & copita", "Ivanov Ivan Ivanovich", "Manager", "+71234567890", "+70123654789", "example@example.ru", "www.example.example")   
#createDb()
#insertDb(d)
#insertDb(d)
#insertDb(d)
#insertDb(d)
#insertDb(d)
#selectDb(1) 
#excelDb()
#print(lastIdInDb())
