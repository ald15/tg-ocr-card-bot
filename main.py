import sql

import telebot
from telebot import types


try:
    from PIL import Image
except ImportError: 
    import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def ocr_core(filename):
    text = pytesseract.image_to_string(Image.open(filename), lang='rus+eng') 
    return text 

def test_sql():
    d = ("Roga & copita", "Ivanov Ivan Ivanovich", "Manager", "+71234567890", "+70123654789", "example@example.ru", "www.example.example")
    d1 = ("TVOY ROT", "Petr Evgenevich", "", "+71234567890", "", "example@example.ru", "www.example.example")
    sql.createDb()
    sql.insertDb(d)
    sql.excelDb()



bot = telebot.TeleBot('6473764124:AAHx0vL35z5gK1r4PElgagK5W8KKZWLXknc')

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
        btn1 = types.KeyboardButton('Как стать автором на Хабре?')
        btn2 = types.KeyboardButton('Правила сайта')
        btn3 = types.KeyboardButton('Получить Excel')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup) #ответ бота


    elif message.text == 'Как стать автором на Хабре?':
        bot.send_message(message.from_user.id, 'Вы пишете первый пост, его проверяют модераторы, и, если всё хорошо, отправляют в основную ленту Хабра, где он набирает просмотры, комментарии и рейтинг. В дальнейшем премодерация уже не понадобится. Если с постом что-то не так, вас попросят его доработать.\n \nПолный текст можно прочитать по ' + '[ссылке](https://habr.com/ru/sandbox/start/)', parse_mode='Markdown')

    elif message.text == 'Правила сайта':
        bot.send_message(message.from_user.id, 'Прочитать правила сайта вы можете по ' + '[ссылке](https://habr.com/ru/docs/help/rules/)', parse_mode='Markdown')

    elif message.text == 'Получить Excel':
        test_sql()
        f = open("out.xlsx", "rb")
        bot.send_document(message.from_user.id, f)
        #bot.send_message(message.from_user.id, 'Подробно про советы по оформлению публикаций прочитать по ' + '[ссылке](https://habr.com/ru/docs/companies/design/)', parse_mode='Markdown')


@bot.message_handler(content_types=['photo'])
def photo(message):
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

    f_name = "image.jpg"
    with open(f_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    print("Text ", ocr_core(f_name))




bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
