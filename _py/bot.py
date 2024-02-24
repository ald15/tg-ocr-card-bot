import telebot
import pytesseract
import shutil
from _py import sql
from _py import DataProcessor as DP
from telebot import types
try: from PIL import Image
except ImportError: import Image


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
bot = telebot.TeleBot('6473764124:AAHx0vL35z5gK1r4PElgagK5W8KKZWLXknc')


def ocr_core(filename): 
    return pytesseract.image_to_string(Image.open(filename), lang='rus+eng')  


def save_image(f_name, d_name):
    shutil.copyfile(f_name, d_name + "img" + sql.lastIdInDb() + ".jpg") #

def create_archive(f_name, d_name):
    shutil.make_archive(f_name, 'zip', d_name)

def start():
    f_name = "./image.jpg" # Имя временного файла-картинки
    d_name = "./img/" # Директория для постоянного хранения картинок
    out_file = "./out.xlsx" # Имя Excel файла
    archive_name = "./out" # Имя архива сс картинками
    archive_dir = d_name[:] # Директория архива с картинками


    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("👋 Поздороваться")
        markup.add(btn1)
        bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)


    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text == '👋 Поздороваться':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
            btn1 = types.KeyboardButton('Как пользоваться ботом?')
            btn2 = types.KeyboardButton('Получить фото-архив карточек')
            btn3 = types.KeyboardButton('Получить таблицу карточек')
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup) #ответ бота
        elif message.text == 'Как пользоваться ботом?':
            bot.send_message(message.from_user.id, '*В разработке*', parse_mode='Markdown')
        elif message.text == 'Получить фото-архив карточек':
            create_archive(archive_name, archive_dir) # Создание архива картинок
            bot.send_document(message.from_user.id, open(archive_name + ".zip", "rb")) # Отправка zip файла пользователю 
            bot.send_message(message.from_user.id, f'Файл {archive_name.lstrip("./")}.zip - архив, содержащий фото всех добавленных визитных карточек.', parse_mode='Markdown')
        elif message.text == 'Получить таблицу карточек':
            sql.excelDb(out_file) # Экспорт БД в Excel
            bot.send_document(message.from_user.id, open(out_file, "rb")) # Отправка Excel файла пользователю 
            bot.send_message(message.from_user.id, f'Файл {out_file.lstrip("./")} - таблица, содержащая все добавленные визитные карточки.', parse_mode='Markdown')


    @bot.message_handler(content_types=['photo'])
    def photo(message):
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        sql.createDb() # Создание БД, если это необходимо
        raw_data = ocr_core(f_name) # Сырые данные, полученнные из OCR
        dp = DP.DataProcessor(raw_data)
        bot.send_message(message.from_user.id, text=raw_data)

        ```test```
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Сайт Хабр", url='https://habr.com/ru/all/')
        markup.add(button1)
        bot.send_message(message.chat.id, raw_data.format(message.from_user), reply_markup=markup)
        ```test```
        
        data = dp.dataExtract()
        # data = ("1", "1", "1", "1", "1", "1", "1") # Преобразованные данные
        sql.insertDb(data) # Добавление данных в БД
        save_image(f_name, d_name) # Сохранение картинки
        
    
    bot.polling(none_stop=False, interval=1) #обязательная для работы бота часть
