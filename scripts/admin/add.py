from vkbottle import Bot,BaseStateGroup
from vkbottle.bot import Message

from database.create_table import *
import keyboards as kb

class AddEx(BaseStateGroup):
    NUMBER = 0
    TEXT = 1
    ANSWER = 2

def add_initialise(bot: Bot):
    @bot.on.message(state=AddEx.NUMBER)
    async def addexnum(message: Message):
        if message.text == "Отмена":await bot.state_dispenser.delete(message.peer_id)
        else:
            state_data = await bot.state_dispenser.get(message.peer_id)
            d = state_data.payload
            try:
                n = int(message.text.strip())
                if d["stud"] == "Математика" and 1<=n<=19\
                   or d["stud"] == "Физика" and 1<=n<=26:
                    l = select("study",
                               f"math = {d['stud']=='Математика'} AND number = {int(message.text)}"
                               )
                    ind = 0 if l == [] else l[-1][3]+1
                    await bot.state_dispenser.set(message.peer_id,
                                                  state=AddEx.TEXT,
                                                  **d,
                                                  number=n,
                                                  index = ind
                                                  )
                    await message.answer("Введите текст задания",
                                         keyboard=kb.cancel
                                         )
                else:raise ValueError("Не тот формат")
            except ValueError as e:await message.answer(e,keyboard=kb.cancel)

    @bot.on.message(state=AddEx.TEXT)
    async def addexind(message: Message):
        state_data = await bot.state_dispenser.get(message.peer_id)
        d = state_data.payload
        if message.text == "Отмена":await bot.state_dispenser.delete(message.peer_id)
        else:
            await bot.state_dispenser.set(message.peer_id,
                                          state=AddEx.ANSWER,
                                          **d,
                                          text=message.text
                                          )
            await message.answer("Ответ?",keyboard=kb.cancel)

    @bot.on.message(state=AddEx.ANSWER)
    async def answer(message: Message):
        state_data = await bot.state_dispenser.get(message.peer_id)
        d = state_data.payload
        await bot.state_dispenser.delete(message.peer_id)
        d["answer"]=message.text
        insert("study",
               ("math","number","ind","answer","exersize","ball"),
               [(d["stud"]=="Математика",d["number"],d["index"],d["answer"],d["text"],2)]
               )
        await message.answer("Сохранено")
                                          
        
            
                
            
