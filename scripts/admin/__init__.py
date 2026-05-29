from vkbottle import Bot,BaseStateGroup,Keyboard,Text
from keyboards import colors
import keyboards as kb
from vkbottle.bot import Message

from .add import *
from .stat import *
from .user_control import *
from utils import *
from database.create_table import select

class Admin(BaseStateGroup):
    START = 0
    ADDEX = 1
    STAT = 2
    USERS = 3

def adm_initialise(bot: Bot):
    @bot.on.message(state=Admin.START)
    async def start(message: Message):
        match message.text:
            case "Добавить задание":
                await bot.state_dispenser.set(message.peer_id,
                                            state=Admin.ADDEX
                                            )
                await message.answer("Вы хотите добавить задание по физике или по математике?",
                                    keyboard=kb.phys_or_math
                                    )
            case "Посмотреть статистику":
                await bot.state_dispenser.set(message.peer_id,
                                            state=Admin.STAT
                                            )
                await message.answer("Что вы хотите посмотреть?",keyboard=kb.stat_types)
            case "Управление учениками":
                await bot.state_dispenser.set(message.peer_id,
                                            state=Admin.USERS
                                            )
                await message.answer("Выберите действие",keyboard=(
                    Keyboard(inline=True)
                    .add(Text("Изменить права"),color=colors[0])
                    .add(Text("Удалить ученика"),color=colors[0])
                    .add(Text("Составить тест"),color=colors[0])
                    .row()
                    .add(Text("Отмена"),color=colors[3])
                    )
                                    )
            case _: await message.answer("Пожалуйста, пользуйтесь кнопками")

    @bot.on.message(state=Admin.ADDEX)
    async def addex(message: Message):
        match message.text:
            case "Отмена":
                await bot.state_dispenser.delete(message.peer_id)
            case "Физика" | "Математика":
                await bot.state_dispenser.set(message.peer_id,
                                            state=add.AddEx.NUMBER,
                                            stud=message.text
                                            )
                await message.answer("Выберите тему задания",
                                    keyboard=(kb.physic_themes if message.text == "Физика" else kb.math_themes))
            case _: await message.answer("Пожалуйста, пользуйтесь кнопками")

    @bot.on.message(state=Admin.STAT)
    async def statistic(message: Message):
        match message.text:
            case "Отмена":
                await bot.state_dispenser.delete(message.peer_id)
                return "До свидания"
            case "Статистику ученика":
                await bot.state_dispenser.set(message.peer_id,
                                            state=stat.Stat.USER
                                            )
                await message.answer("Одного или всех?",keyboard=kb.one_or_more)
            case "Статистику задания":
                await bot.state_dispenser.set(message.peer_id,
                                            state=stat.Stat.EXERSIZE
                                            )
                await message.answer("""Данные указаны в формате (id задания, задание, ответ, класс).
Укажите id задания.
Ваши задания по математике:\n"""+"\n".join(str(i) for i in select("study",
                                                                    'math = 1',
                                                                    ("id","exersize","answer","class")))+\
"\nВаши задания по физике:\n"+"\n".join(str(i) for i in select("study",
                                            'math = 0',
                                            ("id","exersize","answer","class"))),
                                    keyboard=kb.cancel)
            case _: return "Пожалуйста, пользуйтесь кнопками"

    @bot.on.message(state=Admin.USERS)
    async def ucontrol(message: Message):
        match message.text:
            case "Отмена":
                await bot.state_dispenser.delete(message.peer_id)
            case "Изменить права" | "Удалить ученика" | "Составить тест":
                await bot.state_dispenser.set(message.peer_id,
                                            state=user_control.Control.ID,
                                            action=message.text
                                            )
                await message.answer("Введите id ученика",keyboard=kb.cancel)
            case _: await message.answer("Пожалуйста, пользуйтесь кнопками")

    add_initialise(bot)
    stat_initialise(bot)
    control_initialise(bot)
