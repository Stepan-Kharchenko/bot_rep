from vkbottle import Bot,BaseStateGroup
from vkbottle.bot import Message
import random as r
from dotenv import set_key,load_dotenv
import os
load_dotenv("secret.env")
admin_ids = list(map(int,os.getenv("admin").split()))

from database.create_table import *
import keyboards as kb
from utils import *

path = "secret.env"

class Control(BaseStateGroup):
    ID = 100
    RIGHTS = 101
    DEL = 102
    TEST = 103
    TEST2 = 104

def control_initialise(bot: Bot):
    @bot.on.message(state=Control.ID)
    async def user_id(message: Message):
        if message.text == "Отмена": 
            await bot.state_dispenser.delete(message.peer_id)
            return "До свидания"
        try:
            uid = int(message.text.strip())
            state_data = await bot.state_dispenser.get(message.peer_id)
            d = state_data.payload
            if (uid,) in select("users","1 = 1",("id",)):
                if d["action"] == "Изменить права":
                    await bot.state_dispenser.set(message.peer_id,
                                                  Control.RIGHTS,
                                                  uid=uid)
                    await message.answer(f"{'Забрать' if uid in admin_ids else 'Дать'} права админа",
                                        keyboard=kb.yes)
                elif d["action"] == "Удалить ученика":
                    await bot.state_dispenser.set(message.peer_id,
                                                  state=Control.DEL,
                                                  uid=uid)
                    await message.answer("Вы действительно хотите удалить ученика?",
                                         keyboard=kb.yes)
                elif d["action"] == "Составить тест":
                    await bot.state_dispenser.set(message.peer_id,
                                                  state=Control.TEST,
                                                  uid=uid)
                    await message.answer("По физике или по математике?",
                                         keyboard=kb.phys_or_math)
            else: raise ValueError("no id in table")
        except ValueError as e: await message.answer("Нет такого ID или он введен неверно")

    @bot.on.message(state=Control.RIGHTS)
    async def rights(message: Message):
        state_data = await bot.state_dispenser.get(message.peer_id)
        uid = state_data.payload["uid"]
        await bot.state_dispenser.delete(message.peer_id)
        if message.text == "Да":
            if uid == message.peer_id: return "Вы не можете лишить себя прав админа"
            if uid in admin_ids:s = " ".join(map(str,admin_ids)).replace(str(uid),"").replace("  "," ")
            else:s = " ".join(map(str,admin_ids))+" "+str(uid)
        with open("secret.env") as f:
            olds = "\n".join(i for i in f)
        with open("secret.env", "w") as f:
            for i in olds.split("\n"):
                if "admin" in i:f.write('admin="'+s+'"\n')
                else:f.write(i+"\n")
    
    @bot.on.message(state=Control.DEL)
    async def udelete(message: Message):
        state_data = await bot.state_dispenser.get(message.peer_id)
        await bot.state_dispenser.delete(message.peer_id)
        uid = state_data.payload["uid"]
        if message.text == "Да":
            if (uid,) in select("users","1 = 1",("id",)):
                delete("users",uid)
                return "В базе данных нет такого ученика"
            else: return "В базе данных нет такого ученика"

    @bot.on.message(state=Control.TEST)
    async def test1(message: Message):
        state_data = await bot.state_dispenser.get(message.peer_id)
        uid = state_data.payload["uid"]
        await message.answer("Введите количество заданий по темам:",keyboard=kb.physic_add_exersizes)
        #while not flag_for_test: pass
        await bot.state_dispenser.set(message.peer_id,
                                      Control.TEST2,
                                      uid=uid,
                                      study=message.text)
    
    @bot.on.message(state=Control.TEST2)
    async def test2(message: Message):
        state_data = await bot.state_dispenser.get(message.peer_id)
        d = state_data.payload
        d["dct"] = became_dict()
        print(d)
        #l = tuple(map(int,message.text.split())) if message.text.strip() != "0" else \
        #    (i for i in range(1,(20 if message.text == 'math' else 27)))
        #exl = []
        #print(l)
        #for i in l:
        #    variants = select("study",f"math = {d['study'] == 'Математика'} AND number = {i}")
        #    exl.append(r.choice(variants))
        #try: variant = max(i[4] for i in select("results",f"id = {d['uid']}"))+1
        #except ValueError:
        #    variant = 1
        #insert("results",
        #       ("user_id","exersize_id","var","ball"),
        #       [(d["uid"],i[0],variant,-1) for i in exl])