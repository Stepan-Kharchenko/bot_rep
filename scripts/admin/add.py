from vkbottle import Bot,BaseStateGroup
from vkbottle.bot import Message

from database.create_table import *
import keyboards as kb
import utils as ut
from ..registration import kb_class

class AddEx(BaseStateGroup):
    NUMBER = 0
    TEXT = 1
    ANSWER = 2
    CLASS = 3

def add_initialise(bot: Bot):
    @bot.on.message(state=AddEx.NUMBER)
    async def addexnum(message: Message):
        if message.text == "Отмена": await bot.state_dispenser.delete(message.peer_id)
        else:
            state_data = await bot.state_dispenser.get(message.peer_id)
            d = state_data.payload
            if ut.validate_theme(d,message):
                await bot.state_dispenser.set(message.peer_id,
                                              state=AddEx.TEXT,
                                              theme=message.text)
                await message.answer("Пожалуйста, введите текст задания", keyboard=kb.cancel)
            else: await message.answer("Пожалуйста, пользуйтесь кнопками")

    @bot.on.message(state=AddEx.TEXT)
    async def addexind(message: Message):
        state_data = await bot.state_dispenser.get(message.peer_id)
        d = state_data.payload
        if message.text == "Отмена": await bot.state_dispenser.delete(message.peer_id)
        else:
            await bot.state_dispenser.set(message.peer_id,
                                          state=AddEx.ANSWER,
                                          **d,
                                          text=message.text)
            await message.answer("Пожалуйста, введите ответ",keyboard=kb.cancel)

    @bot.on.message(state=AddEx.ANSWER)
    async def answer(message: Message):
        if message.text == "Отмена": await bot.state_dispenser.delete(message.peer_id)
        else:
            state_data = await bot.state_dispenser.get(message.peer_id)
            d = state_data.payload
            await bot.state_dispenser.set(message.peer_id,
                                          state=AddEx.CLASS,
                                          **d,
                                          answer=message.text)
            await message.answer("Введите класс/курс",keyboard=kb_class)
            
    @bot.on.message(state=AddEx.CLASS)
    async def aeclass(message: Message):
        state_data = await bot.state_dispenser.get(message.peer_id)
        d = state_data.payload
        await bot.state_dispenser.delete(message.peer_id)
        try:
            class_ = int(message.text)
            if not ((class_ in range(9,12)) or (class_ in range(1,6))): raise ValueError
            math = d["theme"] in ("Алгебра","Геометрия","Вероятность и Статистика")
            l = select("study", f"theme = '{d['theme']}'", ("ind",))
            index = l[-1][0] if l else 0
            insert("study",
                   ("math","theme","ind","exersize","answer","class"),
                   [(math,d["theme"],index+1,d["text"],d["answer"],message.text)])
            await message.answer("Сохранено")
        except ValueError: return "Пожалуйста, пользуйтесь кнопками"
                                          
        
            
                
            
