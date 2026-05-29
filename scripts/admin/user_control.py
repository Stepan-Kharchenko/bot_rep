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
    ID = 0
    RIGHTS = 1
    DEL = 2
    TEST = 3
    TEST2 = 4

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
                match d["action"]:
                    case "Изменить права":
                        await bot.state_dispenser.set(message.peer_id,
                                                    Control.RIGHTS,
                                                    uid=uid)
                        await message.answer(f"{'Забрать' if uid in admin_ids else 'Дать'} права админа",
                                            keyboard=kb.yes)
                    case "Удалить ученика":
                        await bot.state_dispenser.set(message.peer_id,
                                                    state=Control.DEL,
                                                    uid=uid)
                        await message.answer("Вы действительно хотите удалить ученика?",
                                            keyboard=kb.yes)
                    case "Составить тест":
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
            if uid in admin_ids: s = " ".join(map(str,admin_ids)).replace(str(uid),"").replace("  "," ")
            else: s = " ".join(map(str,admin_ids))+" "+str(uid)
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
        await message.answer("Введите количество заданий по темам:",
                             keyboard=(kb.math_add_exersizes if message.text == "Математика" else kb.physic_add_exersizes))
        await bot.state_dispenser.set(message.peer_id,
                                      Control.TEST2,
                                      uid=uid,
                                      study=message.text)
    
    @bot.on.message(state=Control.TEST2)
    async def test2(message: Message):
        state_data = await bot.state_dispenser.get(message.peer_id)
        await bot.state_dispenser.delete(message.peer_id)
        d = state_data.payload
        await add_test(message,bot,d)

