import telebot
import time
import json
import os

from telebot import types


admin = 767815871

file1 = open("token.txt", "r")
while True:
    line = file1.readline()
    if not line:
        break
    token = line

file1.close
token = token
bot = telebot.TeleBot(str(token))
print('Бот работает!')

@bot.message_handler(commands = ['start'])
def news(message):
    keyboard = types.InlineKeyboardMarkup()
    sending_news = types.InlineKeyboardButton(text = "Отправить новость", callback_data = 'send_news')
    keyboard.row(sending_news)
    bot.send_message(message.chat.id, 'Чтобы отправить новость, `нажмите`, пожалуйста, на кнопку ниже.', parse_mode = 'Markdown', reply_markup = keyboard)

@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'send_news':
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Отправь новость прямо в этот чат. Принимаем все форматы файлов, в том числе и голосовые сообщения.')
            bot.register_next_step_handler(call.message, get_message)

def get_message(message):
    str_countes = ''
    countes = [f'{message.from_user.first_name} — имя,\n',
               f'@{message.from_user.username} — username.'
              ]
    for x in countes:
        str_countes += x
    keyboard = types.InlineKeyboardMarkup()
    sending_news = types.InlineKeyboardButton(text = "Отправить новость", callback_data = 'send_news')
    keyboard.row(sending_news)
    bot.send_message(message.chat.id, 'Спасибо! *Мы получили* Вашу новость! Обязательно её обработаем в ближайшее время.', parse_mode = 'Markdown', reply_markup = keyboard)
    if message.content_type == 'text':
        bot.send_message(admin, f'Новость получена от: \n{str_countes}\n\n Текст новости: `{message.text}`', parse_mode = 'Markdown')
    elif message.content_type == 'photo':
        if message.caption != None:
            signature = message.caption
        else:
            signature = 'Без подписи'
        bot.send_message(admin, f'Новость получена от: \n{str_countes}\n\n Текст новости: `{signature}`', parse_mode = 'Markdown')
        bot.send_photo(admin, photo = message.photo[1].file_id)
    elif message.content_type == 'video':
        if message.caption != None:
            signature = message.caption
        else:
            signature = 'Без подписи'
        bot.send_message(admin, f'Новость получена от: \n{str_countes}\n\n Видео: `{signature}`', parse_mode = 'Markdown')
        bot.send_video(admin, video = message.video.file_id)
    bot.clear_step_handler_by_chat_id(chat_id = message.chat.id)
    
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop = True)
        except Exception as e:
            time.sleep(3)
            print(f'Возникла ошибка: {e}')
