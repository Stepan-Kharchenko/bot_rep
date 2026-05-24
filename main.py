from vkbottle import Bot,GroupEventType,Keyboard,Text
from vkbottle.bot import Message,MessageEvent

import keyboards as kb
from database.create_table import *
import scripts
import utils as ut
import images.img as img

from dotenv import load_dotenv
import os
load_dotenv("secret.env")
TOKEN = os.getenv("VK_TOKEN")
admin_ids = list(map(int,os.getenv("admin").split()))
bot = Bot(token=TOKEN)

dct = ut.defaultdict(int)

@bot.on.message(text=["/start","Начать"])
async def start(message: Message):
    string = select("users",f"id = {message.peer_id}")
    if string == []:
        await message.answer("Вы не зарегестрированы, хотите зарегестрироваться?",
                             keyboard=kb.not_reg)
    else:
        l = string[0]
        await message.answer(f"""Вы зарегестрированы, ваши данные:
Вас зовут {l[1]} {l[2]}, вы в {l[3]} классе, занимаетесь {l[4]*'физикой'} {l[5]*'и математикой'}.
Что хотите?
""",keyboard=kb.in_reg)
    #await message.answer(attachment = await img.send_photo("Котик",bot)) - картинка

@bot.on.message(text=["Отмена","/help"])
async def cancel(message: Message):
    await message.answer("""Список команд:
/start - регистрация
/help - помощь
/test - решить тест
/statistic - узнать статистику
/admin - админ панель
""",keyboard=kb.commands)

@bot.on.message(command="test")
async def test(message: Message):
    await bot.state_dispenser.set(message.peer_id,
                                  state=scripts.test.Test.INITTEST)
    await message.answer("Вы хотите пройти тест по физике или по математике?",keyboard=kb.phys_or_math)

@bot.on.message(command="statistic")
async def stat(message: Message):
    await message.answer(f"""{int(ut.user_stat(message.peer_id)[0])}% выполненных заданий.
Учится {ut.user_stat(message.peer_id)[1]}""")

@bot.on.message(command="admin")
async def admin(message: Message):
    if ut.validate(message):
        await bot.state_dispenser.set(message.peer_id,
                                      state=scripts.admin.Admin.START)
        await message.answer("Доступ разрешён",keyboard=kb.admin)
    else:await message.answer("Доступ запрещен - вы не админ")

scripts.bot_initialise(bot)       
        
@bot.on.raw_event(GroupEventType.MESSAGE_EVENT,dataclass=MessageEvent)
async def callback(event: MessageEvent):
    if "reg" in event.payload:
        if event.payload["reg"]:
            await bot.state_dispenser.set(event.peer_id,
                                          state=scripts.reg.Reg.NAME)
            await event.send_message("Начнем. Введите Имя Фамилию через пробел",
                                     keyboard=kb.cancel)
            s = "Начнем"
        else:s="До свидания"
        await event.show_snackbar(s)
    if "in_reg" in event.payload:
        if event.payload["in_reg"] == "delete":
            await event.send_message("Вы уверены?",keyboard=kb.yes_no)
            await event.show_snackbar("Вы уверены?")
    if "del" in event.payload:
        if event.payload["del"]:
            delete("users",event.peer_id)
            await event.send_message("Ваша запись удалена")
        else:
            await event.send_message("Добро пожаловать, нажмите /help",
                                     keyboard=kb.helpk
                                     )
        await event.show_snackbar("До свидания")
    if tuple(event.payload.keys())[0] in (i[1] for i in kb.physic_themes_list+kb.math_themes_list):
        global dct
        if tuple(event.payload.values())[0] == None:
            ut.end_of_test(dct)
            await event.send_message("Завершите добавление",keyboard=Keyboard(one_time=True).add(Text("Закончить")))
            await event.show_snackbar("Сохранено")
            dct = ut.defaultdict(int)
        else:
            dct = ut.add_exersizes_in_test(tuple(event.payload.keys())[0],tuple(event.payload.values())[0],dct)
            await event.show_snackbar("Добавлено" if tuple(event.payload.values())[0] else "Убрано")

@bot.on.message()
async def random(message: Message):
    if "SQL" in message.text.split("\n")[0].upper():
        l = message.text.split("\n")[1:]
        await message.answer(selbst("\n".join(l)))
    else:await message.answer("Добро пожаловать, нажмите /help",keyboard=kb.helpk)


if __name__ == "__main__":
    print("run")
    bot.run_forever()
