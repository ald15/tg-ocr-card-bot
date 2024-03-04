import telebot
import pytesseract
import shutil
import os
from _py import sqlNotes
from _py import sqlEditor
from _py import DataProcessor as DP
from telebot import types
try: from PIL import Image
except ImportError: import Image

with open("token.txt", "r+") as f: # Считывание telegram token из файла
    token = f.readlines()[0].strip() 
bot = telebot.TeleBot(token)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#arbitrary_callback_data = True
f_name = "./image.jpg" # Имя временного файла-картинки
d_name = "./img/" # Директория для постоянного хранения картинок
out_file = "./out.xlsx" # Имя Excel файла
archive_name = "./out" # Имя архива с картинками
archive_dir = d_name[:] # Директория архива с картинками
text_instruction = """*Инструкция по использованию*

__1\. Добавление карточки__
Чтобы добавить новую карточку в бота, необходимо просто отправить фотографию визитки\. Далее бот предложит действия по сохранению или её редактированию\.

__2\. Изменение карточки__

Чтобы редактировать вручную поля карточки, необходимо нажать кнопку "изменить", которую Вам предложит бот после отправки фотографии\.
Затем выбрать поле, подлежащее изменению, и отправить сообщение боту с правильным текстом в записи\.

Дополнительные изменения Вы всегда можете применить, нажав кнопку "изменить" для соответствующей карточки повторно\.

__3\. Описиание кнопок__

В меню отправки сообщений Вам всегда будут доступны 3 кнопки:
\- "Как пользоваться ботом?" \- инструкция по использованию бота;
\- "Получить фото\-архив карточек" \- бот отправит файл с архивом из всех фотографий, которые прислали пользователи;
\- "Получить таблицу карточек" \- бот отправит excel файл со всеми записями по визиткам, которые запомнил бот\."""


class MyCallbackData():
    def __init__(self, s: str):
        self.s = s
    def get(self):
        return self.s

sqlNotes.createDb() # Создание БД, если это необходимо
sqlEditor.createDb() # Создание БД, если это необходимо
if not os.path.isdir(d_name): # Создание директории для постоянного хранения картинок, если это необходимо
    os.mkdir(d_name)


def ocr_core(filename): # OCR анализ текста
    return pytesseract.image_to_string(Image.open(filename), lang='rus+eng')  


def save_image(f_name, d_name): # Сохранение картинки в  постоянное место хранения
    shutil.copyfile(f_name, d_name + "img" + sqlNotes.lastIdInDb() + ".jpg")


def create_archive(f_name, d_name): # Создание архива картинок
    shutil.make_archive(f_name, 'zip', d_name)


def start():

    # Обработчик команды /start
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("👋 Поздороваться")
        markup.add(btn1)
        bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)


    # Обработчик сообщений-текст
    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text == '👋 Поздороваться':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
            btn1 = types.KeyboardButton('Как пользоваться ботом?')
            btn2 = types.KeyboardButton('Получить фото-архив карточек')
            btn3 = types.KeyboardButton('Получить таблицу карточек')
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup) #ответ бота
        elif message.text == 'Как пользоваться ботом?': # Дописать инсструкцию!
            bot.send_message(message.from_user.id, f'{text_instruction}', parse_mode='MarkdownV2')
        elif message.text == 'Получить фото-архив карточек':
            if int(sqlNotes.lastIdInDb()) >= 0: # Проверка на наличие записей в БД
                create_archive(archive_name, archive_dir) # Создание архива картинок
                bot.send_document(message.from_user.id, open(archive_name + ".zip", "rb")) # Отправка zip файла пользователю 
                bot.send_message(message.from_user.id, f'Файл {archive_name.lstrip("./")}.zip - архив, содержащий фото всех добавленных визитных карточек.', parse_mode='Markdown')
            else: # БД пуста -> извещаем пользователя о невозможности проведения операции
                bot.send_message(message.from_user.id, f'Архив не может быть сформирован, т.к. отсутствуют фото визитных карточек.', parse_mode='Markdown')
        elif message.text == 'Получить таблицу карточек':
            if int(sqlNotes.lastIdInDb()) >= 0: # Проверка на наличие записей в БД
                sqlNotes.excelDb(out_file) # Экспорт БД в Excel
                bot.send_document(message.from_user.id, open(out_file, "rb")) # Отправка Excel файла пользователю 
                bot.send_message(message.from_user.id, f'Файл {out_file.lstrip("./")} - таблица, содержащая все добавленные визитные карточки.', parse_mode='Markdown')
            else: # БД пуста -> извещаем пользователя о невозможности проведения операции
                bot.send_message(message.from_user.id, f'Таблица не может быть сформирована, т.к. отсутствует информация о визитных карточках.', parse_mode='Markdown')  

    @bot.callback_query_handler(func=lambda call: call.data.split(';')[0] == 'Edit note')
    def get_card_number(call):
        cur_card_id = call.data.split(';')[1]
        message = call.message
        chat_id = message.chat.id
        msg_id = message.message_id
        
        markup = types.InlineKeyboardMarkup()
        button_company = types.InlineKeyboardButton('Изменить поле Компания', callback_data='Edit;company;Компания;' + cur_card_id + f';{msg_id}')
        button_name = types.InlineKeyboardButton('Изменить поле ФИО', callback_data='Edit;name;ФИО;' + cur_card_id + f';{msg_id}')
        button_post = types.InlineKeyboardButton('Изменить поле Должность', callback_data='Edit;post;Должность;' + cur_card_id + f';{msg_id}')
        button_tel1 = types.InlineKeyboardButton('Изменить поле Тел. №1', callback_data='Edit;tel1;Тел. №1;' + cur_card_id + f';{msg_id}')
        button_tel2 = types.InlineKeyboardButton('Изменить поле Тел. №2', callback_data='Edit;tel2;Тел. №2;'+ cur_card_id + f';{msg_id}')
        button_email = types.InlineKeyboardButton('Изменить поле E-mail', callback_data='Edit;email;E-mail;' + cur_card_id + f';{msg_id}')
        button_site = types.InlineKeyboardButton('Изменить поле Сайт', callback_data='Edit;site;Сайт;' + cur_card_id + f';{msg_id}')
        button_comment = types.InlineKeyboardButton('Изменить поле Комментарий', callback_data='Edit;comment;Комментарий;'+ cur_card_id + f';{msg_id}')
        markup.add(button_company)
        markup.add(button_name)
        markup.add(button_post)
        markup.add(button_tel1)
        markup.add(button_tel2)
        markup.add(button_email)
        markup.add(button_site)
        markup.add(button_comment)

        bot.send_message(chat_id, f"Вы редактируете визитку: {cur_card_id}\nВыберите поле для редактирования:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.split(';')[0] == 'Edit')
    def edit_btn(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        column_ru = call.data.split(';')[2]
        cur_card_id = call.data.split(';')[3]
        data = call.data

        message = call.message
        chat_id = message.chat.id
        bot.send_message(chat_id, f'Вы редактируете визитку: {cur_card_id}\nВведите новое поле {column_ru}')
        #bot.register_next_step_handler(message, handler_edit, data)
        bot.register_next_step_handler(message, save_column, data)

    def handler_edit(message, data):
        chat_id = message.chat.id
        input_data = message.text
        key_data_id = sqlEditor.insertDb(input_data)
        keyboard = telebot.types.InlineKeyboardMarkup()

        column_ru = data.split(';')[2]
        button_save = telebot.types.InlineKeyboardButton(text="Сохранить",
                                                     callback_data=f'Save;{key_data_id};{data}')
        button_change = telebot.types.InlineKeyboardButton(text="Изменить",
                                                       callback_data=data)
        keyboard.add(button_save, button_change)

        bot.send_message(chat_id, f'Сохранить данные?\nполе {column_ru} значение: {input_data}', reply_markup=keyboard)

    #@bot.callback_query_handler(func=lambda call: call.data.split(';')[0] == 'Save')
    def save_column(message, data):
        # call - Save;input_data;Edit;column_eng;column_ru;cur_card_id
        # data - Edit;column_eng;column_ru;cur_card_id
        chat_id = message.chat.id
        input_data = message.text
        #key_data_id = sqlEditor.insertDb(input_data)

        data = data.split(';')
        key = data[3]
        #key_data_id = data[1]
        #val = sqlEditor.selectrowDb(key_data_id)[0][1]
        val = input_data
        #print(val)
        column = data[1]
        sqlNotes.updateDb(key, val, column)

        #message = call.message
        #chat_id = message.chat.id
        asnwr_bd = sqlNotes.selectrowDb(key)[0]
        res_str = show_data(asnwr_bd[1:])

        cur_card_id = key

        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Изменить запись повторно', callback_data=f'Edit note;{cur_card_id}')
        markup.add(button1)
        bot.send_message(chat_id, f"Сохранены изменения (Карточка {key})\n{res_str}\nЖду новых фото или изменений", reply_markup=markup)
        

    @bot.callback_query_handler(func=lambda call: call.data == 'Done')
    def save_answr(call):
        message = call.message
        chat_id = message.chat.id
        bot.send_message(chat_id, f"Карточка сохранена, жду новых фото")

    
    def show_data(data: tuple) -> str:
        res = ''
        names = ('Компания', 'ФИО', 'Должность', 'Тел. №1', 'Тел. №2', 'E-mail', 'Сайт', 'Комментарий')
        for i in range(len(names)):
            res += f'{names[i]}: {data[i]}\n'
        return res

    # Обработчик сообщений-изображение
    @bot.message_handler(content_types=['photo'])
    def photo(message):
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        raw_data = ocr_core(f_name) # Сырые данные, полученнные из OCR
        dp = DP.DataProcessor(raw_data)
        #print(dp.dataExtract())
        #print(*dp.dataExtract())
        data = (*dp.dataExtract(), "")
        #print(str(data))

        # data = ("1", "1", "1", "1", "1", "1", "1", "1") # Преобразованные данные
        sqlNotes.insertDb(data) # Добавление данных в БД
        save_image(f_name, d_name) # Сохранение картинки

        markup = types.InlineKeyboardMarkup()
        cur_card_id = sqlNotes.lastIdInDb()
        button1 = types.InlineKeyboardButton('Изменить запись', callback_data=f'Edit note;{cur_card_id}')
        button2 = types.InlineKeyboardButton('Все верно', callback_data=f'Done')
        markup.add(button1)
        markup.add(button2)

        bot.send_message(message.chat.id, f"*Номер визитки: {cur_card_id}*\n" + "Полученная информация:\n" + \
            show_data(data).format(message.from_user), reply_markup=markup)

        # ...
        #bot.send_message(message.from_user.id, text=raw_data)

    
        #markup = types.InlineKeyboardMarkup()
        #button1 = types.InlineKeyboardButton("Сайт Хабр", url='https://habr.com/ru/all/')
        #markup.add(button1)
        #bot.send_message(message.chat.id, raw_data.format(message.from_user), reply_markup=markup)
                          
    bot.polling(none_stop=False, interval=1) # Обязательная для работы бота часть
