from vkbottle import Bot, BaseStateGroup
from vkbottle.bot import Message

from database.create_table import *
import keyboards as kb
import utils as ut


class Test(BaseStateGroup):
    INITTEST = 0
    TEST = 1
    TEST1 = 2
    TEST2 = 3
    END = 4

def initialise(bot: Bot):
    @bot.on.message(state=Test.INITTEST)
    async def init(message: Message):
        match message.text:
            case "Отмена": await bot.state_dispenser.delete(message.peer_id)
            case "Физика" | "Математика":
                async def foo(message:Message, bot:Bot):
                    await bot.state_dispenser.set(message.peer_id,
                                                Test.TEST,
                                                tid=test_ids,
                                                eid=ex_ids)
                    await message.answer(mess, keyboard=kb.yes)
                def get_l(): return [i for i in select("results",f"ball = -1 AND user_id = {message.peer_id}",("id","exersize_id"))]
                l = get_l()
                if not l:
                    await ut.add_test(message,bot,{"uid":message.peer_id,
                                                "study":message.text})
                    mess = "Для вас нет теста, сейчас он сгенерируется, приступить к выполнению?"
                else: mess = "Для вас есть составленный тест, приступить к выполнению?"
                l = get_l()
                test_ids, ex_ids = [i[0] for i in l], [i[1] for i in l]
                await foo(message,bot)
            case _: await message.answer("Пожалуйста, пользуйтесь кнопками")
    
    @bot.on.message(state=Test.TEST)
    async def test(message: Message):
        match message.text:
            case "Нет":
                bot.state_dispenser.delete(message.peer_id)
                return "До свидания"
            case "Да":
                d = (await bot.state_dispenser.get(message.peer_id)).payload
                await bot.state_dispenser.set(message.peer_id,
                                            state=Test.TEST1,
                                            **d,
                                            counter=0)
                await message.answer(any_select("study",d["eid"][0])[4],keyboard=kb.cancel)
            case _: await message.answer("Пожалуйста, пользуйтесь кнопками")

    @bot.on.message(state=Test.TEST1)
    async def test1(message: Message):
        if message.text == "Отмена": await bot.state_dispenser.delete(message.peer_id)
        else:
            d = (await bot.state_dispenser.get(message.peer_id)).payload
            if "answers" not in d:
                await bot.state_dispenser.set(message.peer_id,
                                              state=Test.TEST2,
                                              eid=d["eid"],
                                              tid=d["tid"],
                                              counter=1,
                                              answers=[message.text])
                await message.answer(any_select("study",d["eid"][1])[4],keyboard=kb.cancel)
            else:
                counter=d["counter"]+1
                answers = d["answers"]+[message.text]
                if counter == len(d["eid"]):
                    await bot.state_dispenser.set(message.peer_id,
                                                state=Test.END,
                                                tid=d["tid"],
                                                eid=d["eid"],
                                                answers=answers)
                    await message.answer("Вы хотите завершить тест?",keyboard=kb.yes)
                else:
                    await bot.state_dispenser.set(message.peer_id,
                                                state=Test.TEST2,
                                                eid=d["eid"],
                                                tid=d["tid"],
                                                counter=counter,
                                                answers=answers)
                    await message.answer(any_select("study",d["eid"][counter])[4],keyboard=kb.cancel)

    @bot.on.message(state=Test.TEST2)
    async def test2(message: Message):
        if message.text == "Отмена":
            await bot.state_dispenser.delete(message.peer_id)
            return "До свидания"
        else:
            d = (await bot.state_dispenser.get(message.peer_id)).payload
            counter=d["counter"]+1
            answers = d["answers"]+[message.text]
            if counter == len(d["eid"]):
                await bot.state_dispenser.set(message.peer_id,
                                              state=Test.END,
                                              tid=d["tid"],
                                              eid=d["eid"],
                                              answers=answers)
                await message.answer("Вы хотите завершить тест?",keyboard=kb.yes)
            else:
                await bot.state_dispenser.set(message.peer_id,
                                            state=Test.TEST1,
                                            eid=d["eid"],
                                            tid=d["tid"],
                                            counter=counter,
                                            answers=answers)
                await message.answer(any_select("study",d["eid"][counter])[4],keyboard=kb.cancel)

    @bot.on.message(state=Test.END)
    async def end(message: Message):
        d = (await bot.state_dispenser.get(message.peer_id)).payload
        await bot.state_dispenser.delete(message.peer_id)
        answers = d["answers"]
        print(d["eid"])
        print(d["tid"])
        match message.text:
            case"Да":
                true_answers = [any_select("study",i)[5] for i in d["eid"]]
                for i in range(len(d["eid"])):
                    t,a,ta = d["tid"][i],answers[i],true_answers[i]
                    update("results", t, int(a==ta), "ball")
                ball = sum(true_answers[i]==answers[i] for i in range(len(true_answers)))
                await message.answer(f"У вас {ball} правильных ответов")
            case "Нет":
                for i in d["tid"]:
                    update("results",i,-1)
                return "До свидания"
            case _: return "Пожалуйста, пользуйтесь кнопками"

    


        