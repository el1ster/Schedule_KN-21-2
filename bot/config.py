# config.py

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
        {'time': '9:00 - 10:25', 'send_time': '8:55', 'subject': 'ОБДЗ лр.', 'link': 'https://meet.google.com/your-link'},
        {'time': '10:45 - 12:10', 'send_time': '10:40', 'subject': 'СА лек.', 'link': 'https://meet.google.com/ung-ffgu-qwq'},
        {'time': '12:25 - 13:50', 'send_time': '12:20', 'subject': 'ОБДЗ лр.', 'link': 'https://meet.google.com/your-link'},
    ],
}

# Список подписанных пользователей
subscribed_users = [
    # Добавьте chat_id пользователей, которым нужно отправлять уведомления
    1022897421,
    -1001530972086,
]

# chat_id вашего бота для отправки уведомлений
BOT_CHAT_ID = 6560084642  # Замените на chat_id вашего бота