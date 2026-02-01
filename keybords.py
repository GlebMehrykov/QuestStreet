from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

admin_kb2 = InlineKeyboardMarkup(row_width=2)
admin_kb2.add(InlineKeyboardButton(text='Админ', callback_data='states'))

admin_kb = InlineKeyboardMarkup(row_width=2)
admin_kb.add(InlineKeyboardButton(text='Админ', callback_data='states'),
             InlineKeyboardButton(text='Игрок', callback_data='test'))

change_user_state = InlineKeyboardMarkup(row_width=1)
change_user_state.add(InlineKeyboardButton(text='Назад', callback_data='back'))\
    .add(InlineKeyboardButton(text='Изменить состояние', callback_data='change_state'))

back_back = ReplyKeyboardMarkup(resize_keyboard=True)
back1 = KeyboardButton(text='🐙Назад')
back_back.add(back1)

backIn = InlineKeyboardMarkup(row_width=1)
backIn.add(InlineKeyboardButton(text='🐙Вернуться в главное меню', url='https://t.me/QuestStreetBot'))

cb = CallbackData('ikb')
cb1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Художник', callback_data='hello')]])

markup_finish = ReplyKeyboardMarkup(resize_keyboard=True)
mf1 = KeyboardButton(text='Вернуться в начало квеста▶️')
markup_finish.add(mf1)

kb_city = ReplyKeyboardMarkup(resize_keyboard=True)
city1 = KeyboardButton(text='🕍Москва')
city2 = KeyboardButton(text='🌉Санкт-Петербург')
city3 = KeyboardButton(text='🏝Краснодарский край')
city4 = KeyboardButton(text='🐙Назад')
kb_city.add(city1)
kb_city.add(city3)
kb_city.add(city2)
kb_city.add(city4)

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kbm1 = KeyboardButton(text='🧠Выбрать квест')
kbm2 = KeyboardButton(text='🌐Сообщество')
kbm3 = KeyboardButton(text='🎬Media')
kbm4 = KeyboardButton(text='📜Перейти в свой профиль')
kb_menu.add(kbm1)
kb_menu.add(kbm2, kbm3)
kb_menu.add(kbm4)

back = ReplyKeyboardMarkup(resize_keyboard=True)
back1 = KeyboardButton(text='🐙Назад')
back.add(back1)

ikb_quest_Krasnodar = InlineKeyboardMarkup(row_width=1)
ikb_quest_Krasnodar.add(InlineKeyboardButton(text='⛵️Сочи - В поисках сокровищ', url='https://t.me/QuestAdlerBot'))
ikb_quest_Krasnodar.add(InlineKeyboardButton(text='🌳Парк Ривьера - Полет на луну.',
                                             url='https://t.me/RivieraQuestStreetBot'))
ikb_quest_Krasnodar.add(InlineKeyboardButton(text='🔮Сириус - Школа магии.',
                                             url='https://t.me/SochQuestStreetBot'))

ikb_quest_Moscow = InlineKeyboardMarkup(row_width=1)
ikb_quest_Moscow.add(InlineKeyboardButton(text='Ⓜ️Таганская - Пришельцы', url='https://t.me/QuestTagankaBot'))
ikb_quest_Moscow.add(InlineKeyboardButton(text='Ⓜ️Парк культуры - Тайный агент',
                                          url='https://t.me/QuestParkCultureBot'))
ikb_quest_Moscow.add(InlineKeyboardButton(text='Ⓜ️Киевская - Эшхолорадо', url='https://t.me/QuestKievscayBot'))
ikb_quest_Moscow.add(InlineKeyboardButton(text='Ⓜ️Чистые пруды - Зомби', url='https://t.me/ChistyePrudyBot'))

ikb_community = InlineKeyboardMarkup(row_width=1)
ikb_community.add(InlineKeyboardButton(text='🧖VK-автора', url='https://vk.com/id825339583'))
ikb_community.add(InlineKeyboardButton(text='👭Общий чат', url='https://t.me/QuestStreet'))
ikb_community.add(InlineKeyboardButton(text='🧿Группа в VK', url='https://vk.com/public222408104'))

kb_Media = InlineKeyboardMarkup(row_width=1)
kb_Media.add(InlineKeyboardButton(text='✉️Отправить фото', url='https://vk.com/im?sel=-222408104'))
kb_Media.add(InlineKeyboardButton(text='✉️Отправить видео', url='https://vk.com/im?sel=-222408104'))


kb_id_info = ReplyKeyboardMarkup(resize_keyboard=True)
kb1 = KeyboardButton(text='✍️Редактировать профиль')
kb2 = KeyboardButton(text='ℹ️Информация о моём профиле')
kb3 = KeyboardButton(text='🐙Назад')
kb_id_info.add(kb1, kb2)
kb_id_info.add(kb3)


kb_profile = ReplyKeyboardMarkup(resize_keyboard=True)
kbf1 = KeyboardButton(text='📷Изменить фотографию')
kbf2 = KeyboardButton(text='👁‍🗨Изменить Никнейм')
kbf3 = KeyboardButton(text='🌕🌖🌗🌘🌑Изменить Возраст')
kbf4 = KeyboardButton(text='📝Изменить комментарий о себе')
kbf5 = KeyboardButton(text='🐙Назад')
kb_profile.add(kbf1)
kb_profile.add(kbf2)
kb_profile.add(kbf3)
kb_profile.add(kbf4)
kb_profile.add(kbf5)

Photokb = ReplyKeyboardMarkup(resize_keyboard=True)
pkb = KeyboardButton(text='Добавить или заменить фото.')
Photokb.add(pkb)


ikb_my_info = InlineKeyboardMarkup(row_width=1)
ikb_my_info.add(InlineKeyboardButton(text='Узнать', callback_data='My_info'))


chat = InlineKeyboardMarkup(row_width=2)
chat.add(InlineKeyboardButton(text='VK', url='https://vk.com/public222408104'))
chat.add(InlineKeyboardButton(text='Чат Telegram', url='https://t.me/QuestStreet'))


markup_avtar = InlineKeyboardMarkup(row_width=1)
markup_avtar.add(InlineKeyboardButton(text='VK автора', url='https://vk.com/id825339583'))

markup_avtar2 = InlineKeyboardMarkup(row_width=1)
markup_avtar2.add(InlineKeyboardButton(text='VK программиста', url='https://vk.com/id825339583'))

finish = ReplyKeyboardMarkup(resize_keyboard=True)
fin = KeyboardButton(text='🐙Конец')
finish.add(fin)

yesno = ReplyKeyboardMarkup(resize_keyboard=True)
ib1 = KeyboardButton(text='нет')
ib2 = KeyboardButton(text='да')
yesno.row(ib1, ib2)


xkb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='1')
b2 = KeyboardButton(text='2')
b3 = KeyboardButton(text='3')
b4 = KeyboardButton(text='4')
b5 = KeyboardButton(text='5')
b6 = KeyboardButton(text='6')
b7 = KeyboardButton(text='7')
b8 = KeyboardButton(text='8')
b9 = KeyboardButton(text='9')
b10 = KeyboardButton(text='10')
b11 = KeyboardButton(text='11')
b12 = KeyboardButton(text='12')
b13 = KeyboardButton(text='13')
b14 = KeyboardButton(text='14')
b15 = KeyboardButton(text='15')
b16 = KeyboardButton(text='16')
b17 = KeyboardButton(text='17')
b18 = KeyboardButton(text='18')
b19 = KeyboardButton(text='19')
b20 = KeyboardButton(text='20')

xkb.row(b1, b2, b3, b4, b5)
xkb.row(b6, b7, b8, b9, b10)
xkb.row(b11, b12, b13, b14, b15)
xkb.row(b16, b17, b18, b19, b20)

titles = ReplyKeyboardMarkup(resize_keyboard=True)
tit1 = KeyboardButton(text='Конец')
titles.add(tit1)


kbb = ReplyKeyboardMarkup(resize_keyboard=True)
kbb1 = KeyboardButton(text='1')
kbb2 = KeyboardButton(text='2')
kbb3 = KeyboardButton(text='3')
kbb4 = KeyboardButton(text='4')
kbb5 = KeyboardButton(text='5')
kbb6 = KeyboardButton(text='6')
kbb7 = KeyboardButton(text='7')
kbb8 = KeyboardButton(text='8')
kbb9 = KeyboardButton(text='9')
kbb10 = KeyboardButton(text='10')
kbb.add(kbb1, kbb2, kbb3)
kbb.add(kbb4, kbb5, kbb6)
kbb.add(kbb7, kbb8, kbb9)
kbb.add(kbb10)

kievskay = ReplyKeyboardMarkup(resize_keyboard=True)
k133 = KeyboardButton(text='🔮Оправа')
k233 = KeyboardButton(text='⚙️Механизм')
k333 = KeyboardButton(text='🪨Камень')
kievskay.add(k133)
kievskay.add(k233)
kievskay.add(k333)

bocman = ReplyKeyboardMarkup(resize_keyboard=True)
ib1 = KeyboardButton(text='Пообщаться с боцманом')
bocman.add(ib1)

oblomki4 = ReplyKeyboardMarkup(resize_keyboard=True)
ib1 = KeyboardButton(text='Перейти к поиску 1️⃣ обломка')
ib2 = KeyboardButton(text='Перейти к поиску 2️⃣ обломка')
ib3 = KeyboardButton(text='Перейти к поиску 3️⃣ обломка')
ib4 = KeyboardButton(text='Перейти к поиску 4️⃣ обломка')
oblomki4.add(ib1, ib2, ib3, ib4)

kompas = ReplyKeyboardMarkup(resize_keyboard=True)
ib1 = KeyboardButton(text='Север')
ib2 = KeyboardButton(text='Запад')
ib3 = KeyboardButton(text='Юг')
ib4 = KeyboardButton(text='Восток')
kbf5 = KeyboardButton(text='🐙Назад')
kompas.add(ib1, ib2, ib3, ib4)
kompas.add(kbf5)

back_VPS = ReplyKeyboardMarkup(resize_keyboard=True)
ib1 = KeyboardButton(text='🐙Назад')
back_VPS.add(ib1)

Riviera_kb = ReplyKeyboardMarkup(resize_keyboard=True)
ib1 = KeyboardButton(text='Отправиться к Скелету💀')
ib2 = KeyboardButton(text='Отправиться к Гномам⛏')
Riviera_kb.add(ib1, ib2)

Riviera_kb = ReplyKeyboardMarkup(resize_keyboard=True)
ib1 = KeyboardButton(text='Отправиться к Скелету💀')
ib2 = KeyboardButton(text='Отправиться к Гномам⛏')
Riviera_kb.add(ib1, ib2)

School_of_Magic_kb = ReplyKeyboardMarkup(resize_keyboard=True)
ib1 = KeyboardButton(text='Отправиться к Андеграунд🗝')
ib2 = KeyboardButton(text='Отправиться к Скалиграунд🪨')
ib3 = KeyboardButton(text='Отправиться к Мировед🕊')
School_of_Magic_kb.add(ib1)
School_of_Magic_kb.add(ib2)
School_of_Magic_kb.add(ib3)

School_of_Magic_kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
ib2 = KeyboardButton(text='Отправиться к Скалиграунд🪨')
ib3 = KeyboardButton(text='Отправиться к Мировед🕊')
School_of_Magic_kb1.add(ib2)
School_of_Magic_kb1.add(ib3)

School_of_Magic_kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
ib3 = KeyboardButton(text='Отправиться к Мировед🕊')
School_of_Magic_kb2.add(ib3)

School_of_Magic_kb3 = ReplyKeyboardMarkup(resize_keyboard=True)
ib2 = KeyboardButton(text='Отправиться к Скалиграунд🪨')
School_of_Magic_kb3.add(ib2)

School_of_Magic_kb4 = ReplyKeyboardMarkup(resize_keyboard=True)
ib1 = KeyboardButton(text='Отправиться к Андеграунд🗝')
ib3 = KeyboardButton(text='Отправиться к Мировед🕊')
School_of_Magic_kb4.add(ib1)
School_of_Magic_kb4.add(ib3)

School_of_Magic_kb5 = ReplyKeyboardMarkup(resize_keyboard=True)
ib1 = KeyboardButton(text='Отправиться к Андеграунд🗝')
ib2 = KeyboardButton(text='Отправиться к Скалиграунд🪨')
School_of_Magic_kb5.add(ib1)
School_of_Magic_kb5.add(ib2)

School_of_Magic_kb6 = ReplyKeyboardMarkup(resize_keyboard=True)
ib1 = KeyboardButton(text='Отправиться к Андеграунд🗝')
School_of_Magic_kb6.add(ib1)