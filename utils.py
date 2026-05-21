from vkbottle.bot import Message
from database.create_table import *

from dotenv import load_dotenv
import os
load_dotenv("secret.env")
admin_ids = list(map(int,os.getenv("admin").split()))

import datetime as dt
from collections import defaultdict

def validate(message: Message)->bool:
    return message.peer_id in admin_ids

def user_stat(uid:int)->tuple:
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT AVG(ball) FROM results WHERE user_id = {uid} AND ball != -1")
        try: ball = cursor.fetchone()[0]*100
        except TypeError: ball = 0
        cursor.execute(f"SELECT crated_at FROM users WHERE id = {uid}")
        date = cursor.fetchone()[0].split("-")
        date_created_at = dt.date(int(date[0]),int(date[1]),int(date[2]))
        date_now = dt.date.today()
        time_in_learning = str(date_now - date_created_at).split(",")[0]
    return ball,time_in_learning

def get_user_ids():
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users")
        for i in cursor.fetchall(): yield i[0]

def exersize_stat(eid:int)->int:
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT AVG(ball) FROM results WHERE exersize_id = {eid} AND ball != -1")
        try: ball = cursor.fetchone()[0]*100
        except TypeError: ball = 0
        return int(ball)
    
def validate_theme(d:dict, message:Message)->bool:
    return (d["stud"] == "Математика" and message.text in ("Алгебра","Геометрия","Вероятность и Статистика"))\
        or (d["stud"] == "Физика" and message.text in ("Механика","МКТ и Термоденамика","Электромагнетизм","Квантовая"))
    
def add_exersizes_in_test(theme:str, add:bool, d:defaultdict)->dict:
    d[theme] += (1 if add else (-1 if d[theme]>0 else 0))
    return d

flag_for_test,ut_dct = False,{}
def end_of_test(d:defaultdict):
    global flag_for_test,ut_dct
    flag_for_test = True
    ut_dct = d
    
def became_dict():
    return dict(ut_dct)
    
