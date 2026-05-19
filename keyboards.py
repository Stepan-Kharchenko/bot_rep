from vkbottle import Keyboard,Callback,Text
from vkbottle import KeyboardButtonColor

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
    Keyboard(one_time=False)
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

yes = Keyboard(inline=True).add(Text("Да"),color=colors[2]).add(Text("Нет"),color=colors[3])