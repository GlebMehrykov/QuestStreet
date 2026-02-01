import random
from datetime import datetime

import aiogram.utils.exceptions
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile

import AIP_Soch_VPS
from db import Database
from keybords import *

responses = ['🐙Да, да.', '🐙Прювет', "🐙Как ты там?", '🐙Кто выпил весь ром!', "🐙На абордаж", "🐙Ну чего тебе?",
             '🐙Как долго ты готов(а) со мной общаться?', "🐙А это забавно."]
db = Database("2.db")
bot = Bot(token=AIP_Soch_VPS.TELEGRAM_BOT)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db.create_table_users()
ADMIN_IDS = [1219523153, 6522187160]


class AdminState(StatesGroup):
    select_user = State()
    change_user_state = State()


class InputWhatever(StatesGroup):
    Soch_1 = State()
    Soch_Pay = State()
    Soch_2 = State()
    Soch_3 = State()
    Soch_4 = State()
    Soch_5 = State()
    Soch_6 = State()
    Soch_7 = State()
    Soch_8 = State()
    Soch_9 = State()
    Soch_10 = State()
    Soch_11 = State()
    Soch_12 = State()
    Soch_13 = State()
    Soch_14 = State()
    Soch_15 = State()
    Soch_16 = State()
    Soch_100 = State()
    Soch_finish = State()


@dp.callback_query_handler(state=InputWhatever.Soch_finish)
async def ikb_cb_handler(callback: types.CallbackQuery):
    await callback.answer('🐙ИИ меня не устраивает, вакансия открыта, пишите.')


@dp.message_handler(commands=['start'], state=[AdminState, None])
async def start_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        print(message.from_user.id)
        db.insert_user(message.from_user.id)
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('🐙 🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb)
        elif message.text.lower() == '🐙':
            await bot.send_message(message.chat.id, random.choice(responses))
        else:
            messages.append(await message.answer(text='🐙<b>Готовы найти сокровище,          💎️'
                                                 '\nПройтись по приятным локациям,     🌴'
                                                 '\nПогрузиться в мир таинственного острова,      🔮'
                                                 '\nПознакомиться с пиратами,          🏴‍☠️'
                                                 '\nИ попытаться выжить при всем этом?         🚸'
                                                 '\n \n🐙    <em>Пройти квест ---> '
                                                 '\n \n \n<a href="https://t.me/QuestStreetBot"><b>Выбрать другой '
                                                 'квест.</b></a>/V_poiskah_sokrovish</em>'
                                                      '</b>', parse_mode='html', disable_web_page_preview=True))

        messages.append(message)
        data['messages'] = messages

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
                              '\nSoch_1 = <b>1</b>,'
                              '\nSoch_Pay = <b>2</b>,'
                              '\nSoch_2 = <b>3</b>,'
                              '\nelfi_3 = <b>4</b>,'
                              '\nSoch_4 = <b>5</b>,'
                              '\nSoch_5 = <b>6</b>,'
                              '\nSoch_6 = <b>7</b>,'
                              '\nSoch_7 = <b>8</b>,'
                              '\nSoch_8 = <b>9</b>,'
                              '\nSoch_9 = <b>10</b>,'
                              '\nSoch_10 = <b>11</b>,'
                              '\nSoch_11 = <b>12</b>,'
                              '\nSoch_12 = <b>13</b>,'
                              '\nSoch_13 = <b>14</b>,'
                              '\nSoch_14 = <b>15</b>,'
                              '\nSoch_15 = <b>16</b>,'
                              '\nSoch_16 = <b>17</b>,'
                              '\nSoch_100 = <b>18</b>,'
                              '\nSoch_finish = <b>19</b>.', parse_mode='html')


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
        dict_values = {1: ' Soch_1',
                       2: ' Soch_Pay',
                       3: ' Soch_2',
                       4: ' Soch_3',
                       5: ' Soch_4',
                       6: ' Soch_5',
                       7: ' Soch_6',
                       8: ' Soch_7',
                       9: ' Soch_8',
                       10: ' Soch_9',
                       11: ' Soch_10',
                       12: ' Soch_11',
                       13: ' Soch_12',
                       14: ' Soch_13',
                       15: ' Soch_14',
                       16: ' Soch_15',
                       17: ' Soch_16',
                       18: ' Soch_100',
                       19: ' Soch_finish'}
        if int(message.text) in range(1, 20):
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
        await callback.message.edit_text(text='🐙<b>Готовы найти сокровище,          💎️'
                                              '\nПройтись по приятным локациям,     🌴'
                                              '\nПогрузиться в мир таинственного острова,      🔮'
                                              '\nПознакомиться с пиратами,          🏴‍☠️'
                                              '\nИ попытаться выжить при всем этом?</b>         🚸'
                                              '\n\n \n🐙    <em>Пройти квест ---> '
                                              '/V_poiskah_sokrovish</em>'
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


@dp.message_handler(commands=["V_poiskah_sokrovish"])
async def start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        photo_VPS_0 = InputFile("VPS_0.png", 'rb0')
        messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_VPS_0))
        messages.append(await message.answer("<b>🐙Добро пожаловать на таинственный остров.\n "
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
        await InputWhatever.Soch_1.set()
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Soch_1)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Soch_1', message.from_user.id)
        if message.text.lower() == "go":
            photo_VPS_1 = InputFile("VPS_1.png", 'rb1')

            data["number"] = message.text
            messages.append(await message.answer("<b>🐙Начало.</b>", parse_mode="html"))
            messages.append(await message.answer(' <u>Капитан</u>:\n<b>Отплываем!\nНаша миссия выполнена, '
                                                 'пора отправляться домой.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Неужели, 17 месяцев '
                                                 'мы потратили на поиски новых земель,'
                                                 ' ресурсов, возможностей, я думаю, что Император'
                                                 ' будет доволен нашим новым находкам.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Да, и не только он'
                                                 ', с новыми возможностями, моя семья'
                                                 ' заживет по-новому!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Друзья, мои поздравления!'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Мы еще не дома.\nЕсли будет попутный ветер '
                                                 ',то дома мы окажемся дней через 40, там и будете радоваться'
                                                 '.</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>23 день в море</em>', parse_mode="html"))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Капитан, погода меняется, '
                                                 'мы входим в сильный туман, признаю'
                                                 'сь, я еще не видел такого тумана при свете дня и '
                                                 'спокойной погоды!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Что ж, я тоже, природа уникальная, но не '
                                                 'будем впадать в панику, держимся курса.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Капитан, что творится, я'
                                                 ' дальше носа не вижу.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Испугались?!\nНебольшой природный каприз, '
                                                 'вернитесь в свою каюту, если боитесь.</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Мощный удар молнии в нос корабля.</em>', parse_mode="html"))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_VPS_1))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Боже!'
                                                 '\nЧто это?\nНебольшой каприз!?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Все целы?\nВ том крыле никого не было, '
                                                 'быстро тушим пожар!\nВоды, воды!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Боюсь, воды предостаточно, '
                                                 'молния насквозь пробила корабль, мы тонем.</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Капитан бежит осматривать корабль.</em>', parse_mode="html"))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Нам нужно срочно эвакуироваться, '
                                                 'спускаем лодки. Быстрее, '
                                                 'медленные мухи, не спим!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Господи, гроза, '
                                                 'еще этот туман при свете дня, '
                                                 'это все неспроста.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Лодки спущены, эвакуируемся.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Отплывают на 100 метров от тонущего корабля.'
                                                 '</em>', parse_mode="html"))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Гляньте, туман рассеялся.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>'
                                                 'Все наши находки, доказательства, '
                                                 'весь наш труд, все в воду, ая-я-яй.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Нам нужно думать о спасении, а не о бумажках.'
                                                 '\nЯ вижу птиц, это хороший знак, значит, где-то должна быть земля.\n'
                                                 'Боцман, дай подзорную трубу.'
                                                 '\nЯ вижу сушу, отправляемся в ту сторону.</b>', parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - вы прибываете на берег и видите старый корабль, "
                                                 "возле него валяется скелет большой рыбы, якорь и Разбитый парус."
                                                 "\nНапишите названия корабля."
                                                 "</em>", parse_mode="html"))
            await InputWhatever.Soch_Pay.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('go'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>go</code> 🫲', parse_mode='html'))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okO"
                                                           "jYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))

        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Soch_Pay)
async def get_number(message: types.Message):
    db.update_user_state('Soch_Pay', message.from_user.id)
    if message.from_user.id in ADMIN_IDS and message.text == '/skip8998':
        await message.answer('Вы успешно пропустили процесс оплаты.\n'
                             'Напишите 🐙 🫱 <code>флибустьер</code> 🫲.', parse_mode='html')
        await InputWhatever.Soch_2.set()
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == 'назад':
        await InputWhatever.Soch_1.set()
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
                             ' \n<b>🐙   Если вам нужна подсказка квеста то:</b>\n'
                             'Напоминаем, что картой Яндекс придется пользоваться постоянно.'
                             '\nДавайте пройдемся по набережной.', parse_mode='html')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Тут должен быть ответ, но его не будет, видите ли, первая задача'
                             ' квеста достаточно простая, '
                             'при все это у вас есть подсказка, и я уверен, что вы справитесь с этой задачей.\n'
                             'После оплаты квеста вам будут доступны ответы, но чтобы оплатить, вам нужно пройти '
                             'первую задачу, а чтобы ее пройти, нужно приехать и разгадать ее.\n'
                             '<b>Все квесты по 1500р.</b>', parse_mode='html')
    elif message.text.lower() == 'глеб, дай скидку!🙏🏻':
        await bot.send_message(message.from_user.id, '<b>🐙Особым гостям особая цена.'
                                                     '</b>', parse_mode='html')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста.',
                               description='🐙Оплата для того, чтобы пройти квест.',
                               provider_token="390540012:LIVE:47207",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=300 * 100)])

    elif message.text.lower() == 'Ваше кодовая фраза':
        await bot.send_message(message.from_user.id, '<b>🐙Особым гостям особая цена.'
                                                     '</b>', parse_mode='html')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста.',
                               description='🐙Оплата для того, чтобы пройти квест.',
                               provider_token="390540012:LIVE:47207",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=1250 * 100)])

    else:
        await bot.send_message(message.from_user.id, '<b>🐙Оплатите квест, для того чтобы продолжить работу бота.'
                                                     '</b>', parse_mode='html')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста.',
                               description='🐙Оплата для того, чтобы пройти квест.',
                               provider_token="390540012:LIVE:47207",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=1500 * 100)])


@dp.pre_checkout_query_handler(state=InputWhatever.Soch_Pay)
async def process_precheck(precheck: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(precheck.id, ok=True)


@dp.message_handler(content_types=[types.ContentType.SUCCESSFUL_PAYMENT], state=InputWhatever.Soch_Pay)
async def successful_payment(message: types.Message):
    if message.successful_payment.invoice_payload == 'buy_sub':
        await bot.send_message(message.from_user.id, '<b>🐙Вы успешно оплатили доступ к боту.</b>💸\n'
                                                     'Напишите ответ на предыдущий вопрос.', parse_mode='html')
        await InputWhatever.Soch_2.set()


@dp.message_handler(state=InputWhatever.Soch_2)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        d1 = datetime.now()
        data['start_time'] = d1
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Soch_2', message.from_user.id)
        db.new_level(message.chat.id)
        if (message.text.lower() == 'ресторан флибустьер'
                or message.text.lower() == 'флибустьер ресторан'
                or message.text.lower() == 'флибустьер'):
            photo_VPS_2 = InputFile("VPS_2.jpg", 'rb2')
            photo_VPS_3 = InputFile("VPS_3.png", 'rb4')
            photo_VPS_4 = InputFile("VPS_4.png", 'rb6')
            await message.answer(d1.strftime("%H:%M:%S"))
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Таймер на прохождение квеста запущен."
                                                 "</em>", parse_mode="html"))

            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Капитан, это корабль?'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>По всей видимости, но я еще не видел '
                                                 'столь печального '
                                                 'корабля, если вы думаете, что на нем можно уплыть, то забудьте, '
                                                 'проще новый сделать.</b>', parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_VPS_2))
            messages.append(await message.answer('🐙<em>Находят рядом скелета с бутылкой.</em>', parse_mode="html"))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Видимо, эта группа попала сюда '
                                                 'при сильном шторме и не смогла отсюда выбраться, не думаю, '
                                                 'что на острове еще кто-то из людей остался, '
                                                 'судя по зубам, ему лет 50.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>То есть это уже было раньше,'
                                                 ' что-то похожее на то, что случилось с нами?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>При этом у этой '
                                                 'группы был корабль, и они все равно не выбрались, мне кажется, '
                                                 'наша история куда печальнее.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Посмотрите на их корабль, самопалы, '
                                                 'без флага, они явно были пиратами.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Согласен.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Я вижу неподалеку от '
                                                 'скелета из песка торчит бутылка. \nРебят, посмотрите, вдруг она '
                                                 'полная, хоть дух перевести бы.</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Достают бутыль.</em>', parse_mode="html"))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Капитан, это похоже на предсмертную '
                                                 'записку.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Откупоривай. \nЧитай.</b>', parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_VPS_3))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Тут есть золото?'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Ну ты же слышал Боцмана.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Давайте не будем воспринимать все, '
                                                 'что там было написано всерьёз.'
                                                 '\nНаша задача - изучить местность, разбить лагерь, '
                                                 'построить корабль и убраться отсюда.'
                                                 '\nЖивыми!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Не, не, не, мы не можем '
                                                 'вернуться с пустыми руками, '
                                                 'тогда смысл нам возвращаться, нам там голову отрубят.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Он прав, с пустыми руками '
                                                 'домой нельзя, у меня семья голодная.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Забудьте, остров большой, а у нас ничего нет,'
                                                 ' а мы понятия не имеем, откуда что искать, '
                                                 'давайте думать, как нам выжить, глядишь, оно само найдется.'
                                                 '\nБоцман, обыщи корабль пиратов, может мы чего '
                                                 'полезного сможем найти.</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Боцман бежит проверять корабль.</em>', parse_mode="html"))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Ну, что там?</b>', parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_VPS_4))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Все в плесени, покрыто мхом, '
                                                 'у них тут маски всякие, они, похоже, на маскарад плыли.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Что еще видишь?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Капитан, ничего особого. '
                                                 '\nШмотье, пивные кружки '
                                                 'валяются на полу. \nНичего, что могло бы пригодиться.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Сползай, будем осваивать остров.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Спустя какое-то время.</em>', parse_mode="html"))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Тут точно кто-то жил, ну или разводили тут'
                                                 ' временный лагерь.</b>', parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - найти это место. \nПодсказки находятся в тексте."
                                                 "</em>", parse_mode="html"))
            await InputWhatever.Soch_3.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Вы пользуетесь картой яндекс?\n Пройдитесь по набережной.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Флибустьер</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.568616, longitude=39.731552))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0o"
                                                           "kOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))

        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Soch_3)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Soch_3', message.from_user.id)
        if (message.text.lower() == 'парк им. м.в фрунзе'
                or message.text.lower() == 'м.в фрунзе'
                or message.text.lower() == 'фрунзе'):

            data["number"] = message.text
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Нужно осмотреться тут, '
                                                 'может здесь и остановимся на '
                                                 'первое время. \nБоцман, посмотри палатки. '
                                                 '\nРазведывательная группа, осмотритесь у окрестностей.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Иду.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Пойдемте, мож, что '
                                                 'интересное найдем.</b>', parse_mode='html'))
            messages.append(await message.answer('🐙<em>Спустя время.</em>', parse_mode="html"))
            messages.append(await message.answer("<em>🐙Пообщайтесь с Боцманом и разведывательной группой.</em>",
                                                 parse_mode="html", reply_markup=bocman))
            await InputWhatever.Soch_4.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Что мы знаем о корабле и с какой локацией это можно связать?'
                                                 '\nБез Яндекс карты, квест не пройти.🪬'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Парк им. М.В Фрунзе</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.568617, longitude=39.733543))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOj"
                                                           "YoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Soch_4)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Soch_4', message.from_user.id)
        if message.text.lower() == 'пообщаться с боцманом':
            photo_VPS_5 = InputFile("VPS_5.png", 'rb3')

            data["number"] = message.text
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Капитан, я нашел главную палатку, '
                                                 'тут за столом сидят 3 скелета, думаю, они '
                                                 'были начальниками, вроде ничего полезного, но картина'
                                                 ' интересная, посмотрите, может вы тут что-то увидите.'
                                                 '</b>', parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_VPS_5))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Этот остров все больше влечет нас за '
                                                 'своей историей.</b>', parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - как зовут центрального скелета?</em>",
                                                 parse_mode="html",
                                                 reply_markup=types.ReplyKeyboardRemove()))
            await InputWhatever.Soch_5.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Откройте клавиатуру. Если клавиатуры нет, нажмите на четыре'
                                                 ' кнопки.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Пообщаться с Боцманом</code> 🫲.', parse_mode='html'))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf"
                                                           "0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Soch_5)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Soch_5', message.from_user.id)
        if (message.text.lower() == 'глинка м.и.'
                or message.text.lower() == 'глинка'):
            photo_VPS_6 = InputFile("VPS_6.png", 'rb6')

            data["number"] = message.text
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Разведывательная группа, как у вас идут '
                                                 'дела, нашли что-то полезное?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Капитан, мы нашли скрижаль,'
                                                 ' похоже это та самая карта.'
                                                 '\nВот и сама судьба говорит нам, что нужно начать поиски.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Да!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Да мало ли, что там за каракули на этом камне,'
                                                 ' нам нужно думать, как выбраться отсюда.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Капитан, мы вас, конечно '
                                                 'уважаем, чтим, но давайте'
                                                 ' не будем забывать, кто за все платит, и если мы вернемся '
                                                 'с пустыми руками, да еще и на самодельной лодке вместо корабля,'
                                                 ' то нас просто выгонят обратно. '
                                                 '\nМы должны попытаться!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Ладно, дайте взглянуть на скрижаль.'
                                                 '</b>', parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_VPS_6))
            messages.append(await message.answer("<em>🐙Задача - напишите название скрижали."
                                                 "\n Скрижаль будет неподалеку.\n(Можно аббревиатурой)"
                                                 "</em>", parse_mode="html"))
            await InputWhatever.Soch_6.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Прогуляйтесь по парку и увидите трех интересных персонажей.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Глинка М.И.</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.569467, longitude=39.733292))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0"
                                                           "okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Soch_6)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Soch_6', message.from_user.id)
        if (message.text.lower() == 'маршрут дозированной ходьбы'
                or message.text.lower() == 'мдх'):

            data["number"] = message.text
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Это не целая скрижаль, '
                                                 'тут точно еще две, может, даже три части будет. '
                                                 '\nГде мы их найдем?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Также, как и этот. '
                                                 '\nЧто там написано?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Боцман, иди сюда, ты помоложе, тебе эти'
                                                 ' ребусы должны быть понятней.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Дайте взгляну. '
                                                 '\nЯ так понимаю, мы тут находимся, потому что здесь у них '
                                                 'нарисован корабль, '
                                                 'к которому нас выбросило море. \nСудя по всему, нам нужно '
                                                 'идти от корабля на запад, '
                                                 'вдоль моря, там мы увидим синоид. \nДавайте дойдем до туда, '
                                                 'если найдем его, значит, в карте есть толк.</b>', parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - найди синоид</em>",
                                                 parse_mode="html"))
            await InputWhatever.Soch_7.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙В этой локации должна быть карта, поищите ее, '
                                                 'как найдете, напишите ее название.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Маршрут дозированной ходьбы'
                                                 '</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.568647, longitude=39.733668))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf"
                                                           "0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Soch_7)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Soch_7', message.from_user.id)
        if message.text.lower() == 'дионис':

            data["number"] = message.text
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Ну что, получается, идем на поиски '
                                                 'сокровищ.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Ура, товарищи, ура!'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Боцман, что там дальше?'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Дальше нам нужно идти так же на запад, тут '
                                                 'нарисованы амброзия с зубами, '
                                                 'думаю, стоит остерегаться и не поддаваться роскоши острова. '
                                                 '\nВ общем, идем до спуска.</b>', parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - давайте убедимся, что вы идете верно,"
                                                 " какой фрукт видите?</em>", parse_mode="html"))
            await InputWhatever.Soch_8.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Он будет перевернут.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Дионис</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.569898, longitude=39.730465))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk"
                                                           "6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Soch_8)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Soch_8', message.from_user.id)
        if message.text.lower() == 'манго' or message.text.lower() == '🥭':

            data["number"] = message.text
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Осталось чу-чуть, еще нужно пройти вперед, и'
                                                 ' будет тропа в гору, '
                                                 'нужно будет по ней подняться, но на этом все, карта обрывается'
                                                 '.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Не удивлюсь, что когда '
                                                 'мы поднимемся, вторая часть будет лежать на срубленном пеньке, '
                                                 'освещенном солнцем.</b>', parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - как поднимитесь, что видите?</em>",
                                                 parse_mode="html"))
            await InputWhatever.Soch_9.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Как спуститесь, сразу увидите тропический желтый фрукт.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Манго</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.571035, longitude=39.728977))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0"
                                                           "okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Soch_9)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Soch_9', message.from_user.id)
        if (message.text.lower() == 'зимний театр'
                or message.text.lower() == 'театр'
                or message.text.lower() == 'театр зимний'):
            photo_VPS_7 = InputFile("VPS_7.png", 'rb7')
            photo_VPS_100 = InputFile("VPS_100.png", 'rb100')

            data["number"] = message.text
            messages.append(await message.answer('🐙<em>Поднимаясь наверх, группа была удивлена.\n '
                                                 'При освещенном солнце на пеньке сидит старик. '
                                                 '\nСтарику на вид больше ста лет, но сидит он без трости и с ровной '
                                                 'спиной и в позе лотоса.</em>', parse_mode="html"))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_VPS_7))
            messages.append(await message.answer('<u>Старик</u>:\n<b>О... а вот и вы, я вас ждал.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Нас?!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Старик</u>:\n<b>Вы же попали сюда случайно, по не '
                                                 'понятным обстоятельствам?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Молния поразила нос нашего корабль.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Старик</u>:\n<b>Молния... в нос корабля, ну да, это же '
                                                 'частое явление.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>А еще туман был, да'
                                                 ' такой, что я и носа-то своего не видал.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Старик</u>:\n<b>Вы тут не случайно, остров выбрал вас, '
                                                 'и вы гости этого острова, '
                                                 'как и я когда-то.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>То есть вы из этой группы пиратов?'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Старик</u>:\n<b>Все верно.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Сколько вам лет тогда?'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Старик</u>:\n<b>Видишь вот этот большой дуб? '
                                                 '\nКогда-то я посадил на его место жёлудь.</b>', parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_VPS_100))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Это невероятно, ему уже около 150 лет. '
                                                 '\nБред, люди столько не живут, а этот Старец нам еще фору даст.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Старик</u>:\n<b>Это благословение острова, правда я долго'
                                                 ' этого не мог понять.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Может, вы знаете, где нам'
                                                 ' найти остальные части скрижали?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Старик</u>:\n<b>Вы хотите найти сокровище, мы тоже '
                                                 'хотели его найти, '
                                                 'но мы не нашли сундук с золотом, оставьте это, вы еще не '
                                                 'слишком далеко зашли, '
                                                 'остров даст вам время и ресурсы на то, чтобы оправиться и '
                                                 'уплыть домой на новом, '
                                                 'пусть не столь шикарном корабле.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n'
                                                 '<b>Мы думали, что вы нам поможете, '
                                                 'мы взрослые люди, и будем искать то, что вам не удалось найти.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Старик</u>:\n<b>Так или иначе, я все же помогу вам. '
                                                 '\nВторая часть скрижали была найдена нами, но '
                                                 'чем ближе мы подходили к поискам, тем сложнее'
                                                 ' становилось управлять людьми, чем ближе к месту, '
                                                 'тем сильнее жажда выгоды.\n'
                                                 'Найдя вторую скрижаль, мы рассорились, и произошла'
                                                 ' кровопролитная битва, '
                                                 'кто уцелел взял себе по кусочку от разбитой скрижали и унес с собой.'
                                                 '\nЕсли вы хотите найти все кусочки второй скрижали, то вам нужно '
                                                 'будет хорошо постараться.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Старик</u>:\n<b>Первая часть будет у нашего главного места, '
                                                 'оно на западе, отсюда.'
                                                 '\n Там собирались ключевые лица и решались главные вопросы. '
                                                 '\nВозле этого места вы найдете скелета вождя, обыщите его и '
                                                 'найдете первый обломок.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Старик</u>:\n<b>Вторая часть будет у нашего '
                                                 'талантливого музыканта. '
                                                 '\nВы его найдете к югу от вождя.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Старик</u>:\n<b>Третья часть будет у нашего просветлённого,'
                                                 ' который решил закончить свой путь уходом в нирвану. '
                                                 '\nНайти вы его сможете, если найдете нашу святую обитель '
                                                 'и от неё спуститесь вниз.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Старик</u>:\n<b>Четвертую и последнюю часть вы найдете '
                                                 'у нашей воспитательнице, '
                                                 'которая любила детей и всегда вела свои заметки, '
                                                 'ее можно найти на нашей центральной площади.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Старик</u>:\n<b>Что на счет третей скрижали. '
                                                 '\nЕё вы найдете на пересечение дорог, '
                                                 'что каждая вас будет манить, но истина будет та, на что укажет луна.'
                                                 '\nУдачи вам.</b>', parse_mode='html'))
            messages.append(await message.answer('<em>Старик уходит.</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Сходи туда, найди то, '
                                                 'возьми у того.\nЧто просто не дать?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Сундук сразу, да?\nПойдём искать!'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - объедините четыре обломка и прочитайте их.\n"
                                                 "Тут придется пользоваться клавиатурой.\nЕсли у вас пропала "
                                                 "клавиатура, нажмите на четыре точки возле скребки.</em>",
                                                 parse_mode="html", reply_markup=oblomki4))
            await InputWhatever.Soch_14.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Там будет лестница.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>зимний театр</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.572352, longitude=39.730643))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQ"
                                                           "ADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Soch_10)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Soch_10', message.from_user.id)
        if message.text.lower() == 'н.а. островский'\
                or message.text.lower() == 'островский':
            data["number"] = message.text
            messages.append(await message.answer('🐙18.10', reply_markup=oblomki4))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Отличная работа.</b>', parse_mode='html'))
            await InputWhatever.Soch_14.set()
        elif message.text.lower() == '🐙назад':
            data["number"] = message.text
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Может начнем с другой '
                                                 'часть искать?</b>', parse_mode='html', reply_markup=oblomki4))
            messages.append(await message.answer("<em>🐙Если вы собрали все скрижали то объедините их и "
                                                 "разгадайте координаты.</em>",
                                                 parse_mode="html"))
            await InputWhatever.Soch_14.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Это будет большой памятник.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Н.А. Островский</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.579587, longitude=39.724243))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0"
                                                           "okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Soch_11)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Soch_11', message.from_user.id)
        if (message.text.lower() == 'в.высоцкий'
                or message.text.lower() == 'высоцкий'):
            data["number"] = message.text
            messages.append(await message.answer('🐙3.30', reply_markup=oblomki4))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Молодцы.</b>', parse_mode='html'))
            await InputWhatever.Soch_14.set()
        elif message.text.lower() == '🐙назад':
            data["number"] = message.text
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Может начнем с другой '
                                                 'часть искать?</b>', parse_mode='html', reply_markup=oblomki4))
            messages.append(await message.answer("<em>🐙Если вы собрали все скрижали то объедините их и "
                                                 "разгадайте координаты.</em>", parse_mode="html"))
            await InputWhatever.Soch_14.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Статуя будет с гитарой.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>В.Высоцкий</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.578806, longitude=39.723418))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Soch_12)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Soch_12', message.from_user.id)
        if (message.text.lower() == 'северо запад'
                or message.text.lower() == 'на северо запад'
                or message.text.lower() == 'северо-запад'):
            data["number"] = message.text
            messages.append(await message.answer('🐙6.18', reply_markup=oblomki4))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Вот это смекалка.</b>', parse_mode='html'))
            await InputWhatever.Soch_14.set()
        elif message.text.lower() == '🐙назад':

            data["number"] = message.text
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Может начнем с другой '
                                                 'часть искать?</b>', parse_mode='html', reply_markup=oblomki4))
            messages.append(await message.answer("<em>🐙Если вы собрали все скрижали то объедините их и "
                                                 "разгадайте координаты.</em>", parse_mode="html"))
            await InputWhatever.Soch_14.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Нужно объединить.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Северо-Запад</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.581057, longitude=39.720213))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Soch_13)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Soch_13', message.from_user.id)
        if message.text.lower() == 'журнал':
            data["number"] = message.text
            messages.append(await message.answer('🐙1.0', reply_markup=oblomki4))
            messages.append(await message.answer("<em>🐙Если вы собрали все скрижали то объедините их и "
                                                 "разгадайте координаты.</em>", parse_mode="html"))
            await InputWhatever.Soch_14.set()
        elif message.text.lower() == '🐙назад':
            data["number"] = message.text
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Может начнем с другой '
                                                 'часть искать?</b>', parse_mode='html', reply_markup=oblomki4))
            messages.append(await message.answer("<em>🐙Если вы собрали все скрижали то объедините их и "
                                                 "разгадайте координаты.</em>", parse_mode="html"))
            await InputWhatever.Soch_14.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Статуя будет в 30 метрах от центральной площади.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Журнал</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.585133, longitude=39.722380))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Soch_14)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Soch_14', message.from_user.id)
        if (message.text.lower() == 'парк ривьера'
                or message.text.lower() == 'ривьера'):
            photo_VPS_9 = InputFile("VPS_9.png", 'rb9')

            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_VPS_9))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Возможно, мы продвинулись дальше, чем они, '
                                                 'и ощущение куража на пределе, '
                                                 'я даже не знаю, как мы отсюда выберемся, но чувствую, '
                                                 'что это меня уже и не особо '
                                                 'интересует, сейчас у нас одна цель.\nЯ надеюсь, '
                                                 'что мы не перегрыземся, как эти '
                                                 'пираты за золото. '
                                                 '\nКарта ведёт нас через мост, на этом вторая скрижаль '
                                                 'заканчивается, очевидно, что, где-то там будет третья скрижаль, '
                                                 'помнится, что-то про нее говорил Старик.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Старик говорил, '
                                                 '"Что на счет 3-й скрижали.\nТак это вы найдете '
                                                 'на пересечение дорог, '
                                                 'что каждая вас будет манить, но истина будет та, '
                                                 'на что укажет луна".</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>А старик не соврал, '
                                                 'глаза разбегаются, '
                                                 'красивые скалы, водопады,'
                                                 ' фрукты, тут и жить можно.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Давайте сконцентрируемся!'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - кто он?</em>",
                                                 parse_mode="html"))
            await InputWhatever.Soch_15.set()
        elif message.text.lower() == 'перейти к поиску 1️⃣ обломка':
            data["number"] = message.text
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Старик говорил, что первая часть будет у'
                                                 ' нашего главного места, оно на западе, отсюда.\n'
                                                 'Там собирались ключевые лица и решались главные вопросы.'
                                                 '</b>', parse_mode='html', reply_markup=types.ReplyKeyboardRemove()))
            messages.append(await message.answer("<em>🐙Задача - как зовут вождя?</em>",
                                                 parse_mode="html", reply_markup=back_VPS))
            await InputWhatever.Soch_10.set()
        elif message.text.lower() == 'перейти к поиску 2️⃣ обломка':
            data["number"] = message.text
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Старик говорил, '
                                                 'что вторая часть будет у нашего талантливого музыканта. '
                                                 '\nВы его найдете к югу от вождя.</b>', parse_mode='html',
                                                 reply_markup=types.ReplyKeyboardRemove()))
            messages.append(await message.answer("<em>🐙Задача - как его зовут музыканта?</em>",
                                                 parse_mode="html", reply_markup=back_VPS))
            await InputWhatever.Soch_11.set()
        elif message.text.lower() == 'перейти к поиску 3️⃣ обломка':
            photo_VPS_8 = InputFile("VPS_8.png", 'rb8')
            data["number"] = message.text
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Старик говорил, '
                                                 'что третья часть будет у нашего просветлённого, '
                                                 'который решил закончить свой путь уходом в нирвану. '
                                                 '\nНайти вы его сможете, если найдете нашу святую обитель '
                                                 'и от неё спуститесь вниз.</b>',
                                                 parse_mode="html",
                                                 reply_markup=types.ReplyKeyboardRemove()))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_VPS_8))
            messages.append(await message.answer("<em>🐙Задача - куда повернута его голова?</em>",
                                                 parse_mode="html", reply_markup=kompas))
            await InputWhatever.Soch_12.set()
        elif message.text.lower() == 'перейти к поиску 4️⃣ обломка':
            data["number"] = message.text
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Старик говорил, что четвертую и последнюю'
                                                 ' часть вы найдете у нашей воспитательнице, '
                                                 'которая любила детей и всегда вела свои заметки. '
                                                 'Её можно найти на нашей центральной площади.</b>', parse_mode='html',
                                                 reply_markup=types.ReplyKeyboardRemove()))
            messages.append(await message.answer("<em>🐙Задача - что у неё в руках?</em>",
                                                 parse_mode="html", reply_markup=back_VPS))
            await InputWhatever.Soch_13.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Кот-14.33.21.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Парк Ривьера</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.587953, longitude=39.715370))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_M"
                                                           "EbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Soch_15)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Soch_15', message.from_user.id)
        if (message.text.lower() == 'космонавт'
                or message.text.lower() == 'космонавт ссср'
                or message.text.lower() == 'ссср'):
            photo_VPS_10 = InputFile("VPS_10.png", 'rb9')
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_VPS_10))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Ура, у нас получилось '
                                                 'найти все части скрижали и объединить их в одно целое. '
                                                 '\nБоцман, давай, я хочу быстрее получить свое сокровище!'
                                                 '</b>', parse_mode='html',
                                                 reply_markup=types.ReplyKeyboardRemove()))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Не томи, говори, куда '
                                                 'нам нужно идти дальше!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Я не понимаю, раньше был маршрут, '
                                                 'а теперь столько поворотов, '
                                                 'тут можно заблудиться, это лабиринт какой-то, я не понимаю.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n'
                                                 '<b>Врет он все, хочет золото себе все забрать, не верю!'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Успокойтесь! Вы что, хотите, '
                                                 'чтобы мы закончили, как те пираты?!</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Старик</u>:\n<b>А Капитан дело говорит.</b>', parse_mode='html'))
            messages.append(await message.answer('<em>🐙Все удивленно поворачиваются. Старик уже не '
                                                 'тот, что был несколько часов назад, '
                                                 'он слаб, идет с тростью и едва может говорить.'
                                                 '</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Раз ты знал, куда нужно идти, '
                                                 'что просто не привел нас сюда?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Старик</u>:\n<b>Я служу острову, а не вам. '
                                                 '\nЯ так полагаю, вы думаете, что скоро станете богатыми? '
                                                 '\nМы в своё время также думали.'
                                                 '\nИ чтобы найти тут сокровища, мы разделились по одному, '
                                                 'в тот момент, когда мы разъединились,'
                                                 ' все как будто поняли, что с золотом уйдет отсюда только один.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Так получается, ты тот самый, который'
                                                 ' ушел с золотом?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Старик</u>:\n<b>Плохо ты меня слушал, я не нашел золото, '
                                                 'но то сокровище, которое вы ищете,'
                                                 ' не сделает вас богатым материально, это ни золото, это познание '
                                                 'мира, бытия и шанс выбраться '
                                                 'отсюда домой, если вы достойны этого, мы не были достойны.\nИ '
                                                 'вот как мы закончили, '
                                                 'а остров выбрал меня как посланника из меньших грехов. '
                                                 '\nЕсли вы достойны, то не распыляйтесь на все блага, что тут есть, '
                                                 'идите вперед и слепо ищите руки, что освящают жизнь.</b>',
                                                 parse_mode='html'))
            messages.append(await message.answer('🐙<em>Старик умирает.</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Вот те раз, умер.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Старик прав, соблазна много, '
                                                 'куда идти непонятно.\n'
                                                 'Давайте не будет разбиваться на группы и рассматривать то, '
                                                 'что нас погубит.</b>', parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - что спрятано в треугольнике?</em>",
                                                 parse_mode="html"))
            await InputWhatever.Soch_16.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Гордость России. \n1961 года.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Космонавт</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.592473, longitude=39.716619))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQX"
                                                           "zwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Soch_16)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Soch_16', message.from_user.id)
        if (message.text.lower() == 'капсула времени'
                or message.text.lower() == 'капсула'):
            photo_VPS_11 = InputFile("VPS_11.png", 'rb10')
            data["number"] = message.text
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Свиток? Даже не серебро, а '
                                                 'просто клочок бумаги?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Уйди, вам бы лишь бы деньги, старик с '
                                                 'самого начала сказал, что золота нет.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Разведывательная группа</u>:\n<b>Но сокровище же,'
                                                 ' как понимать еще?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Боцман</u>:\n<b>Может, мы еще не закончили искать сокровище. '
                                                 '\nВдруг это карта, где спрятан сундук с золотом? '
                                                 '\nДавайте прочтем.</b>', parse_mode='html'))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_VPS_11))
            messages.append(await message.answer('🐙<em>Поздравляю, вы смогли пройти испытание острова и доказать, '
                                                 'что достойны вернуться назад.'
                                                 '\nВ награду вы получите свой корабль, '
                                                 'на котором плыли, в целостности и '
                                                 'со всеми своими вещами. '
                                                 '\nНемногим удостоилась бы на этом острове, побывать тут, '
                                                 'столкнуться со сложностями острова. '
                                                 '\nЭто бесценный опыт, что дарует остров, используйте его с умом. '
                                                 '\nПопутного ветра вам.</em>', parse_mode="html"))
            await message.answer("<b>🐙Конец.©</b>", parse_mode="html", reply_markup=finish)
            await InputWhatever.Soch_finish.set()
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == '🚪':
            await state.finish()
            db.update_user_state('start', message.from_user.id)
            if message.from_user.id in ADMIN_IDS:
                await message.answer('🐙 🫱 <code>1219523153</code> 🫲 | <b>Выберите одну из функций ниже:</b>',
                                     parse_mode='html')
                await bot.send_message(message.from_user.id,
                                       '1. Смена состояния\n'
                                       '2. Запустить бота',
                                       reply_markup=admin_kb2)
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Вы точно не сворачивали? \nРуки, не рука.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Капсула времени</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=43.592473, longitude=39.716619))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_M"
                                                           "EbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Soch_finish)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Soch_finish', message.from_user.id)
    async with state.proxy() as data:
        if 'messages' in data.keys():
            for msg in data['messages'][::-1]:
                try:
                    await msg.delete()
                except Exception:
                    pass
        if message.text.lower() == "🐙конец":
            mp3_Soch = InputFile('V_poiskah_sokrovish.mp3', 'Конец')
            await bot.send_audio(chat_id=message.chat.id, audio=mp3_Soch)
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
