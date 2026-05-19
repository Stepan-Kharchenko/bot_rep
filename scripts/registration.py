from vkbottle.bot import Message
from vkbottle import BaseStateGroup,Keyboard,Callback,Text,KeyboardButtonColor
from database.create_table import insert

colors = [KeyboardButtonColor.PRIMARY,
          KeyboardButtonColor.SECONDARY,
          KeyboardButtonColor.POSITIVE,
          KeyboardButtonColor.NEGATIVE
          ]

class Reg(BaseStateGroup):
    NAME = 0
    CLASS = 1
    PHYSIC = 2
    MATH = 3

kb = Keyboard(one_time=True)
for i in [9,10,11]:kb=kb.add(Text(str(i)),color=colors[0])
kb_class = kb.row().add(Text("Назад"),color=colors[1])
yes_or_no = (
    Keyboard(inline=True)
    .add(Text("Да"),color=colors[2])
    .add(Text("Нет"),color=colors[3])
    .row()
    .add(Text("Назад"),color=colors[1])
    )
    
def initialise(bot):
    @bot.on.message(state=Reg.NAME)
    async def reg_name(message: Message):
        l = message.text.split()
        if len(l) == 2:
            await bot.state_dispenser.set(message.peer_id,
                                          state=Reg.CLASS,
                                          first_name=l[0],
                                          last_name=l[1])
            await message.answer("Хорошо, укажите класс",
                                 keyboard=kb_class)
        elif l[0] == "Отмена":
            await bot.state_dispenser.delete(message.peer_id)
            return "До свидания"
        else:await message.answer("Что-то пошло не так")
        
    @bot.on.message(state=Reg.CLASS)
    async def reg_class(message: Message):
        if message.text=="Назад":
            await bot.state_dispenser.set(message.peer_id,state=Reg.NAME)
            await message.answer("Начнем. Введите Имя Фамилию через пробел",
                                 keyboard=kb.cancel)
        elif message.text in ('9','10','11'):
            state_data = await bot.state_dispenser.get(message.peer_id)
            await bot.state_dispenser.set(message.peer_id,
                                          state=Reg.PHYSIC,
                                          **state_data.payload,
                                          uclass = int(message.text))
            await message.answer("Хорошо, занимаетесь физикой?",
                                 keyboard=yes_or_no)
        else:await message.answer("Пожалуйста, пользуйтесь кнопками")
    @bot.on.message(state=Reg.PHYSIC)
    async def reg_ph(message: Message):
        state_data = await bot.state_dispenser.get(message.peer_id)
        d = state_data.payload
        if message.text=="Назад":
            del d["uclass"]
            await bot.state_dispenser.set(message.peer_id,
                                          state=Reg.CLASS,
                                          **d)
            await message.answer("Хорошо, укажите класс",
                                 keyboard=kb_class)
        elif message.text in ("Да","Нет"):
            await bot.state_dispenser.set(message.peer_id,
                                          state=Reg.MATH,
                                          **d,physic=(message.text=="Да")
                                          )
            await message.answer("Хорошо, а математикой?",
                                 keyboard=yes_or_no)
        else:await message.answer("Пожалуйста, пользуйтесь кнопками")
    @bot.on.message(state=Reg.MATH)
    async def reg_ma(message: Message):
        state_data = await bot.state_dispenser.get(message.peer_id)
        d = state_data.payload
        if message.text == "Назад":
            del d["physic"]
            await bot.state_dispenser.set(message.peer_id,
                                          state=Reg.CLASS,
                                          **d)
            await message.answer("Хорошо, занимаетесь физикой?",
                                 keyboard=yes_or_no)
        elif message.text in ("Да","Нет"):
            await bot.state_dispenser.delete(message.peer_id)
            insert("users",
                   ("id","first_name","last_name","class","physic","math"),
                   [[message.peer_id,
                     d["first_name"],
                     d["last_name"],
                     d["uclass"],
                     d["physic"],
                     message.text=="Да"
                     ]
                    ]
                   )
            return "Сохранено"
        else:await message.answer("Пожалуйста, пользуйтесь кнопками")
