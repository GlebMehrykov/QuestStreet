import random
from datetime import datetime

import aiogram.utils.exceptions
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile

import AIP_Agent
from db import Database
from keybords import *

bot = Bot(token=AIP_Agent.TELEGRAM_BOT)
db = Database("2.db")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db.create_table_users()
responses = ['🐙Да, да.', '🐙Прювет', "🐙Как ты там?", '🐙Кто выпил весь ром!', "🐙На абордаж", "🐙Ну чего тебе?",
             '🐙Как долго ты готов(а) со мной общаться?', "🐙А это забавно."]
ADMIN_IDS = [1219523153, 6522187160]


class AdminState(StatesGroup):
    select_user = State()
    change_user_state = State()

class InputWhatever(StatesGroup):
    Agent_1 = State()
    Agent_Pay = State()
    Agent_2 = State()
    Agent_3 = State()
    Agent_4 = State()
    Agent_5 = State()
    Agent_6 = State()
    Agent_7 = State()
    Agent_8 = State()
    Agent_9 = State()
    Agent_10 = State()
    Agent_11 = State()
    Agent_12 = State()
    Agent_13 = State()
    Agent_100 = State()
    Agent_finish = State()


@dp.callback_query_handler(state=InputWhatever.Agent_finish)
async def ikb_cb_handler(callback: types.CallbackQuery):
    await callback.answer('🐙ИИ меня не устраивает, вакансия открыта, пишите.')


@dp.message_handler(commands=['start'], state=[AdminState, None])
async def start_command(message: types.Message, state: FSMContext):
    db.insert_user(message.from_user.id)
    await state.finish()
    db.update_user_state('start', message.from_user.id)
    if message.from_user.id in ADMIN_IDS:
        await message.answer('<b>🐙🫱 <code>1219523153</code> 🫲 или Выберите одну из функций ниже:</b>', parse_mode='html')
        await bot.send_message(message.from_user.id,
                               '1. Смена состояния\n'
                               '2. Запустить бота',
                               reply_markup=admin_kb)
    else:
        await message.answer(text='<b>Вы попал в квест "Тайный агент" наⓂ️Парк культуры.'
                                  '\nТут вы сможете '
                                  'почувствовать себя тайным агентом, которому выпало не простое задание.   😎'
                                  '\nТакже пройти интересные задания.       📖'
                                  '\nПрогуляться по интересным закоулка Москвы.     🚶‍♂️'
                                  '\nВступить в флирт.          ❤️‍🔥'
                                  '\nПосетить интересное заведение.         🏛'
                                  '\n \n    <em>🐙Пройти квест ---> /Secret_Agent</em></b> '
                                  '\n \n \n<a href="https://t.me/QuestStreetBot"><b>Выбрать другой квест.</b></a>',
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
                    InlineKeyboardButton('<<< Предыдущая', callback_data='previous'),
                    InlineKeyboardButton('Следующая >>>', callback_data='next')
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
        await call.message.edit_text('🐙Выберите пользователя из меню ниже или напишите сюда его chat_id',
                                     reply_markup=admin_select_user)


@dp.callback_query_handler(text='change_state', state=[None, AdminState])
async def select_new_state(call: types.CallbackQuery):
    await AdminState.change_user_state.set()
    await call.message.answer('<b>🐙Напишите номер нового состояния из списка ниже.</b>\n'
                              '<em>Формат списка: состояние = номер состояния.</em>'
                              '\nAgent_1 = <b>1</b>,'
                              '\nAgent_Pay = <b>2</b>,'
                              '\nAgent_2 = <b>3</b>,'
                              '\nAgent_3 = <b>4</b>,'
                              '\nAgent_4 = <b>5</b>,'
                              '\nAgent_5 = <b>6</b>,'
                              '\nAgent_6 = <b>7</b>,'
                              '\nAgent_7 = <b>8</b>,'
                              '\nAgent_8 = <b>9</b>,'
                              '\nAgent_9 = <b>10</b>,'
                              '\nAgent_10 = <b>11</b>,'
                              '\nAgent_11 = <b>12</b>,'
                              '\nAgent_12 = <b>13</b>,'
                              '\nAgent_13 = <b>14</b>,'
                              '\nAgent_100 = <b>15</b>,'
                              '\nAgent_finish = <b>16</b>.',
                              parse_mode='html')


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
        await message.answer('🐙Такой пользователь не найден в базе данных!')


@dp.message_handler(state=AdminState.change_user_state)
async def change_user_state_f(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        dict_values = {1: 'Agent_1',
                       2: 'Agent_Pay',
                       3: 'Agent_2',
                       4: 'Agent_3',
                       5: 'Agent_4',
                       6: 'Agent_5',
                       7: 'Agent_6',
                       8: 'Agent_7',
                       9: 'Agent_8',
                       10: 'Agent_9',
                       11: 'Agent_10',
                       12: 'Agent_11',
                       13: 'Agent_12',
                       14: 'Agent_13',
                       15: 'Agent_100',
                       16: 'Agent_finish'}
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
        await callback.message.edit_text(text='<b>🐙Вы попал в квест "Тайный агент" на Ⓜ️Парк культуры.'
                                              '\nТут вы сможете почувствовать себя тайным агентом, '
                                              'которому выпало не простое задание.   😎'
                                              '\nТакже пройти интересные задания.       📖'
                                              '\nПрогуляться по интересным закоулка Москвы.     🚶‍♂️'
                                              '\nВступить в флирт.          ❤️‍🔥'
                                              '\nПосетить интересное заведение.</b>         🏛'
                                              '\n  \n    <em>🐙Пройти квест ---> /Secret_Agent</em> '
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
            await callback.message.edit_text('🐙Выберите пользователя из меню ниже или напишите сюда его chat_id',
                                             reply_markup=admin_select_user)
            await AdminState.select_user.set()


@dp.message_handler(commands=["Secret_Agent"])
async def start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        photo_Agent0 = InputFile("Agent0.png", 'rb')
        db.update_user_state('Secret_Agent', message.from_user.id)
        messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_Agent0))
        messages.append(await message.answer("<b>🐙Добро пожаловать в Quest Street на Парк культуры.\n "
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
        messages.append(await message.answer("<b>🐙Если готовы пишите \"🫱 <code>go</code> 🫲\".</b>", parse_mode='html'))
        await InputWhatever.Agent_1.set()
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Agent_1)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        photo_Agent1 = InputFile("Agent1.jpg", 'rb1')
        db.update_user_state('Agent_1', message.from_user.id)
        if message.text.lower() == "go":
            data["number"] = message.text
            messages.append(await message.answer("<b>🐙Начало.</b>", parse_mode="html"))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_Agent1))
            messages.append(await message.answer('🐙<em>Рейс BR-802 New york - Москва, успешно приземлился,'
                                                 ' спасибо, что выбрали нашу авиалинию.\n'
                                                 'Flight BR-802 New york - Moscow, landed successfully,'
                                                 ' thank you for choosing our airline, thank you.'
                                                 '</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Связной</u>:\n<b>Агент, здравствуйте, с успешным '
                                                 'приземлением, скоро я вышлю всю информацию о вашем заказе,'
                                                 '\nСейчас вам нужно ехать к центру.\nБольше сказать не могу, '
                                                 'заказчик держит все в секрете '
                                                 'до последнего момента.\nЗнаю, это форма не соответствует нашим '
                                                 'стандартам, но ни чего '
                                                 'поделать не могу, заказчик платит в десять раз больше нужного, '
                                                 'вынуждены подчиниться.\n'
                                                 'Статус операции - красный уровень, '
                                                 'пять звезд.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Агент</u>:\n<b>Связной, вы знаете отношение моё к деньгам и '
                                                 'правилам.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Связной</u>:\n<b>Знаю, извините.\n'
                                                 'Все что я могу сказать это, как выйдите из аэропорта,'
                                                 ' обойдите его и сядьте на центральную лавку.</b>', parse_mode='html'))
            messages.append(await message.answer('<em>🐙Задача - как сядете на лавку, найдите число и напишите его.'
                                                 '</em>', parse_mode='html'))
            await InputWhatever.Agent_Pay.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('go'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('Ответ: 🫱 <code>go</code> 🫲', parse_mode='html'))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI"
                                                           "_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Agent_Pay)
async def get_number(message: types.Message):
    db.update_user_state('Agent_Pay', message.from_user.id)
    if message.from_user.id in ADMIN_IDS and message.text == '/skip8998':
        await message.answer('🐙Вы успешно пропустили процесс оплаты.\n'
                             'Напишите 🫱 <code>2/1</code> 🫲.', parse_mode='html')
        await InputWhatever.Agent_2.set()
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == 'назад':
        await InputWhatever.Agent_1.set()
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        user_id = message.from_user.id
        await message.answer(f"Ваш ID TG: <code>{user_id}</code>", parse_mode='html')
        await message.answer('<b>🐙   Если у вас возникли проблемы с оплатой:</b>\n'
                             '1. Напишите "назад" затем, напишите "go" и попробуйте оплатить еще раз.\n'
                             '2. Попробуйте оплатить другой картой.\n'
                             '3. Если это не помогло, то пишите \n🐙---> https://t.me/glebmehrykov\n'
                             '      Пишите: \n              1.В чем трудность.\n              2.Какой квест. \n    '
                             '          3.Ваш ID TG. Узнать его можно в '
                             '\n                                <a href="https://t.me/QuestStreetBot">Главном меню</a>.'
                             '\nИли скопировать сверху.'
                             '\n<b>🐙Если вам нужна подсказка то</b>:'
                             ' \nВам нужно найти аэропорт, в 300м от М.Парк победы есть подобие, '
                             'и там нужно найти 5 лавок, и сесть на центральную.'
                             '\nБез Яндекса далеко вы не уйдёте.'
                             '\nДавайте пройдемся по набережной, на карте.', parse_mode='html')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Тут должен быть ответ, но его не будет, видите ли, первая задача'
                             ' квеста достаточно простая, '
                             'при все это у вас есть подсказка, и я уверен, что вы справитесь с этой задачей.\n'
                             'После оплаты квеста вам будут доступны ответы, но чтобы оплатить, вам нужно пройти '
                             'первую задачу, а чтобы ее пройти, нужно приехать и разгадать ее.\n'
                             '<b>Все квесты по 1500р.</b>', parse_mode='html')
    elif message.text.lower() == 'глеб, дай скидку!🙏🏻':
        await bot.send_message(message.from_user.id, '🐙Особым игрокам, особая цена!')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста',
                               description='🐙Оплата для того, чтобы пройти квест!',
                               provider_token="390540012:LIVE:40346",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=300 * 100)])
    elif message.text.lower() == 'гилшод' or message.text.lower() == 'гилшот':
        await bot.send_message(message.from_user.id, '🐙Особым игрокам, особая цена!')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста',
                               description='🐙Оплата для того, чтобы пройти квест!',
                               provider_token="390540012:LIVE:40346",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=1200 * 100)])
    else:
        await bot.send_message(message.from_user.id, '<b>🐙Оплатите квест, для того чтобы продолжить '
                                                     'работу бота.</b>', parse_mode='html')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста',
                               description='🐙Оплата для того, чтобы пройти квест!',
                               provider_token="390540012:LIVE:40346",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=1500 * 100)])


@dp.pre_checkout_query_handler(state=InputWhatever.Agent_Pay)
async def process_precheck(precheck: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(precheck.id, ok=True)


@dp.message_handler(content_types=[types.ContentType.SUCCESSFUL_PAYMENT], state=InputWhatever.Agent_Pay)
async def successful_payment(message: types.Message):
    if message.successful_payment.invoice_payload == 'buy_sub':
        await bot.send_message(message.from_user.id, '<b>🐙Вы успешно оплатили доступ к боту.💸</b>\n'
                                                     'Напишите ответ еще раз или воспользуйтесь подсказками.',
                               parse_mode='html')
        await InputWhatever.Agent_2.set()


@dp.message_handler(state=InputWhatever.Agent_2)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        d1 = datetime.now()
        data['start_time'] = d1
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Agent_2', message.from_user.id)
        db.new_level(message.chat.id)
        if message.text.lower() == '2/1':
            photo_Agent2 = InputFile("Agent2.jpg", 'rb2')
            await message.answer(d1.strftime("%H:%M:%S"))
            data["number"] = message.text
            messages.append(await message.answer("<b>🐙Таймер на прохождение квеста запущен"
                                                 ".</b>", parse_mode="html"))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_Agent2))
            messages.append(await message.answer("<u>Связной</u>:\n<b>Агент, получена информация"
                                                 " о заказе.\nВаша цель убрать Варго,"
                                                 " этот человек относится к Русской элите. "
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Агент</u>:\n<b>Это очень высокая цель"
                                                 ".</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Связной</u>:\n<b>Да, по  информации, "
                                                 "Варго зазнался и перестал играть по правилам, "
                                                 "сейчас он имеет"
                                                 " большое влияние и город находится на 30% под "
                                                 "его контролем, можно считать, что каждая"
                                                 " третья камера, каждый третий человек в погонах "
                                                 "это его люди, такие высокие показатели "
                                                 "только у него. \nЗаказчик желает убрать его  в "
                                                 "течение сегодняшнего дня, без лишнего "
                                                 "шума, так что сегодня обойдетесь без оружия. \n"
                                                 "Заказчик желает убрать Варго токсичным"
                                                 " ядом, ваша задача найти конверт внутри которого "
                                                 "будет наше новое изобретение"
                                                 ", токсичный дым, необходимо, чтоб Варго вскрыл этот конверт, "
                                                 "токсичного дыма внутри хватит, чтоб отравить всех кто будет в радиусе"
                                                 " четырех метров."
                                                 "\nКак это сделать я скажу позже, сейчас вам нужно"
                                                 " найти конверт.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - отправляйтесь к входу Парка искусств, найдите "
                                                 "там звезду и напишите, что выше звезды.</em>", parse_mode="html"))
            await InputWhatever.Agent_3.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Вам нужно найти аэропорт, в 300м от М.Парк победы есть подобие, '
                                                 'и там нужно найти 5 лавок, и сесть на центральную.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: Это номер дома 🫱 <code>2/1</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.734333, longitude=37.595641))
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI"
                                                           "_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Agent_3)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Agent_3', message.from_user.id)
        if message.text.lower() == 'мир земле':
            photo_Agent3 = InputFile("Agent3.jpg", 'rb3')
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_Agent3))
            messages.append(await message.answer("<em>🐙Задача - мы знаем, что конверт сейчас перевоплощён в"
                                                 " свиток, найдите в этом "
                                                 "парке статую со свитком и напишите кому принадлежит эта"
                                                 " статуя.</em>", parse_mode="html"))
            await InputWhatever.Agent_4.set()
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Статуя находится при входе в Парке искусств музеон.'))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('<b>🫱 <code>1219523153</code> 🫲 или Выберите одну из функций '
                                     'ниже:</b>', parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Мир земле</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.732982, longitude=37.604451))
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Agent_4)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Agent_4', message.from_user.id)
        if message.text.lower() == 'петр 1' or message.text.lower() == 'петр1':
            photo_Agent4 = InputFile("Agent4.png", 'rb4')
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_Agent4))
            messages.append(await message.answer("<b>🐙Все верно.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Связной</u>:\n<b>Отлично, конверт у вас, теперь вам "
                                                 "необходимо встретить его любовницу. \nЛинда,"
                                                 " бывшая элитная эскортница, Варго часто крутится с ней, вам "
                                                 "нужно завязать с ней "
                                                 "разговор и передать конверт.\nКак, это уже на ваше усмотрение, "
                                                 "но она должна передать"
                                                 " это письмо Варго в целостности и сохранности. \nМы знаем, что она "
                                                 "каждый день заходит в "
                                                 "VK и у нее есть подруга Алена.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - найти место куда Линда заходит каждый день."
                                                 "\nДавайте проверим, "
                                                 "что вы пришли правильно, найдите две стрелки между "
                                                 "ними будет длинное слово, "
                                                 "напишите его.</em>", parse_mode="html"))
            await InputWhatever.Agent_5.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'калинин':
            messages.append(await message.answer('🐙Слишком грозный, не думаю что он дас вам свиток, '
                                                 'давайте поищем еще.'))
        elif message.text.lower() == 'смуров':
            messages.append(await message.answer('🐙Вы нашли свиток, но перевоплотить его в конверт '
                                                 'у вас не получилось, наверно это не тот свиток.'))
        elif message.text.lower() == 'клио':
            messages.append(await message.answer('🐙Вы нашли свиток, но перевоплотить его в конверт '
                                                 'у вас не получилось, наверно это не тот свиток.'))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Свиток будет золотой.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Петр 1</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.738582, longitude=37.607904))
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQX"
                                                           "zwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Agent_5)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Agent_5', message.from_user.id)
        if message.text.lower() == 'сыроварня':
            photo_Agent5 = InputFile("Agent5.jpg", 'rb5')
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_Agent5))
            messages.append(await message.answer("<b>🐙Все верно.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Связной</u>:\n<b>Я вижу ее, я вас сориентирую. "
                                                 "\nИдите вдоль набережной, справа будет Алена,"
                                                 " она зашла во двор, догоняйте.</b>", parse_mode='html'))
            messages.append(await message.answer("<b>🐙Найдите шоколадку, какая буква слева"
                                                 "?</b>", parse_mode="html"))
            await InputWhatever.Agent_6.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Пусть Петр ведет и держитесь его позади.\n'
                                                 'Давайте представим треугольник, и скажем что\n'
                                                 'A=VK, а B=Алена. Чему равно C=?'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Сыроварня</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.739737, longitude=37.609317))
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Agent_6)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Agent_6', message.from_user.id)
        if message.text.lower() == 'г':
            data["number"] = message.text
            messages.append(await message.answer("<b>🐙Все верно.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Связной</u>:\n<b>Не дойдя до шаурмы, повернула налево."
                                                 "\nВижу ее, вышла из туннеля, повернула налево."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - кто издает мощный свет?</em>", parse_mode="html"))
            await InputWhatever.Agent_7.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Осмотрите стены.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>г</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.740308, longitude=37.609730))
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Agent_7)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Agent_7', message.from_user.id)
        if message.text.lower() == 'железный человек':
            photo_Agent6 = InputFile("Agent6.jpg", 'rb6')
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_Agent6))
            messages.append(await message.answer("<b>🐙Все верно.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Связной</u>:\n<b>Заходит в туннель, вышла, обходит "
                                                 "Магадан.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - из какого фильма он?</em>", parse_mode="html"))
            await InputWhatever.Agent_8.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Герой.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Железный человек</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.740918, longitude=37.609359))
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbP"
                                                           "MQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Agent_8)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Agent_8', message.from_user.id)
        if message.text.lower() == 'трансформеры':
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Все верно.</em>", parse_mode="html"))
            messages.append(await message.answer("<u>Связной</u>:\n<b>Идёт под мост, догоняйте ее, повернула "
                                                 "направо, идёт до конца, "
                                                 "повернула налево, заходит в ГЭЗ идите за ней."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - вы зарегистрировались?"
                                                 "😅</em>", parse_mode="html", reply_markup=yesno))
            await InputWhatever.Agent_9.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Не медлите, идите дальше.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Трансформеры</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.741854, longitude=37.609793))
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Agent_9)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Agent_9', message.from_user.id)
        if message.text.lower() == 'да':
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Добро пожаловать."
                                                 "</em>", parse_mode="html", reply_markup=types.ReplyKeyboardRemove()))
            messages.append(await message.answer("<u>Связной</u>:\n<b>Выходит на улицу, поднимается на верх, "
                                                 "она в замкнутом пространстве, и место"
                                                 " располагает, она идет на смотровую. "
                                                 "\nСледуйте за ней. \nДальше дело за вами!</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - что зачёркнуто?</em>", parse_mode="html"))
            await InputWhatever.Agent_10.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'нет':
            messages.append(await message.answer('🐙Регистрируйтесь, регистрация бесплатная.\n'
                                                 'В ином случае пишите /help.'))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Вам нужно зайти внутрь белого здания.\n'
                                                 'Если будет так что в ГЭЗ будет особый день и вход '
                                                 'будет закрыт, или же платный,'
                                                 'то пишите "Да" а затем пишите /answer.\nК сожалению мир не идеален.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Да</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.742619, longitude=37.613159))
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Agent_10)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Agent_10', message.from_user.id)
        if (message.text.lower() == 'якорь'
                or message.text.lower() == '⚓️'
                or message.text.lower() == '⚓'
                or message.text.lower() == '⚓'):
            photo_Agent7 = InputFile("Agent7.jpg", 'rb7')
            photo_Agent8 = InputFile("Agent8.jpg", 'rb8')
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_Agent7))
            messages.append(await message.answer("<b>🐙Все верно.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Агент</u>:\n<b>Прелестная погода, не находите"
                                                 "?</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Лисенок</u>:\n<b>Мы знакомы?"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Агент</u>:\n<b>Боюсь что нет, мне повезло меньше чем Варго."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Лисенок</u>:\n<b>О, вы знакомы?</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Агент</u>:\n<b>Кто его не знает.\nМы, можно сказать, в "
                                                 "00-х были хорошими друзьями,"
                                                 " а сейчас я приехал на всеобщую конференцию.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Лисенок</u>:\n<b>А как вы узнал про меня?"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Агент</u>:\n<b>Ну, лисенок, работа такая,"
                                                 " все знать, все уметь.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Лисенок</u>:\n<b>Вы пугаете.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Агент</u>:\n<b>Неужто вы будете бояться друзей Варго, "
                                                 "тем более, что с его репутацией мне не сравниться.\n"
                                                 "Я честно сказать, надеялся встретить его, но, видно, у"
                                                 " меня не получится это сделать.\n"
                                                 "Вы можете сделать для старого друга Варго одно дело, притом "
                                                 "что это в его интересах?</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Лисенок</u>:\n<b>Что за дело?</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Агент</u>:\n<b>Можете передать ему письмо, хочу чтоб он "
                                                 "получил его до конференции,"
                                                 " эти бумаги очень важны для него.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Лисенок</u>:\n<b>Ладно... А как вас приставить?"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Агент</u>:\n<b>Ха-ха-ха, уверяю тебя в этом нет необходимости,"
                                                 " как только он вскроет конверт, он все поймет."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Передает конверт и незаметно подбрасывает в "
                                                 "сумочку жучка.</em>", parse_mode="html"))
            messages.append(await message.answer("<u>Лисенок</u>:\n<b>Ладно, я пойду тогда, рада "
                                                 "была познакомиться.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Агент</u>:\n<b>А я то как, прощайте.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Связной</u>:\n<b>Агент, отличная работа, мы будем "
                                                 "следить за ними, как только письмо будет вскрыто,"
                                                 " миссия будет выполнена, а сейчас вы можете отдохнуть, "
                                                 "советую посетить это место.</b>", parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_Agent8))
            messages.append(await message.answer("<em>🐙1861 год, кто прославил эту дату?\n"
                                                 "Задача -  что написано позади него? Первые 2 слова."
                                                 "</em>", parse_mode="html"))
            await InputWhatever.Agent_11.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Вы точно на смотровой?'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Якорь</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.741941, longitude=37.612465))
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Agent_11)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Agent_11', message.from_user.id)
        if message.text.lower() == 'царю-освободителю':
            data["number"] = message.text
            messages.append(await message.answer("<b>🐙Все верно.</b>", parse_mode="html"))
            messages.append(await message.answer("<em><b>🐙На прослушке.</b>\nЛинда с конвертом идет домой, "
                                                 "придя домой начинает готовить "
                                                 "и в скором времени возвращается Варго домой."
                                                 "</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Варго</u>:\n<b>Лисенок, я дома.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Лисенок</u>:\n<b>Пуся, я готовлю твоё любимое блюдо."
                                                 "\nЕще я сегодня встретила твоего старого друга с 00-х."
                                                 "\nОн просил передать тебе конверт с важными бумагами и сказал "
                                                 "что тебе стоит с ними"
                                                 " ознакомиться перед конференцией.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Варго</u>:\n<b>Что еще за мужик моим другом назвался!"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Лисенок</u>:\n<b>Ой, не знаю, я спросила как его зовут, "
                                                 "а он сказал, что в этом нет нужды, ты поймешь "
                                                 "как вскроешь конверт, он на полке лежит.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Берет конверт.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Варго</u>:\n<b>Нет у меня не кого из друзей 00-х, "
                                                 "они умерли все или сидят.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Вскрывает.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Лисенок</u>:\n<b>Ну он такой, лысый, у него еще на "
                                                 "затылке ближе к шее татуировка странная, "
                                                 "в виде кода.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Варго</u>:\n<b>Дура!!!!!!</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Начинает сильно кашлять.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Лисенок</u>:\n<b>Что случилось.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Бежит из кухни к нему и тоже начинает сильно кашлять."
                                                 "\nВарго берет телефон и набирает охране.</em>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Сильно кашляет</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Варго</u>:\n<b>Это Хи... хит... </b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Падает, умирает вместе с Линдой.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Связной</u>:\n<b>Агент, это связной, я звоню с личного, "
                                                 "это информация не официальная, меня за неё "
                                                 "могут уволить.\nЛюди Варго узнали про вас, и сейчас "
                                                 "все всё своё внимание сконцентрировали"
                                                 " на вас, город перекрыт, выйти из него не "
                                                 "получится, городской транспорт прослеживается,"
                                                 " вам нужно срочно выдвигаться, я скажу куда.</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Идите ко второму выходу, там вас встретит "
                                                 "Антон и проведет вас до главного повара.\nТам вас встретит "
                                                 "Владимир, чей отец был Илья.\nНо вас проведет через арку и "
                                                 "спустит вниз.\nТам вы уже сами, за долгое нахождение с вами, "
                                                 "могут заподозрить и их, так что, сильно рисковать не будем."
                                                 "</em>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Задача - что написано на серебреной медали?"
                                                 "</em>", parse_mode="html"))
            await InputWhatever.Agent_12.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Кто отменил крепостное право? '))
        elif message.text.lower() == 'памятник установлен':
            messages.append(await message.answer('<em>🐙Не плохо, но слишком низковато.</em>', parse_mode='html'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Царю-освободителю</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.745718, longitude=37.606938))
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Agent_12)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Agent_12', message.from_user.id)
        if message.text.lower() == 'за веру и верность':
            photo_Agent9 = InputFile("Agent9.jpg", 'rb9')
            data["number"] = message.text
            messages.append(await message.answer("<b>🐙Все верно.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Связной</u>:\n<b>Агент, я выяснила, кто был заказчиком, "
                                                 "заказчик был сам Варго точнее его двойник,"
                                                 " он все подстроил и теперь пытается давить на "
                                                 "то, что миссия была выполнена грязно."
                                                 " \nВы отстранены от задания, но если вы хотите "
                                                 "с ним рассчитаться, то я могу вам помочь.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Агент</u>:\n<b>Говорите.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Связной</u>:\n<b>В течение 20 минут он "
                                                 "приедет в Кремль через специальный выезд для "
                                                 "чиновников.\n"
                                                 "У нас на территории 29 квартала есть выкупленная "
                                                 "квартира для особых случаев, сейчас"
                                                 "мне кажется тот случай, там будет гранатомет, мощи хватит? чтоб "
                                                 "пробить бронированный танк.\n"
                                                 "Заходите быстрее, Варго скоро подъедет.</b>", parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_Agent9))
            messages.append(await message.answer("<em>🐙Вы заходите в квартиру, обустраиваетесь и ждете.\n"
                                                 "Выдвигается кортеж, вы видите, проезжает полицейская"
                                                 " легковушка, следом"
                                                 " 3 гелендвагена, по середине лимузин, сзади еще 2 "
                                                 "гелендвагена, и позади едет "
                                                 "такая же полицейская легковушка, что и в начале."
                                                 "</em>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Напишите ответ. \n"
                                                 "Посчитайте все колеса, при условии, что лимузин "
                                                 "на четырех колесах = x.\nx * на "
                                                 "количество машин = ???</em>", parse_mode="html"))
            await InputWhatever.Agent_13.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Вы не дошли.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>За веру и верность</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.748157, longitude=37.609678))
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI"
                                                           "_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Agent_13)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Agent_13', message.from_user.id)
        if message.text.lower() == '296':
            photo_Agent10 = InputFile("Agent10.jpg", 'rb10')
            data["number"] = message.text
            messages.append(await message.answer("<b>🐙Отлично </b>", parse_mode="html"))
            messages.append(await message.answer('<u>Связной</u>:\n<b>Агент, расстояние 296 метров будет, '
                                                 'когда лимузин будет на повороте в Кремль, снаряд'
                                                 ' долетит за 0.9секунд, это самые оптимальные условия.\n'
                                                 'Поворот через.\n3\n2\n1</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Связной</u>:\n<b>Агент, лимузин взорван.\n'
                                                 'Ваше место обнаружено, на полке есть ключ, берите его ключ и '
                                                 'перед выходом заминируйте бомбу с таймером на две минуты. '
                                                 'Поднимайтесь на последний этаж, там будет чердак, ключ его откроет, '
                                                 'как зайдете внутрь, попадете в систему лифта, '
                                                 'по лестнице спускайтесь вниз и '
                                                 'выходите в туннель, это наше секретное место.\n'
                                                 'Тут сможете переодеться и выйти чистым.</b>', parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_Agent10))
            messages.append(await message.answer('<u>Агент</u>:\n<b>Приятно было иметь с вами дело, '
                                                 'Связной.</b>', parse_mode='html'))
            await message.answer('<b>🐙Конец.©</b>', parse_mode='html', reply_markup=finish)
            await InputWhatever.Agent_finish.set()

        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙У гелендвагена пять колес, одно сзади.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>296</code> 🫲.', parse_mode='html'))
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAAC"
                                                           "AQADr8ZRGhLj3-N0EyK_MAQ"))
            messages.append(message)
            data['messages'] = messages


@dp.message_handler(state=InputWhatever.Agent_100)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Agent_100', message.from_user.id)
    if (message.text.lower() == 'answer'
            or message.text.lower() == 'help'):
        async with state.proxy() as data:
            data["number"] = message.text
            if 'messages' in data.keys():
                messages = data['messages']
            else:
                messages = []
            await InputWhatever.Agent_2.set()
            messages.append(await message.answer('🐙Нажмите 🫱 <code><u>2/1</u></code>. 🫲 '
                                                 '\nИ отправьте ответ Боту.',
                                                 parse_mode='html'))
            messages.append(message)
            data['messages'] = messages


@dp.message_handler(state=InputWhatever.Agent_finish)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Agent_finish', message.from_user.id)
    async with state.proxy() as data:
        if 'messages' in data.keys():
            for msg in data['messages'][::-1]:
                try:
                    await msg.delete()
                except Exception:
                    pass
        if message.text.lower() == "конец" or message.text.lower() == "🐙конец":
            Agent_mp3 = InputFile('Agent_mus.mp3', 'Конец')
            await bot.send_audio(chat_id=message.chat.id, audio=Agent_mp3)
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
                await message.answer('<b>🫱 <code>1219523153</code> 🫲 или напишите назад.</b>', parse_mode='html')
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
