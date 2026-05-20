from vkbottle import Bot,BaseStateGroup
from vkbottle.bot import Message

from database.create_table import *
import keyboards as kb
import utils as ut

class AddEx(BaseStateGroup):
    NUMBER = 0
    TEXT = 1
    ANSWER = 2

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
        state_data = await bot.state_dispenser.get(message.peer_id)
        d = state_data.payload
        await bot.state_dispenser.delete(message.peer_id)
        if message.text != "Отмена":
            math = d["theme"] in ("Алгебра","Геометрия","Вероятность и Статистика")
            l = select("study", f"theme = '{d['theme']}'", ("ind",))
            index = l[-1][0] if l else 0
            insert("study",
                   ("math","theme","ind","exersize","answer"),
                   [(math,d["theme"],index+1,d["text"],message.text)])
            await message.answer("Сохранено")
                                          
        
            
                
            
