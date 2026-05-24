import sqlite3
path = "database/learning.db"

with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM results WHERE 1 = 1")
    conn.commit()

def insert(table:str, columns:tuple, values:list):
    "вставляет в столбцы columns таблицы table все значения из двумерного массива values"
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        lenght,k = len(columns),0
        s = "("+",".join("?" for i in range(lenght))+")"
        for i in values:
            if len(i)!=lenght: raise Exception("Несовпадение количества значений и полей")
        command = f"""INSERT INTO {table} ({','.join(columns)})
    VALUES {',\n'.join(s for i in range(len(values)))};"""
        cursor.execute(command,[i for l in values for i in l])
        conn.commit()

def delete(table:str, ID:int):
    "удаляет запись под id ID"
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table} WHERE id = {ID}")
        conn.commit()

def select(table:str, condition:str="1 = 1", columns=tuple())->list:
    "выбирает все записи с условием condition"
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        if columns == tuple():
            cursor.execute(f"SELECT * FROM {table} WHERE {condition}")
        if columns != tuple():
            cursor.execute(f"SELECT {','.join(columns)} FROM {table} WHERE {condition}")
        l = cursor.fetchall()
    return l

def any_select(table:str, ID:int)->tuple:
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE id = {ID}")
        l = cursor.fetchone()
    return l

def selbst(s:str):
    "Ручное управление"
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute(s)
        if "SELECT" in s.upper():
            return "\n".join([str(i) for i in cursor.fetchall()])
        return "Готово"

def update(table:str, condition, new_value, column):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cond = f"id = {condition}" if type(condition) == int else condition
        cursor.execute(f"UPDATE {table} SET {column} = {new_value} WHERE {cond}")
        conn.commit()

def max_value(table:str, column:str, condition:str = "1 = 1"):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT MAX({column}) FROM {table} WHERE {condition}")
        value = cursor.fetchone()[0]
        return value if value!=None else 0