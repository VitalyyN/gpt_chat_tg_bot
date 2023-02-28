import telebot
import openai
from dotenv import load_dotenv
import os


load_dotenv()

# Устанавливаем токен бота из переменной окружения
bot_token = os.getenv('BOT_TOKEN')

# Устанавливаем токен API OpenAI из переменной окружения
openai.api_key = os.getenv('OPENAI_API_KEY')

# Создаем экземпляр бота
bot = telebot.TeleBot(bot_token)


# Обрабатываем команду /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, готовый помочь вам с задачами!")


# Обрабатываем текстовые сообщения
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Используем API OpenAI для получения ответа на сообщение
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message.text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Отправляем ответ пользователю
    bot.reply_to(message, response.choices[0].text)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
