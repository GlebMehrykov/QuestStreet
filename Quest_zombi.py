import random
from datetime import datetime

import aiogram.utils.exceptions
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile

import AIP_ChistyePrudy
from db import Database
from keybords import *

db = Database("2.db")
bot = Bot(token=AIP_ChistyePrudy.TELEGRAM_BOT)
db.create_table_users()
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
ADMIN_IDS = [1219523153, 6522187160]
responses = ['🐙Да, да.', '🐙Прювет', "🐙Как ты там?", '🐙Кто выпил весь ром!', "🐙На абордаж", "🐙Ну чего тебе?",
             '🐙Как долго ты готов(а) со мной общаться?', "🐙А это забавно."]


class AdminState(StatesGroup):
    select_user = State()
    change_user_state = State()


class InputWhatever(StatesGroup):
    Prudy_1 = State()
    Prudy_Pay = State()
    Prudy_2 = State()
    Prudy_3 = State()
    Prudy_4 = State()
    Prudy_5 = State()
    Prudy_6 = State()
    Prudy_7 = State()
    Prudy_8 = State()
    Prudy_9 = State()
    Prudy_10 = State()
    Prudy_11 = State()
    Prudy_100 = State()
    Prudy_finish = State()


@dp.callback_query_handler(state=InputWhatever.Prudy_finish)
async def ikb_cb_handler(callback: types.CallbackQuery):
    await callback.answer('🐙ИИ меня не устраивает, вакансия открыта, пишите.')


@dp.message_handler(commands=['start'], state=[AdminState, None])
async def start_command(message: types.Message, state: FSMContext):
    db.insert_user(message.from_user.id)
    await state.finish()
    db.update_user_state('start', message.from_user.id)
    if message.from_user.id in ADMIN_IDS:
        await message.answer('🐙 🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>', parse_mode='html')
        await bot.send_message(message.from_user.id,
                               '1. Смена состояния\n'
                               '2. Запустить бота',
                               reply_markup=admin_kb)
    else:
        await message.answer(text='<b>🐙Здравствуйте, вы попали в "QuestZombie".🧟‍♀️🧟‍♂️🧟‍♂️'
                                  '\nТут вы попадаете в мир где люди уже 25 лет живут в метро.'
                                  '\nВойна поглотила всех, остались только проигравшие.⚔️ '
                                  '\nГлавные герои больше не могут сидеть в метро и вынуждены выйти на свободу, '
                                  'где знакомятся с новыми людьми и их миром.☢️'
                                  '\n \n🐙    <em>Пройти квест ---> /Chistye_prudy</em></b>'
                                  '\n \n \n<a href="https://t.me/QuestStreetBot">'
                                  '<b>Выбрать другой квест.</b></a>',
                             parse_mode='html', disable_web_page_preview=True)


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

            await call.message.edit_text(f'Никнейм пользователя: "{user.nickname}"\n\n'
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
        await call.message.edit_text('Выберите пользователя из меню ниже или напишите сюда его chat_id',
                                     reply_markup=admin_select_user)


@dp.callback_query_handler(text='change_state', state=[None, AdminState])
async def select_new_state(call: types.CallbackQuery):
    await AdminState.change_user_state.set()
    await call.message.answer('<b>🐙Напишите номер нового состояния из списка ниже.\n '
                              '<em>Формат списка: состояние = номер состояния</em></b>:'
                              '\nPrudy_1 = <b>1</b>,'
                              '\nPrudy_Pay = <b>2</b>,'
                              '\nPrudy_2 = <b>3</b>,'
                              '\nPrudy_3 = <b>4</b>,'
                              '\nPrudy_4 = <b>5</b>,'
                              '\nPrudy_5 = <b>6</b>,'
                              '\nPrudy_6 = <b>7</b>,'
                              '\nPrudy_7 = <b>8</b>,'
                              '\nPrudy_8 = <b>9</b>,'
                              '\nPrudy_9 = <b>10</b>,'
                              '\nPrudy_10 = <b>11</b>,'
                              '\nPrudy_11 = <b>12</b>,'
                              '\nPrudy_100 = <b>13</b>,'
                              '\nPrudy_finish = <b>14</b>.', parse_mode='html')


@dp.message_handler(state=AdminState.select_user)
async def render_chat_id(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            user = db.select_user(message.text)
            data['id'] = user.id
            await message.answer(f'Никнейм пользователя: "{user.nickname}"\n\n'
                                 f'chat_id: "{user.chat_id}"\n'
                                 f'Возраст: "{user.age}"\n'
                                 f'Уровень: "{user.level}"\n'
                                 f'Текущее состояние: "{user.user_state}"',
                                 reply_markup=change_user_state)

    except TypeError:
        await message.answer('Такой пользователь не найден в базе данных!')


@dp.message_handler(state=AdminState.change_user_state)
async def change_user_state_f(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        dict_values = {1: 'Prudy_1',
                       2: 'Prudy_Pay',
                       3: 'Prudy_2',
                       4: 'Prudy_3',
                       5: 'Prudy_4',
                       6: 'Prudy_5',
                       7: 'Prudy_6',
                       8: 'Prudy_7',
                       9: 'Prudy_8',
                       10: 'Prudy_9',
                       11: 'Prudy_10',
                       12: 'Prudy_11',
                       13: 'Prudy_100',
                       14: 'Prudy_finish'}
        if int(message.text) in range(1, 14):
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
            await message.answer('Состояние пользователя успешно изменено!', reply_markup=admin_kb2)


@dp.callback_query_handler(state=None)
async def render_call(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'test':
        await callback.message.edit_text(text='<b>🐙Здравствуйте, вы попали в "QuestZombie".🧟‍♀️🧟‍♂️🧟‍♂️'
                                              '\nТут вы попадаете в мир где люди 25 лет живут в метро.Ⓜ️'
                                              '\nВойна поглотила всех, остались только проигравшие.⚔️ '
                                              '\nГлавные герои больше не могут сидеть в метро и вынуждены выйти на '
                                              'свободу, где знакомятся с новыми людьми и их миром.☢️'
                                              '\n \n    <em>🐙Пройти квест ---> /Chistye_prudy</em></b>'
                                              '\n \n \n<a href="https://t.me/QuestStreetBot">'
                                              '<b>Выбрать другой квест.</b></a>',
                                         parse_mode='html', disable_web_page_preview=True)
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
            await callback.message.edit_text('Выберите пользователя из меню ниже или напишите сюда его chat_id',
                                             reply_markup=admin_select_user)
            await AdminState.select_user.set()


@dp.message_handler(commands=["Chistye_prudy"])
async def start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        photo_prudy_0 = InputFile("Prudy0.jpg", 'rb0')
        messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_prudy_0))
        messages.append(await message.answer("<b>🐙Добро пожаловать в Quest Street на Чистые пруды.\n "
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
        await InputWhatever.Prudy_1.set()
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Prudy_1)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Prudy_1', message.from_user.id)
        if message.text.lower() == "go":
            photo_prudy_1 = InputFile("Prudy1.png", 'rb1')
            await InputWhatever.Prudy_Pay.set()
            messages.append(await message.answer("<b>🐙Начало.</b>", parse_mode="html"))
            messages.append(await message.answer('🐙<em>Стас прибегает на базу, поднимая всех на уши.'
                                                 '</em>', parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Наташа, крысы прогрызли нашу трубу, "
                                                 "теперь по рельсам течет наша вода. \n"
                                                 "я боюсь, мы не в состоянии ее залатать.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Крысы, вечное терпение Рейха, отсутствие"
                                                 " квалифицированных рук, "
                                                 "а теперь еще и водопровод продырявили, наши дети не заслужили"
                                                 " все это.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Я знаю, что ты не хотела покидать метро, "
                                                 "но я боюсь, что это уже не предложение, "
                                                 "а единственный способ выжить, как бы это не звучало."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Наташа бьёт в колокол, созывая всех на собрание."
                                                 "</em>", parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_prudy_1))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Друзья, плохие вести, к всем нашим проблемам "
                                                 "добавилась еще одна,"
                                                 " мы лишились водопровода, а запасов воды, еды хватит на неделю, "
                                                 "предложить что-то "
                                                 "другим станциям мы не можем, а рассчитывать на их милосердие глупо, "
                                                 "мне не приятно это"
                                                 " говорить, но нам нужно собирать вещи, оружие и выходить наружу.\nПо "
                                                 "слухам, уже как два "
                                                 "года люди выходят туда, но возвращаются, потому что тут безопаснее, "
                                                 "но, боюсь, не для нас.\n"
                                                 "</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Стас</u>:\n<b>На улице сейчас должно быть лето, "
                                                 "я думаю, что нам месяца хватит,"
                                                 " чтоб адаптироваться.\nТем более, сейчас будет лучшее время для "
                                                 "переезда.\n"
                                                 "Всем 2 часа на сбор, берите самое необходимое!"
                                                 "</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Задача - найти памятник Грибоедова.\nКто его отливал?\n"
                                                 "              Только фамилия.</em>", parse_mode="html"))
        elif message.text.lower() == '🚪':
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await state.finish()
                await message.answer('<b>🐙 🫱 <code>1219523153</code> 🫲 или напишите назад.</b>', parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
            data["number"] = message.text
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙go'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: go'))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQ"
                                                           "ADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Prudy_Pay)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Prudy_Pay', message.from_user.id)
    if message.from_user.id in ADMIN_IDS and message.text == '/skip8998':
        await message.answer('🐙Вы успешно пропустили процесс оплаты.\n'
                             'Напишите 🫱 <code>Лукьянов</code> 🫲.', parse_mode='html')
        await InputWhatever.Prudy_2.set()
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == 'назад':
        await InputWhatever.Prudy_1.set()
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        user_id = message.from_user.id
        await message.answer(f"Ваш ID TG: <code>{user_id}</code>", parse_mode='html')
        await message.answer('<b>🐙   Если у вас возникли проблемы с оплатой:</b>\n'
                             '1. Напишите "Назад" затем, напишите "go" и попробуйте оплатить еще раз.\n'
                             '2. Попробуйте оплатить другой картой.\n'
                             '3. Если это не помогло, то пишите \n🐙---> https://t.me/glebmehrykov\n'
                             '      Пишите: \n              1.В чем трудность.\n              2.Какой квест. \n    '
                             '          3.Ваш ID TG. Узнать его можно в '
                             '\n                                <a href="https://t.me/QuestStreetBot">Главном меню</a>.'
                             '\nИли скопировать сверху.\n '
                             '\n<b>🐙    Если вам нужна подсказка к квесту.</b>\n'
                             ' \n<em>               Эта информация будет возле памятника</em>.', parse_mode='html')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Тут должен быть ответ, но его не будет, видите ли, первая задача'
                             ' квеста достаточно простая, '
                             'при все это у вас есть подсказка, и я уверен, что вы справитесь с этой задачей.\n'
                             'После оплаты квеста вам будут доступны ответы, но чтобы оплатить, вам нужно пройти '
                             'первую задачу, а чтобы ее пройти, нужно приехать и разгадать ее.\n'
                             '<b>Все квесты по 1500р.</b>', parse_mode='html')
    elif message.text.lower() == '🚪':
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await state.finish()
            await message.answer('<b>🐙 🫱 <code>1219523153</code> 🫲 или напишите назад.</b>', parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'глеб, дай скидку!🙏🏻':
        await bot.send_message(message.from_user.id, '🐙Оплатите подписку, для того чтобы продолжить работу бота')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста',
                               description='🐙Оплата для того, чтобы пройти квест!',
                               provider_token="390540012:LIVE:40342",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=300 * 100)])
    elif message.text.lower() == 'гилшод' or message.text.lower() == 'гилшот':
        await bot.send_message(message.from_user.id, '🐙Оплатите подписку, для того чтобы продолжить работу бота')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста',
                               description='🐙Оплата для того, чтобы пройти квест!',
                               provider_token="390540012:LIVE:40342",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=1200 * 100)])
    else:
        await bot.send_message(message.from_user.id, '🐙Оплатите подписку, для того чтобы продолжить работу бота')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста',
                               description='🐙Оплата для того, чтобы пройти квест!',
                               provider_token="390540012:LIVE:40342",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=1500 * 100)])


@dp.pre_checkout_query_handler(state=InputWhatever.Prudy_Pay)
async def process_precheck(precheck: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(precheck.id, ok=True)


@dp.message_handler(content_types=[types.ContentType.SUCCESSFUL_PAYMENT], state=InputWhatever.Prudy_Pay)
async def successful_payment(message: types.Message):
    if message.successful_payment.invoice_payload == 'buy_sub':
        await bot.send_message(message.from_user.id, '<b>🐙Вы успешно оплатили доступ к боту.💸</b>\n'
                                                     'Напишите ответ на предыдущий вопрос.', parse_mode='html')
        await InputWhatever.Prudy_2.set()


@dp.message_handler(state=InputWhatever.Prudy_2)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        d1 = datetime.now()
        data['start_time'] = d1
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Prudy_2', message.from_user.id)
        if message.text.lower() == 'лукьянов':
            photo_prudy_2 = InputFile("Prudy2.jpg", 'rb2')
            await message.answer(d1.strftime("%H:%M:%S"))
            data["number"] = message.text
            messages.append(await message.answer("<b>🐙Таймер на прохождение квеста запущен."
                                                 "</b>", parse_mode="html"))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_prudy_2))
            messages.append(await message.answer("<u>Гоша</u>:\n<b>О, что это, такой свет, как будто на нас "
                                                 "светит поезд?</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Гоша, это солнце, я тебе говорила про него"
                                                 ".</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Гоша</u>:\n<b>Ма, да, но, я и представить себе не мог такое.\n"
                                                 "Я не могу даже голову повернуть к выходу.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Тише, я не хочу столкнуться с проблемой, не "
                                                 "выйдя из метро,"
                                                 " в общем шепотом и по делу.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Выходят из метро.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>О... я была тут лет так 25 тому назад."
                                                 "\nЯ и не думала, что город может быть таким "
                                                 "красивым и зеленным, я представляла его серым, разбитым,"
                                                 " а тут джунгли.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Смотрите, вот и зомбак стоит на тротуаре, "
                                                 "я думал, что их будет больше, "
                                                 "ладно давайте пойдем по прямой, вроде их не наблюдаю."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Проходят вперед.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Тут вообще зомби то и нет, "
                                                 "осмотритесь, странно это все, неужто вымерли."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - найдите источник музыки.</em>", parse_mode="html"))
            await InputWhatever.Prudy_3.set()
        elif message.text.lower() == '🚪':
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await state.finish()
                await message.answer('<b>🐙 🫱 <code>1219523153</code> 🫲 или напишите назад.'
                                     '</b>', parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Эта информация будет возле памятника.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Лукьянов</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.764526, longitude=37.639358))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEb"
                                                           "bPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))

        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Prudy_3)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Prudy_3', message.from_user.id)
        if message.text.lower() == 'поющий журавль':
            photo_prudy_3 = InputFile("Prudy3.jpg", 'rb3')
            photo_prudy_4 = InputFile("Prudy4.jpg", 'rb4')
            db.new_level(message.chat.id)
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_prudy_3))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Фонтан на удивление чист и работает, "
                                                 "не думаю, что эту зеленую "
                                                 "воду можно пить, но за ним явно кто-то ухаживает."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Гоша находит кран.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Гоша</u>:\n<b>Ма, смотри, что это?</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Это кран, он отвечает за напор воды, если его "
                                                 "повернуть, то вода перестанет идти.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Гоша поворачивает кран и фонтан перестает работать."
                                                 "</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Наташа, у меня плохое предчувствие, ты "
                                                 "слышишь это?</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Что? Я ничего не слышу."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Вот именно, а раньше слышала,"
                                                 " а значит, звуки поменялись, "
                                                 "и чувство безопасности пропало напрочь."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Ой, то есть, по этому зомби тут и не"
                                                 " ходят, потому что обходят эти звуки, "
                                                 "а сейчас для них тут играет музыка, и они попрут сюда.\n"
                                                 "Нужно срочно уходить отсюда.</b>", parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_prudy_4))
            messages.append(await message.answer("<b>Маршрут - вы смотрите на журавля, сзади на вас бегут"
                                                 " зомби, справа стоит"
                                                 " статуя, оттуда тоже бегут зомби, вы идете левее к дороге.\n"
                                                 "С права идут зомби, с пруда тоже идут зомби, вы выбираете "
                                                 "безопасный маршрут.\n"
                                                 "Слева идут зомби.</b>", parse_mode="html"))
            messages.append(await message.answer("🐙<em>Задача - найдите большое железное, похоже на цветок, "
                                                 "что под ним?</em>",
                                                 parse_mode="html"))
            await InputWhatever.Prudy_4.set()
        elif message.text.lower() == '🚪':
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await state.finish()
                await message.answer('<b>🐙 🫱 <code>1219523153</code> 🫲 или напишите назад.</b>', parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await state.finish()
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Идите дальше и доверьтесь интуиции.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Поющий журавль</code> 🫲. ',
                                                 parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.762332, longitude=37.643630))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Prudy_4)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Prudy_4', message.from_user.id)
        if message.text.lower() == 'лестница':
            photo_prudy_5 = InputFile("Prudy5.png", 'rb5')
            data["number"] = message.text
            messages.append(await message.answer("<u>Стас</u>:\n<b>Бегом, бегом, во дворах должно быть"
                                                 " безопаснее, чем в парке!</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Заходят во двор, видят лестницу на крышу."
                                                 "</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Быстро, залазим на крышу, я прикрою."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Давайте ребята, быстрее."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Стас, имея мачете, отбивается от зомби."
                                                 "\nВсе залезли на крышу."
                                                 "</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Стас, милый мой, давай к нам!"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Стас пытается найти момент, чтобы добраться "
                                                 "до лестницы, отходит в другой "
                                                 "конец двора, встает на мусорный бак и кричит, чтобы все зомби"
                                                 " сошлись возле него, "
                                                 "когда зомби подходят так близко, что начинают забираться к нему, "
                                                 "он выпрыгивает им "
                                                 "на голову и как по пенькам ловко проходит через толпу, "
                                                 "но на последней голове "
                                                 "теряет равновесие и спотыкается. Зомби быстро переключаются на него, "
                                                 "Стас не теряя время, восстанавливает координацию, оббегает двор, "
                                                 "чтобы зомби опять"
                                                 " ушли в другой конец, и оттуда бежит к лестнице.\n"
                                                 "Успешно забирается.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Ты наш герой! Все в порядке?"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Вроде да.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Осматривают крышу, видят под козырьком, лижет тело,"
                                                 " подходят ближе.</em>",
                                                 parse_mode='html'))
            messages.append(await message.answer("<u>Гоша</u>:\n<b>Смотрите, у него на шее укус, но он не выглядит, "
                                                 "как те обглоданные зомби.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Да, его укусили, но мозги, я думаю, он "
                                                 "сам себе вышиб.\n"
                                                 "Нужно его обыскать, как минимум пистолет нам пригодится."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Находят камень, который придерживает картонку, убирают его."
                                                 "</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Стас, по моему, я нашла какой-то текст."
                                                 "\nТут похоже предсмертная записка.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>👤Я был в группе «Зонт», наш командир Павел, повел нас на"
                                                 " разведку местности, где мы "
                                                 "встретились с рейховцами, командира и его сына убили, его друг "
                                                 "Петр тоже был убит, "
                                                 "остальные члены группы разбежались, из-за выстрелов сбежались "
                                                 "зомби, к сожалению мне"
                                                 " не удалось забраться на крышу до того, как меня укусили,"
                                                 " попав на крышу, я понял, что домой возвращаться нельзя, а"
                                                 " становиться зомбаком "
                                                 "я не хотел. Прости меня, Господи.<b>Аминь</b>."
                                                 "</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Чертовы рейховцы,"
                                                 " и тут свою монополию крутят.\nСмотрите, он пишет, \"домой\", "
                                                 "значит, где-то тут есть их дом, и я не думаю, что далеко, "
                                                 "нужно найти где они живут,"
                                                 " я читаю его предсмертную записку и не вижу в нем опасности, "
                                                 "тем более выбор у нас "
                                                 "не большой.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - в истории заложен квест. Найдите их дом"
                                                 ".</em>", parse_mode="html"))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_prudy_5))
            await InputWhatever.Prudy_5.set()
        elif message.text.lower() == '🚪':
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await state.finish()
                await message.answer('<b>🐙 🫱 <code>1219523153</code> 🫲 или напишите назад.</b>', parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Если бы вас окружили, куда бы вы бежали?'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Лестница</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.761777, longitude=37.642145))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI"
                                                           "_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Prudy_5)
async def get_number(message: types.Message, state: FSMContext):
    async with (state.proxy() as data):
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Prudy_5', message.from_user.id)
        if message.text.lower() == 'собор петра и павла' or message.text.lower() == 'собор павла и петра':
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Задача - возле собора будет пожарная охрана.\n"
                                                 "Напишите точное время?\n</em><b>Формат ответа '01:01'</b>",
                                                 parse_mode="html"))
            await InputWhatever.Prudy_6.set()
        elif message.text.lower() == '🚪':
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await state.finish()
                await message.answer('<b>🐙 🫱 <code>1219523153</code> 🫲 или напишите назад.</b>', parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Сконцентрируйте внимание на предсмертной записке, '
                                                 'там есть три связующих элемента.\nБез Яндекс карты, вам не пройти.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Собор Петра и Павла</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.756506, longitude=37.641192))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQX"
                                                           "zwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Prudy_6)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Prudy_6', message.from_user.id)
        if (message.text.lower() == '05:04' or
                message.text.lower() == '17:04'):
            photo_prudy_6 = InputFile("Prudy6.png", 'rb6')
            photo_prudy_7 = InputFile("Prudy7.png", 'rb7')
            data["number"] = message.text
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Я думаю, стоит переждать этот день, к утру, я"
                                                 " надеюсь, они рассосутся.\nВыйдем завтра утром."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Утро.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Эй, встаем, я сегодня прогулялся по"
                                                 " крыши и видел дым, он шел из трубы какой-то "
                                                 "церкви или храма, я думаю, стоит сходить туда."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Собираемся. Собираемся в полной тишине, "
                                                 "мы же не хотим проблем.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Спускаются, направляются в сторону храма.\n"
                                                 "Придя, стучат в дверь.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Ау, тут есть кто-нибудь?"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Жендос</u>:\n<b>Кто там?!</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Выходит дед с двухстволкой.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Прошу, не стреляйте, мы с "
                                                 "добрыми намерениями, с нами ребенок.\n"
                                                 "Мы вышли из метро, наша станция  «Чистые пруды», "
                                                 "крысы прогрызли трубопровод, и "
                                                 "мы остались без воды.</b>", parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_prudy_6))
            messages.append(await message.answer("<u>Жендос</u>:\n<b>Слава Богу, вы не с Рейха, а то это "
                                                 "кровопийцы нам покоя не дают.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Вы тут один живете?</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Жендос</u>:\n<b>Не, что вы, у нас тут группа, только группа "
                                                 "вышла на разведку и не вернулась.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Может мне поискать их, "
                                                 "а группа пока тут посидит?\n"
                                                 "Скажем, в честь нового союза.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Жендос</u>:\n<b>Это не плохая идея.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Без меня?\nНе, это ужасная идея, "
                                                 "я с тобой.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Но куда они отправились?"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Жендос</u>:\n<b>Да, сложно сказать, у них карта с собой.\n"
                                                 "Но место им это нравилось, напоминало молодые учебные годы,"
                                                 " хотя все остальные "
                                                 "предпочитали обходить стороной, поговаривают, "
                                                 "что там водятся призраки.\nМало нам зомби, "
                                                 "еще и призраков не хватало.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Стас и Наташа идут искать местность.</em>", parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_prudy_7))
            messages.append(await message.answer("<em>🐙Задача - напишите место.</em>", parse_mode="html"))
            await InputWhatever.Prudy_7.set()
        elif message.text.lower() == '🚪':
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await state.finish()
                await message.answer('<b>🐙 🫱 <code>1219523153</code> 🫲 или напишите назад.</b>', parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Вам нужно найти МЧС, и осмотреться.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>17:04</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.757149, longitude=37.641786))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI"
                                                           "_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Prudy_7)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Prudy_7', message.from_user.id)
        if message.text.lower() == 'заброшенное общежитие':
            photo_prudy_8 = InputFile("Purdy8.png", 'rb8')
            data["number"] = message.text
            messages.append(await message.answer("<u>Стас</u>:\n<b>Эй, Наташа, там вроде как жизнь кипит,"
                                                 " да и чуваки крутые, "
                                                 "как ты думаешь, это могут быть те, кого мы ищем?"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Сзади выпрыгивает Сталкер и оглушает обоих "
                                                 "волыной.</em>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Их связывают, приводят в логово, "
                                                 "будят.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Косарь</u>:\n<b>Вы бессмертные что-ли?\n"
                                                 "Ходить с пистолетом и двумя патронами, вы как тут оказались?"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Мы поднялись со станции  «Чистые пруды»"
                                                 ".</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Смотрящий</u>:\n<b>Слышал про эту станцию, говорили, что"
                                                 " не повезло им с местом и людьми, "
                                                 "постоянно прессовали их там.\nБезобидные должны быть.\n"
                                                 "Че вышли то?</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Скажем, условия для жизни там закончились."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Смотрящий</u>:\n<b>Косарь, отпусти их, та они мухи не обидят."
                                                 "\nВы тут в 2-м или еще с кем то?</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>У нас группа из шесть человек, мы нашли "
                                                 "собор, в котором живет старик, он нас и принял,"
                                                 " так же старик сказал, что у него есть группа, "
                                                 "которая вышла на разведку, "
                                                 "но так и не вернулась, а мы пошли их искать."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Косарь</u>:\n<b>А Жендос не сказал, как давно они ушли?"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Нет.</b>", parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_prudy_8))
            messages.append(await message.answer("<u>Косарь</u>:\n<b>Мы уже больше месяца покинули собор, "
                                                 "нас он задолбал, в этом мире зомби стали обычным"
                                                 " делом, они медленные, тупые, их никто не боится, тут проблема в"
                                                 " припасах, еда, вода.\n"
                                                 "Ну, я хочу сказать, что вам крупно повезло, что именно мы вас "
                                                 "нашли, иначе шлепнули вас"
                                                 " и даже рот бы открыть не успели.\n"
                                                 "У нас тут как бы свободное общество, чем то напоминает капитализм"
                                                 " в нынешних реалиях, "
                                                 "тут есть смотрящие, они всем рулят.\nОни берут с каждого, кто тут "
                                                 "присутствует:\n"
                                                 "3 пачки сигарет, 3 банки воды и консервы или ее аналог, "
                                                 "а так же свиней, патроны.\nВсе "
                                                 "принимают в оплату.\nЗа это они держат тут строгие правила.\n"
                                                 "Каждый сам за себя, если это твое, то только твоё, ни кто тебя не "
                                                 "ограбит, но и ни кто"
                                                 " тебе руку помощи не даст, ходим мы в месте, но если кто-то отстал, "
                                                 "то это его проблемы.\nНам выгодно иметь людей, но не выгодно "
                                                 "заботиться об их проблемах."
                                                 "\nСлаб - пошел вон, не можешь платить - пошел вон"
                                                 ".</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Смотрящий</u>:\n<b>Чем платить будите? "
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Так у нас все добро в собор."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Смотрящий</u>:\n<b>Ну тогда не смею вас больше задерживать."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - найдите в парке что-то похожее на антенну, "
                                                 "какого она цвета?\n"
                                                 "</em>", parse_mode="html"))
            await InputWhatever.Prudy_8.set()
        elif message.text.lower() == '🚪':
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await state.finish()
                await message.answer('<b>🐙 🫱 <code>1219523153</code> 🫲 или напишите назад.</b>', parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Где стены усталы от пустоты и грусти,\n'
                                                 'Там тихо живут призраки давно минувших дней.\n'
                                                 'Пыль и запах старины захватывают воздух,\n'
                                                 'Оно воплощается в чахлые коридоры свои.\n'
                                                 'Однажды шумно было в этом здании,\n'
                                                 'Молодые голоса, смех и песни звучали.\n'
                                                 'Но сегодня остались одни лишь отголоски,\n'
                                                 'Где властвуют молчание и пустота,\n'
                                                 'независимо от времени.\n'
                                                 'В радиусе 500м.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Заброшенное общежитие</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.755474, longitude=37.636808))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Prudy_8)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Prudy_8', message.from_user.id)
        if message.text.lower() == 'красный':
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Вбегает Сталкер и начинает громко рассказывать о находке.\n"
                                                 "Стас и Наташа остаются послушать.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Разведчик</u>:\n<b>Я нашел клад, всем хватит! Это корабль, "
                                                 "возможно, он не заправлен, если решить как-"
                                                 "то эту проблему, то мы сможем отплыть от Москвы куда подальше, "
                                                 "на сколько я знаю карту,"
                                                 " там будет маленький лагерь рейхов, нам хватит винтовок,"
                                                 " чтобы убрать всех при первом повороте.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Косарь</u>:\n<b>Бензин закончился еще лет сто назад, "
                                                 "забудь.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Господа, я пять лет провел на военном флоте, "
                                                 "разбираюсь в суднах, "
                                                 "судно может проплыть на любом горючем, что имеет более 80% спирта"
                                                 ".</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Смотрящий</u>:\n<b>Ха, этого у нас добра хватает, что-что,"
                                                 " а спирт мы с"
                                                 " первого дня Нового мира начали делать.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Но судно так проживет не долго, но уплыть"
                                                 " сможем.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Косарь</u>:\n<b>Это главное.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Смотрящий</u>:\n<b>Тогда план такой - всем на сборы 2ч, "
                                                 "выдвигаемся к вечеру, до заката нужно отплыть.</b>",
                                                 parse_mode='html'))
            messages.append(await message.answer("🐙<em>Задача -  12-13век,  вы пришли на рынок, выбрали "
                                                 "ряд и встали в очередь.\n"
                                                 "Что за место?</em>", parse_mode="html"))
            await InputWhatever.Prudy_9.set()
        elif message.text.lower() == '🚪':
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await state.finish()
                await message.answer('<b>🐙 🫱 <code>1219523153</code> 🫲 или напишите назад.</b>', parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Прогуляйтесь по парку.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Красный</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.755606, longitude=37.635735))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Prudy_9)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Prudy_9', message.from_user.id)
        if message.text.lower() == 'парк зарядье' or message.text.lower() == 'зарядье':
            photo_prudy_9 = InputFile("Prudy9.png", 'rb9')
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_prudy_9))
            messages.append(await message.answer("<u>Косарь</u>:\n<b>Что, так просто, пришли, сели, поплыли?"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Смотрящий</u>:\n<b>Сейчас узнаем.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - в парке, найдите памятник зодчества, "
                                                 "тот, что ближе к воде.\n"
                                                 "Его название?</em>", parse_mode="html"))
            await InputWhatever.Prudy_10.set()
        elif message.text.lower() == '🚪':
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await state.finish()
                await message.answer('<b>🐙 🫱 <code>1219523153</code> 🫲 или напишите назад.</b>', parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Раньше это место было рынком, и рынок состоял из рядов, '
                                                 'люди заходили туда толпами и эта'
                                                 ' ситуация стала названием места.\n'
                                                 'Сейчас конечно рынка нет, но название осталось прежним.\n'
                                                 ' \n🐙Если этой подсказки мало, напишите "🆘" и я дам вам еще одну.'))
        elif message.text.lower() == '🆘' or message.text.lower() == 'sos':
            messages.append(await message.answer('🐙Давайте вспомним сюжетную линию, за чем мы идем?'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Парк Зарядье</code> 🫲. ', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.750973, longitude=37.628370))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI"
                                                           "_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Prudy_10)
async def get_number(message: types.Message, state: FSMContext):
    async with (state.proxy() as data):
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Prudy_10', message.from_user.id)
        if (message.text.lower() == 'церковь зачатия святой анны'
                or message.text.lower() == 'храм зачатия анны'):
            photo_prudy_10 = InputFile("Prudy10.png", 'rb10')
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Стас заводит корабль, но срабатывает сигнализация."
                                                 "</em>", parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_prudy_10))
            messages.append(await message.answer("<u>Косарь</u>:\n<b>Что за дела, это корыто сейчас "
                                                 "всех сюда приведет, "
                                                 "решай эту задачу, сними сигнализацию.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Нужно время, отбивайтесь."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - так, открываем щиток, я вижу четыре провода. "
                                                 "\nКрасный, синий, желтый, белый,"
                                                 " но сигнализация работает от зеленого.\nКакой провод нужно отрезать,"
                                                 " чтоб выключить сигнализацию.</em>", parse_mode="html"))
            await InputWhatever.Prudy_11.set()
        elif message.text.lower() == '🚪':
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await state.finish()
                await message.answer('<b>🐙 🫱 <code>1219523153</code> 🫲 или напишите назад.</b>', parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Памятник является старинной постройкой.\nНапишите его название.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Церковь зачатия святой Анны</code> 🫲.'
                                                 '', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.750187, longitude=37.630904))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Prudy_11)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Prudy_11', message.from_user.id)
        if (message.text.lower() == 'желтый и синий'
                or message.text.lower() == 'синий и желтый'
                or message.text.lower() == 'желтый синий'
                or message.text.lower() == 'синий желтый'
                or message.text.lower() == 'жёлтый и синий'
                or message.text.lower() == 'синий и жёлтый'
                or message.text.lower() == 'жёлтый синий'
                or message.text.lower() == 'синий жёлтый'):
            photo_prudy_11 = InputFile("Prudy11.png", 'rb11')
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Отстреливаются от зомби.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Смотрящий</u>:\n<b>Быстрее, быстрее, залазим на борт."
                                                 " Все тут?</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Да, Все!</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Косарь</u>:\n<b>Тогда, поднимаем трамп."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Наташа</u>:\n<b>Благо черепушки не плавают."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Стас</u>:\n<b>Господа, куда путь держим?"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Смотрящий</u>:\n<b>Подальше от этого места."
                                                 "</b>", parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_prudy_11))
            await message.answer("<b>🐙Конец.©</b>", parse_mode='html', reply_markup=finish)
            await InputWhatever.Prudy_finish.set()
        elif message.text.lower() == '🚪':
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await state.finish()
                await message.answer('<b>🐙 🫱 <code>1219523153</code> 🫲 или напишите назад.</b>', parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            await bot.send_message(message.chat.id, random.choice(responses))
        elif message.text.lower() == 'зеленый':
            messages.append(await message.answer('Вообще то верно, но только вы его видите, но подлезть туда не можете.'
                                                 '\nНайдите другой способ.'))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Соедините.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Желтый и синий</code> 🫲.', parse_mode='html'))
        elif message.text.lower() == 'белый':
            photo_prudy_100 = InputFile("Prudy100.jpg", 'rb100')
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_prudy_100))
            messages.append(await message.answer('🐙Вы отрезали не тот провод, корабль не пригоден.\nЗомби вас окружили,'
                                                 ' идти вам не куда, патроны заканчиваются, половину ваших друзей '
                                                 'уже жрут.\n'
                                                 ' Гоша вот-вот превратится в зомби, его мать этого не выдерживает и '
                                                 'пускает мозги '
                                                 'по ветру. Вы допустили ошибку☠️.\n Но, благо, что вы сохранились, и'
                                                 ' сейчас идет загрузка.'))
            messages.append(await message.answer('<em>🐙Загрузка завершена.</em>\n \n Только не режьте белый '
                                                 'провод.', parse_mode='html'))
        elif message.text.lower() == 'красный':
            photo_prudy_101 = InputFile("Prudy101.jpg", 'rb101')
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_prudy_101))
            messages.append(await message.answer('🐙Вы отрезали не тот провод, корабль не пригоден. \n'
                                                 'Зомби вас окружили, '
                                                 'идти вам не куда, патроны заканчиваются, половину ваших '
                                                 'друзей уже жрут.\n'
                                                 'Гоша вот-вот превратится в зомби, его мать этого не выдерживает и'
                                                 ' пускает мозги '
                                                 'по ветру. Вы допустили ошибку☠️. \nНо, благо, что вы сохранились, и'
                                                 ' сейчас идет загрузка.'))
            messages.append(await message.answer('<em>🐙Загрузка завершена.\n \n</em> Только не режьте красный '
                                                 'провод.', parse_mode='html'))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbb"
                                                           "PMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Prudy_100)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Prudy_100', message.from_user.id)
    if (message.text.lower() == 'answer'
            or message.text.lower() == 'help'):
        async with state.proxy() as data:
            data["number"] = message.text
            if 'messages' in data.keys():
                messages = data['messages']
            else:
                messages = []
            await InputWhatever.Prudy_2.set()
            messages.append(await message.answer('🐙<em>Нажмите 🫱 <code><u>Лукьянов</u></code>. 🫲 '
                                                 '\nИ отправьте ответ Боту.</em>',
                                                 parse_mode='html'))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Prudy_finish)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Prudy_finish', message.from_user.id)
    async with state.proxy() as data:
        if 'messages' in data.keys():
            for msg in data['messages'][::-1]:
                try:
                    await msg.delete()
                except Exception:
                    pass
        if message.text.lower() == "🐙конец" or message.text.lower() == "конец":
            mp3_prudy = InputFile('Prudy.mp3', 'Конец')
            await bot.send_audio(chat_id=message.chat.id, audio=mp3_prudy)
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
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲 или напишите назад.</b>', parse_mode='html')
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
