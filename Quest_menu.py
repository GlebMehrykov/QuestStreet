from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import AIP_menu
from db import Database
from keybords import *

db = Database("2.db")
db.create_table_users()

bot = Bot(token=AIP_menu.TELEGRAM_BOT)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class StateMenu(StatesGroup):
    Quest = State()
    Quest_Moscow = State()
    Quest_Krasnodar = State()
    Quest_SPB = State()
    Quest_RedEdge = State()
    Community = State()
    Media = State()
    id_info = State()
    Profile = State()
    Photo = State()
    Name = State()
    Age = State()
    Comment = State()


@dp.message_handler(lambda message: message.chat.type == "private", commands=['start'], state='*')
async def start_command(message: types.Message, state: FSMContext):
    await message.answer(
        text='<b>🐙Добро пожаловать, вы попали в \"QuestStreet\" здесь вы сможете найти, интересные квесты с'
             ' сюжетной линией и интересными локациями.\n'
             'Ниже вы можете:\n \n🧠    Выбрать квест, прочесть его описание, подобрать оптимальный район.\n'
             '📜     Пройти регистрацию, в ней нет необходимости, но если вы ее пройдете, то при прохождение квестов '
             'у вас будет повышаться ваш уровень, а в будущем это будет иметь влияние на цену последующего квеста.\n'
             '🎬     Отправить медиа файлы в группу VK, и попасть в альбом активистов.\n'
             '🌐     Ознакомиться с нашим сообществом.'
             '\n \n \n      <em>🐙Если у вас пропала клавиатура нажмите на 4 кнопки возле скребки.</em></b>',
        parse_mode='html',
        reply_markup=kb_menu)
    await state.finish()
    db.insert_user(message.chat.id)
    print(message.from_user.id)


@dp.message_handler()
async def start_menu(message: types.Message):
    if message.text.lower() == "🧠выбрать квест":
        await StateMenu.Quest.set()
        await message.answer('<b>🐙В будущем квесты будут в каждом городе России, '
                             'и в курортных зонах дружественных стран.'
                             '\nНа данный момент квесты имеются в следующих районах:</b>',
                             reply_markup=kb_city, parse_mode='html')
    elif message.text.lower() == "🌐сообщество":
        await StateMenu.Community.set()
        await message.answer('<b>🐙Мы будем признательны, если вы везде подпишитесь на нас.</b>🧡',
                             reply_markup=back, parse_mode='html')
        await message.answer("<b>🐙А также вы можете подписаться и на автора, ему будет приятно.</b>🧡",
                             reply_markup=ikb_community, parse_mode='html')

    elif message.text.lower() == "🎬media":
        await StateMenu.Media.set()
        await message.answer('<b>🐙Тут вы можете поделиться своим видео и фото с места квеста.</b>',
                             reply_markup=kb_Media, parse_mode='html')
        await message.answer('🐙Файл пройдет проверку и будет выгружен в группу '
                             '<a href="https://vk.com/queststreetru">VK</a>.', parse_mode='html',
                             disable_web_page_preview=True, reply_markup=back)
    elif message.text.lower() == "📜перейти в свой профиль":
        await StateMenu.id_info.set()
        await message.answer('<b>🐙Тут вы можете изменить информацию о себе.</b>', parse_mode='html')
        await message.answer("<b>🐙А так же посмотреть данную информацию о себе.</b>",
                             reply_markup=kb_id_info, parse_mode='html')
    elif message.text.lower() == "назад":
        await message.answer("Возвращаемся в главное меню.", reply_markup=kb_menu)


@dp.message_handler(state=StateMenu.Quest)
async def quest(message: types.Message, state: FSMContext):
    if message.text.lower() == '🕍москва':
        await StateMenu.Quest_Moscow.set()
        await message.answer('🐙Выберите', reply_markup=back)
        await message.answer("Квест", reply_markup=ikb_quest_Moscow)
    elif message.text.lower() == "🐙назад":
        await state.finish()
        await message.answer("🐙Возвращаемся в главное меню.", reply_markup=kb_menu)
    elif message.text.lower() == '🌉санкт-петербург':
        await message.answer('🐙Питерские квесты будут в начале весны!')
    elif message.text.lower() == '🏝краснодарский край':
        await message.answer('🐙Выберите', reply_markup=back)
        await message.answer("Квест", reply_markup=ikb_quest_Krasnodar)
        await StateMenu.Quest_Krasnodar.set()


@dp.message_handler(state=StateMenu.Quest_Moscow)
async def quest(message: types.Message):
    if message.text.lower() == "🐙назад":
        await StateMenu.Quest.set()
        await message.answer("🐙Возвращаемся в меню квестов.", reply_markup=kb_city)

@dp.message_handler(state=StateMenu.Quest_Krasnodar)
async def quest(message: types.Message):
    if message.text.lower() == "🐙назад":
        await StateMenu.Quest.set()
        await message.answer("🐙Возвращаемся в меню квестов.", reply_markup=kb_city)

@dp.message_handler(state=StateMenu.Community)
async def community(message: types.Message, state: FSMContext):
    if message.text.lower() == "🐙назад":
        await state.finish()
        await message.answer("🐙Возвращаемся в главное меню.", reply_markup=kb_menu)


@dp.message_handler(state=StateMenu.Media)
async def media(message: types.Message, state: FSMContext):
    if message.text.lower() == "🐙назад":
        await state.finish()
        await message.answer("🐙Возвращаемся в главное меню.", reply_markup=kb_menu)


@dp.message_handler(state=StateMenu.id_info)
async def id_info(message: types.Message, state: FSMContext):
    if message.text.lower() == "🐙назад":
        await state.finish()
        await message.answer("🐙Возвращаемся в главное меню.", reply_markup=kb_menu)

    elif message.text.lower() == "✍️редактировать профиль":
        await StateMenu.Profile.set()
        await message.answer('🐙Выберите что хотите изменить.', reply_markup=kb_profile)

    elif message.text.lower() == "ℹ️информация о моём профиле":
        user = db.select_user(message.chat.id)
        text = ""
        text += f"🐙 ID: {user.id}\n"
        text += f'      TG_ID: <code>{message.from_user.id}</code>\n'
        text += f"      Никнейм: {user.nickname}\n"
        text += f"      Возраст: {user.age}\n"
        text += f"      Уровень: {user.level}\n"
        text += f"      Комментарий: {user.comment}\n"
        if not user.photo_id:
            await message.answer(text, parse_mode='html')
        else:
            await bot.send_photo(message.chat.id, user.photo_id, text, 'html')


@dp.message_handler(state=StateMenu.Profile)
async def profile(message: types.Message):
    if message.text.lower() == "🐙назад":
        await StateMenu.id_info.set()
        await message.answer("🐙Возвращаемся в меню профиля.", reply_markup=kb_id_info)
    elif message.text.lower() == "📷изменить фотографию":
        await StateMenu.Photo.set()
        await message.answer('🐙Пришлите фото.', reply_markup=back)
    elif message.text.lower() == "👁‍🗨изменить никнейм":
        await StateMenu.Name.set()
        await message.answer('🐙Напишите никнейм.', reply_markup=back)
    elif message.text.lower() == "🌕🌖🌗🌘🌑изменить возраст":
        await StateMenu.Age.set()
        await message.answer('🐙Напишите ваш возраст.', reply_markup=back)
    elif message.text.lower() == "📝изменить комментарий о себе":
        await StateMenu.Comment.set()
        await message.answer('🐙Тут вы можете написать свой девиз по жизни.', reply_markup=back)


@dp.message_handler(content_types=['photo'], state=StateMenu.Photo)
async def photo_photo(message: types.Message):
    db.update("photo_id", message.chat.id, message.photo[0].file_id)
    await message.answer('🐙Фото добавлено.', reply_markup=kb_profile)
    await StateMenu.Profile.set()


@dp.message_handler(lambda message: not message.photo, state=StateMenu.Photo)
async def photo_text(message: types.Message):
    if message.text.lower() == "🐙назад":
        await message.answer('🐙Что будем редактировать?!', reply_markup=kb_profile)
        await StateMenu.Profile.set()
    else:
        await message.answer('🐙Это не фотография!')


@dp.message_handler(state=StateMenu.Name)
async def load_name(message: types.Message):
    if message.text.lower() == "🐙назад":
        await message.answer('🐙Что будем редактировать?', reply_markup=kb_profile)
        await StateMenu.Profile.set()
    else:
        db.update("nickname", message.chat.id, message.text)
        await message.answer('🐙Имя установленно.', reply_markup=kb_profile)
        await StateMenu.Profile.set()


@dp.message_handler(state=StateMenu.Age)
async def age(message: types.Message):
    if message.text.lower() == "🐙назад":
        await message.answer('🐙Что будем редактировать?', reply_markup=kb_profile)
        await StateMenu.Profile.set()
        return

    if not message.text.isdigit():
        await message.answer('🐙Введите число.')
    else:
        db.update("age", message.chat.id, message.text)
        await message.answer('🐙Возраст установлен.', reply_markup=kb_profile)
        await StateMenu.Profile.set()


@dp.message_handler(state=StateMenu.Comment)
async def comment(message: types.Message):
    if message.text.lower() == "🐙назад":
        await message.answer('🐙Что будем редактировать?', reply_markup=kb_profile)
    else:
        db.update("comment", message.chat.id, message.text)
        await message.answer('🐙Комментарий установлен.', reply_markup=kb_profile)
    await StateMenu.Profile.set()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
