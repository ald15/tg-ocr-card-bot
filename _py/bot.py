import telebot
import pytesseract
import shutil
import os
from _py import sql
from _py import DataProcessor as DP
from telebot import types
try: from PIL import Image
except ImportError: import Image


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
bot = telebot.TeleBot('6473764124:AAHx0vL35z5gK1r4PElgagK5W8KKZWLXknc')
f_name = "./image.jpg" # Имя временного файла-картинки
d_name = "./img/" # Директория для постоянного хранения картинок
out_file = "./out.xlsx" # Имя Excel файла
archive_name = "./out" # Имя архива с картинками
archive_dir = d_name[:] # Директория архива с картинками


sql.createDb() # Создание БД, если это необходимо
if not os.path.isdir(d_name): # Создание директории для постоянного хранения картинок, если это необходимо
    os.mkdir(d_name)


def ocr_core(filename): # OCR анализ текста
    return pytesseract.image_to_string(Image.open(filename), lang='rus+eng')  


def save_image(f_name, d_name): # Сохранение картинки в  постоянное место хранения
    shutil.copyfile(f_name, d_name + "img" + sql.lastIdInDb() + ".jpg")


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
            bot.send_message(message.from_user.id, '*В разработке*', parse_mode='Markdown')
        elif message.text == 'Получить фото-архив карточек':
            if int(sql.lastIdInDb()) >= 0: # Проверка на наличие записей в БД
                create_archive(archive_name, archive_dir) # Создание архива картинок
                bot.send_document(message.from_user.id, open(archive_name + ".zip", "rb")) # Отправка zip файла пользователю 
                bot.send_message(message.from_user.id, f'Файл {archive_name.lstrip("./")}.zip - архив, содержащий фото всех добавленных визитных карточек.', parse_mode='Markdown')
            else: # БД пуста -> извещаем пользователя о невозможности проведения операции
                bot.send_message(message.from_user.id, f'Архив не может быть сформирован, т.к. отсутствуют фото визитных карточек.', parse_mode='Markdown')
        elif message.text == 'Получить таблицу карточек':
            if int(sql.lastIdInDb()) >= 0: # Проверка на наличие записей в БД
                sql.excelDb(out_file) # Экспорт БД в Excel
                bot.send_document(message.from_user.id, open(out_file, "rb")) # Отправка Excel файла пользователю 
                bot.send_message(message.from_user.id, f'Файл {out_file.lstrip("./")} - таблица, содержащая все добавленные визитные карточки.', parse_mode='Markdown')
            else: # БД пуста -> извещаем пользователя о невозможности проведения операции
                bot.send_message(message.from_user.id, f'Таблица не может быть сформирована, т.к. отсутствует информация о визитных карточках.', parse_mode='Markdown')  

    @bot.callback_query_handler(func=lambda call: call.data.split(';')[0] == 'Edit note')
    def get_card_number(call):
        cur_card_id = call.data.split(';')[1]
        message = call.message
        chat_id = message.chat.id
        
        markup = types.InlineKeyboardMarkup()
        button_company = types.InlineKeyboardButton('Изменить поле Компания', callback_data='Editcompany;' + cur_card_id)
        button_name = types.InlineKeyboardButton('Изменить поле ФИО', callback_data='Editname;' + cur_card_id)
        button_post = types.InlineKeyboardButton('Изменить поле Должность', callback_data='Editpost;' + cur_card_id)
        button_tel1 = types.InlineKeyboardButton('Изменить поле Тел. №1', callback_data='Edittel1;' + cur_card_id)
        button_tel2 = types.InlineKeyboardButton('Изменить поле Тел. №2', callback_data='Edittel2;'+ cur_card_id)
        button_email = types.InlineKeyboardButton('Изменить поле E-mail', callback_data='Editemail;' + cur_card_id)
        button_site = types.InlineKeyboardButton('Изменить поле Сайт', callback_data='Editsite;' + cur_card_id)
        button_comment = types.InlineKeyboardButton('Изменить поле Комментарий', callback_data='Editcomment;'+ cur_card_id)
        markup.add(button_company)
        markup.add(button_name)
        markup.add(button_post)
        markup.add(button_tel1)
        markup.add(button_tel2)
        markup.add(button_email)
        markup.add(button_site)
        markup.add(button_comment)

        bot.send_message(chat_id, f"Вы редактируете визитку - {cur_card_id}\nВыберите поле для редактирования:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.split(';')[0] == 'Editcompany')
    def edit_btn_company(call):
        cur_card_id = call.data.split(';')[1]
        message = call.message
        chat_id = message.chat.id
        bot.send_message(chat_id, f'Введите Компанию')
        bot.register_next_step_handler(message, handler_company, cur_card_id)

    def handler_company(message, val):
        chat_id = message.chat.id
        input_data = message.text
        keyboard = telebot.types.InlineKeyboardMarkup()
        button_save = telebot.types.InlineKeyboardButton(text="Сохранить",
                                                     callback_data=f'Save company;{input_data};{val}')
        button_change = telebot.types.InlineKeyboardButton(text="Изменить",
                                                       callback_data='Editcompany; ')
        keyboard.add(button_save, button_change)

        bot.send_message(chat_id, f'Сохранить данные?', reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data.split(';')[0] == 'Save company')
    def save_company(call):
        data = call.data.split(';')
        key = data[2]
        val = data[1]
        column = 'company'
        sql.updateDb(key, val, column)

        message = call.message
        chat_id = message.chat.id
        bot.send_message(chat_id, f"Сохранено")



    
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
        print(dp.dataExtract())
        print(*dp.dataExtract())
        data = (*dp.dataExtract(), "")
        print(str(data))

        # data = ("1", "1", "1", "1", "1", "1", "1", "1") # Преобразованные данные
        sql.insertDb(data) # Добавление данных в БД
        save_image(f_name, d_name) # Сохранение картинки

    
        markup = types.InlineKeyboardMarkup()
        cur_card_id = sql.lastIdInDb()
        button1 = types.InlineKeyboardButton('Изменить запись', callback_data=f'Edit note;{cur_card_id}')
        markup.add(button1)

        bot.send_message(message.chat.id, f"Номер визитки: {cur_card_id}\n" + "Полученная информация:\n" + \
            show_data(data).format(message.from_user), reply_markup=markup)

        # ...
        #bot.send_message(message.from_user.id, text=raw_data)

    
        #markup = types.InlineKeyboardMarkup()
        #button1 = types.InlineKeyboardButton("Сайт Хабр", url='https://habr.com/ru/all/')
        #markup.add(button1)
        #bot.send_message(message.chat.id, raw_data.format(message.from_user), reply_markup=markup)
        
        
        
        
        
    
    bot.polling(none_stop=False, interval=1) # Обязательная для работы бота часть
