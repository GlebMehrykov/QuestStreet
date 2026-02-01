import random
from datetime import datetime

import aiogram.utils.exceptions
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile

import AIP_Kievscay
from db import Database
from keybords import *

responses = ['🐙Да, да.', '🐙Прювет', "🐙Как ты там?", '🐙Кто выпил весь ром!', "🐙На абордаж", "🐙Ну чего тебе?",
             '🐙Как долго ты готов(а) со мной общаться?', "🐙А это забавно."]
db = Database("2.db")
bot = Bot(token=AIP_Kievscay.TELEGRAM_BOT)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db.create_table_users()
ADMIN_IDS = [1219523153, 6522187160]


class AdminState(StatesGroup):
    select_user = State()
    change_user_state = State()


class InputWhatever(StatesGroup):
    elfi_1 = State()
    elfi_Pay = State()
    elfi_2 = State()
    elfi_3 = State()
    elfi_4 = State()
    elfi_5 = State()
    elfi_6 = State()
    elfi_7 = State()
    elfi_8 = State()
    elfi_9 = State()
    elfi_10 = State()
    elfi_11 = State()
    elfi_12 = State()
    elfi_13 = State()
    elfi_14 = State()
    elfi_100 = State()
    elfi_finish = State()


@dp.callback_query_handler(state=InputWhatever.elfi_finish)
async def ikb_cb_handler(callback: types.CallbackQuery):
    await callback.answer('🐙ИИ меня не устраивает, вакансия открыта, пишите.')


@dp.message_handler(commands=['start'], state=[AdminState, None])
async def start_command(message: types.Message, state: FSMContext):
    print(message.from_user.id)
    db.insert_user(message.from_user.id)
    await state.finish()
    db.update_user_state('start', message.from_user.id)
    if message.from_user.id in ADMIN_IDS:
        await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                             parse_mode='html')
        await bot.send_message(message.from_user.id,
                               '1. Смена состояния\n'
                               '2. Запустить бота',
                               reply_markup=admin_kb)
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    else:
        await message.answer(text='🐙<b>Квест создан'
                                  '\n <em>            При сотрудничестве и поддержке\n'
                                  '                                </em></b>'
                                  ' <a href="https://mir-kvestov.ru/"><b>Мир квестов</b></a>\n \n'
                                  '<b><em>🐙 Вы попал в Квест-Эшхолорадо на Ⓜ️Киевская.</em>'
                                  '\nТут я предлагаю вам:                   ‍♀ '
                                  '\nПройтись по приятным локациям,         🚶‍♂️'
                                  '\nПогрузиться в мир эльфов и магии,      🔮'
                                  '\nЗащитить город от демонов,             👹'
                                  '\nИсполнить пророчество.                 📜'
                                  '\n \n \n         <em>🐙Пройти квест ---> /Eshholorado</em></b> '
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
                              '\nelfi_1 = <b>1</b>,'
                              '\nelfi_Pay = <b>2</b>,'
                              '\nelfi_2 = <b>3</b>,'
                              '\nelfi_3 = <b>4</b>,'
                              '\nelfi_4 = <b>5</b>,'
                              '\nelfi_5 = <b>6</b>,'
                              '\nelfi_6 = <b>7</b>,'
                              '\nelfi_7 = <b>8</b>,'
                              '\nelfi_8 = <b>9</b>,'
                              '\nelfi_9 = <b>10</b>,'
                              '\nelfi_10 = <b>11</b>,'
                              '\nelfi_11 = <b>12</b>,'
                              '\nelfi_12 = <b>13</b>,'
                              '\nelfi_13 = <b>14</b>,'
                              '\nelfi_14 = <b>15</b>,'
                              '\nelfi_100 = <b>16</b>'
                              '\nelfi_finish = <b>17</b>.', parse_mode='html')


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
        dict_values = {1: ' elfi_1',
                       2: ' elfi_Pay',
                       3: ' elfi_2',
                       4: ' elfi_3',
                       5: ' elfi_4',
                       6: ' elfi_5',
                       7: ' elfi_6',
                       8: ' elfi_7',
                       9: ' elfi_8',
                       10: ' elfi_9',
                       11: ' elfi_10',
                       12: ' elfi_11',
                       13: ' elfi_12',
                       14: ' elfi_13',
                       15: ' elfi_14',
                       16: ' elfi_100',
                       17: ' elfi_finish'}
        if int(message.text) in range(1, 17):
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
        await callback.message.edit_text(text='🐙<b>Квест создан'
                                              '\n<em>            При сотрудничестве и поддержке\n'
                                              '                                </em></b>'
                                              ' <a href="https://mir-kvestov.ru/"><b>Мир квестов</b></a>\n \n'
                                              '<b><em>🐙 Вы попал в Квест-Эшхолорадо на Ⓜ️Киевская.</em>'
                                              '\nТут мы предлагаю вам:                  🧝‍♀️'
                                              '\nПройтись по приятным локациям,         🚶‍♂️'
                                              '\nПогрузиться в мир эльфов и магии,      🔮'
                                              '\nЗащитить город от демонов,             👹'
                                              '\nИсполнить пророчество.                 📜'
                                              '\n \n \n         <em>🐙Готовы пройти квест ---> /Eshholorado</em></b>'
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


@dp.message_handler(commands=["Eshholorado"])
async def start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        photo_elfi_0 = InputFile("elfi0.png", 'rb')
        messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_elfi_0))
        messages.append(await message.answer("<b>🐙Добро пожаловать в Эшхолорадо.\n "
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
        await InputWhatever.elfi_1.set()
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.elfi_1)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('elfi_1', message.from_user.id)
        if message.text.lower() == "go":
            data["number"] = message.text
            messages.append(await message.answer("<b>🐙Начало.</b>", parse_mode="html"))
            messages.append(await message.answer('<u>Лирон</u>:\n<b>Эй, Хорри, хватит дома сидеть, пойдем гулять, '
                                                 'сегодня все отмечают праздник, '
                                                 'сегодня нашему городу Эшхолорадо исполняется 876 лет.'
                                                 '</b>', parse_mode="html"))
            messages.append(await message.answer('<u>Хорри</u>:\n<b>Лирон, для тебя каждый день, '
                                                 'что не день, то праздник.</b>', parse_mode="html"))
            messages.append(await message.answer('<u>Лирон</u>:\n<b>Мир прекрасен, разве нет?'
                                                 '</b>', parse_mode="html"))
            messages.append(await message.answer('<u>Хорри</u>:\n<b>Ладно, куда пойдем?</b>', parse_mode="html"))
            messages.append(await message.answer('<u>Лирон</u>:\n<b>Куда ноги поведут!\n'
                                                 'Глядишь, эльфийку себе найдешь.\n'
                                                 'Давай встретимся через тридцать минут на нашем '
                                                 'месте.</b>', parse_mode="html"))
            messages.append(await message.answer('<u>Хорри</u>:\n<b>Вот чего, мне и так хорошо.\n'
                                                 'Давай на нашем через час.</b>', parse_mode="html"))
            messages.append(await message.answer('<u>Лирон</u>:\n<b>Договорились.</b>', parse_mode="html"))
            messages.append(await message.answer("<em>Задача - Найти место инь-ян, что за символ на памятнике "
                                                 "в конце текста.</em>", parse_mode="html"))
            await InputWhatever.elfi_Pay.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
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
            messages.append(await message.answer('Ответ: go'))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.elfi_Pay)
async def get_number(message: types.Message):
    db.update_user_state('elfi_Pay', message.from_user.id)
    if message.from_user.id in ADMIN_IDS and message.text == '/skip8998':
        await message.answer('Вы успешно пропустили процесс оплаты.\n'
                             'Напишите 🫱 <code>Звезда</code> 🫲.', parse_mode='html')
        await InputWhatever.elfi_2.set()
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🐙назад':
        await InputWhatever.elfi_1.set()
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
                             '\nИли скопировать сверху.'
                             ' \n<b>🐙Откройте карту, посмотрите, что больше всего похоже на \nинь-ян, '
                             'место в 200 метрах от М.Киевская</b>', parse_mode='html')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Тут должен быть ответ, но его не будет, видите ли, первая задача'
                             ' квеста достаточно простая, '
                             'при все это у вас есть подсказка, и я уверен, что вы справитесь с этой задачей.\n'
                             'После оплаты квеста вам будут доступны ответы, но чтобы оплатить, вам нужно пройти '
                             'первую задачу, а чтобы ее пройти, нужно приехать и разгадать ее.\n'
                             '<b>Все квесты по 1500р.</b>', parse_mode='html')
    elif message.text.lower() == 'глеб, дай скидку!🙏🏻':
        await bot.send_message(message.from_user.id, '<b>🐙Особым игрокам, особая цена!'
                                                     '</b>', parse_mode='html')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста.',
                               description='🐙Оплата для того, чтобы пройти квест.',
                               provider_token="390540012:LIVE:40674",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=300 * 100)])
    elif (message.text.lower() == 'гилшод'
          or message.text.lower() == 'гилшот'):
        await bot.send_message(message.from_user.id, '<b>🐙Особым игрокам, особая цена!'
                                                     '</b>', parse_mode='html')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста.',
                               description='🐙Оплата для того, чтобы пройти квест.',
                               provider_token="390540012:LIVE:40674",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=1200 * 100)])
    else:
        await bot.send_message(message.from_user.id, '<b>🐙Оплатите квест, для того чтобы продолжить работу бота.'
                                                     '</b>', parse_mode='html')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста.',
                               description='🐙Оплата для того, чтобы пройти квест.',
                               provider_token="390540012:LIVE:40674",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=1500 * 100)])


@dp.pre_checkout_query_handler(state=InputWhatever.elfi_Pay)
async def process_precheck(precheck: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(precheck.id, ok=True)


@dp.message_handler(content_types=[types.ContentType.SUCCESSFUL_PAYMENT], state=InputWhatever.elfi_Pay)
async def successful_payment(message: types.Message):
    if message.successful_payment.invoice_payload == 'buy_sub':
        await bot.send_message(message.from_user.id, '<b>🐙Вы успешно оплатили доступ к боту.</b>💸\n'
                                                     'Напишите ответ на предыдущий вопрос.', parse_mode='html')
        await InputWhatever.elfi_2.set()


@dp.message_handler(state=InputWhatever.elfi_2)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        d1 = datetime.now()
        data['start_time'] = d1
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('elfi_2', message.from_user.id)
        db.new_level(message.chat.id)
        if message.text.lower() == 'звезда':
            photo_elfi_1 = InputFile("elfi1.jpg", 'rb1')
            photo_elfi_2 = InputFile("elfi2_1.png", 'rb2')
            await message.answer(d1.strftime("%H:%M:%S"))
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Таймер на прохождение квеста "
                                                 "запущен.</em>", parse_mode="html"))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_elfi_1))
            messages.append(await message.answer("<em>🐙Лирон подходит к месту раньше, чем Хорри, и резко впадает в сон,"
                                                 " но он этого не понимает.\n"
                                                 "Лирону становится не по себе, цвета вокруг начинают тускнеть.\n"
                                                 "На другой стороне памятника появляется его брат."
                                                 "</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Аваддон? Я думал, ты гниёшь в "
                                                 "аду за свои поступки!</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Демоническим голосом.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Аваддон</u>:\n<b>Брат мой, ты правда думаешь, "
                                                 "что я бы сгнил в темнице, нет, я их поработил, теперь"
                                                 " управляю армией демонов, я свободен, а вы за все "
                                                 "заплатите дорогой ценой.\n"
                                                 "Я закую всех эльфов в оковы и подчиню их волю, а нет, будут гореть!\n"
                                                 "Брат, у тебя еще есть шанс встать на сторону победителей."
                                                 "</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Я ни за что не стану иметь с тобой дела."
                                                 "\nТы позор нашего дома.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Аваддон</u>:\n<b>Ха-ха-ха, ты думаешь, что-то останется "
                                                 "от Эшхолорадо?\n"
                                                 "Я сотру все воспоминания, все о чем ты знаешь, будет забыто.\n"
                                                 "Оглядись, такую ты учесть хочешь?</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Лирон использует заклинания воды, "
                                                 "чтоб нанести удар по Аваддону."
                                                 "</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Аваддон</u>:\n<b>Ха-ха-ха, глупец, очнись, очнись, очнись!"
                                                 "</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Лирон просыпается, понимает, что был во сне,"
                                                 " но сон был вещий.</em>",
                                                 parse_mode='html'))
            messages.append(await message.answer("<u>Хорри</u>:\n<b>Лирон, привет! Ты что, такой бледный?"
                                                 "</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Не знаю, но у меня плохое предчувствие."
                                                 "</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Звуки сирены.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Хорри</u>:\n<b>Что это, город в опасности?"
                                                 "</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Значит, сон был и вправду вещим, нам "
                                                 "нужно срочно перебежать на ту сторону.\n"
                                                 "Аваддон, мой брат, он выбрался из темницы и хочет сжечь город, "
                                                 "а всех эльфов "
                                                 "заковать и предать в рабство.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Хорри</u>:\n<b>Аваддон? Тот самый псих, что баловался "
                                                 "темной магией?</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Боюсь, что да. \nНам нельзя медлить, "
                                                 "нужно перейти Бородианский мост.</b>", parse_mode="html"))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_elfi_2))
            messages.append(await message.answer("<em>🐙Направление - идите по левой стороне.\n"
                                                 "Задача: кндапя.п... Допишите.</em>",
                                                 parse_mode="html"))
            await InputWhatever.elfi_3.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Откройте карту, посмотрите, что больше всего похоже на \nинь-ян, '
                                                 'место в 200 метрах от М.Киевская'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>звезда</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.744100, longitude=37.569910))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.elfi_3)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('elfi_3', message.from_user.id)
        if message.text.lower() == 'кульнев' or message.text.lower() == 'кульнёв':
            data["number"] = message.text
            messages.append(await message.answer("<b>🐙Правильно, перейдите мост до конца.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Хорри</u>:\n<b>Лирон, о нет, армия уже тут, "
                                                 "нас разделяет только мост.</b>", parse_mode="html"))
            messages.append(await message.answer('<em>🐙На весь город.</em>', parse_mode='html'))
            messages.append(await message.answer("<u>Аваддон</u>:\n<b>Мой брат, ты же не думал, что я шучу, "
                                                 "я даю тебе последний шанс получить билет на сладкую жизнь, "
                                                 "иди ко мне!</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Лирон призывает духа воды, взывает мощь водных глубин.\n"
                                                 "Огромная волна проходит по речке, смывая все на своём пути."
                                                 "</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Аваддон</u>:\n<b>Неплохо, братец, ты лишил меня моста, "
                                                 "но уверяю тебя, "
                                                 "отсрочка в 20 минут не сыграет для вас роли.</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Аваддон приказывает строить катапульты и "
                                                 "мост.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Хорри</u>:\n<b>Что они делают?</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Хорри, не те вопросы "
                                                 "задаёшь, нужно срочно эвакуировать город,"
                                                 " начнем помогать ближайшим, тем, кому это больше всего "
                                                 "нужно.</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Задача - Красно-синие. Кто в белом, кто в синем, "
                                                 "а имя белому тому?</em>",
                                                 parse_mode="html"))
            await InputWhatever.elfi_4.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Вы не найдете ответа если, перешли мост'
                                                 ' и не найдете ответа если, прошли больше половины моста.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Кульнев</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.745585, longitude=37.573757))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.elfi_4)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('elfi_4', message.from_user.id)
        if message.text.lower() == 'косса':
            photo_elfi_3 = InputFile("elfi3.jpg", 'rb3')
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Катапульты в действии.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Хорри</u>:\n<b>Это шутка такая?\nАваддон хочет нас "
                                                 "костями забросать?</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Лучше было бы так, но боюсь это "
                                                 "армия скелетов.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Хорри</u>:\n<b>О нет.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Нужно вывести всех детей, пока есть время.\n"
                                                 "Еще нужно попасть к святому, он даст совет.</b>", parse_mode="html"))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_elfi_3))
            messages.append(await message.answer("<em>🐙Задача - Отправиться к святыне хапещанского леса. "
                                                 "Напишите полное название.</em>",
                                                 parse_mode="html"))
            await InputWhatever.elfi_5.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Кто по городу ездит светит, музыкой играет.\n'
                                                 'Поищите во дворах.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Косса</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.746458, longitude=37.577873))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.elfi_5)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('elfi_5', message.from_user.id)
        if message.text.lower() == 'церковь николы на щепах':
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Задача - Отправляйтесь туда, "
                                                 "найдите большое число, напишите его.</em>",
                                                 parse_mode="html"))
            await InputWhatever.elfi_6.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Если бы вы были людьми то, что было бы для вас святым местом?'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Церковь Николы на '
                                                 'Щепах</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.749016, longitude=37.580384))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.elfi_6)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('elfi_6', message.from_user.id)
        if message.text.lower() == '30':
            photo_elfi_4 = InputFile("elfi4.png", 'rb4')
            photo_elfi_20 = InputFile("elfi20.png", 'rb4')
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_elfi_4))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Здравствуйте, святой Нико, вы "
                                                 "наверно уже в курсе, мой брат вышел из темницы и "
                                                 "теперь мстит нам за то, что отвергли его от нашего "
                                                 "общества.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Нико</u>:\n<b>Да. Все как в пророчестве!"
                                                 "</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>А что за пророчество?</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Нико</u>:\n<b>Старая книга гласит, что в "
                                                 "момент процветания и счастья граждан, придет изгнанный и"
                                                 " будет мстить, но только брат со своим верным другом смогут его "
                                                 "остановить.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Хорри</u>:\n<b>Верным другом, это что-ли я?\nЯ есть в "
                                                 "пророчестве ухууу.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Нико</u>:\n<b>Да, но это всего лишь строчки в книге, "
                                                 "боюсь его остановят не пророчество, а сила "
                                                 "Тирельского талисмана, но боюсь он потерян.\n"
                                                 "Лирон, твой отец последний видел его, может ты знаешь?"
                                                 "</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Мне отец еще в раннем детстве подарил "
                                                 "такой талисман.\nВот он.</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Показывает талисман.</em>", parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_elfi_20))
            messages.append(await message.answer("<u>Нико</u>:\n<b>Святые ангелы, неужто вещь, "
                                                 "которую искали годами, "
                                                 "сотни людей, все время была при тебе?</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Я не знал, что это важный "
                                                 "талисман.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Нико</u>:\n<b>Слава Элуне, но это не полный талисман,"
                                                 " его необходимо собрать еще три части. "
                                                 "<em>\nОтправляйтесь к памятнику, который стоит на зеленой "
                                                 "территории, трехногом, трехруким,"
                                                 " но безголовым.</em> Детали должны быть в этом "
                                                 "районе.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - Кому принадлежит памятник?"
                                                 "</em>", parse_mode="html"))
            await InputWhatever.elfi_7.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
            messages.append(await message.answer("<em>🐙Задача - Кому принадлежит памятник?</em>", parse_mode="html"))
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Число ниже всех но, больше всех'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>30</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.749016, longitude=37.580384))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.elfi_7)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('elfi_7', message.from_user.id)
        if message.text.lower() == 'пушкин':
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Задача: какой день настанет.</em>", parse_mode="html"))
            await InputWhatever.elfi_8.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Памятник принадлежит великому поэту, и находится он'
                                                 ' на зеленной территории в виде патрона.\nМетров 500 от вас.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Пушкин</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.750000, longitude=37.587802))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.elfi_8)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('elfi_8', message.from_user.id)
        if message.text.lower() == 'веселья':
            photo_elfi_5 = InputFile("elfi5.png", 'rb5')
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_elfi_5))
            messages.append(await message.answer("<u>Хорри</u>:\n<b>Лирон, скелеты!</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Хорри, призови духа "
                                                 "земли и заблокируй деревьями проход с улиц, а я разберусь с "
                                                 "скелетами.</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Лирон призывает ближайшую воду, вода сбивает"
                                                 " их с ног, а Хорри призывает"
                                                 " лианы, которые сковывают кости и погружают их в землю."
                                                 "</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Хорри</u>:\n<b>От этой пачки скелетов мы отбились, "
                                                 "но сзади бегут еще скелеты, тут нужен другой "
                                                 "подход, Лирон, думай! \nДеревья долго не продержатся"
                                                 ".</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Я думаю, думаю. \n"
                                                 "У меня из головы не выходит про талисман, что отец "
                                                 "мне дал и ни слова "
                                                 "не сказал. \nНужно его внимательней осмотреть.\n"
                                                 "Смотри, я вижу тут гравировку, мелко, но рассмотреть можно, "
                                                 "вроде 'эк', я ничего "
                                                 "не понимаю, как он может нам помочь?</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Хорри</u>:\n<b>Иногда, нужно отдалиться, чтоб увидеть картину"
                                                 " целиком.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>О чем это ты?</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Хорри</u>:\n<b>Лирон, талисман издает свет, в нем есть "
                                                 "магическая сила, тебе нужно только разобраться "
                                                 "в нем.</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Скелеты прорываются и начинают ломиться"
                                                 " из каждого окна, падают с крыши."
                                                 "</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Возможно ты прав, "
                                                 "но боюсь сейчас не до этого, нужно"
                                                 " уходить от сюда.</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Задача - от правой ноги, беги, вплоть до последнего, беги, "
                                                 "не сверни, добежишь, постучи."
                                                 "\n🐙По кому вы стучите?</em>", parse_mode="html"))
            await InputWhatever.elfi_9.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Осмотрите памятник.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Веселья</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.750000, longitude=37.587802))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.elfi_9)
async def get_number(message: types.Message, state: FSMContext):
    async with (state.proxy() as data):
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('elfi_9', message.from_user.id)
        if message.text.lower() == 'лев' or message.text.lower() == 'льву':
            photo_elfi_6 = InputFile("elfi6.png", 'rb6')
            data["number"] = message.text
            messages.append(await message.answer("<u>Хорри</u>:\n<b>Лирон, мы окружены, их слишком много.\n"
                                                 "Смотри, вон еще идут, нам не справиться.</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Лирон достаёт из кармана талисман.</em>", parse_mode='html',
                                                 reply_markup=kievskay))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Талисман, может ты...</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Использует силу талисмана и прерывает магию Аваддона.\n"
                                                 "Без магии скелеты начинают сгорать. </em>", parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_elfi_6))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Хорри, возможно, пророчество не"
                                                 " врет, и нам с тобой нужно остановить Аваддона."
                                                 "</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Хорри</u>:\n<b>Лирон, святейший сказал, "
                                                 "что в районе Арбалиана есть три недостающие "
                                                 "части талисмана, и нам нужно"
                                                 " их собрать, и тогда мощи талисмана хватит, что упрячь Аваддона "
                                                 "в эльфийскую "
                                                 "темницу, думаю от туда он точно не выйдет, и не заставит"
                                                 " эльфов встать на его сторону, и"
                                                 " не пойдет следом уничтожать другую расу, типа орков, хотя... Я"
                                                 " бы мож...</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Классно, что ты нашел время поразмышлять, "
                                                 "давай думать, как и где мы будем искать недостающие детали.\n"
                                                 "Тут, очевидно, нужна оправа, механизм и камень."
                                                 "</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Хорри</u>:\n<b>Святейший сказал, что где-то тут, давай"
                                                 " определимся какую часть будем искать первую."
                                                 "</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Задание: Вам нужно найти три части, также"
                                                 " у вас есть три кнопки."
                                                 "\nВсе детали можно увидеть на линии Арбалиана."
                                                 "\n🐙Вы можете посмотреть все три задания, "
                                                 "но писать ответ нужно находясь в соответствующим задание.\n"
                                                 "Также в каждом задание будут работать подсказки.\n"
                                                 "</em>", parse_mode="html"))
            await InputWhatever.elfi_10.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙"рад" это конечная часть слова.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Лев</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.748571, longitude=37.588498))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.elfi_10)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('elfi_10', message.from_user.id)
        if message.text.lower() == 'экспектапотронум':
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Читает заклинание \" Экспектапотронум\", "
                                                 "получает мощный прилив сил."
                                                 "</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Хорри</u>:\n<b>О нет, Аваддон уже"
                                                 " тут.</b>",
                                                 reply_markup=types.ReplyKeyboardRemove(), parse_mode='html'))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Хорри, не переживай, "
                                                 "Талисман собран, с ним я могу одолеть его.\n"
                                                 "Попробуй отвлечь его и сконцентрировать на себе, если он "
                                                 "начнет использовать магию "
                                                 ",то будет ослаблен.\nВ этот момент я и нанесу мощный водный удар "
                                                 "и потушу его пламя.</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Хорри</u>:\n<b>Как мне это сделать?</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Лирон</u>:\n<b>Просто привлеки его "
                                                 "внимание, Аваддон сам все сделает, он думает, "
                                                 "что бессмертный и"
                                                 " будет играться с вами, но ты не переживай, я выйду в нужный "
                                                 "момент.</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Задача - дойдите до конца Арболиана и найти предмет, "
                                                 "который заставит Аваддона привлечь "
                                                 "внимание.</em>", parse_mode="html"))
            await InputWhatever.elfi_14.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🔮оправа':
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Задача - найдите памятник с книгой."
                                                 "\nКакого года рукав?</em>"
                                                 "", parse_mode="html", reply_markup=back_back))
            await InputWhatever.elfi_11.set()
        elif message.text.lower() == '⚙️механизм':
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Задача: найдите ветхий дом, кто его защищает?</em>",
                                                 parse_mode="html", reply_markup=back_back))
            await InputWhatever.elfi_12.set()
        elif message.text.lower() == '🪨камень':
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Задача - найдите террасу, что за животное на тележке?</em>",
                                                 parse_mode="html", reply_markup=back_back))
            await InputWhatever.elfi_13.set()
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Напишите заклинание, оно состоит из четырех отрывков.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>экспектапотронум</code> 🫲', parse_mode='html'))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.elfi_11)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('elfi_11', message.from_user.id)
        if message.text.lower() == '2020':
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Получена оправа. \n"
                                                 "На оправе вы увидели \"спек\""
                                                 "</em>", parse_mode="html", reply_markup=kievskay))
            messages.append(await message.answer("<em>🐙Нужно найти все три предмета и активировать "
                                                 "талисман.</em>", parse_mode="html"))
            await InputWhatever.elfi_10.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🐙назад':
            data["number"] = message.text
            messages.append(await message.answer('🐙Запомнили? давайте посмотрим другие '
                                                 'задания.', reply_markup=kievskay))
            await InputWhatever.elfi_10.set()
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Это будет большой памятник, а рукав будет хорошо спрятан.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>2020</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.749542, longitude=37.591661))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYo"
                                                           "I_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.elfi_12)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('elfi_12', message.from_user.id)
        if message.text.lower() == 'государство':
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Получен механизм. \n"
                                                 "На механизме вы увидели \"тапо\""
                                                 "</em>", parse_mode="html", reply_markup=kievskay))
            messages.append(await message.answer("<em>🐙Нужно найти все три предмета и активировать "
                                                 "талисман.</em>", parse_mode="html"))
            await InputWhatever.elfi_10.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🐙назад':
            data["number"] = message.text
            messages.append(await message.answer('🐙Запомнили? давайте посмотрим другие задания.'
                                                 '', reply_markup=kievskay))
            await InputWhatever.elfi_10.set()
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Он прям деревянный и находится рядом с линией Арбалиана.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Государство</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.749767, longitude=37.594505))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.elfi_13)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('elfi_13', message.from_user.id)
        if message.text.lower() == 'волк':
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Получен камень. \n"
                                                 "На камне вы увидели \"тронум\"</em>"
                                                 "", parse_mode="html", reply_markup=kievskay))
            messages.append(await message.answer("<em>🐙Нужно найти все три предмета и активировать талисман.</em>"
                                                 "", parse_mode="html"))
            await InputWhatever.elfi_10.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🐙назад':
            data["number"] = message.text
            messages.append(await message.answer('🐙Запомнили? Давайте посмотрим другие '
                                                 'задания.', reply_markup=kievskay))
            await InputWhatever.elfi_10.set()
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Прогуляйтесь подальше, возможно на обратном пути вы найдете место.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Волк</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.751626, longitude=37.596978))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.elfi_100)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('elfi_100', message.from_user.id)
    if (message.text.lower() == 'answer'
            or message.text.lower() == 'help'):
        async with state.proxy() as data:
            data["number"] = message.text
            if 'messages' in data.keys():
                messages = data['messages']
            else:
                messages = []
            messages.append(await message.answer('🐙Нажмите 🫱 <code><u>Звезда</u></code>. 🫲 '
                                                 '\nИ отправьте ответ Боту.',
                                                 parse_mode='html'))
            await InputWhatever.elfi_2.set()
            messages.append(message)
            data['messages'] = messages


@dp.message_handler(state=InputWhatever.elfi_14)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('elfi_14', message.from_user.id)
        if (message.text.lower() == 'колокол'
                or message.text.lower() == 'колокола'
                or message.text.lower() == 'колоколов'):
            photo_elfi_7 = InputFile("elfi7.png", 'rb7')
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Хорри призывает мощь земных недр, и на главном входе "
                                                 "к ул.Арбалиану "
                                                 "начинают прорастать густые деревья, так что эльфы не "
                                                 "могут выйти.\nАваддон стоит на "
                                                 "перекрестке и обращает на это внимание.</em>", parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_elfi_7))
            messages.append(await message.answer('<em>🐙Эльфы как овцы заперты в пространстве, '
                                                 "они не могу выйти, и Аваддон прожигает своими лучами из своих "
                                                 "очей, брусчатка начинает"
                                                 " взлетать вверх от сильной мощи Аваддона, эльфы бегут к деревьям от "
                                                 "безысходности, что сделал Хорри.\nАваддон не торопится их сжигать, он"
                                                 " издевается над добычей, снося боковые заведения в прах и "
                                                 "наслаждается "
                                                 "беспомощными криками эльфов, когда район испепелен, а все эльфы уже"
                                                 " собраны и в отчаяние начинают вставать на колени, сзади "
                                                 "Аваддона выходит"
                                                 " Лирон и читает мощное заклинание 'Water strike'.\n"
                                                 "Мощный удар воды с неба, можно сказать, взорвал Аваддона."
                                                 "\nАваддон лежит в отключке, "
                                                 "тут же подбегают правоохранители и сковывают его.\n "
                                                 "\n    🐙Лирон так и не стал известным героем, а Хорри чудом отделался"
                                                 " за свой неадекватный "
                                                 "поступок, который заблокировал выход, списали на панику и "
                                                 "хороший конец.\n"
                                                 "Но друзья знали, что они часть важной истории, и им было "
                                                 "этого достаточно,"
                                                 " ну, может Хорри хотел чуть больше.</em>", parse_mode="html"))
            await message.answer("🐙<b>Конец.©</b>", parse_mode='html', reply_markup=finish)
            await InputWhatever.elfi_finish.set()
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙8+1'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Колокол</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.752237, longitude=37.600143))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.elfi_finish)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('elfi_finish', message.from_user.id)
    async with state.proxy() as data:
        if 'messages' in data.keys():
            for msg in data['messages'][::-1]:
                try:
                    await msg.delete()
                except Exception:
                    pass
        if message.text.lower() == "🐙конец":
            mp3_elfi = InputFile('elfi_mus.mp3', 'Конец')
            await bot.send_audio(chat_id=message.chat.id, audio=mp3_elfi)
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
                await message.answer('🐙🫱 <code>1219523153</code> 🫲 или напишите назад.</b>', parse_mode='html')
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
