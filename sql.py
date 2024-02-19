import sqlite3
import pandas as pd

def createDb(db_name = 'sqlite_python.db'):
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


def insertDb(data, db_name = 'sqlite_python.db'):
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


def selectDb(p = 0, db_name = 'sqlite_python.db'):
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
    

def excelDb(out_file = "out.xlsx", db_name = 'sqlite_python.db'):
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

    
#createDb()
#insertDb(d1)
#selectDb() 
#excelDb()
