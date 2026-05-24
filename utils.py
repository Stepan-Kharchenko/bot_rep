from vkbottle.bot import Message
from vkbottle import Bot
import random as r

from database.create_table import *
import keyboards as kb

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
        cursor.execute(f"SELECT created_at FROM users WHERE id = {uid}")
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
    return (d["stud"] == "Математика" and message.text.strip() in ("Алгебра","Геометрия",kb.ver))\
        or (d["stud"] == "Физика" and message.text.strip() in ("Механика","МКТ и Термоденамика","Электромагнетизм","Квантовая"))
    
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

async def add_test(message:Message, bot:Bot, d:dict):
    if message.text in ("Физика","Математика"):
        ut_dct = {ab:1 for th,ab in (kb.math_themes_list if message.text == "Математика" else kb.physic_themes_list)}
        d["dct"] = ut_dct
    else: d["dct"] = became_dict()
    print(d["dct"])
    math = any(i == j for i in d["dct"] for j in ("AL","GE","VE"))
    var,uclass = max_value("results","var",f"user_id = {d['uid']}"),any_select("users",d["uid"])[3]
    stud_themes_list = kb.math_themes_list if math else kb.physic_themes_list   #dict_of_themes: {тема(полностью):кортеж id-шек}
    dict_of_themes = {i[0]:list(j[0] for j in select("study",
                                                     f'theme = "{i[0]}" AND class = {uclass}',
                                                     ("id",))) for i in stud_themes_list}
    dict_of_themes_names = {i[1]:i[0] for i in stud_themes_list}   #dict_of_themes_names: {тема(аббревиатура):тема(полностью)}
    exemples = []
    print(dict_of_themes,dict_of_themes_names,sep="\n")
    try:
        for i in d["dct"]:#темы (сокращённо)
            for j in range(d["dct"][i]):#нужное кол-во тем
                ind = r.randint(0,len(dict_of_themes[dict_of_themes_names[i]])-1)
                exemples.append(dict_of_themes[dict_of_themes_names[i]][ind])
                del dict_of_themes[dict_of_themes_names[i]][ind]
        insert("results",("user_id","exersize_id","var","ball"),
               [(d["uid"],i,var+1,-1) for i in exemples])
        return "Вариант составлен"
    except IndexError: return "Не хватает заданий в базе данных"
    
