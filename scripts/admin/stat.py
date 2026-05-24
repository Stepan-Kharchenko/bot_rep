from vkbottle import Bot,BaseStateGroup
from vkbottle.bot import Message

from database.create_table import *
import keyboards as kb
from utils import *

class Stat(BaseStateGroup):
    USER = 0
    EXERSIZE = 1
    ONE_STUDENT = 2
    ONE_EXERSIZE = 3
    END = 4

def stat_initialise(bot: Bot):
    @bot.on.message(state=Stat.USER)
    async def stat_user(message: Message):
        if message.text == "Отмена": await bot.state_dispenser.delete(message.peer_id)
        elif message.text == "Одного":
            await bot.state_dispenser.set(message.peer_id, state=Stat.ONE_STUDENT)
            return "Введите id ученика"
        elif message.text == "Всех":
            ids = [i for i in get_user_ids()]
            balls = (user_stat(i)[0] for i in ids)
            await message.answer(f"У вас {len(ids)} учеников, среди них средний балл - {sum(balls)/len(ids)}")
            l = select("users","1 = 1")
            s = "Ваши ученики:\n"
            for i in l:
                s += f"id - {i[0]}. {i[1]} {i[2]}, {i[3]} класс. \
{"Физика и математика" if i[4] and i[5] else ("Физика" if i[4] else "Математика")}. \
Учится {user_stat(i[0])[1]}\n"
            await message.answer(s)
        else:await message.answer("Пожалуйста, пользуйтесь кнопками")
        
    @bot.on.message(state=Stat.EXERSIZE)
    async def stat_ex(message: Message):
        await bot.state_dispenser.delete(message.peer_id)
        if message.text == "Отмена": return "До свидания"
        else:
            try:
                l,s = select("study",f"id = {int(message.text)}"),""
                for i in l:
                    s += f'Задание {i[0]}. "{i[4]}", Ответ - {i[5]}. Средний балл выполнения - {exersize_stat(i[0])}%\n'
                return s 
            except ValueError: return "Вводите только число - id задания"

    @bot.on.message(state=Stat.ONE_STUDENT)
    async def stat_one_user(message: Message):
        await bot.state_dispenser.delete(message.peer_id)
        try:
            uid = int(message.text)
            if (uid,) in select("users","1 = 1",("id",)):
                await message.answer(f"У ученика {int(user_stat(uid)[0])}% выполненных заданий. Учится {user_stat(uid)[1]}")
            else: raise ValueError
        except ValueError: await message.answer("Неправильно введен id или его нет в списках")
    

            
