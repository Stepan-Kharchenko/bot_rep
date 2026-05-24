from vkbottle import Keyboard,Callback,Text
from vkbottle import KeyboardButtonColor

ver = "Вероятность и Статистика"
physic_themes_list = (("Механика","ME"),("МКТ и Тд","MK"),
                      ("Электромагнетизм","EL"),("Квантовая","KV"))
math_themes_list = (("Алгебра","AL"),("Геометрия","GE"),(ver,"VE"))

colors = [KeyboardButtonColor.PRIMARY,
          KeyboardButtonColor.SECONDARY,
          KeyboardButtonColor.POSITIVE,
          KeyboardButtonColor.NEGATIVE
          ]

commands = (
    Keyboard(inline=True)
    .add(Text("/start"),color=colors[0])
    .add(Text("/help"),color=colors[0])
    .add(Text("/statistic"),color=colors[0])
    .row()
    .add(Text("/test"),color=colors[2])
    .add(Text("/admin"),color=colors[3])
    )
    
not_reg = (
    Keyboard(inline=True)
    .add(Callback("Да",payload={"reg":True}),color=colors[2])
    .add(Callback("Нет",payload={"reg":False}),color=colors[3])
    )

cancel = (
    Keyboard(one_time=True)
    .add(Text("Отмена"),color=colors[3])
    )

in_reg = (
    Keyboard(inline=True)
    .add(Callback("Удалить данные",payload={"in_reg":"delete"}),color=colors[3])
    .add(Callback("Решить тест",payload={"in_reg":"test"}),color=colors[0])
    .add(Text("Отмена"),color=colors[1])
    )

yes_no = (
    Keyboard(inline=True)
    .add(Callback("Да",payload={"del":True}),color=colors[3])
    .add(Callback("Нет",payload={"del":False}),color=colors[2])
    )

helpk = Keyboard(one_time=True).add(Text("/help"),color=colors[0])

admin = (
    Keyboard(one_time=True)
    .add(Text("Добавить задание"),color=colors[0])
    .add(Text("Посмотреть статистику"),color=colors[0])
    .row()
    .add(Text("Управление учениками"),color=colors[0])
    )

phys_or_math = (
    Keyboard(inline=True)
    .add(Text("Физика"),color=colors[0])
    .add(Text("Математика"),color=colors[0])
    .row()
    .add(Text("Отмена"),color=colors[3])
    )

stat_types = (
    Keyboard(inline=True)
    .add(Text("Статистику ученика"),color=colors[0])
    .add(Text("Статистику задания"),color=colors[0])
    .row()
    .add(Text("Отмена"),color=colors[3])
    )

one_or_more = (
    Keyboard(inline=True)
    .add(Text("Одного"),color=colors[0])
    .add(Text("Всех"),color=colors[0])
    .row()
    .add(Text("Отмена"),color=colors[3])
    )

physic_themes = (
    Keyboard(one_time=True)
    .add(Text("Механика"),color=colors[0])
    .add(Text("МКТ и Термодинамика"),color=colors[0])
    .row()
    .add(Text("Электромагнетизм"),color=colors[0])
    .add(Text("Квантовая"),color=colors[0])
    .row()
    .add(Text("Отмена"),color=colors[3])
)

math_themes = (
    Keyboard(one_time=True)
    .add(Text("Алгебра"),color=colors[0])
    .add(Text("Геометрия"),color=colors[0])
    .add(Text("Вероятность и Cтатистика"),color=colors[0])
    .row()
    .add(Text("Отмена"),color=colors[3])
)

yes = Keyboard(inline=True).add(Text("Да"),color=colors[2]).add(Text("Нет"),color=colors[3])

physic_add_exersizes = Keyboard()
math_add_exersizes = Keyboard()
for th,ab in physic_themes_list:
    physic_add_exersizes = physic_add_exersizes.add(Callback("-",payload={ab:False}),color=colors[3])
    physic_add_exersizes = physic_add_exersizes.add(Callback(th,payload={ab:None}))
    physic_add_exersizes = physic_add_exersizes.add(Callback("+",payload={ab:True}),color=colors[2]).row()
for th,ab in math_themes_list:
    math_add_exersizes = math_add_exersizes.add(Callback("-",payload={ab:False}),color=colors[3])
    math_add_exersizes = math_add_exersizes.add(Callback(th,payload={ab:None}))
    math_add_exersizes = math_add_exersizes.add(Callback("+",payload={ab:True}),color=colors[2]).row()
physic_add_exersizes = physic_add_exersizes.add(Callback("Конец",payload={ab:None}),color=colors[0])
math_add_exersizes = math_add_exersizes.add(Callback("Конец",payload={ab:None}),color=colors[0])