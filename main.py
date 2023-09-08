import telebot
import config
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import os
import sys

bot = telebot.TeleBot(config.TOKEN)


def restart_bot():
    print("Restarting bot...")
    python = sys.executable
    os.execl(python, python, *sys.argv)


# Определение следующей пары
def get_next_lecture(day, time):
    try:
        if day in config.schedule:
            for lecture in config.schedule[day]:
                lecture_time = lecture['time'].split(' - ')
                start_time = datetime.strptime(lecture_time[0], '%H:%M')
                end_time = datetime.strptime(lecture_time[1], '%H:%M')
                current_time = datetime.strptime(time, '%H:%M')
                if start_time > current_time:
                    return lecture
        return None
    except Exception as e:
        bot.send_message(config.admin_id, f"Ошибка в функции get_next_lecture: {e}")


# Проверка времени и отправка ссылки за 5 минут до начала пары
def check_time_and_send_link():
    try:
        current_day = datetime.now().strftime('%A').lower()
        current_time = datetime.now().strftime('%H:%M')

        next_lecture = get_next_lecture(current_day, current_time)

        if next_lecture:
            lecture_start_time = datetime.strptime(next_lecture['time'].split(' - ')[0], '%H:%M')
            time_difference = lecture_start_time - datetime.strptime(current_time, '%H:%M')
            if time_difference <= timedelta(minutes=5) and time_difference >= timedelta(minutes=0):
                response = (
                    f"Через {int(time_difference.total_seconds() // 60)} минут начнется следующая пара:\n"
                    f"Предмет: {next_lecture['subject']}\n"
                    f"Время: {next_lecture['time']}\n"
                    f"Ссылка: {next_lecture['link']}"
                )
                for chat_id in config.subscribed_users:
                    bot.send_message(chat_id, response)
    except Exception as e:
        bot.send_message(config.admin_id, f"Ошибка в функции check_time_and_send_link: {e}")


# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        bot.reply_to(message,
                     "Привет! Я бот с расписанием пар. Используй команду /get_schedule, чтобы получить ближайшую пару.")
    except Exception as e:
        bot.send_message(config.admin_id, f"Ошибка в команде /start: {e}")


# Команда /get_schedule
@bot.message_handler(commands=['get_schedule'])
def send_next_lecture_link(message):
    try:
        current_day = datetime.now().strftime('%A').lower()
        current_time = datetime.now().strftime('%H:%M')
        next_lecture = get_next_lecture(current_day, current_time)

        if next_lecture:
            response = (
                f"Ближайшая пара:\n"
                f"Предмет: {next_lecture['subject']}\n"
                f"Время: {next_lecture['time']}\n"
                f"Ссылка: {next_lecture['link']}"
            )
            bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, "Сегодня больше пар нет.")
    except Exception as e:
        bot.send_message(config.admin_id, f"Ошибка в команде /get_schedule: {e}")


# Команда /send_greetings
@bot.message_handler(commands=['send_greetings'])
def send_greetings_to_all(message):
    try:
        for chat_id in config.subscribed_users:
            bot.send_message(chat_id,
                             "Привет! Я бот с расписанием пар. Используй команду /get_schedule, чтобы получить ближайшую пару.")
    except Exception as e:
        bot.send_message(config.admin_id, f"Ошибка в команде /send_greetings: {e}")


if __name__ == '__main__':
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(check_time_and_send_link, 'interval', minutes=1)
        scheduler.start()

        bot.polling()
    except Exception as e:
        bot.send_message(config.admin_id, f"Ошибка при запуске бота: {e}")
        restart_bot()
