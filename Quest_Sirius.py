import random
from datetime import datetime

import aiogram.utils.exceptions
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile

import AIP_Sirius_School_of_Magic
from db import Database
from keybords import *

responses = ['🐙Да, да.', '🐙Прювет', "🐙Как ты там?", '🐙Кто выпил весь ром!', "🐙На абордаж", "🐙Ну чего тебе?",
             '🐙Как долго ты готов(а) со мной общаться?', "🐙А это забавно."]
db = Database("2.db")
bot = Bot(token=AIP_Sirius_School_of_Magic.TELEGRAM_BOT)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db.create_table_users()
ADMIN_IDS = [1219523153, 6522187160]


class AdminState(StatesGroup):
    select_user = State()
    change_user_state = State()


class InputWhatever(StatesGroup):
    School_of_Magic_1 = State()
    School_of_Magic_Pay = State()
    School_of_Magic_2 = State()
    School_of_Magic_3 = State()
    School_of_Magic_4 = State()
    School_of_Magic_5 = State()
    School_of_Magic_6 = State()
    School_of_Magic_7 = State()
    School_of_Magic_8 = State()
    School_of_Magic_9 = State()
    School_of_Magic_10 = State()
    School_of_Magic_11 = State()
    School_of_Magic_12 = State()
    School_of_Magic_100 = State()
    School_of_Magic_finish = State()


@dp.callback_query_handler(state=InputWhatever.School_of_Magic_finish)
async def ikb_cb_handler(callback: types.CallbackQuery):
    await callback.answer('🐙ИИ меня не устраивает, вакансия открыта, пишите.')


@dp.message_handler(commands=['start'], state=[AdminState, None])
async def start_command(message: types.Message, state: FSMContext):
    print(message.from_user.id)
    db.insert_user(message.from_user.id)
    await state.finish()
    db.update_user_state('start', message.from_user.id)
    if message.from_user.id in ADMIN_IDS:
        await message.answer('🐙 🫱 <code>1219523153</code> 🫲| <b>Выберите одну из функций ниже:</b>',
                             parse_mode='html')
        await bot.send_message(message.from_user.id,
                               '1. Смена состояния\n'
                               '2. Запустить бота',
                               reply_markup=admin_kb)
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    else:
        await message.answer(text=' 🐙<b>Мы в Сириусе, а вы попали в квест \n"Школа магии".    🏰'
                                  '\nТут мы предлагаем вам: '
                                  '\nПройтись по приятным локациям,     🌴'
                                  '\nПогрузиться в мир магии,       🔮'
                                  '\nПознать мудрость всех факультетов,     🎆'
                                  '\nИзбавить школу от не чистой силы.      😈'
                                  '\n \n🐙    <em>Пройти квест ---> /School_of_Magic</em></b> '
                                  '\n \n \n<a href="https://t.me/QuestStreetBot"><b>Выбрать другой квест.</b>'
                                  '</a>', parse_mode='html', disable_web_page_preview=True)


@dp.callback_query_handler(text='next')
async def create_post(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.from_user.id in ADMIN_IDS:
            try:
                admin_select_user = InlineKeyboardMarkup(row_width=2)
                all_users = db.select_all_users()
                all_posts_index = [i[0] for i in all_users]

                data['first_index'] = data['second-index']
                data['second-index'] += 5

                for user_id in all_posts_index[data['first_index']:data['second-index']:]:
                    user = db.select_user(user_id)
                    admin_select_user.add(InlineKeyboardButton(f'{user.id}-{user.chat_id}-{user.nickname}',
                                                               callback_data=f'user{user.id}'))
                admin_select_user.add(
                    InlineKeyboardButton('<< Предыдущая', callback_data='previous'),
                    InlineKeyboardButton('Следующая >>', callback_data='next')
                )

                await callback.message.edit_reply_markup(admin_select_user)
                await AdminState.select_user.set()
            except aiogram.utils.exceptions.MessageNotModified:
                pass
        await AdminState.select_user.set()


@dp.callback_query_handler(text='previous', state=AdminState.select_user)
async def create_post(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.from_user.id in ADMIN_IDS:
            try:
                admin_select_user = InlineKeyboardMarkup(row_width=2)
                all_users = db.select_all_users()
                all_posts_index = [i[0] for i in all_users]

                data['first_index'] = (data['first_index'] - 5) if (data['first_index'] - 5) >= 5 else 0
                data['second-index'] = (data['second-index'] - 5) if (data['second-index'] - 5) >= 10 else 5

                for user_id in all_posts_index[data['first_index']:data['second-index']:]:
                    user = db.select_user(user_id)
                    admin_select_user.add(InlineKeyboardButton(f'{user.id}-{user.chat_id}-{user.nickname}',
                                                               callback_data=f'user{user.id}'))
                admin_select_user.add(
                    InlineKeyboardButton('Предыдущая <<', callback_data='previous'),
                    InlineKeyboardButton('Следующая >>', callback_data='next')
                )
                await callback.message.edit_reply_markup(admin_select_user)
            except aiogram.utils.exceptions.MessageNotModified:
                pass


@dp.callback_query_handler(lambda call: call.data.startswith('user'), state=AdminState.select_user)
async def render_call_id(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if call.from_user.id in ADMIN_IDS:
            number = "".join(i for i in call.data if str(i).isdigit())
            data['id'] = number
            user = db.select_user_with_db_id(int(number))

            await call.message.edit_text(f'🐙Никнейм пользователя: "{user.nickname}"\n\n'
                                         f'chat_id: "{user.chat_id}"\n'
                                         f'Возраст: "{user.age}"\n'
                                         f'Уровень: "{user.level}"\n'
                                         f'Текущее состояние: "{user.user_state}"',
                                         reply_markup=change_user_state)


@dp.callback_query_handler(text='back', state=AdminState.select_user)
async def back(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        admin_select_user = InlineKeyboardMarkup(row_width=2)
        all_users = db.select_all_users()
        all_posts_index = [i[0] for i in all_users]
        data['first_index'] = 0
        data['second-index'] = 5

        for user_id in all_posts_index[data['first_index']:data['second-index']:]:
            user = db.select_user(user_id)
            admin_select_user.add(InlineKeyboardButton(f'{user.id}-{user.chat_id}-{user.nickname}',
                                                       callback_data=f'user{user.id}'))
        admin_select_user.add(
            InlineKeyboardButton('Предыдущая <<', callback_data='previous'),
            InlineKeyboardButton('Следующая >>', callback_data='next')
        )
        await call.message.edit_text('🐙Выберите пользователя из меню ниже или напишите сюда его chat_id',
                                     reply_markup=admin_select_user)


@dp.callback_query_handler(text='change_state', state=[None, AdminState])
async def select_new_state(call: types.CallbackQuery):
    await AdminState.change_user_state.set()
    await call.message.answer('<b>🐙Напишите номер нового состояния из списка ниже '
                              '<em>\nФормат списка: состояние = номер состояния</em></b>:'
                              '\nSchool_of_Magic_1 = <b>1</b>,'
                              '\nSchool_of_Magic_Pay = <b>2</b>,'
                              '\nSchool_of_Magic_2 = <b>3</b>,'
                              '\nSchool_of_Magic_3 = <b>4</b>,'
                              '\nSchool_of_Magic_4 = <b>5</b>,'
                              '\nSchool_of_Magic_5 = <b>6</b>,'
                              '\nSchool_of_Magic_6 = <b>7</b>,'
                              '\nSchool_of_Magic_7 = <b>8</b>,'
                              '\nSchool_of_Magic_8 = <b>9</b>,'
                              '\nSchool_of_Magic_9 = <b>10</b>,'
                              '\nSchool_of_Magic_10 = <b>11</b>,'
                              '\nSchool_of_Magic_11 = <b>12</b>,'
                              '\nSchool_of_Magic_12 = <b>13</b>,'
                              '\nSchool_of_Magic_100 = <b>14</b>,'
                              '\nSchool_of_Magic_finish = <b>15</b>.', parse_mode='html')


@dp.message_handler(state=AdminState.select_user)
async def render_chat_id(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            user = db.select_user(message.text)
            data['id'] = user.id
            await message.answer(f'🐙Никнейм пользователя: "{user.nickname}"\n\n'
                                 f'chat_id: "{user.chat_id}"\n'
                                 f'Возраст: "{user.age}"\n'
                                 f'Уровень: "{user.level}"\n'
                                 f'Текущее состояние: "{user.user_state}"',
                                 reply_markup=change_user_state)

    except TypeError:
        await message.answer('🐙Такой пользователь не найден в базе данных!')


@dp.message_handler(state=AdminState.change_user_state)
async def change_user_state_f(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        dict_values = {1: ' School_of_Magic_1',
                       2: ' School_of_Magic_Pay',
                       3: ' School_of_Magic_2',
                       4: ' School_of_Magic_3',
                       5: ' School_of_Magic_4',
                       6: ' School_of_Magic_5',
                       7: ' School_of_Magic_6',
                       8: ' School_of_Magic_7',
                       9: ' School_of_Magic_8',
                       10: ' School_of_Magic_9',
                       11: ' School_of_Magic_10',
                       12: ' School_of_Magic_11',
                       13: ' School_of_Magic_12',
                       14: ' School_of_Magic_100',
                       15: ' School_of_Magic_finish'}
        if int(message.text) in range(1, 16):
            user_id = db.select_user_with_db_id(int(data['id'])).chat_id
            new_state = dict_values[int(message.text)]
            db.update_user_state(new_state, user_id)

            current_user_state = dp.current_state(chat=user_id, user=user_id)
            user_data = await current_user_state.get_data()
            try:
                user_data['start_time']
            except KeyError:
                user_data['start_time'] = datetime.now()

            result_state = f'InputWhatever.{new_state}'
            await state.finish()

            await current_user_state.set_state(eval(result_state))
            await current_user_state.set_data(user_data)
            await message.answer('🐙Состояние пользователя успешно изменено!', reply_markup=admin_kb2)


@dp.callback_query_handler(state=None)
async def render_call(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'test':
        async with state.proxy() as data:
            if 'messages' in data.keys():
                messages = data['messages']
            else:
                messages = []
            await callback.message.edit_text(text=' 🐙<b>Мы в Сириусе, а вы попали в квест \n"Школа магии".    🏰'
                                             '\nТут мы предлагаем вам: '
                                             '\nПройтись по приятным локациям,     🌴'
                                             '\nПогрузиться в мир магии,       🔮'
                                             '\nПознать мудрость всех факультетов,     🎆'
                                             '\nИзбавить школу от не чистой силы.      😈'
                                             '\n \n🐙    <em>Пройти квест ---> '
                                             '/School_of_Magic</em></b> '
                                             '\n \n \n<a href="https://t.me/QuestStreetBot"><b>'
                                             'Выбрать другой квест.</b>'
                                             '</a>', parse_mode='html', disable_web_page_preview=True)
            data['messages'] = messages
    elif callback.data == 'states':
        async with state.proxy() as data:
            admin_select_user = InlineKeyboardMarkup(row_width=2)
            all_users = db.select_all_users()
            all_posts_index = [i[0] for i in all_users]
            data['first_index'] = 0
            data['second-index'] = 5

            for user_id in all_posts_index[data['first_index']:data['second-index']:]:
                user = db.select_user(user_id)
                admin_select_user.add(InlineKeyboardButton(f'{user.id}-{user.chat_id}-{user.nickname}',
                                                           callback_data=f'user{user.id}'))
            admin_select_user.add(
                InlineKeyboardButton('Предыдущая <<', callback_data='previous'),
                InlineKeyboardButton('Следующая >>', callback_data='next')
            )
            await callback.message.edit_text('🐙Выберите пользователя из меню ниже или напишите сюда его chat_id',
                                             reply_markup=admin_select_user)
            await AdminState.select_user.set()


@dp.message_handler(commands=["School_of_Magic"])
async def start(message: types.Message, state: FSMContext):
    photo_School_of_Magic_0 = InputFile("School_of_Magic_0.png", 'rb')
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []
        messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_School_of_Magic_0))
        messages.append(await message.answer("<b>🐙Добро пожаловать в Школу магии.\n "
                                             "Для прохождения вам понадобится:\n2️⃣ часа свободного времени\n"
                                             "Заряженный телефон    🤳\nЯндекс карта     🗺\n"
                                             "Позитивное настроение.😎 </b>", parse_mode="html"))
        messages.append(await message.answer("<b>🐙Если у вас возникнут трудности, то можете написать "
                                             "\n/help и бот вам подскажет.      🆘\n"
                                             "Если этого будет мало, то пишите \n/answer и бот выдаст ответ.\n"
                                             "Если будут трудности с ботом то пишите.       ✍️"
                                             "\n \n🐙---> https://t.me/glebmehrykov\n \n"
                                             "Если у вас пропала клавиатура,"
                                             " то нажмите на четыре точки возле скребки.\n"
                                             "</b>", parse_mode="html", disable_web_page_preview=True))
        messages.append(await message.answer('<b><em>🐙Хочу обратить ваше внимание:'
                                             '\nНе пытайтесь пройти квест быстрее, проходите с удовольствием, гуляйте!'
                                             '\nКвесты имеют расстояние друг от друга около 750м.'
                                             '\nКартой Яндекс придется пользоваться часто.'
                                             '\nДумать тоже.        🧠'
                                             '\nИногда нужно увеличить масштаб карты.       🔎'
                                             '\nЕсли вы застряли и писать help или answer не хочется, '
                                             'прочитайте это сообщение еще раз.\n '
                                             '\n🐙Стоимость квеста 1500р, но вы можете ознакомится с '
                                             'первой частью квеста и пройти его.'
                                             '\nПроцесс оплаты будет доступен после прохождения '
                                             'первого задания.</em></b>'
                                             '\n \n     <em>Текст защищен. «Российское Авторское Общество»</em> (РАО)',
                                             parse_mode='html'))
        messages.append(await message.answer("<b>🐙Если готовы пишите \"🫱 <code>go"
                                             "</code> 🫲\".</b>", parse_mode='html'))
        messages.append(message)
        data['messages'] = messages
        await InputWhatever.School_of_Magic_1.set()


@dp.message_handler(state=InputWhatever.School_of_Magic_1)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('School_of_Magic_1', message.from_user.id)
    photo_School_of_Magic_1 = InputFile("School_of_Magic_1.png", 'rb1')
    photo_School_of_Magic_2 = InputFile("School_of_Magic_2.png", 'rb2')
    photo_School_of_Magic_3 = InputFile("School_of_Magic_3.png", 'rb3')
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []
        messages.append(message)

        if message.text.lower() == "go":
            await InputWhatever.School_of_Magic_Pay.set()
            messages.append(await message.answer("<b>🐙Начало.</b>", parse_mode="html"))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_School_of_Magic_1))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Луи, вставай! '
                                                 '\nУже глубокая ночь, все спят. '
                                                 '\nОдевайся!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Уже? '
                                                 '\nЕще чу-чуть. '
                                                 '\nАааам... '
                                                 '\n5 минуточек.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Нет времени!\nОдевайся. '
                                                 '\nНужно успеть вернуться пока все не проснулись. '
                                                 '\nТем более, Эми нас уже ждет.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Да все, все.'
                                                 '\nОдеваюсь.</b>', parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_School_of_Magic_2))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Тише!</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Соррах и Луи встречаются с Эми возле статуи гоночной метлы.'
                                                 '</em>', parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_School_of_Magic_3))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Вы серьезно? '
                                                 '\nНа вас нельзя полагаться. '
                                                 '\nДа как я вообще подписалась на вашу авантюру?!'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Эми, да там твоих интересов не меньше. '
                                                 '\nСравнишь подлинность библиотеки с реальностью.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Ребят, а нам точно нужно идти к запретному морю? '
                                                 '\nЯ, если честно, боюсь.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Это ты вовремя. '
                                                 '\nПредлагаю обсудить это во время пути, времени у нас мало.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Пошлите.</b>', parse_mode='html'))
            messages.append(await message.answer(' \n<u>Луи</u>:\n<b>Эх... А в голове это выглядело безопаснее…'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Нам нужно добраться до Заброшенного корабля, '
                                                 'что стоит на камнях у берега моря. </b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>В книжке я читала, что найти его будет сложно, '
                                                 'но ориентиром будет железный человек.'
                                                 ' \nПо слухам, это старый маг, который захотел стать бессмертным и'
                                                 ' вложил свою душу '
                                                 'в груду металла.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Вы себя слышите? '
                                                 '\nЗаброшенный корабль, какой-то железный безумец, а там, '
                                                 'наверное, еще эти пауки возле корабля! '
                                                 '\nБоюсь пауков.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Быстрым шагом дойдем минут за восемнадцать'
                                                 '.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Луи, не отставай, пошли.</b>', parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - чей корабль?\nТолько имя.</em>", parse_mode="html"))
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('go'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('Ответ: 🫱 <code>go</code> 🫲', parse_mode='html'))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                   "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
            data['messages'] = messages


@dp.message_handler(state=InputWhatever.School_of_Magic_Pay)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('School_of_Magic_Pay', message.from_user.id)
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []
        if message.from_user.id in ADMIN_IDS and message.text == '/skip8998':
            messages.append(await message.answer('Вы успешно пропустили процесс оплаты.\n'
                                                 'Напишите <code>Виктории</code>.', parse_mode='html'))
            await InputWhatever.School_of_Magic_2.set()
        elif message.text.lower() == '🐙':
            await bot.send_message(message.chat.id, random.choice(responses))
        elif message.text.lower() == '🐙назад':
            await InputWhatever.School_of_Magic_1.set()
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            user_id = message.from_user.id
            await message.answer(f"Ваш ID TG: <code>{user_id}</code>", parse_mode='html')
            await message.answer('<b>🐙   Если у вас возникли проблемы с оплатой:</b>\n'
                                 '1. Напишите "Назад" затем, напишите "go" и попробуйте оплатить еще раз.\n'
                                 '2. Попробуйте оплатить другой картой.\n'
                                 '3. Если это не помогло, то пишите \n🐙---> https://t.me/glebmehrykov\n'
                                 '      Пишите: \n              1.В чем трудность.\n              2.Какой квест. \n    '
                                 '          3.Ваш ID TG. Узнать его можно в '
                                 '\n                            <a href="https://t.me/QuestStreetBot">Главном меню</a>.'
                                 '\nИли скопировать сверху.'
                                 ' \n<b>🐙   Если вам нужна подсказка квеста то:</b>\n'
                                 'Напоминаем, что картой Яндекс придется пользоваться постоянно.'
                                 '\nДавайте пройдемся по набережной, на карте.', parse_mode='html')
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            await message.answer('🐙Тут должен быть ответ, но его не будет, видите ли, первая задача'
                                 ' квеста достаточно простая, '
                                 'при все это у вас есть подсказка, и я уверен, что вы справитесь с этой задачей.\n'
                                 'После оплаты квеста вам будут доступны ответы, но чтобы оплатить, вам нужно пройти '
                                 'первую задачу, а чтобы ее пройти, нужно приехать и разгадать ее.\n'
                                 '<b>Все квесты по 1500р</b>', parse_mode='html')
        elif message.text.lower() == 'глеб, дай скидку!🙏🏻':
            await bot.send_message(message.from_user.id, '<b>🐙Особым гостям особая цена.'
                                                         '</b>', parse_mode='html')
            await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста.',
                                   description='🐙Оплата для того, чтобы пройти квест.',
                                   provider_token="390540012:LIVE:47826",
                                   payload='buy_sub', start_parameter='test_bot',
                                   currency='rub',
                                   prices=[types.LabeledPrice(label='rub', amount=300 * 100)])
        elif message.text.lower() == 'ваша кодовая фраза':
            await bot.send_message(message.from_user.id, '<b>🐙Особым гостям особая цена.'
                                                         '</b>', parse_mode='html')
            await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста.',
                                   description='🐙Оплата для того, чтобы пройти квест.',
                                   provider_token="390540012:LIVE:47826",
                                   payload='buy_sub', start_parameter='test_bot',
                                   currency='rub',
                                   prices=[types.LabeledPrice(label='rub', amount=1250 * 100)])
        else:
            await bot.send_message(message.from_user.id, '<b>🐙Оплатите квест, для того чтобы продолжить работу бота.'
                                                         '</b>', parse_mode='html')
            await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста.',
                                   description='🐙Оплата для того, чтобы пройти квест.',
                                   provider_token="390540012:LIVE:47826",
                                   payload='buy_sub', start_parameter='test_bot',
                                   currency='rub',
                                   prices=[types.LabeledPrice(label='rub', amount=1500 * 100)])
        messages.append(message)
        data['messages'] = messages

@dp.pre_checkout_query_handler(state=InputWhatever.School_of_Magic_Pay)
async def process_precheck(precheck: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(precheck.id, ok=True)


@dp.message_handler(content_types=[types.ContentType.SUCCESSFUL_PAYMENT], state=InputWhatever.School_of_Magic_Pay)
async def successful_payment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []
        if message.successful_payment.invoice_payload == 'buy_sub':
            messages.append(await bot.send_message(message.from_user.id, '<b>🐙Вы успешно оплатили доступ к '
                                                                         'боту.</b>💸\nНапишите ответ на предыдущий '
                                                                         'вопрос.', parse_mode='html'))
            await InputWhatever.School_of_Magic_2.set()
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.School_of_Magic_2)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        d1 = datetime.now()
        data['start_time'] = d1
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('School_of_Magic_2', message.from_user.id)
        db.new_level(message.chat.id)
        if message.text.lower() == 'виктория' or message.text.lower() == 'виктории':
            await message.answer(d1.strftime("%H:%M:%S"))
            data["number"] = message.text
            messages.append(await message.answer("<b>🐙Таймер на прохождение квеста запущен."
                                                 "</b>", parse_mode="html"))
            messages.append(await message.answer("<b>🐙Давайте убедимся, что вы у нужного корабля - "
                                                 "что внутри якоря?</b>", parse_mode="html"))
            await InputWhatever.School_of_Magic_3.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Воспользуйтесь Яндекс картой.'
                                                 '\nДавайте пробежимся по набережной!'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Виктория</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.410899, longitude=39.934539))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.School_of_Magic_3)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('School_of_Magic_3', message.from_user.id)
        photo_School_of_Magic_4 = InputFile("School_of_Magic_4.png", 'rb4')
        photo_School_of_Magic_5 = InputFile("School_of_Magic_5.png", 'rb5')

        if message.text.lower() == 'стекло' or message.text.lower() == 'камни':
            data["number"] = message.text
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Смотрите, кажется это он. '
                                                 '\nДавайте подойдем поближе.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Я вас тут подожду.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Как хочешь.</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Соррах с Эми проходят 15 метров.</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Три, два, один...</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Стойте, подождите меня.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Не кричи. '
                                                 '\nМы тут можем быть не одни.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Корабль</u>:\n<b>Конечно, вы тут не одни!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Ааа, что, кто это?!</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Луи сбивается с ног. '
                                                 '\nСоррах с Эми отходят назад.</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Эми, ты знала, что корабль может говорить?'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Нет.</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Корабль резким движением натягивает парус на себя и '
                                                 'Соррах с Эми на несколько'
                                                 ' шагов по инерции подходят к кораблю.</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Корабль</u>:\n<b>Что вы забыли в запретной зоне? '
                                                 '\nДиректор вам разве не говорил, что сюда заходить нельзя?'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>В книгах такого не было написано.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Мы не причиним вам вреда.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Корабль</u>:\n<b>Вреда, мне? '
                                                 '\nАх-ха-ха. '
                                                 '\nГлупцы, что вы можете, вы думаете, если у вас в школе пятерки,'
                                                 ' то вы что-то можете?'
                                                 '\nМне нет до вас дела, но не думайте, что, то-что вам преподают, '
                                                 'поможет вам в реальном сражении. '
                                                 '\nКстати, скоро проверим.</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Луи трясется и дрожащим голосом спрашивает.'
                                                 '</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Это еще, что значит?'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Корабль</u>:\n<b>Вы когда-нибудь читали о Эмолитах?'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>В один голос.'
                                                 '\nНет.</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Корабль</u>:\n<b>Ах-ха-ха! '
                                                 '\nБегите домой, пока ещё есть время!</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Корабль перестает подавать признаки жизни.'
                                                 '</em>', parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_School_of_Magic_4))
            messages.append(await message.answer('<u>Луи:</u>\n<b>Довольны?'
                                                 '\nИдем домой! '
                                                 '\nПрушу вас.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Да, пожалуй, нам пора.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Мне кажется, мы тут не одни, '
                                                 'давайте выбираться отсюда.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b><u><em>Движ</em></u>емся к озеру.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Куда дальше?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>От ноль-скара направо.</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Проносится сильный холодный ветер, температура резко '
                                                 'падает до нуля.</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Вы это чувствуете?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Да, становится страшно и холодно. '
                                                 '\nНельзя останавливаться.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Впереди кто-то стоит.</b>', parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_School_of_Magic_5))
            messages.append(await message.answer('🐙<em>Подлетает черный дух в капюшоне к Сорраху и хватает '
                                                 'длинными костлявыми пальцами за голову. '
                                                 '\nСоррах бесконтрольно падает на колени, '
                                                 'а Эмолит высасывает его разум, оставляя '
                                                 'только страх и чувство беспомощности.</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Соррах, нет!</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Эми использует заклинания, но Эмолит этого не ощущает, '
                                                 'только его капюшон едва потрепался.</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Что это было? '
                                                 '\nКак с ним бороться?!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Я не знаю, но нужно пробовать что-то еще! '
                                                 '\nСоррах синеет!</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Луи произносит заклинание, но все безуспешно.'
                                                 '</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Соррах, держись, мы что-то при...'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Проносится резкий поток воздуха и сильный звук. '
                                                 '\nЭмолит теряет равновесие и переключается на новую цель.'
                                                 '</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Корабль</u>:\n<b>Не ждали, детишки, я говорил, '
                                                 'что это вам не стрекозу в лягушку превратить. '
                                                 '\nПередайте Жагоне, что долг уплачен.\nБегите.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Жагоне?</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Эми подбегает к Сорраху, следом Луи и тащат его на себе.</em>',
                                                 parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Держись, все позади, скоро будем дома.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Нам же просто по прямой?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Да, до конца.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Ну все, вспомнил. '
                                                 '\nВот тут мы встретились, мы возле школы. '
                                                 '\nЛишь бы нас не заметили.</b>', parse_mode='html'))
            messages.append(await message.answer("🐙<em>Задача - найдите гоночную метлу. "
                                                 "\nЧто написано красным цветом?</em>",
                                                 parse_mode="html"))
            await InputWhatever.School_of_Magic_4.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲| <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Тут нужно прийти, Яндекс карта вам уже не поможет.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Стекло</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.410899, longitude=39.934539))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0"
                                                           "okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
            messages.append(message)
            data['messages'] = messages


@dp.message_handler(state=InputWhatever.School_of_Magic_4)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('School_of_Magic_4', message.from_user.id)
        photo_School_of_Magic_6 = InputFile("School_of_Magic_6.png", 'rb')
        if message.text.lower() == 'ссср':
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_School_of_Magic_6))
            messages.append(await message.answer('<u>Жагона</u>:\n<b>Мальчики, стоять!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Ну вот, влипли.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Жагона</u>:\n<b>Эми, я от тебя такого не ожидала, '
                                                 'гордость школы!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Я даже рада, что не пришлось Вас искать. '
                                                 '\nПростите нас, но Соррах, он еле спасся!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Жагона</u>:\n<b>Кого вы встретили, Кентавров, '
                                                 'Болотников, Пауков?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Хуже!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Мы искали таинственный корабль.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Жагона</u>:\n<b>Но вы же знаете, что это всего лишь сказка'
                                                 '.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Эмолиты тоже сказка?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Жагона</u>:\n<b>Как ты сказала?!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Эмолиты. '
                                                 '\nКорабль мы нашли, он нас и спас от Эмолита. '
                                                 '\nИ просил передать вам "Долг уплачен".</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Жагона</u>:\n<b>Так, ну все, это перебор. '
                                                 '\nВы оба наказаны!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Оба?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Жагона</u>:\n<b>Соррах уже получил свое наказание, '
                                                 'я отведу его в госпиталь, '
                                                 'к утру будет как новенький. '
                                                 '\nИдите по своим комнатам. '
                                                 '\nИ да, игровой турнир начнется через четыре часа,'
                                                 ' если вы опоздаете, то будете отчислены. '
                                                 '\nСпокойной ночи!</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Луи и Эми в один голос. '
                                                 '\nСпокойной ночи, леди Жагона!</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Луи, давай как обычно, встретимся над огнем.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - напишите место встречи.</em>",
                                                 parse_mode="html"))
            await InputWhatever.School_of_Magic_5.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲| <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Яндекс карта тут тоже понадобится, '
                                                 'прочитайте текст еще раз, в тексте указан маршрут.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>СССР</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.414151, longitude=39.948922))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okO"
                                                           "jYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
            messages.append(message)
            data['messages'] = messages


@dp.message_handler(state=InputWhatever.School_of_Magic_5)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('School_of_Magic_5', message.from_user.id)
        photo_School_of_Magic_7 = InputFile("School_of_Magic_7.png", 'rb')
        if (message.text.lower() == 'поющие фонтаны'
                or message.text.lower() == 'фонтаны'
                or message.text.lower() == 'фонтан'):
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_School_of_Magic_7))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Ну ты как, Соррах?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Лучше, но состояние все еще паршивое. '
                                                 '\nГде Эми?</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Подходит Эми.</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Выспались?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Эм... '
                                                 '\nНе особо.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Я узнала в запретной библиотеке, '
                                                 'что Эмолиты были раньше, лет 30 назад. '
                                                 '\nЖагона работала тут в это время, она точно знает больше,'
                                                 ' чем нам вчера сказала.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Там написано кто они и как их можно остановить?'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Да, там сказано, что нужно найти '
                                                 'четыре камня силы, интересный факт, что каждый камень относится '
                                                 'к магическому факультету, но не сказано, где их искать.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>'
                                                 '\nМировед. '
                                                 '\nТриуглс.'
                                                 '\nФотонграунд.'
                                                 '\nИ Зириус.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Первые два факультета обитают тут.'
                                                 '\nПредлагаю отправиться к Мироведу, так как он рядом, и поискать '
                                                 'там первый камень силы.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Ты шутишь, как мы поймем, где искать их?'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Мы все не больше тебя знаем.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Да, я думаю, разберемся.'
                                                 '\nДавайте найдем факультет Мировед, он вроде золотом и '
                                                 'серебром обсыпан.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Возможно, камень будет спрятан в '
                                                 'одной из магических плит, '
                                                 'что украшает их герб.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Вы вообще помните, сколько их там?'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Да, но нам нужна одна, а она точно '
                                                 'будет выделяться.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Думаю, стоит найти самую главную плиту '
                                                 'и посмотреть ниже.</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Задача - напишите название плиты.</em>', parse_mode='html'))
            await InputWhatever.School_of_Magic_6.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲| <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Найдите тренировочный комплекс, там будет вечный огонь,'
                                                 ' что под ним?'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Поющие фонтаны</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.405505, longitude=39.954678))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf"
                                                           "0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
            messages.append(message)
            data['messages'] = messages


@dp.message_handler(state=InputWhatever.School_of_Magic_6)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('School_of_Magic_6', message.from_user.id)
        photo_School_of_Magic_8 = InputFile("School_of_Magic_8.png", 'rb')
        if message.text.lower() == "португалия" \
                or message.text.lower() == "republic portuguese" \
                or message.text.lower() == "portuguese" \
                or message.text.lower() == "portugal":
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_School_of_Magic_8))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Луи, ты выше всех, проверь камень.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Ну конечно.</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Луи проверяет и находит первый магический камень.'
                                                 '</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Отлично, осталось еще три камня.'
                                                 '\nДавайте отправимся к факультету Триуглс.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Нам нужно отправиться к полусфере.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Это возле зала мертвых!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Просто не смотри туда.😂</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Задача - напишите название.</em>', parse_mode='html'))
            await InputWhatever.School_of_Magic_7.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲| <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Найдите мир.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Republic Portuguese</code> 🫲.',
                                                 parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.407148, longitude=39.954091))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okO"
                                                           "jYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
            messages.append(message)
            data['messages'] = messages


@dp.message_handler(state=InputWhatever.School_of_Magic_7)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('School_of_Magic_7', message.from_user.id)
        photo_School_of_Magic_9 = InputFile("School_of_Magic_9.png", 'rb')
        if message.text.lower() == 'планетарий':
            data["number"] = message.text
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Отлично, мы пришил, но где '
                                                 'искать этот камень?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Наверно, нужно пообщаться с их Архимейстором'
                                                 ' магии.</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Ребята заходят в факультет и обращаются к Фаусту.'
                                                 '</em>', parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_School_of_Magic_9))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Здравствуйте, Фауст.'
                                                 '\nНе примите за грубость, но мы бы хотели узнать у вас, '
                                                 'где можно найти магический камень факультета "Триуглс".'
                                                 '\nЯ понимаю, это ваш камень, но он нам крайне необходим, '
                                                 'чтобы защитить школу от Эмолитов.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Фауст</u>:\nИзрядно лицезреть <em><b>трех</b></em> юных лиц,'
                                                 ' что вовлекли себе, '
                                                 '<em><b>сто</b></em>ль учесть благородную.'
                                                 '\nИ стало б мне, мешая вам, <em><b>пя</b></em>тн'
                                                 'и<em><b>ть</b></em> свой белый лик?'
                                                 '\nНелепо и ссылаться мне на ваш зеленый вид, видь если разум ваш '
                                                 'до<em><b>сто</b></em>ин,'
                                                 ' то вы найдете то, что спрятано внутри речей моих.'
                                                 '\n \nЯ знаю, времени в обрез.'
                                                 '\nНе смею больше вам мешать. '
                                                 '\nУдачи вам.', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Фауст покидает комнату, за его спиной все время стоял '
                                                 'сундук с замком.</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Кто ни-будь, что ни-будь понял?'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Не сразу, как Фауст ушел, '
                                                 'я увидела сундук и поняла, почему он так странно '
                                                 'акцентировал на некоторых звуках.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Согласен, но что же это могло бы означать?'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Задача - открыть замок.</em>', parse_mode='html'))
            await InputWhatever.School_of_Magic_8.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲| <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Зал мертвых это кладбище, в 50 метрах будет полусфера.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Планетарий</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.404772, longitude=39.959501))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk"
                                                           "6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
            messages.append(message)
            data['messages'] = messages


@dp.message_handler(state=InputWhatever.School_of_Magic_8)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('School_of_Magic_8', message.from_user.id)
        photo_School_of_Magic_10 = InputFile("School_of_Magic_10.png", 'rb')
        if message.text.lower() == '31005100' \
                or message.text.lower() == '3 100 5 100':
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_School_of_Magic_10))
            messages.append(await message.answer('<em>🐙Ребята вскрывают сундук и находят второй магический '
                                                 'камень.</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Мы молодцы, пол дела сделано.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Да, осталось еще два, '
                                                 'но эти два факультета находятся дальше.'
                                                 '\nВроде, факультет будет возле большого колеса. '
                                                 '\nТам мы увидим фиолетовое сердце, а справа '
                                                 'будет факультет, и где-то там камень.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Что-то с погодой. '
                                                 '\nЯ думала, её разгоняют, когда проводятся большие турниры.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Идем!'
                                                 '\nСейчас не до погоды.</b>', parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - что на камне?</em>",
                                                 parse_mode="html"))
            await InputWhatever.School_of_Magic_9.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲| <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Тут нужно написать цифры по очереди.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>3 100 5 100</code> 🫲.', parse_mode='html'))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubL"
                                                           "f0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
            messages.append(message)
            data['messages'] = messages


@dp.message_handler(state=InputWhatever.School_of_Magic_9)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('School_of_Magic_9', message.from_user.id)
        photo_School_of_Magic_20 = InputFile("School_of_Magic_20.png", 'rb')
        if message.text.lower() == 'фонарь':
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_School_of_Magic_20))
            messages.append(await message.answer('<em>🐙Получен - третий камень.</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Мы нашли третий камень, остался последний.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Факультет - Зириус, самый таинственный, '
                                                 'любят они делать все на виду, но так, что не видишь.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Я знаю, что они золотом богаты.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Читала, что у них при входе будет магическая'
                                                 ' лавка.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Но интересно то, что мы ищем то, чего нет. '
                                                 '\nНам нужно узнать номер дома, но как, если мы его не видим.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - напишите номер дома.</em>",
                                                 parse_mode="html"))
            await InputWhatever.School_of_Magic_10.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲| <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Сердце будет огромное, железное.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Фонарь</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.404386, longitude=39.963684))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5x"
                                                           "k6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.School_of_Magic_10)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        photo_School_of_Magic_11 = InputFile("School_of_Magic_11.png", 'rb')
        db.update_user_state('School_of_Magic_10', message.from_user.id)
        if (message.text.lower() == '6'
                or message.text.lower() == 'шестой'
                or message.text.lower() == 'шестой дом'
                or message.text.lower() == 'шесть'):
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_School_of_Magic_11))
            messages.append(await message.answer('<em>🐙Находите шестой дом и внутри четвертый камень.</em>',
                                                 parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>А вот и последний камень.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Друзья, мы сделали это!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Осталось их объединить.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<em>🐙Пытаются втроем направить магию, '
                                                 'но ничего не выходит.</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Словно обычные камни, видимо, '
                                                 'что-то мы делаем не так.</b>', parse_mode='html'))
            messages.append(await message.answer('<em>🐙Погода начинает резко темнеть. '
                                                 '\nС неба летят призрачные Эмолиты. '
                                                 '\nНа всей территории объявляется тревога.</em>',
                                                 parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>О нет, нужно вернуться в школу и '
                                                 'помочь нашим ребятам!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Там мы им ничем не поможем, мы уже так близки, '
                                                 'нам нужно продолжить путь, и чем быстрее мы разберемся с камнем, '
                                                 'тем быстрее поможем ребятам.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Но мы не знаем, как его активировать!'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Возможно, нужна сила магического озера.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Точно, в одном из двух озер, тот, '
                                                 'что ближе к нам, есть тропа, что ведет вдоль магического озера, '
                                                 'у тропы есть ответвление, там есть магический круг, '
                                                 'нужно попробовать там активировать камни.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Но туда же нельзя, это закрытая территория.'
                                                 '\nТам столько запретов.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Ты сейчас серьезно.'
                                                 '\nСколько там запретов, Луи?</b>', parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - сколько запретов?</em>",
                                                 parse_mode="html"))
            await InputWhatever.School_of_Magic_11.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲| <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Там будет много домов, счёт которых будет увеличиваться на 2, '
                                                 'но одного дома не будет. '
                                                 '\nЭто и есть таинственный дом, который нам нужен. '
                                                 '\nСам факультет находится от Фотонграунда в 50 метрах.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Шестой дом</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.403949, longitude=39.963437))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf"
                                                           "0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.School_of_Magic_11)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('School_of_Magic_11', message.from_user.id)
        photo_School_of_Magic_30 = InputFile("School_of_Magic_30.png", 'rb')
        if (message.text.lower() == '10'
                or message.text.lower() == 'десять'
                or message.text.lower() == '🔟'):
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_School_of_Magic_30))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Это точно, то место, камни начинают '
                                                 'светиться.</b>', parse_mode='html'))
            messages.append(await message.answer('<em>🐙В округе летящие Эмолиты, в '
                                                 'сторону школы. \nЭмолиты останавливаются, чувствуют угрозу, '
                                                 'которая идет от озера, и начинают лететь к ребятам.</em>',
                                                 parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>Ребята!\nБыстрее!\n'
                                                 'Нам нужно срочно объединить их силу.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Нам нужно заклинание, но мы не знаем какое!'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>В смысле, еще что-то нужно?!'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Успокойтесь!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Луи</u>:\n<b>А, ну да, на нас летят Эмолиты, '
                                                 'сейчас мы все станем кормом, хоть у нас и есть '
                                                 'четыре бесполезных магических камня. '
                                                 '\nПоэтому, да, давайте успокоимся!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>У нас есть камни;'
                                                 '\n        триуглс'
                                                 '\n            мировед'
                                                 '\n                фотоновый'
                                                 '\n                    зириуйский.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Соррах</u>:\n<b>Я думаю, что заклинание есть в их названиях.'
                                                 '\nНо я пока не понимаю, мне нужно время.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Эми</u>:\n<b>Луи, давай создадим'
                                                 ' защитную сферу и выиграем время.</b>', parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - заклинание будет из 8 букв."
                                                 "\nНапишите его.</em>",
                                                 parse_mode="html"))
            await InputWhatever.School_of_Magic_12.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲| <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Найдите на карте два озера, тот, что будет ближе к вам, туда '
                                                 'и идите. \nУ озера будет тропинка, идя по ней, найдете круг.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Десять</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.400901, longitude=39.972534))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6Iu"
                                                           "bLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.School_of_Magic_100)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('School_of_Magic_100', message.from_user.id)
        if message.text.lower() == 'help' or message.text.lower() == 'answer':
            await InputWhatever.School_of_Magic_2.set()
            data["number"] = message.text
            messages.append(await message.answer('🐙Нажмите 🫱 <code>Виктории</code> 🫲 \n'
                                                 'И отправьте ответ Боту.', parse_mode='html'))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.School_of_Magic_12)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        photo_School_of_Magic_12 = InputFile("School_of_Magic_12.png", 'rb12')
        db.update_user_state('School_of_Magic_12', message.from_user.id)
        if message.text.lower() == 'трмифози':
            data["number"] = message.text
            messages.append(await message.answer('🐙<em>Соррах произносит заклинание, камни отрываются от '
                                                 'земли и начинают крутиться, '
                                                 'создавая сильную воронку света, освещая всю территорию Школы.'
                                                 '\nВоронка поднимается все выше и становится все сильнее, '
                                                 'Эмолиты засасываться в воронку,'
                                                 ' теряя контроль над погодными условиями и исчезая из этого мира.'
                                                 '</em>', parse_mode='html'))
            await InputWhatever.School_of_Magic_finish.set()
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_School_of_Magic_12))
            await message.answer("<em><b>Конец.©</b></em>", parse_mode="html", reply_markup=finish)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Возьмите по 2 буквы из каждого камня.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>трмифози</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.400901, longitude=39.972534))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf"
                                                           "0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.School_of_Magic_finish)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('School_of_Magic_finish', message.from_user.id)
    async with state.proxy() as data:
        if 'messages' in data.keys():
            for msg in data['messages'][::-1]:
                try:
                    await msg.delete()
                except Exception:
                    pass
        if message.text.lower() == "🐙конец":
            mp3_School_of_Magic = InputFile('School_of_Magic_mus.mp3', 'Конец')
            await bot.send_audio(chat_id=message.chat.id, audio=mp3_School_of_Magic)
            db.new_level(message.chat.id)
            d1 = data['start_time']
            data["number"] = message.text
            d2 = datetime.now()
            result = (d2 - d1)
            d2 = d2.strftime("%H:%M:%S")
            hours, minutes, seconds = str(result).split(':')
            seconds = seconds.split('.')[0]
            await message.answer(f'🐙Время вашего прохождения: {hours}:{minutes}:{seconds}',
                                 reply_markup=markup_finish)
            await message.answer('<em><b>За сколько у вас получилось пройти квест?</b> \nПишите в группу VK или'
                                 ' Telegram чат.</em>',
                                 parse_mode='html', reply_markup=chat)
            await message.answer('<b>Автор текста✍️</b>', parse_mode='html', reply_markup=markup_avtar)
            await message.answer('<b>Программист👨‍💻</b>', parse_mode='html', reply_markup=markup_avtar2)
            await message.answer('<b>Художник🎨</b>', parse_mode='html', reply_markup=cb1)
            await message.answer('<em><b>Вернуться в меню квестов🚪</b></em>', parse_mode='html', reply_markup=backIn)
        elif message.text.lower() == '🐙':
            await bot.send_message(message.chat.id, random.choice(responses))
        elif message.text.lower() == '🚪':
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await state.finish()
                await message.answer('<code>1219523153</code> или напишите назад.</b>', parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
            else:
                await message.answer(text='<u>🐙Это потайная комната, но она не для тебя.</u>', parse_mode='html')
        elif (message.text == 'Вернуться в начало квеста▶️'
              or message.text == 'Вернуться в начало квеста▶'
              or message.text == '▶️'
              or message.text == '▶'):
            await state.finish()
            await message.answer('🐙Вы успешно закончили квест! '
                                 'Для того чтобы пройти квест еще раз напишите /start',
                                 reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer('🐙Это конец, вы можете пройти квест еще раз! '
                                 '\nЖмите на клавиатуру, если ее нет жмите на 4 точки или напишите "▶".')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
