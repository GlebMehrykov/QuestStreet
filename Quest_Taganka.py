import random
from datetime import datetime

import aiogram.utils.exceptions
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile

import AIP_Taganka
from db import Database
from keybords import *

db = Database("2.db")
bot = Bot(token=AIP_Taganka.TELEGRAM_BOT)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db.create_table_users()
responses = ['🐙Да, да.', '🐙Прювет', "🐙Как ты там?", '🐙Кто выпил весь ром!', "🐙На абордаж", "🐙Ну чего тебе?",
             '🐙Как долго ты готов(а) со мной общаться?', "🐙А это забавно."]
ADMIN_IDS = [1219523153, 6522187160]
class InputWhatever(StatesGroup):
    Taga_1 = State()
    Taga_Pay = State()
    Taga_2 = State()
    Taga_3 = State()
    Taga_4 = State()
    Taga_5 = State()
    Taga_6 = State()
    Taga_7 = State()
    Taga_8 = State()
    Taga_9 = State()
    Taga_10 = State()
    Taga_11 = State()
    Taga_12 = State()
    Taga_13 = State()
    Taga_14 = State()
    Taga_15 = State()
    Taga_16 = State()
    Taga_17 = State()
    Taga_18 = State()
    Taga_19 = State()
    Taga_20 = State()
    Taga_100 = State()
    Taga_finish = State()
class AdminState(StatesGroup):
    select_user = State()
    change_user_state = State()


@dp.callback_query_handler(state=InputWhatever.Taga_finish)
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
        await message.answer(text='<b>🐙Вы попал в квест "Пришельцы" на Ⓜ️Таганская.'
                                  '\nВ этом квесте:         🛸'
                                  '\nВы пройдетесь по интересным локация,       🚶‍♂️'
                                  '\nПолучите интересные задания,           📖'
                                  '\nПогрузитесь в экшен,               ☠️'
                                  '\nВступите в ополчение,          🛡'
                                  '\nПознакомитесь с пришельцами.</b>👽'
                                  '\n \n \n         <em>🐙Пройти квест</em> ---> /Aliens'
                                  '\n \n \n<a href="https://t.me/QuestStreetBot"><b>Выбрать другой '
                                  'квест.</b></a>', parse_mode='html', disable_web_page_preview=True)


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
            InlineKeyboardButton('Предыдущая <<<', callback_data='previous'),
            InlineKeyboardButton('Следующая >>>', callback_data='next')
        )
        await call.message.edit_text('Выберите пользователя из меню ниже или напишите сюда его chat_id',
                                     reply_markup=admin_select_user)


@dp.callback_query_handler(text='change_state', state=[None, AdminState])
async def select_new_state(call: types.CallbackQuery):
    await AdminState.change_user_state.set()
    await call.message.answer('<b>🐙Напишите номер нового состояния из списка ниже.'
                              '<em>\nФормат списка: состояние = номер состояния.\n '
                              '\n</em></b>'
                              'Taga_1 = <b>1</b>,'
                              '\nTaga_Pay = <b>2</b>,'
                              '\nTaga_2 = <b>3</b>,'
                              '\nTaga_3 = <b>4</b>,'
                              '\nTaga_4 = <b>5</b>,'
                              '\nTaga_5 = <b>6</b>,'
                              '\nTaga_6 = <b>7</b>,'
                              '\nTaga_7 = <b>8</b>,'
                              '\nTaga_8 = <b>9</b>,'
                              '\nTaga_9 = <b>10</b>,'
                              '\nTaga_10 = <b>11</b>,'
                              '\nTaga_11 = <b>12</b>,'
                              '\nTaga_12 = <b>13</b>,'
                              '\nTaga_13 = <b>14</b>,'
                              '\nTaga_14 = <b>15</b>,'
                              '\nTaga_15 = <b>16</b>,'
                              '\nTaga_16 = <b>17</b>,'
                              '\nTaga_17 = <b>18</b>,'
                              '\nTaga_18 = <b>19</b>,'
                              '\nTaga_19 = <b>20</b>,'
                              '\nTaga_20 = <b>21</b>,'
                              '\nTaga_100 = <b>22</b>,'
                              '\nTaga_finish = <b>23</b>.', parse_mode='html')


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
        await message.answer('🐙Такой пользователь не найден в базе данных.')


@dp.message_handler(state=AdminState.change_user_state)
async def change_user_state_f(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        dict_values = {1: ' Taga_1',
                       2: ' Taga_Pay',
                       3: ' Taga_2',
                       4: ' Taga_3',
                       5: ' Taga_4',
                       6: ' Taga_5',
                       7: ' Taga_6',
                       8: ' Taga_7',
                       9: ' Taga_8',
                       10: ' Taga_9',
                       11: ' Taga_10',
                       12: ' Taga_11',
                       13: ' Taga_12',
                       14: ' Taga_13',
                       15: ' Taga_14',
                       16: ' Taga_15',
                       17: ' Taga_16',
                       18: ' Taga_17',
                       19: ' Taga_18',
                       20: ' Taga_19',
                       21: ' Taga_20',
                       22: ' Taga_100',
                       23: ' Taga_finish'}
        if int(message.text) in range(1, 24):
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
        await callback.message.edit_text(text='<b>🐙Вы попал в квест "Пришельцы" на Ⓜ️Таганская.'
                                              '\nВ этом квесте:         🛸'
                                              '\nВы пройдетесь по интересным локация,       🚶‍♂️'
                                              '\nПолучите интересные задания,           📖 '
                                              '\nПогрузитесь в экшен,               ☠️'
                                              '\nВступите в ополчение,          🛡'
                                              '\nПознакомитесь с пришельцами.</b>👽'
                                              '\n \n \n         <em>🐙Пройти квест</em> ---> /Aliens</b>'
                                              '\n \n \n<a href="https://t.me/QuestStreetBot"><b>Выбрать другой '
                                              'квест.</b></a>', parse_mode='html', disable_web_page_preview=True)
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


@dp.message_handler(commands=["Aliens"])
async def start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        photo_taga_0 = InputFile("Taga_0.jpg", 'rb')
        messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_taga_0))
        messages.append(await message.answer("<b>🐙Добро пожаловать в квест 'Пришельцы'\n "
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
        await InputWhatever.Taga_1.set()
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_1)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        d1 = datetime.now()
        data['start_time'] = d1
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_1', message.from_user.id)
        if message.text.lower() == "go":
            await message.answer(d1.strftime("%H:%M:%S"))
            data["number"] = message.text
            messages.append(await message.answer("<b>🐙Таймер на прохождение квеста запущен.\nНачало."
                                                 "</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙На улице стояла прелестная погода, не жарко, "
                                                 "но тепло, в этом году лето людей сильно не баловало, "
                                                 "но сегодня природа дала людям немного счастья."
                                                 "</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Миша</u>:\n<b>Эй, Кость, ты видел, вышел новый фильм про "
                                                 "пришельцев, давай сходим.\n"
                                                 "Говорят, что эта картина заставляет людей иначе относиться "
                                                 "к жизни за границей нашей планеты</b>.\n ",
                                                 parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Не, ты же знаешь, я не люблю фантастику, "
                                                 "я больше классику уважаю, да и не кино, а театры</b>.\n ",
                                                 parse_mode='html'))
            messages.append(await message.answer('<em>🐙проходят мимо \"Театр на Таганке\".'
                                                 '</em>', parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Вот, кстати, театр.\nГоворят "
                                                 "там новый спектакль вышел \"Белый кот, черная кошка\", "
                                                 "не хочешь сходить?</b>",
                                                 parse_mode='html'))
            messages.append(await message.answer("<u>Миша</u>:\n<b>Ну, может, как-нибудь...</b>\n ",
                                                 parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Что это с погодой стало?</b>\n ",
                                                 parse_mode='html'))
            messages.append(await message.answer("<u>Миша</u>:\n<b>Дождь, опять!\nНадоел.</b>\n ",
                                                 parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Солнце вообще ушло, облака стали черными! "
                                                 "\nЧто творится!\n"
                                                 "Это не похоже на грозу или что-то подобное!</b>\n ",
                                                 parse_mode='html'))
            messages.append(await message.answer("<em>\n🐙Земля затряслась.</em>\n ",
                                                 parse_mode='html'))
            messages.append(await message.answer("<u>Миша</u>:\n<b>Возможно, нас кто-то атакует!</b>\n ",
                                                 parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Не неси ерунду.</b>\n ",
                                                 parse_mode='html'))
            messages.append(await message.answer("<u>Миша</u>:\n<b>Я думаю, нам нужно укрыться, пошли в метро, там "
                                                 "должно быть безопасно.</b>\n ",
                                                 parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Не думаю, что метро сейчас "
                                                 "лучший выбор, ты посмотри какая давка, "
                                                 "если мы туда и попадём, то не думаю, "
                                                 "что выживем в этой давке, да и кислорода не хватит.</b>\n ",
                                                 parse_mode='html'))
            messages.append(await message.answer("\n<u>Миша</u>:\n<b>Есть идея по лучше.\nЯ знаю, что тут где-то"
                                                 " есть неподалеку бункер, "
                                                 "лучше скроемся там, люди про него не знают, "
                                                 "там и все необходимое есть для того, чтоб переждать "
                                                 "эту неадекватную бурю.\nПосмотри, "
                                                 "машины отрываются от земли, такой ветер, идти сложно,"
                                                 " нужно быстрее добраться туда! \nЗа мной!</b>\n ",
                                                 parse_mode='html'))
            messages.append(await message.answer("<em>🐙Цель - быстрее добраться до места!</em>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Задача - что перед Миром?</em>",
                                                 parse_mode="html"))
            await InputWhatever.Taga_Pay.set()
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
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙go'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>go</code> 🫲', parse_mode='html'))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8"
                                                           "ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Taga_Pay)
async def get_number(message: types.Message):
    db.update_user_state('Taga', message.from_user.id)
    if message.from_user.id in ADMIN_IDS and message.text == '/skip8998':
        await message.answer('🐙Вы успешно пропустили процесс оплаты.\n'
                             'Напишите 🫱 <code>Серп и молот</code> 🫲.', parse_mode='html')
        await InputWhatever.Taga_2.set()
    elif message.text.lower() == 'назад':
        await InputWhatever.Taga_1.set()
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
                             '\nВы точно у 42?', parse_mode='html')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Тут должен быть ответ, но его не будет, видите ли, первая задача'
                             ' квеста достаточно простая, '
                             'при все это у вас есть подсказка, и я уверен, что вы справитесь с этой задачей.\n'
                             'После оплаты квеста вам будут доступны ответы, но чтобы оплатить, вам нужно пройти '
                             'первую задачу, а чтобы ее пройти, нужно приехать и разгадать ее.\n'
                             '<b>Все квесты по 1500р.</b>', parse_mode='html')
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == 'глеб, дай скидку!🙏🏻':
        await bot.send_message(message.from_user.id, '🐙Особым гостям, особая цена!')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста',
                               description='Оплата для того, чтобы пройти квест!',
                               provider_token="390540012:LIVE:40818",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=300 * 100)])
    elif message.text.lower() == 'гилшод' or message.text.lower() == 'гилшот':
        await bot.send_message(message.from_user.id, '🐙Особым гостям, особая цена!')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста',
                               description='Оплата для того, чтобы пройти квест!',
                               provider_token="390540012:LIVE:40818",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=1200 * 100)])
    else:
        await bot.send_message(message.from_user.id, '🐙Оплатите квест, для того чтобы продолжить работу бота')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста',
                               description='Оплата для того, чтобы пройти квест!',
                               provider_token="390540012:LIVE:40818",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=1500 * 100)])


@dp.pre_checkout_query_handler(state=InputWhatever.Taga_Pay)
async def process_precheck(precheck: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(precheck.id, ok=True)


@dp.message_handler(content_types=[types.ContentType.SUCCESSFUL_PAYMENT], state=InputWhatever.Taga_Pay)
async def successful_payment(message: types.Message):
    if message.successful_payment.invoice_payload == 'buy_sub':
        await bot.send_message(message.from_user.id, '🐙Вы успешно оплатили доступ к боту!💸\n'
                                                     'Напишите ответ на предыдущий вопрос')
        await InputWhatever.Taga_2.set()


@dp.message_handler(state=InputWhatever.Taga_2)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_2', message.from_user.id)
        if message.text.lower() == "серп и молот" or message.text.lower() == "молот":
            photo_taga_1 = InputFile("taga_1.png", 'rb1')
            photo_taga_2 = InputFile("taga_2.jpg", 'rb2')
            data["number"] = message.text
            messages.append(await message.answer("<u>Костя</u>:\n<b>Да, ты прав, тут и вправду нет людей,"
                                                 " и есть все необходимое: еда, вода, телевизор, интернет, "
                                                 "но что мы тут жить останемся?!</b>\n ",
                                                 parse_mode='html'))
            messages.append(await message.answer("\n<u>Миша</u>:\n<b>Сейчас погода разгуляется, и выйдем.</b>\n ",
                                                 parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Смешно, мы пока бежали, меня два раза "
                                                 "чуть машина не прибила, благо столб помешал, "
                                                 "так еще и дерево перед глазами упало, я не думаю, "
                                                 "что это скоро закончится!</b>",
                                                 parse_mode='html'))
            messages.append(await message.answer("\n<u>Миша</u>:\n<b>Расслабься, самое страшное позади, давай "
                                                 "заварим себе чай и посмотрим телевизор, "
                                                 "вдруг там что-то скажут интересное.</b>\n",
                                                 parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Я сделаю кофе, пожалуй.</b>\n ",
                                                 parse_mode='html'))
            messages.append(await message.answer("\n<u>Миша</u>:\n<b>Пожалуй.</b>\n ",
                                                 parse_mode='html'))
            messages.append(await message.answer("<em><b>🐙Включается телевизор на самом интересном месте.\n</b> "
                                                 "📺Прямой эфир - граждане, срочные новости, мы пока не знаем "
                                                 "с чем имеем дело, "
                                                 "облако опустились на землю, ужасная видимость, на часах 17:30"
                                                 ", а видимость как "
                                                 "будто 00:00.\nМЧС и синоптики уже занимаются этим вопросом."
                                                 " \nУбедительная просьба: "
                                                 "граждане, соблюдайте спокойствие, не выходите из дома, те"
                                                 " кто уже попал в метро, "
                                                 "сидите и ждите гуманитарной помощи, она скоро появится! \n"
                                                 "Ни в коем случае не "
                                                 "выходите на улицу. \nОдну секунду, мне только что поступила "
                                                 "информация, наши камеры "
                                                 "заметили, что туман начал резко рассеиваться, погода "
                                                 "понемногу приходит в норму, "
                                                 "но вдали виднеются какие-то высокие дома, непонятно откуда "
                                                 "они взялись, они стоят "
                                                 "на дороге, очень странная ситуация творится, я "
                                                 "повторяюсь, сидеть дома!"
                                                 "</em>", parse_mode="html"))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_taga_1))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Вот тебе кофе, что говорят там?"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("\n<u>Миша</u>:\n<b>Уже лучше, но мы все еще в заднице!"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Это Россия, тут всегда так было."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Бууууууум, Буууууууууум.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Ты это слышал?</b>", parse_mode='html'))
            messages.append(await message.answer("\n<u>Миша</u>:\n<b>Эм да, что-то упало нам на крышу?"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Или пробило её, нужно посмотреть, я гляну."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Поднимается на второй этаж и видит, как небесный "
                                                 "корабль припарковался рядом и как игрушечную крышу "
                                                 "сдвинул ее в сторону.\nТуман начал рассеиваться, и "
                                                 "солнце уже давало свои лучи, хотя и весьма слабые.</em>",
                                                 parse_mode='html'))
            messages.append(await message.answer("\n<u>Миша</u>:\n<b>Что, что там?!</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Лучше тебе этого не знать, но бункер "
                                                 "оказался не такой безопасный!</b>", parse_mode='html'))
            messages.append(await message.answer("\n<u>Миша</u>:\n<b>Что это значит.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>А то, что бункер должен находиться под "
                                                 "землей, а не на втором этаже!\n"
                                                 "Вообще крыши у нас больше нет, предлагаю валить отсюда!"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("\n<u>Миша</u>:\n<b>Я так понимаю, к метро, "
                                                 "там самое безопасное место!</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Пошли.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Выбегают на улицу, а там перестрелка."
                                                 "</em>", parse_mode="html"))
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_taga_2))
            messages.append(await message.answer("\n<u>Миша</u>:\n<b>Вашу мать!"
                                                 "\nЧто здесь твориться?\nПочему здесь военные!"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Дорога, которая ведет нас к метро, "
                                                 "сейчас является полигоном.\n"
                                                 "Может подойти к военным, они наверное должны сказать, "
                                                 "что нам делать.</b>", parse_mode='html'))
            messages.append(await message.answer("\n<u>Миша</u>:\n<b>Да, да, только осторожно, а то еще лихой "
                                                 "пули не хватало!</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Тихим голосом, затем все громче и громче."
                                                 "</em>", parse_mode="html"))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Ребята, ау, ребята, "
                                                 "военные, военные! Военные! Аууу!</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Какого хрена вы тут делаете, сосунки!"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Мы решили спрятаться в бункере."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Но это же бункер-музей!"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Миша</u>:\n<b>Даааа... а мы не знали."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Не подскажете, с кем вы там "
                                                 "перестреливаетесь?</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>С небес спустились космические"
                                                 " корабли, и оттуда вышли пришельцы, "
                                                 "сейчас мы их называем чужими, но похоже, что пули "
                                                 "их особо не берут, но и они "
                                                 "пока не проявляют излишней агрессии, мы "
                                                 "предполагаем, что они боятся прямых лучей "
                                                 "солнца, а результата мы особо не добиваемся, я не "
                                                 "намерен больше терять своих "
                                                 "бойцов, скоро мы будем сворачиваться!\nЯ могу "
                                                 "выдать вам оружие, будете в нашем "
                                                 "ополчении.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Закапал дождь.</em>", parse_mode="html"))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Да вы издеваетесь, "
                                                 "еще и дождь, он скроет солнце, и тогда мы "
                                                 "увидим, на что они способны, я уже достаточно потерял бойцов"
                                                 "</b>.", parse_mode="html"))
            messages.append(await message.answer('<em>🐙Свистит.</em>', parse_mode="html"))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Эй, бойцы сворачиваемся,"
                                                 " нам нужно найти группу <em>'Красной армии'</em> "
                                                 "и еще лучше переждать ночь!</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>За мной!\nВсе за мной!"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<b>🐙Маршрут - меж 42 и 703, выше рыбы, ниже ног, "
                                                 "возле булки.</b>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Задача - найдите 5 бойцов красной армии, "
                                                 "как зовут Командира?</em>",
                                                 parse_mode="html"))
            await InputWhatever.Taga_3.set()
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
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Вы точно у 42?'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Серп и молот</code> 🫲.', parse_mode='html'))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_3)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_3', message.from_user.id)
        if message.text.lower() == 'андрей' or message.text.lower() == 'андрей люблинский':
            photo_taga_3 = InputFile("taga_3.png", 'rb3')
            data["number"] = message.text
            db.new_level(message.chat.id)
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_taga_3))
            messages.append(await message.answer("<u>Командир Красной армии</u>:\n<b>Слава Капитану, "
                                                 "он нас нашел! \nМы уже долгое время сидим и отбиваемся, "
                                                 "мы потеряли связь с подстанцией и стали отрезаны от мира"
                                                 ".</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Мы успели взять ваши координаты "
                                                 "перед тем, как связь потерялась, "
                                                 "мы тоже остались без связи, думаю нам больше незачем "
                                                 "здесь оставаться, "
                                                 "победить врага мы не можем, а умирать просто так я не собираюсь, и "
                                                 "вашими жизнями разбрасываться тоже!\n"
                                                 "Командир, доложи обстановку.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Командир</u>:\n<b>Основная высадка чужих была в "
                                                 "центре Москвы, сведений не много Капитан.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Нам нужно выходить из Москвы! "
                                                 "\nСолнце уйдет в закат минут через двадцать, "
                                                 "знаете, я не очень готов с ними биться, так-что, че стоим, "
                                                 "кого ждем, ноги в "
                                                 "руки и пошли отсюда!</b>", parse_mode='html'))
            messages.append(await message.answer("<b>🐙Маршрут - тут становится опасно, "
                                                 "нам следует идти по красной дорожке, она приведет нас к оазису.\n"
                                                 "Скорее время на исходе!\n "
                                                 "\nЗадача - Сколько башен на четвертой ступени?"
                                                 "</b>", parse_mode="html"))
            await InputWhatever.Taga_4.set()
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
            messages.append(await message.answer('Без Яндекс карты далеко не уйдете, маршрут длинный, 1.5км.'
                                                 '\n42 это бункер, а рыба это ресторан.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Андрей</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.744848, longitude=37.635825))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_4)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_4', message.from_user.id)
        if message.text.lower() == '4' or message.text.lower() == "четыре":
            data["number"] = message.text
            messages.append(await message.answer("<u>Миша</u>:\n<b>О нет! Солнце ушло!</b>", parse_mode="html"))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Они уже здесь, но смотрите,"
                                                 " чужие не могут зайти сюда.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Их что-то сдерживает."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Тут, получается, безопасно.\nНо"
                                                 " мы не можем сидеть тут вечно, нам нужно выбираться отсюда."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Один из чужих попытался зайти, и брызги "
                                                 "воды стали разъедать его кожу.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Миша</u>:\n<b>Получается, они боятся воды."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Я не думаю, что так просто."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Один из членов команды облил чужого своей"
                                                 " питьевой водой, но ничего не произошло."
                                                 "</em>", parse_mode="html"))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Я же говорил.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Видимо, это не простая вода."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer('<em>🐙Обращает внимание на висящее рядом  воскресенское '
                                                 'кадило.</em> ',
                                                 parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Кажется, я понял.\nИтак, '
                                                 'что мы знаем, что пули их не берут, но они боятся '
                                                 'света и какой-то воды.</b>', parse_mode='html'))
            messages.append(await message.answer("<u>Командир</u>:\n<b>Значит, на рассвете нам "
                                                 "нужно обзавестись этим оружием!</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Тогда отдыхайте, бойцы.\nА я "
                                                 "узнаю, где можно найти эту воду, и на рассвете поведу "
                                                 "вас.</b>", parse_mode='html'))
            messages.append(await message.answer("<b>🐙Куда идем?</b>", parse_mode="html"))
            await InputWhatever.Taga_5.set()
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
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Красная дорожка, она возле вас, и она вас приведет к оазису.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>4</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.741924, longitude=37.629041))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_5)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_5', message.from_user.id)
        if message.text.lower() == "воскресенская церковь":
            data["number"] = message.text
            messages.append(await message.answer("<b>🐙Вы ответили верно! "
                                                 "\nОтправляйтесь туда.</b>", parse_mode="html"))
            messages.append(await message.answer("<b>🐙Давайте убедимся, что вы пришли куда нужно.\n"
                                                 "Сколько клумб у ворот?</b>", parse_mode="html"))
            await InputWhatever.Taga_6.set()
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
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Обратите внимание на кадило.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Воскресенская '
                                                 'церковь</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.742965, longitude=37.622292))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_6)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_6', message.from_user.id)
        if message.text.lower() == '2' or message.text.lower() == 'два':
            photo_taga_4 = InputFile("taga_4.png", 'rb4')
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_taga_4))
            messages.append(await message.answer("<em>🐙Резервуары наполнены.</em>", parse_mode="html"))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Церковь пуста, но и не "
                                                 "удивительно.\nЛадно, мы возьмем своё, и "
                                                 "я надеюсь, никто против не будет, а Бог нас не покарает."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Командир</u>:\n<b>Капитан, какие дальнейшие планы?"
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Наш город в беде!\nМы не "
                                                 "можем позволить себе сбежать, поджав хвост, "
                                                 "нам необходимо разобраться с этим, тем более "
                                                 "мы обладаем сильным оружием!</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Миша</u>:\n<b>Я думаю, что у них есть капитан"
                                                 " или вождь, если бы мы хоть чуточку знали о них, "
                                                 "мы могли бы разглядеть их иерархическую цепочку и"
                                                 " поразить их вождя!</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Если мы сейчас пойдём к "
                                                 "центру, то мы так или иначе больше о них узнаем."
                                                 "</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Идет с улицы священник."
                                                 "</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Священник</u>:\n<b>Братья и сестры, я по "
                                                 "пути сюда встретил группу бойцов, "
                                                 "которые потеряли связь и след, "
                                                 "мне удалось выдать им немного святой воды, "
                                                 "чтобы они могли добраться до "
                                                 "безопасной точки, но им все равно нужна помощь,"
                                                 " как хорошо, что я встретил такую "
                                                 "серьёзную группу ополчения, "
                                                 "если бы вы успели прийти к ним на помощь, то "
                                                 "они бы вам рассказали то, что увидели.\n"
                                                 "Они говорили про какой-то небесный корабль, возле которого "
                                                 "творятся странные вещи, но вам нужно поторопиться!"
                                                 "\nЕсли выйдите сейчас, то прибудите туда примерно "
                                                 "через час, как и они.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Где, где это место, как туда "
                                                 "добраться!</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Священник</u>:\n<b>Я напишу маршрут, "
                                                 "надеюсь вы не заблудитесь!</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Священник передал вам карту, написанную от руки, "
                                                 "следуйте ей и вы придете на нужное место.</em>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Задача - встать спиной к шлагбауму, лицом к дороге, "
                                                 "поверните на право.\nСколько метров над детьми?"
                                                 "</em>", parse_mode="html"))
            await InputWhatever.Taga_7.set()
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
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Возможно? вы не с той стороны заходите.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>2</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.742965, longitude=37.622292))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_7)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_8', message.from_user.id)
        if message.text.lower() == '50':
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Так держать, первый поворот направо."
                                                 "</em>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Задача - какого цвета забор?</em>", parse_mode="html"))
            await InputWhatever.Taga_8.set()
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
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙У вас права есть?'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>50</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.743227, longitude=37.621555))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_8)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_9', message.from_user.id)
        if message.text.lower() == "черный":
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Все верно, идём дальше до развилки там налево."
                                                 "</em>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Задача - что за братья?</em>", parse_mode="html"))
            await InputWhatever.Taga_9.set()
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
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙йынреч'))
        elif message.text.lower() == 'красный':
            messages.append(await message.answer('🐙Да ну ты чего, он же черный.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Черный</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.743656, longitude=37.622190))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_9)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_10', message.from_user.id)
        if message.text.lower() == "караваевы":
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Супер. Дальше нужно перейти на сторону братьев "
                                                 "и продолжить маршрут в том же направлении.</em>", parse_mode="html"))
            messages.append(await message.answer("<em>🐙Задача - что виднеется вдали?\n"
                                                 "Полное название.</em>", parse_mode="html"))
            await InputWhatever.Taga_10.set()
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
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙У них большая сеть.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Караваевы</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.744671, longitude=37.624855))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_10)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_11', message.from_user.id)
        if message.text.lower() == "храм василия блаженного":
            data["number"] = message.text
            messages.append(await message.answer("<b>🐙Да святится имя его!</b>", parse_mode="html"))
            messages.append(await message.answer("<b>🐙Молодец, держимся правой стороны и идём по мосту к "
                                                 "Храму и спускаемся по первой лестнице.</b>", parse_mode="html"))
            messages.append(await message.answer("<b>🐙Как спустился с лестницы сразу увидел 6 лавок? "
                                                 "</b>", parse_mode="html", reply_markup=yesno))
            await InputWhatever.Taga_11.set()
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
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Это же наше достопримечательность, '
                                                 'но возможно вы пишите не полное название.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Храм василия блаженного</code> 🫲.'
                                                 '', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.752510, longitude=37.622699))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_11)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_12', message.from_user.id)
        if message.text.lower() == "нет":
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Значит вы свернул правильно.\n"
                                                 "Переходим два светофора  с правой стороны и идём вдоль набережной "
                                                 "по левой стороне.</em>", parse_mode="html",
                                                 reply_markup=types.ReplyKeyboardRemove()))
            messages.append(await message.answer("<em>🐙Задача - слева видишь смотровую?</em>",
                                                 parse_mode="html", reply_markup=yesno))
            await InputWhatever.Taga_12.set()
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
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text == 'да':
            messages.append(await message.answer("🐙Видишь?\nЭх, придется возвращаться."))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Нажмите на четыре точки.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Нет</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.748523, longitude=37.625633))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI"
                                                           "_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_12)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_13', message.from_user.id)
        if message.text.lower() == "да":
            photo_taga_5 = InputFile("taga_5.png", 'rb5')
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_taga_5))
            messages.append(await message.answer("<b>🐙well done! Забирайтесь туда.</b>", parse_mode="html",
                                                 reply_markup=types.ReplyKeyboardRemove()))
            messages.append(await message.answer('<u>Командир</u>:\n<b>Путь был не простой, но мы '
                                                 'дошли до места назначения, тут хорошая локация, '
                                                 'чужие в этих местах не сильно обитают, посмотрите,'
                                                 ' они все на другой стороне, ну а если '
                                                 'кто-то до нас дойдет, '
                                                 'то у нас ещё много святой воды. \nТемнеет, другая'
                                                 ' группа должна была уже добраться сюда, '
                                                 'надеюсь, они доберутся до заката солнца, ну а мы '
                                                 'пока что разобьем тут лагерь.</b>', parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Бойцы, укрепить территорию, "
                                                 "избавиться от запахов и дежурить по двое!\n"
                                                 "Смена караула каждые два часа.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Командир, какие у нас планы "
                                                 "на завтра?</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Дождемся вторую группу, у них есть "
                                                 "важная информация, а наша задача запастись оружием."
                                                 " \nСейчас самое время отдохнуть.</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Идёт вторая группа.</em>", parse_mode="html"))
            messages.append(await message.answer('<u>Алексей</u>:\n<b>Приветствую Капитан, меня '
                                                 'зовут Алексей, я привел группу выживших из зоны отчуждения.\n'
                                                 'Страшные времена пришли.\n'
                                                 'Я узнал кое-что о чужих, они прилетели из космоса '
                                                 'и хотят захватить планету, '
                                                 'они не имеют большого интеллекта и дисциплины, '
                                                 'но они весьма выносливы и опасны.\n'
                                                 'Так же я узнал, что они боятся солнца и святой воды.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Удивил.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Алексей</u>:\n<b>Но самое главное, что недалеко отсюда '
                                                 'у них остановился главный корабль, и в основном '
                                                 'все чужие разбежались мародёрствовать, так что '
                                                 'под сердцем главного корабля '
                                                 'достаточно безопасно, но путь будет все равно не '
                                                 'простым, нам нужно будет'
                                                 ' выйти завтра утром, на восходе солнца.</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Так и сделаем!</b>', parse_mode='html'))
            messages.append(await message.answer('<em>🐙Утро.</em>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Командир, я получил еще '
                                                 'информацию, все мосты были взорваны, кроме одного, '
                                                 'через который они передвигаются, '
                                                 'но там не пройти, их слишком много, и помощи ждать '
                                                 'будете неоткуда.\nТакже чужие захватили'
                                                 ' небо, и авиация нам тоже не поможет, так что мы '
                                                 'только своими силами должны пробраться '
                                                 'к ним в корабль и взорвать его.\n<em>Известно, '
                                                 'что главный корабль находится'
                                                 ' на зеленой территории, между детьми'
                                                 ' и перевёрнутым якорем, как только мы подойдем '
                                                 'ближе, чем на сто метров, нас сразу учуют, '
                                                 'и пути назад не будет, нужно действовать '
                                                 'быстро.</em></b>', parse_mode="html"))
            messages.append(await message.answer("<em>🐙Задача - куда направляемся?</em>", parse_mode="html"))
            await InputWhatever.Taga_13.set()
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
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text == 'нет':
            messages.append(await message.answer('Возможно, вам стоит еще пройтись вперед.'))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Ну какая тебе тут подсказа, тут или да, или нет.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Да</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.748715, longitude=37.628991))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI"
                                                           "_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_13)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_14', message.from_user.id)
        if message.text.lower() == "сквер репина" or message.text.lower() == "репинский сквер":
            data["number"] = message.text
            messages.append(await message.answer("<em>🐙Как подойдете к скверу, напишите. \"▶️\"\n"
                                                 "Чтоб не искать смаил вы можете написать в "
                                                 "ТЛ 'старт' и через 3 секунды"
                                                 " ТЛ предложит заменить это слово на смаил.\n"
                                                 "Эта часть квеста имеет отдельное время прохождения.</em>",
                                                 parse_mode="html"))
            await InputWhatever.Taga_14.set()
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
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Репку читали? Скверная, да?'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Сквер Репина</code> 🫲.', parse_mode='html'))
            messages.append(await bot.send_location(chat_id=message.from_user.id,
                                                    latitude=55.745121, longitude=37.617629))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI"
                                                           "_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages

@dp.message_handler(state=InputWhatever.Taga_14)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        d3 = datetime.now()
        data['sqver_time'] = d3
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_15', message.from_user.id)
        if message.text.lower() == "▶️" or message.text.lower() == "▶" or message.text.lower() == "старт":
            photo_taga_6 = InputFile("taga_6.png", 'rb6')
            await message.answer(d3.strftime("%H:%M:%S"))
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_taga_6))
            messages.append(await message.answer('<u>Алексей</u>:\n<b>Командир, я думаю, нас '
                                                 'заметили, нельзя медлить, нужно подойти к кораблю.'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Капитан</u>:\n<b>Не торопитесь, видите магическую оболочку '
                                                 'вокруг?</b>', parse_mode='html'))
            messages.append(await message.answer('<u>Алексей</u>:\n<b>Кажется, да.\nЯ вижу, что '
                                                 'она идет от нескольких точек, '
                                                 'возможно, следует сначала разобраться с ними!'
                                                 '</b>', parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - исключительно на территории сквера, "
                                                 "что левитирует?</em>", parse_mode="html"))
            await InputWhatever.Taga_15.set()
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
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Отправьте этот смаил ▶️.\nЕсли смаил не работает пишите "Старт"'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>▶️</code> 🫲.', parse_mode='html'))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI"
                                                           "_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_15)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_16', message.from_user.id)
        if message.text.lower() == "качели":
            messages.append(await message.answer("<b>🐙Изумительно!</b>", parse_mode="html",
                                                 reply_markup=types.ReplyKeyboardRemove()))
            messages.append(await message.answer("<u>Миша</u>:\n<b>Не знаю что мы сделали, правильно ли мы сделали, "
                                                 "но щит пропал, а вместе с ним и корабль!</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Мы победили?</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Алексей</u>:\n<b>Не думаю, что он"
                                                 " стал прозрачный, его едва видно, видимо, это "
                                                 "их защита.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Что ж, хорошие новости, они"
                                                 " нас боятся, но нам нужно разобраться с этим и побыстрее!</b>",
                                                 parse_mode='html'))
            messages.append(await message.answer("<em>🐙Задача - сколько человеческих лиц вы видите на памятнике\n"
                                                 "(Кусочек лица считается за лицо.)\n"
                                                 "\"Дети - жертвы пророков взрослых\"?</em>",
                                                 parse_mode="html", reply_markup=xkb))
            await InputWhatever.Taga_16.set()
            data["number"] = message.text
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
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Они летают туда сюда.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Качели</code> 🫲.', parse_mode='html'))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI"
                                                           "_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_16)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_18', message.from_user.id)
        if message.text.lower() == '11':
            photo_taga_7 = InputFile("Taga_7.jpg", 'rb7')
            data["number"] = message.text
            messages.append(await bot.send_photo(chat_id=message.chat.id, photo=photo_taga_7))
            messages.append(await message.answer("<u>Командир</u>:\n<b>Корабль снова появился,"
                                                 " похоже он группируется и хочет взлететь!</b>", parse_mode='html',
                                                 reply_markup=types.ReplyKeyboardRemove()))
            messages.append(await message.answer("<u>Алексей</u>:\n<b>Нам срочно нужно успеть "
                                                 "его взорвать, остальные корабли не "
                                                 "трогать, только самый главный, "
                                                 "они должны убегать в страхе!\nИ забыть навсегда дорогу до Земли.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Я вижу, что корабль берет энергию от статуи, "
                                                 "нужно разобраться откуда идет энергия и пресечь ее!</b>", parse_mode='html'))
            messages.append(await message.answer("<b>🐙Чего больше всего на статуе Репина?</b>",
                                                 parse_mode="html"))
            await InputWhatever.Taga_17.set()
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
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Обойдите его, осмотритесь.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>11</code> 🫲.', parse_mode='html'))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_17)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            messages = data['messages']
        else:
            messages = []

        db.update_user_state('Taga_20', message.from_user.id)
        if message.text.lower() == "пуговица" or message.text.lower() == "пуговиц":
            d3 = data['sqver_time']
            data["number"] = message.text
            d2 = datetime.now()
            result = (d2 - d3)
            d2 = d2.strftime("%H:%M:%S")
            hours, minutes, seconds = str(result).split(':')
            seconds = seconds.split('.')[0]
            await message.answer(f'🐙Время прохождение сквера: {hours}:{minutes}:{seconds}')
            messages.append(await message.answer("<em>🐙Победа!</em>", parse_mode="html",
                                                 reply_markup=types.ReplyKeyboardRemove()))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Мы уничтожили все "
                                                 "преграды, осталось дело за малым, бежим к "
                                                 "главному кораблю.\nАлексей, минируй!</b>", parse_mode='html'))
            messages.append(await message.answer("<em>🐙Алексей минирует корабль.</em>", parse_mode='html'))
            messages.append(await message.answer("<u>Алексей</u>:\n<b>Бомба заложена!\nА теперь "
                                                 "группируемся и валим с этого места!</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Миша</u>:\n<b>Но чужие поняли, что мы тут "
                                                 "и группируются у моста!\nЧто делать?</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Напролом, они в панике, "
                                                 "они уже поняли, что проиграли и не будут пытаться "
                                                 "нас уничтожить, они хотят домой, "
                                                 "так пусть валят откуда пришли!\nГруппируемся,"
                                                 " полный напор воды, вперёд!</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Костя</u>:\n<b>Да, мы прошли мост.\nЧужие "
                                                 "пытаются уйти на оставшихся кораблях.\n"
                                                 "Капитан, это исключительно ваша заслуга.</b>", parse_mode='html'))
            messages.append(await message.answer("<u>Капитан</u>:\n<b>Да, я знаю!</b>", parse_mode='html'))
            await message.answer("<em>🐙Конец!©</em>", parse_mode="html", reply_markup=finish)
            await InputWhatever.Taga_finish.set()
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
        elif message.text.lower() == '🐙':
            messages.append(await bot.send_message(message.chat.id, random.choice(responses)))
        elif message.text.lower() == 'help' or message.text.lower() == '/help':
            messages.append(await message.answer('🐙Только те что видим.'))
        elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
            messages.append(await message.answer('🐙Ответ: 🫱 <code>Пуговица</code> 🫲', parse_mode='html'))
        else:
            messages.append(await bot.send_sticker(message.from_user.id,
                                                   sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_"
                                                           "MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ"))
        messages.append(message)
        data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_100)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Taga_100', message.from_user.id)
    if (message.text.lower() == 'answer'
            or message.text.lower() == 'help'):
        async with state.proxy() as data:
            data["number"] = message.text
            if 'messages' in data.keys():
                messages = data['messages']
            else:
                messages = []
            messages.append(await message.answer('🐙Нажмите 🫱 <code><u>Серп и молот</u></code>. 🫲 '
                                                 '\nИ отправьте ответ Боту.',
                                                 parse_mode='html'))
            await InputWhatever.Taga_2.set()
            messages.append(message)
            data['messages'] = messages


@dp.message_handler(state=InputWhatever.Taga_finish)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'messages' in data.keys():
            for msg in data['messages'][::-1]:
                try:
                    await msg.delete()
                except Exception:
                    pass
        db.update_user_state('Taga_finish', message.from_user.id)
        if message.text.lower() == "🐙конец" or message.text.lower() == "конец":
            mp3_taga = InputFile('Taga_mus.mp3', 'Конец')
            await bot.send_audio(chat_id=message.chat.id, audio=mp3_taga)
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
