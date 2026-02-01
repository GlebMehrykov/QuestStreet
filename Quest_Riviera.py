import random
from datetime import datetime

import aiogram.utils.exceptions
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile

import AIP_Riviera
from db import Database
from keybords import *

responses = ['🐙Да, да.', '🐙Прювет', "🐙Как ты там?", '🐙Кто выпил весь ром!', "🐙На абордаж", "🐙Ну чего тебе?",
             '🐙Как долго ты готов(а) со мной общаться?', "🐙А это забавно."]
db = Database("2.db")
bot = Bot(token=AIP_Riviera.TELEGRAM_BOT)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db.create_table_users()
ADMIN_IDS = [1219523153, 6522187160]


class AdminState(StatesGroup):
    select_user = State()
    change_user_state = State()


class InputWhatever(StatesGroup):
    Riviera_1 = State()
    Riviera_Pay = State()
    Riviera_2 = State()
    Riviera_3 = State()
    Riviera_4 = State()
    Riviera_5 = State()
    Riviera_6 = State()
    Riviera_7 = State()
    Riviera_8 = State()
    Riviera_9 = State()
    Riviera_10 = State()
    Riviera_11 = State()
    Riviera_12 = State()
    Riviera_13 = State()
    Riviera_14 = State()
    Riviera_15 = State()
    Riviera_16 = State()
    Riviera_17 = State()
    Riviera_18 = State()
    Riviera_19 = State()
    Riviera_20 = State()
    Riviera_100 = State()
    Riviera_finish = State()


@dp.callback_query_handler(state=InputWhatever.Riviera_finish)
async def ikb_cb_handler(callback: types.CallbackQuery):
    await callback.answer('🐙ИИ меня не устраивает, вакансия открыта, пишите.')


@dp.message_handler(commands=['start'], state=[AdminState, None])
async def start_command(message: types.Message, state: FSMContext):
    print(message.from_user.id)
    db.insert_user(message.from_user.id)
    await state.finish()
    db.update_user_state('start', message.from_user.id)
    if message.from_user.id in ADMIN_IDS:
        await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                             parse_mode='html')
        await bot.send_message(message.from_user.id,
                               '1. Смена состояния\n'
                               '2. Запустить бота',
                               reply_markup=admin_kb)
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    else:
        await message.answer(text='🐙 <b>Мы в Сочи🌞, а вы попали в Квест на Ривьере.'
                                  '\nТут мы предлагаю вам:          🧝‍♀️'
                                  '\nПройтись по приятным локациям,        🌴'
                                  '\nПогрузиться в мир живых кукл,      🔮'
                                  '\nВыполнить интересные задания,          📜'
                                  '\nИ отправиться на луну.         🌜'
                                  '\n<em>       🐙Готовы пройти квест ---> /Riviera</em></b> ?'
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
                              '\nRiviera_1 = <b>1</b>,'
                              '\nRiviera_Pay = <b>2</b>,'
                              '\nRiviera_2 = <b>3</b>,'
                              '\nRiviera_3 = <b>4</b>,'
                              '\nRiviera_4 = <b>5</b>,'
                              '\nRiviera_5 = <b>6</b>,'
                              '\nRiviera_6 = <b>7</b>,'
                              '\nRiviera_7 = <b>8</b>,'
                              '\nRiviera_8 = <b>9</b>,'
                              '\nRiviera_9 = <b>10</b>,'
                              '\nRiviera_10 = <b>11</b>,'
                              '\nRiviera_11 = <b>12</b>,'
                              '\nRiviera_12 = <b>13</b>,'
                              '\nRiviera_13 = <b>14</b>,'
                              '\nRiviera_14 = <b>15</b>,'
                              '\nRiviera_15 = <b>16</b>,'
                              '\nRiviera_16 = <b>17</b>,'
                              '\nRiviera_17 = <b>18</b>,'
                              '\nRiviera_18 = <b>19</b>,'
                              '\nRiviera_19 = <b>20</b>,'
                              '\nRiviera_20 = <b>21</b>,'
                              '\nRiviera_100 = <b>22</b>,'
                              '\nRiviera_finish = <b>23</b>.', parse_mode='html')


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
        dict_values = {1: ' Riviera_1',
                       2: ' Riviera_Pay',
                       3: ' Riviera_2',
                       4: ' Riviera_3',
                       5: ' Riviera_4',
                       6: ' Riviera_5',
                       7: ' Riviera_6',
                       8: ' Riviera_7',
                       9: ' Riviera_8',
                       10: ' Riviera_9',
                       11: ' Riviera_10',
                       12: ' Riviera_11',
                       13: ' Riviera_12',
                       14: ' Riviera_13',
                       15: ' Riviera_14',
                       16: ' Riviera_15',
                       17: ' Riviera_16',
                       18: ' Riviera_17',
                       19: ' Riviera_18',
                       20: ' Riviera_19',
                       21: ' Riviera_20',
                       22: ' Riviera_100',
                       23: ' Riviera_finish'}
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
        await callback.message.edit_text(text='🐙 <b>Мы в Сочи🌞, а вы попали в Квест на Ривьере.'
                                              '\nТут мы предлагаю вам:          🧝‍♀️'
                                              '\nПройтись по приятным локациям,        🌴'
                                              '\nПогрузиться в мир живых кукл,      🔮'
                                              '\nВыполнить интересные задания,          📜'
                                              '\nИ отправиться на луну.         🌜'
                                              '\n<em>       🐙Готовы пройти квест ---> /Riviera</em></b> ?'
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


@dp.message_handler(commands=["Riviera"])
async def start(message: types.Message):
    photo_Riviera_0 = InputFile("Riviera_0.png", 'rb0')
    await bot.send_photo(chat_id=message.chat.id, photo=photo_Riviera_0)
    await message.answer("<b>🐙Добро пожаловать в Парк Ривьера.\n "
                         "Для прохождения вам понадобится:\n1 - 1:30 часа свободного времени\n"
                         "Заряженный телефон\nЯндекс карта\n"
                         "Позитивное настроение😎 </b>", parse_mode="html")
    await message.answer("<b>🐙Для корректной работы с ботом пишите ответы без точек, 'пробелы', "
                         "'/',  '\\',  '-'  допускаются.\n"
                         "Если у вас возникнут трудности то можете написать /help и бот вам подскажет.\n"
                         "Если этого будет мало то пишите /answer и бот выдаст ответ.\n"
                         "Если будут трудности с ботом то пишите. \n🐙---> https://t.me/glebmehrykov\n"
                         "Если у вас пропала клавиатура то нажмите на 4 точки.\n"
                         "</b>", parse_mode="html", disable_web_page_preview=True)
    await message.answer('<b><em>🐙Хочу обратить ваше внимание:'
                         '\nНе пытайтесь пройти квест быстрее, проходите с удовольствием, гуляйте!'
                         '\nКвесты имеют расстояние друг от друга около 50-250м.'
                         '\nКарта Яндекс вам пригодится.'
                         '\nПридется думать.🧠'
                         '\nЕсли вы застряли и писать help или answer не хочется, прочитайте это сообщение еще раз.\n '
                         '\n🐙Стоимость квеста 500р, но вы можете ознакомится с первой частью квеста и пройти его.'
                         '\nПроцесс оплаты будет доступен после прохождения первого задания.</em></b>'
                         '\n \n     <em>Текст защищен. «Российское Авторское Общество»</em> (РАО)',
                         parse_mode='html')
    await message.answer("<b>Если готовы пишите \"<code>go</code>\"</b>", parse_mode='html')
    await InputWhatever.Riviera_1.set()


@dp.message_handler(state=InputWhatever.Riviera_1)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_1', message.from_user.id)
    if message.text.lower() == "go":
        await InputWhatever.Riviera_Pay.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await message.answer("<b>🐙Начало.</b>", parse_mode="html")
        await message.answer('<b>🐙Мир, в котором живут наши персонажи, неведом людям. '
                             '\nЛюди приходят, гуляют, уходят, но так и не замечают их. '
                             '\nА тем временем, у каждой фигуры, скульптуры '
                             '\nв Парке Ривьера есть жизнь, '
                             'и такие же заботы, и мечты как у людей. '
                             '\nДавайте погрузимся в их мир. '
                             '\nКак правило, история начинается с главного персонажа.'
                             '\nНаша же история не будет исключением. '
                             '\nВ нашем парке он – звезда. '
                             '\nОн есть везде: на афишах, плакатах, кружках, майках, поддерживал спортсменов, '
                             'даже в кино его можно увидеть. '
                             '\nСам-то он добрый, пушистый, лопоухий.</b>', parse_mode="html")
        await message.answer("<b>🐙Задача - напишите имя автора нашей звезды.</b>", parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('go')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('Ответ: 🫱 <code>go</code> 🫲', parse_mode='html')
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_Pay)
async def get_number(message: types.Message):
    db.update_user_state('Riviera_Pay', message.from_user.id)
    if message.from_user.id in ADMIN_IDS and message.text == '/skip8998':
        await message.answer('Вы успешно пропустили процесс оплаты.\n'
                             'Напишите 🫱 <code>Эдуард Успенский</code> 🫲.', parse_mode='html')
        await InputWhatever.Riviera_2.set()
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🐙назад':
        await InputWhatever.Riviera_1.set()
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('<b>🐙   Если у вас возникли проблемы с оплатой:</b>\n'
                             '1. Напишите "Назад" затем напишите "go" и попробуйте оплатить еще раз.\n'
                             '2. Попробуйте оплатить другой картой.\n'
                             '3. Если это не помогло то пишите \n🐙---> https://t.me/glebmehrykov\n'
                             '      Пишите: \n              1.В чем трудность.\n              2.Какой квест. \n    '
                             '          3.Ваш TG ID. Узнать его можно в '
                             '\n<a href="https://t.me/QuestStreetBot">Главном меню</a>.'
                             '\n    --->Перейти в свой профиль\n    ---> Информация о моём профиле '
                             '\n    ---> Нажмите на TG ID. \n'
                             ' \n<b>🐙   Если вам нужна подсказка квеста то:</b>\n'
                             '🐙Он будет возле сцены, между Крокодилом и Ларисой.', parse_mode='html')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Тут должен быть ответ, но его не будет, видите ли, первая задача'
                             ' квеста достаточно простая, '
                             'при всем это у вас есть подсказка, и я уверен, что вы справитесь с этой задачей.\n'
                             'После оплаты квеста вам будут доступны ответы, но что бы оплатить вам нужно пройти '
                             'первую задачу, а чтоб ее пройти нужно приехать и разгадать ее.\n'
                             '<b>Все квесты по 500р.</b>', parse_mode='html')
    elif message.text.lower() == 'глеб, нужна скидка':
        await bot.send_message(message.from_user.id, '<b>🐙Особым гостям особая цена.'
                                                     '</b>', parse_mode='html')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста.',
                               description='🐙Оплата для того, чтобы пройти квест.',
                               provider_token="390540012:LIVE:47784",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=250 * 100)])
    else:
        await bot.send_message(message.from_user.id, '<b>🐙Оплатите квест, для того чтобы продолжить работу бота.'
                                                     '</b>', parse_mode='html')
        await bot.send_invoice(message.from_user.id, title='🐙Оплата квеста.',
                               description='🐙Оплата для того, чтобы пройти квест.',
                               provider_token="390540012:LIVE:47784",
                               payload='buy_sub', start_parameter='test_bot',
                               currency='rub',
                               prices=[types.LabeledPrice(label='rub', amount=500 * 100)])


@dp.pre_checkout_query_handler(state=InputWhatever.Riviera_Pay)
async def process_precheck(precheck: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(precheck.id, ok=True)


@dp.message_handler(content_types=[types.ContentType.SUCCESSFUL_PAYMENT], state=InputWhatever.Riviera_Pay)
async def successful_payment(message: types.Message):
    if message.successful_payment.invoice_payload == 'buy_sub':
        await bot.send_message(message.from_user.id, '<b>🐙Вы успешно оплатили доступ к боту.</b>💸\n'
                                                     'Напишите ответ на предыдущий вопрос.', parse_mode='html')
        await InputWhatever.Riviera_2.set()


@dp.message_handler(state=InputWhatever.Riviera_2)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_2', message.from_user.id)
    db.new_level(message.chat.id)
    photo_Riviera_1 = InputFile("Riviera_1.png", 'rb1')
    if message.text.lower() == 'эдуард успенский':
        await InputWhatever.Riviera_3.set()
        d1 = datetime.now()
        await message.answer(d1.strftime("%H:%M:%S"))
        async with state.proxy() as data:
            data["number"] = message.text
            data['start_time'] = d1
        await message.answer("<b>🐙Таймер на прохождение квеста запущен.</b>", parse_mode="html")
        await message.answer("<b>🐙Начните квест от сцены Ривьера.</b>", parse_mode="html")
        await bot.send_photo(chat_id=message.chat.id, photo=photo_Riviera_1)
        await message.answer('Ушастик: Какой прелестный сегодня день! '
                             '\nТак и хочется двинуться на приключения.'
                             '\nЗдравствуйте, Крокодил!'
                             '\nЗдравствуйте, Лариса!'
                             '\nЗдравствуйте, Лошадки!'
                             '\nОх, как я хорошо выгляжу!'
                             '\nЗдравствуйте, Зайчиха!'
                             '\nЗдравствуйте, Люди! Как обычно, так сильно заняты, что не слышат меня.'
                             '\nЗдравствуйте, Господин Хлудовский!'
                             '\nЗдравствуйте, Цапли!'
                             '\nЗдравствуйте, Черепаха!'
                             '\nО, Здравствуй, друг!')
        await message.answer("<b>🐙Давайте вспомним, кого он любил?</b>",
                             parse_mode="html")
        await message.answer("<b>🐙Задача - какую ягоду он любит?</b>",
                             parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Он будет возле сцены, между Крокодилом и Ларисой.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>Эдуард Успенский</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.589350, longitude=39.715953)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_3)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_3', message.from_user.id)
    photo_Riviera_2 = InputFile("Riviera_2.png", 'rb2')
    if message.text.lower() == 'малина' or message.text.lower() == 'малину':
        await InputWhatever.Riviera_4.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await message.answer('Ушастик: Здравствуй друг! '
                             '\nСегодня замечательный день для приключений, не находишь?')
        await bot.send_photo(chat_id=message.chat.id, photo=photo_Riviera_2)
        await message.answer('Деревянный мальчик: Привет! \nКонечно, как и вчера, простоим под солнцем, поулыбаемся,'
                             ' и пойдем готовиться к завтрашнему дню.')
        await message.answer('Ушастик: Нет, он должен быть другим. '
                             '\nНужно сделать что-то особое, чтобы сегодняшний день запомнился. '
                             '\nНужно сделать то, что всегда хотел. '
                             '\nВот скажи чего ты хочешь?')
        await message.answer('Деревянный мальчик: Я бы хотел мороженого.')
        await message.answer('Ушастик: Нет, ну серьезно. '
                             '\nЯ вот хочу отправиться на Луну.')
        await message.answer('Деревянный мальчик: Луну? '
                             '\nЭто же безумие! '
                             '\nА это уже по моей части, подвинься – я с тобой полечу. '
                             '\nЕсть идеи, как туда добраться?')
        await message.answer('Ушастик: Пока никаких. '
                             '\nЯ думал, может ты чего знаешь.')
        await message.answer("<b>🐙В один голос: Точно, Космонавт! \nПошли к нему.</b>",
                             parse_mode="html")
        await message.answer("<b>🐙Задача - напишите страну.</b>",
                             parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Не стесняйтесь,смотреть в интернет.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>Малину</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.589174, longitude=39.714953)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_4)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_4', message.from_user.id)
    photo_Riviera_3 = InputFile("Riviera_3.png", 'rb3')
    if (message.text.lower() == 'ссср'
            or message.text.lower() == 'союз советских социалистических республик'):
        await InputWhatever.Riviera_5.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await message.answer('Деревянный мальчик: Вот он! '
                             '\nЕдинственный, кто смог покинуть нашу планету Ривьера. '
                             '\nИ двух строчек не прислал с Луны.')
        await bot.send_photo(chat_id=message.chat.id, photo=photo_Riviera_3)
        await message.answer('Ушастик: Нужно поспрашивать тех, кто рядом обитают. '
                             '\nМожет они расскажут, как он это сделал.')
        await message.answer('Деревянный мальчик: У кого спрашивать будем?')
        await message.answer('Ушастик: Давай спросим у того, кто выше все обитает. '
                             '\nОн вроде у корабля обитает.')
        await message.answer("<b>🐙Задача - ответ вырван из трех слов. "
                             "\nОтвет будет одним словом.</b>",
                             parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Космонавт будет на пересечении шести дорог.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>СССР</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.589456, longitude=39.715285)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_5)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_5', message.from_user.id)
    photo_Riviera_44 = InputFile("Riviera_44.png", 'rb44')
    if message.text.lower() == 'воробей':
        await InputWhatever.Riviera_6.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await message.answer('Ушастик: Воробей, здравствуй! '
                             '\nТы же в этой части парка выше всех летаешь, подскажи: не видал ли ты Космонавта, '
                             'который отправился на Луну?')
        await bot.send_photo(chat_id=message.chat.id, photo=photo_Riviera_44)
        await message.answer('Воробей: Я голодный даже не общаюсь. '
                             '\nСыра принеси – там поговорим.')
        await message.answer("<b>🐙Задача - найдите сыр, кто его держит. "
                             "\nОтвет найдете в пределах 50 метрах.</b>",
                             parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Он часть пирата.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>Воробей</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.589918, longitude=39.715409)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_6)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_7', message.from_user.id)
    if message.text.lower() == 'ворона':
        await InputWhatever.Riviera_7.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await message.answer('Деревянный мальчик: Вот сыр, воробей. Теперь рассказывай, что знаешь?')
        await message.answer('Воробей: Боцман, сбрасывай якорь. Будем праздновать!')
        await message.answer("<b>🐙Задача - найдите каменный якорь, что за знак на якоре?</b>",
                             parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Посмотрите за динозавром.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>Ворона</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.589613, longitude=39.715223)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_7)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_7', message.from_user.id)
    photo_Riviera_5 = InputFile("Riviera_5.png", 'rb5')
    if message.text.lower() == 'звезда':
        await InputWhatever.Riviera_8.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await bot.send_photo(chat_id=message.chat.id, photo=photo_Riviera_5)
        await message.answer('Деревянный мальчик: Как сыр?')
        await message.answer('Воробей: Хорошо, да мало! '
                             '\nЕще бы.')
        await message.answer('Деревянный мальчик: Не увиливай, расскажи, '
                             'что знаешь про Космонавта и как нам с Ушастиком отправиться на Луну.')
        await message.answer('Воробей: Ах, вы на Луну собрались! '
                             '\nЧто ж, удачи! '
                             '\nЯ с Космонавтом особо не общался, так что не знаю про него. '
                             '\nНо есть Попугай, что сидит на синем плече, охраняет воду. '
                             '\nСходите к нему. '
                             '\nЯ думаю, он вам поможет.')
        await message.answer('Деревянный мальчик: Ух, придется пройтись.')
        await message.answer("<b>🐙Задача - давайте проверим, что вы нашли того попугая, какого он цвета?"
                             "\nЦвета будет два.</b>",
                             parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Там будет два якоря.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>Звезда</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.590073, longitude=39.715305)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_8)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_8', message.from_user.id)
    photo_Riviera_55 = InputFile("Riviera_55.png", 'rb55')
    photo_Riviera_6 = InputFile("Riviera_6.png", 'rb6')
    if (message.text.lower() == 'красно-желтый'
            or message.text.lower() == 'красно желтый'
            or message.text.lower() == 'желтый красно'
            or message.text.lower() == 'желтый-красно'):
        await InputWhatever.Riviera_9.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await bot.send_photo(chat_id=message.chat.id, photo=photo_Riviera_55)
        await message.answer('Попугай: Звезда пришла звезда, что хотел?')
        await message.answer('Ушастик: Мы хотим отправиться на Луну. '
                             '\nВоробей сказал, что ты можешь помочь нам с этим. '
                             '\nНе знаешь ли что-нибудь о том, что поможет нам повторить его маршрут?')
        await message.answer('Попугай: Щас, так и рассказал! '
                             '\nЯ видел откуда он отправился на Луну, '
                             'но скажу я вам только если поможете разгадать загадку – иначе, до свидания.')
        await message.answer('Деревянный мальчик: Конечно, поможем! '
                             '\nГовори, что за загадка.')
        await bot.send_photo(chat_id=message.chat.id, photo=photo_Riviera_6)
        await message.answer('Попугай: По аллее пойдешь, писателей найдешь, но музыку не увидишь, но фею найдешь  '
                             '– и сразу все поймешь. '
                             '\nВопрос, кто они? '
                             '\nЯ летал, летал, да только ничего не увидал.'
                             '\nМожет вам удастся.')
        await message.answer("<b>🐙Задача - кто они?</b>",
                             parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Пройдите по аллее великих и найдете воду.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>Красно-желтый</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.591568, longitude=39.716731)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_9)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_9', message.from_user.id)
    if (message.text.lower() == 'фонари'
            or message.text.lower() == 'фонарные столбы'
            or message.text.lower() == 'фонарный столб'):
        await InputWhatever.Riviera_10.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await message.answer('Деревянный мальчик: Мы отгадали твою загадку. '
                             '\nДоволен? '
                             '\nТеперь рассказывай, откуда Космонавт отправился на Луну?')
        await message.answer('Попугай: Верно, как же я сам-то не догадался. '
                             '\nЛадно уговор есть уговор.'
                             '\nОтправляйтесь на лунную площадку, оттуда Космонавт совершил полет. '
                             '\nНайти вы её сможете возле дома великана.')
        await message.answer('Деревянный мальчик: Не просто получается до Луны добраться.')
        await message.answer('Ушастик: А я знал, что путь до Луны идет через терни.')
        await message.answer('Попугай: А еще, в Ривьере с Космонавтом хорошо общались гномы. '
                             '\nОни проектировали корабль.\nИ Скелет, '
                             'он делал ему костюм, спросите у него.', reply_markup=Riviera_kb)
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Они не просто музыкальные звезда, они еще и светятся как звезда.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>Фонарные столбы</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.592188, longitude=39.716248)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_10)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_10', message.from_user.id)
    if message.text.lower() == 'отправиться к гномам⛏':
        await InputWhatever.Riviera_11.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await message.answer('Найдите Гномов, что они с собой несут.',
                             reply_markup=types.ReplyKeyboardRemove())
        await message.answer("<b>🐙Задача - найдите гномов, что они с собой несут?</b>",
                             parse_mode="html")
    elif message.text.lower() == 'отправиться к скелету💀':
        await InputWhatever.Riviera_17.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await message.answer("<b>🐙Задача - Скелета вы найдете за солнцем."
                             "\nГде находится Скелет?</b>",
                             parse_mode="html", reply_markup=types.ReplyKeyboardRemove())
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Если у вас пропала клавиатура, то нажмите 4 точки.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>Отправиться к Скелету💀</code> 🫲,'
                             ' 🫱 <code>Отправиться к Гномам⛏</code> 🫲.',
                             parse_mode='html')
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_11)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_11', message.from_user.id)
    photo_Riviera_7 = InputFile("Riviera_7.png", 'rb7')
    if message.text.lower() == 'золото':
        await InputWhatever.Riviera_12.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await bot.send_photo(chat_id=message.chat.id, photo=photo_Riviera_7)
        await message.answer('Первый гном: Опять набрали золото в треть больше себя.')
        await message.answer('Второй гном: Обоих. '
                             '\nМы пока донесем, половину растеряв. '
                             '\nВон, опять упала монета.')
        await message.answer('Первый гном: Эх... Как бы домой-то попасть?')
        await message.answer('Ушастик: Гномы, здравствуйте!')
        await message.answer('Второй гном: Ой, здравствуйте, ребята! '
                             '\nЗолото не дадим, сами ищите!')
        await message.answer('Первый гном: Да, идите дальше.')
        await message.answer('Деревянный мальчик: Что вы, мы не за золотом! '
                             '\nНас к вам Попугай отправил. ')
        await message.answer('Ушастик: Да. '
                             '\nОн сказал, что вы видели как Космонавт отправился на Луну.')
        await message.answer('Первый гном: Ну видели.')
        await message.answer('Деревянный мальчик: Подскажите, пожалуйста, как он это сделал.')
        await message.answer('Второй гном: Скажем. '
                             '\nТолько вы помогите нам, и мы скажем. '
                             '\nНам нужно попасть домой, но боимся, что там стервятники летают. '
                             '\nМы посадили туда людей. \n'
                             'Но они достали свои телефоны и уставились в них – не хотят работать. '
                             '\nВот если бы вы проверили обстановку, то мы бы сказали.')
        await message.answer('Ушастик: Уже идем.')
        await message.answer("<b>🐙Задача - найдите дом гномов. "
                             "\nИз чего сделаны стены их дома?</b>",
                             parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Гномы будут возле аллеи.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>Золото</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.591923, longitude=39.715916)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_12)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_12', message.from_user.id)
    photo_Riviera_8 = InputFile("Riviera_8.png", 'rb8')
    if message.text.lower() == 'бамбук':
        await InputWhatever.Riviera_13.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await message.answer('Ушастик: Стервятников нет –  можете спокойно идти.')
        await message.answer('Второй гном: Спасибо! '
                             '\nБереженого Бог бережет.')
        await message.answer('Первый гном: Мы проектировали его ракету. '
                             '\nСразу скажу, что больше такой ракеты сделать не получится. '
                             '\nЕсли вы конечно не найдете что-то с скоростью 10.000 в минуту. '
                             '\nДолетел Космонавт, как нам известно, за 3 минуты 27 секунд.')
        await message.answer('Деревянный мальчик: Да, это нам не сильно помогло. '
                             '\nНо, спасибо вам!')
        await message.answer('Ушастик: Теперь нужно найти Скелета.')
        await message.answer("<b>🐙Задача - Скелета вы найдете за солнцем. "
                             "\nГде находится Скелет?</b>",
                             parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await bot.send_photo(chat_id=message.chat.id, photo=photo_Riviera_8)
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>бамбук</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.588955, longitude=39.715194)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_13)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_13', message.from_user.id)
    photo_Riviera_9 = InputFile("Riviera_9.png", 'rb9')
    if message.text.lower() == 'в клетке':
        await InputWhatever.Riviera_14.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await message.answer('Ушастик: Скелет, Здравствуйте!')
        await bot.send_photo(chat_id=message.chat.id, photo=photo_Riviera_9)
        await message.answer('Скелет: О, шпана пришла! '
                             '\nЧто, хотите отправиться на Луну? '
                             '\nНо вам, я так полагаю, нужен костюм, чтоб отправиться на Луну.')
        await message.answer('Деревянный мальчик: В точку, Сер! '
                             '\nА как вы узнали?')
        await message.answer('Скелет: Мир тесен, друзья. '
                             '\nСорока нашептала. '
                             '\nЕще она сказала, что вы ребята сообразительные, ответственные. '
                             '\nА у меня как раз для вас есть задание. '
                             '\nВыполните – и я выделю вам два костюма. '
                             '\nВам нужен костюм?')
        await message.answer('Ушастик: Конечно нужен. '
                             '\nВсе сделаем. '
                             '\nКак мы можем вам услужить?')
        await message.answer('Скелет: В Ривьере есть легенда о подземном великане, '
                             'который защищает нас от злых помыслов подземного мира и всегда одной рукой с нами. '
                             '\nНайдите его руку.')
        await message.answer("<b>🐙Задача - что в руке?</b>",
                             parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Солнце находится на территории Ривьеры.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>В клетке</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.593851, longitude=39.716846)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_14)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_14', message.from_user.id)
    if message.text.lower() == 'дерево':
        await InputWhatever.Riviera_15.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await message.answer('Скелет: Что ж, легенда не врет. '
                             '\nЯ доволен. '
                             '\nВот вам костюмы, используйте их с умом.')
        await message.answer('Ушастик: Спасибо вам!')
        await message.answer('Ушастик: Костюмы это хорошо. '
                             '\nНо как же мы без корабля-то?')
        await message.answer('Деревянный мальчик: Давай сходим на то место, откуда отправлялся космонавт. '
                             '\nМожет там мы что-то да найдем. '
                             '\nНапомнишь, что там говорил Попугай?')
        await message.answer('Ушастик: Вроде "Отправляйтесь на лунную площадку, оттуда космонавт совершил полет. '
                             '\nНайти вы её сможете возле дома великана."')
        await message.answer('Деревянный мальчик: Сегодня день загадок. '
                             '\nПойдем искать.', reply_markup=xkb)
        await message.answer("<b>🐙Задача - сколько Лун вы насчитали?</b>",
                             parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Будет возле космической базы.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>дерево</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.590991, longitude=39.715734)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_15)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_15', message.from_user.id)
    photo_Riviera_10 = InputFile("Riviera_10.png", 'rb10')
    if message.text.lower() == '12':
        await InputWhatever.Riviera_16.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await message.answer('Ушастик: Вот это место!',
                             reply_markup=types.ReplyKeyboardRemove())
        await message.answer("<b>🐙«Буммм».</b>",
                             parse_mode="html")
        await message.answer('Деревянный мальчик: Что это было?')
        await message.answer("<b>🐙Смотрят за угол, видят великана.</b>",
                             parse_mode="html")
        await bot.send_photo(chat_id=message.chat.id, photo=photo_Riviera_10)
        await message.answer("<b>🐙«Буммм».</b>",
                             parse_mode="html")
        await message.answer('Ушастик: Велика, Здравствуйте!')
        await message.answer('Великан: Доброго дня, ребята!')
        await message.answer('Деревянный мальчик: Ого! '
                             '\nВы такой сильный! '
                             '\nА вы самый сильный на планете?')
        await message.answer('Велика: Конечно.')
        await message.answer('Деревянный мальчик: А я слышал, что самый сильный был двигатель, '
                             'который имел скорость 10.000 в секунду. '
                             '\nНо сейчас этот двигатель на Луне. '
                             '\nТак что, вы точно самый сильный.')
        await message.answer('Великан: Вздор, я всегда был сильнее всех.')
        await message.answer('Деревянный мальчик: То есть у вас хватит сил, чтоб отправить нас на Луну?')
        await message.answer('Великан: Конечно, хватит. Боюсь, что могу и перебросить. '
                             '\nНужно точное расстояние, чтоб я смог вас перебросить туда. ')
        await message.answer("<b>🐙Задача - какое расстояние необходимо преодолеть от планеты Ривьера до Луны.</b>",
                             parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Если вы нашли дом великана, то вы очень рядом с лунной площадкой.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>12</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.588991, longitude=39.715459)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_16)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_16', message.from_user.id)
    photo_Riviera_11 = InputFile("Riviera_11.png", 'rb11')
    if (message.text.lower() == '32.700'
            or message.text.lower() == '32700'):
        await InputWhatever.Riviera_finish.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await message.answer('Великан: Уверены? ')
        await message.answer('Ушастик: На все 100%.')
        await message.answer('Великан: Ну тогда пристегните ремни. '
                             '\nВы отправляетесь на Луну.')
        await message.answer('🐙Оба в один голос: Ура! Ура!')
        await message.answer('Так наши герои исполнили они свою мечту. '
                             '\nТак и вы идите к своей мечте, и пусть вас ничего не пугает.')
        await message.answer("<b>🐙Конец.©</b>",
                             parse_mode="html", reply_markup=finish)
        await bot.send_photo(chat_id=message.chat.id, photo=photo_Riviera_11)
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Мы знаем, что от планеты Ривьера до Луны 3 минуты 27 секунд при скорости '
                             'в 10.000 в минуту.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>32.700</code> 🫲.', parse_mode='html')
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_17)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_17', message.from_user.id)
    photo_Riviera_9 = InputFile("Riviera_9.png", 'rb9')
    if message.text.lower() == 'в клетке':
        await InputWhatever.Riviera_18.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await message.answer('Ушастик: Скелет, Здравствуйте!')
        await bot.send_photo(chat_id=message.chat.id, photo=photo_Riviera_9)
        await message.answer('Скелет: О, шпана пришла! '
                             '\nЧто, хотите отправиться на Луну? '
                             '\nНо вам, я так полагаю, нужен костюм, чтоб отправиться на Луну.')
        await message.answer('Деревянный мальчик: В точку, Сер! '
                             '\nА как вы узнали?')
        await message.answer('Скелет: Мир тесен, друзья. '
                             '\nСорока нашептала. '
                             '\nЕще она сказала, что вы ребята сообразительные, ответственные. '
                             '\nА у меня как раз для вас есть задание. '
                             '\nВыполните – и я выделю вам два костюма. '
                             '\nВам нужен костюм?')
        await message.answer('Ушастик: Конечно нужен. '
                             '\nВсе сделаем. '
                             '\nКак мы можем вам услужить?')
        await message.answer('Скелет: В Ривьере есть легенда о подземном великане, '
                             'который защищает нас от злых помыслов подземного мира и всегда одной рукой с нами. '
                             '\nНайдите его руку.')
        await message.answer("<b>🐙Задача - что в руке?</b>",
                             parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Солнце находится на территории Ривьеры.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>в клетке</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.593847, longitude=39.716845)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_18)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_18', message.from_user.id)
    if message.text.lower() == 'дерево':
        await InputWhatever.Riviera_19.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await message.answer('Скелет: Что ж, легенда не врет. '
                             '\nЯ доволен. '
                             '\nВот вам костюмы, используйте их с умом.')
        await message.answer('Ушастик: Спасибо вам!')
        await message.answer("<b>🐙Получено два костюма.</b>", parse_mode="html")
        await message.answer('Ушастик: Костюмы это хорошо. '
                             '\nНо как же мы без корабля-то?')
        await message.answer('Деревянный мальчик: Давай теперь Гномов искать. '
                             '\nМожет они помогут.')
        await message.answer("<b>🐙Задача - найдите гномов, что они с собой несут?</b>",
                             parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Будет возле космической базы.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>дерево</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.590991, longitude=39.715734)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_19)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_19', message.from_user.id)
    photo_Riviera_7 = InputFile("Riviera_7.png", 'rb7')
    if message.text.lower() == 'золото':
        await InputWhatever.Riviera_20.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await bot.send_photo(chat_id=message.chat.id, photo=photo_Riviera_7)
        await message.answer('Первый гном: Опять набрали золото в треть больше себя.')
        await message.answer('Второй гном: Обоих. '
                             '\nМы пока донесем, половину растеряв. '
                             '\nВон, опять упала монета.')
        await message.answer('Первый гном: Эх... Как бы домой-то попасть?')
        await message.answer('Ушастик: Гномы, здравствуйте!')
        await message.answer('Второй гном: Ой, здравствуйте, ребята! '
                             '\nЗолото не дадим, сами ищите!')
        await message.answer('Первый гном: Да, идите дальше.')
        await message.answer('Деревянный мальчик: Что вы, мы не за золотом! '
                             '\nНас к вам Попугай отправил. ')
        await message.answer('Ушастик: Да. '
                             '\nОн сказал, что вы видели как космонавт отправился на Луну.')
        await message.answer('Первый гном: Ну видели.')
        await message.answer('Деревянный мальчик: Подскажите, пожалуйста, как он это сделал.')
        await message.answer('Второй гном: Скажем. '
                             '\nТолько вы помогите нам, и мы скажем. '
                             '\nНам нужно попасть домой, но боимся, что там стервятники летают. '
                             '\nМы посадили туда людей. \n'
                             'Но они достали свои телефоны и уставились в них – не хотят работать. '
                             '\nВот если бы вы проверили обстановку, то мы бы сказали.')
        await message.answer('Ушастик: Уже идем.')
        await message.answer("<b>🐙Задача - найдите дом гномов. "
                             "\nИз чего сделаны стены их дома?</b>",
                             parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await message.answer('🐙Гномы будут возле аллеи.')
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>Золото</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.591923, longitude=39.715916)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")


@dp.message_handler(state=InputWhatever.Riviera_20)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_20', message.from_user.id)
    photo_Riviera_8 = InputFile("Riviera_8.png", 'rb8')
    if message.text.lower() == 'бамбук':
        await InputWhatever.Riviera_15.set()
        async with state.proxy() as data:
            data["number"] = message.text
        await message.answer('Ушастик: Стервятников нет –  можете спокойно идти.')
        await message.answer('Второй гном: Спасибо! '
                             '\nБереженого Бог бережет.')
        await message.answer('Первый гном: Мы проектировали его ракету. '
                             '\nСразу скажу, что больше такой ракеты сделать не получится. '
                             '\nЕсли вы конечно не найдете что-то с скоростью 10.000 в минуту. '
                             '\nДолетел Космонавт, как нам известно, за 3 минуты 27 секунд.')
        await message.answer('Деревянный мальчик: Да, это нам не сильно помогло. '
                             '\nНо, спасибо вам!')
        await message.answer('Деревянный мальчик: Да, поиски затягиваются.')
        await message.answer('Ушастик: Но за-то посмотри как далеко мы добрались. ')
        await message.answer('Деревянный мальчик: Это верно, пошли лунную площадку искать.'
                             '\nНапомнишь, что там говорил Попугай? ')
        await message.answer('Ушастик: Вроде "Отправляйтесь на лунную площадку, оттуда Космонавт совершил полет. '
                             '\nНайти вы её сможете возле дома великана."')
        await message.answer('Деревянный мальчик: Пойдем искать.', reply_markup=xkb)
        await message.answer("<b>🐙Задача - сколько Лун вы насчитали?</b>",
                             parse_mode="html")
    elif message.text.lower() == '🐙':
        await bot.send_message(message.chat.id, random.choice(responses))
    elif message.text.lower() == '🚪':
        await state.finish()
        db.update_user_state('start', message.from_user.id)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('<code>1219523153</code> | <b>Выберите одну из функций ниже:</b>',
                                 parse_mode='html')
            await bot.send_message(message.from_user.id,
                                   '1. Смена состояния\n'
                                   '2. Запустить бота',
                                   reply_markup=admin_kb2)
    elif message.text.lower() == 'help' or message.text.lower() == '/help':
        await bot.send_photo(chat_id=message.chat.id, photo=photo_Riviera_8)
    elif message.text.lower() == 'answer' or message.text.lower() == '/answer':
        await message.answer('🐙Ответ: 🫱 <code>Бамбук</code> 🫲.', parse_mode='html')
        await bot.send_location(chat_id=message.from_user.id, latitude=43.588955, longitude=39.715194)
    else:
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEKH5xk6IubLf0okOjYoI_MEbbPMQXzwAACAQADr8ZRGhLj3-N0EyK_MAQ")

@dp.message_handler(state=InputWhatever.Riviera_100)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_100', message.from_user.id)
    if (message.text.lower() == 'answer'
            or message.text.lower() == 'help'):
        async with state.proxy() as data:
            data["number"] = message.text
        await InputWhatever.Riviera_2.set()
        await message.answer('🐙Нажмите 🫱 <code><u>Эдуард Успенский</u></code> 🫲 \nИ отправьте ответ Боту.',
                             parse_mode='html')


@dp.message_handler(state=InputWhatever.Riviera_finish)
async def get_number(message: types.Message, state: FSMContext):
    db.update_user_state('Riviera_finish', message.from_user.id)
    if message.text.lower() == "🐙конец":
        mp3_Riviera = InputFile('Riviera_mus.mp3', 'Конец')
        await bot.send_audio(chat_id=message.chat.id, audio=mp3_Riviera)
        db.new_level(message.chat.id)
        async with state.proxy() as data:
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
    elif (message.text.lower() == 'Вернуться в начало квеста▶️'
          or message.text.lower() == 'Вернуться в начало квеста▶'
          or message.text.lower() == '▶️'
          or message.text.lower() == '▶'):
        await state.finish()
        await message.answer('🐙Вы успешно закончили квест! '
                             'Для того чтобы пройти квест еще раз напишите /start',
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer('🐙Это конец, вы можете пройти квест еще раз! '
                             '\nЖмите на клавиатуру, если ее нет жмите на 4 точки или напишите "▶".')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
