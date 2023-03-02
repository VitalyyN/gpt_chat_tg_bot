from dotenv import load_dotenv
import telebot
import openai
import os
import time

load_dotenv()

# Подключаемся к Telegram боту
for i in range(3):
    try:
        bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
        break
    except telebot.apihelper.ApiException as e:
        print(f"Не удалось подключиться к Telegram API. Попытка {i + 1}/3...\n{e}")
        time.sleep(3)
else:
    print("Не удалось подключиться к Telegram API. Проверьте токен и подключение к сети.")
    exit(1)

# Подключаемся к OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я готов помочь тебе с генерацией текста. Напиши мне что-нибудь.")


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def generate_text(message):
    # Получаем идентификатор пользователя, чтобы поддерживать работу с несколькими пользователями
    user_id = message.from_user.id

    # Получаем текст запроса от пользователя
    prompt_text = message.text

    for i in range(3):
        try:
            # Генерируем ответ на основе запроса с помощью OpenAI API
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt_text,
                max_tokens=2024,
                n=1,
                stop=None,
                temperature=0.7,
            )

            # Получаем сгенерированный текст из ответа OpenAI API
            generated_text = response.choices[0].text

            # Отправляем сгенерированный текст пользователю
            bot.send_message(user_id, generated_text)

            break  # Если всё хорошо, выходим из цикла

        except Exception as e:
            print(f"Произошла ошибка при генерации текста. Попытка {i + 1}/3...\n")
            time.sleep(3)
    else:
        bot.send_message(user_id, "Произошла ошибка при генерации текста. Попробуйте еще раз позже.")


# Запускаем бота
if __name__ == '__main__':
    print('start')
    bot.polling(none_stop=True, interval=0)
