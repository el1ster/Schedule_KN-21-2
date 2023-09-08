import telebot
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import os
import sys

TOKEN = '6560084642:AAFsR9ux5rmqQktwHDfW0gZqFo63jewRyrw'
admin_id = '1022897421'

schedule = {
    'monday': [
        {'time': '9:00 - 10:25', 'send_time': '8:55', 'subject': 'КСКС лр.', 'link': 'https://meet.google.com/oef-esfj-gfa'},
        {'time': '10:45 - 12:10', 'send_time': '10:40', 'subject': 'КСКС лек.', 'link': 'https://meet.google.com/ofk-smwe-gwe'},
        {'time': '12:45 - 14:10', 'send_time': '12:40', 'subject': 'ГМтаГК лр.', 'link': 'http://meet.google.com/omj-hase-vvo'},
    ],
    'tuesday': [
        {'time': '9:00 - 10:25', 'send_time': '8:55', 'subject': 'WEB ОСМП лек.', 'link': 'https://meet.google.com/dbs-fsbt-gav'},
        {'time': '10:45 - 12:10', 'send_time': '10:40', 'subject': 'Історія науки і техники лек.', 'link': 'https://meet.google.com/pgi-tfug-kzj'},
        {'time': '12:45 - 14:10', 'send_time': '12:40', 'subject': 'ОБДЗ лек.', 'link': 'https://meet.google.com/jvv-ejuw-uzu'},
        {'time': '14:30 - 15:55', 'send_time': '14:25', 'subject': 'ДГМтаГК лек.', 'link': 'https://meet.google.com/zwk-iiht-szq'},
    ],
    'wednesday': [
        {'time': '9:00 - 10:25', 'send_time': '8:55', 'subject': 'WEB ОСМП лр.', 'link': 'https://meet.google.com/dbs-fsbt-gav'},
        {'time': '10:45 - 12:10', 'send_time': '10:40', 'subject': 'Історія науки і техники лр.', 'link': 'https://meet.google.com/pgi-tfug-kzj'},
    ],
    'thursday': [
        {'time': '10:45 - 12:10', 'send_time': '10:40', 'subject': 'СА лр.', 'link': 'https://meet.google.com/hfj-xgpt-zwi'},
        {'time': '12:45 - 14:10', 'send_time': '12:40', 'subject': 'ОБДЗ лек.', 'link': 'https://meet.google.com/jvv-ejuw-uzu'},
    ],
    'friday': [
        {'time': '9:00 - 10:25', 'send_time': '8:55', 'subject': 'ОБДЗ лр.', 'link': '(Кузьменко-https://meet.google.com/yum-rvfv-oka)\n(Голуб-https://meet.google.com/jnm-uncm-esb)'},
        {'time': '10:45 - 12:10', 'send_time': '10:40', 'subject': 'СА лек.', 'link': 'https://meet.google.com/ung-ffgu-qwq'},
        {'time': '12:25 - 13:50', 'send_time': '12:20', 'subject': 'ОБДЗ лр.', 'link': '(Кузьменко-https://meet.google.com/yum-rvfv-oka)\n(Голуб-https://meet.google.com/jnm-uncm-esb)'},
    ],
}

# Список подписанных пользователей
subscribed_users = [
    # Добавьте chat_id пользователей, которым нужно отправлять уведомления
    1022897421,
    -1001530972086,
]

bot = telebot.TeleBot(TOKEN)


def restart_bot():
    print("Restarting bot...")
    python = sys.executable
    os.execl(python, python, *sys.argv)


# Определение следующей пары
def get_next_lecture(day, time):
    try:
        if day in schedule:
            for lecture in schedule[day]:
                lecture_time = lecture['time'].split(' - ')
                start_time = datetime.strptime(lecture_time[0], '%H:%M')
                end_time = datetime.strptime(lecture_time[1], '%H:%M')
                current_time = datetime.strptime(time, '%H:%M')
                if start_time > current_time:
                    return lecture
        return None
    except Exception as e:
        bot.send_message(admin_id, f"Ошибка в функции get_next_lecture: {e}")


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
                for chat_id in subscribed_users:
                    bot.send_message(chat_id, response)
    except Exception as e:
        bot.send_message(admin_id, f"Ошибка в функции check_time_and_send_link: {e}")


# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        bot.reply_to(message,
                     "Привет! Я бот с расписанием пар. Используй команду /get_schedule, чтобы получить ближайшую пару.")
    except Exception as e:
        bot.send_message(admin_id, f"Ошибка в команде /start: {e}")


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
        bot.send_message(admin_id, f"Ошибка в команде /get_schedule: {e}")


# Команда /send_greetings
@bot.message_handler(commands=['send_greetings'])
def send_greetings_to_all(message):
    try:
        for chat_id in subscribed_users:
            bot.send_message(chat_id,
                             "Привет! Я бот с расписанием пар. Используй команду /get_schedule, чтобы получить ближайшую пару.")
    except Exception as e:
        bot.send_message(admin_id, f"Ошибка в команде /send_greetings: {e}")


if __name__ == '__main__':
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(check_time_and_send_link, 'interval', minutes=1)
        scheduler.start()

        bot.polling()
    except Exception as e:
        bot.send_message(admin_id, f"Ошибка при запуске бота: {e}")
        restart_bot()