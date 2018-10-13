import telepot
import os
import time
import datetime
import Calendar
from telepot.loop import MessageLoop
from api import Database
import os.path
import message_templates as mt


adding = {}
starting = {}
id_min = {}
history = {'id': {'started': None, 'ended': None, 'id': None}}


def parseMessage(msg, id):
    global adding
    global starting
    global id_min
    global history
    text = msg['text']
    print(text, ' : ', msg['from']['first_name'])
    if text == '/start':
        reply_markup = {'keyboard': [['Start', 'Finish']],
                        "one_time_keyboard": False, "resize_keyboard": True}
        bot.sendMessage(id, 'Hello {0}!'.format(msg['from']['first_name']) + mt.hello_message,
                        reply_markup=reply_markup)
        bot.sendMessage(id, mt.get_acess_message)
        bot.sendMessage(id, Calendar.get_link())
    elif 'https://www.googleapis.com/auth/calendar.events' in text:
        Calendar.save_creds(text[23:-54], id)
    elif text == '/empty':
        users.empty_tasks(id)
    elif text == '/add':
        bot.sendMessage(id, 'Enter your tasks here')
        adding['id'] = True
    elif text == '/update':
        pass
    elif text == '/tasks':
        tasks = [x[1] for x in users.get_tasks(id)]
        if len(tasks) > 0:
            bot.sendMessage(id, '\n'.join(tasks))
        else:
            bot.sendMessage(id, 'You have no tasks to do.')
    elif text == '/help':
        bot.sendMessage(id, mt.help_message)
    elif text == 'Start' and not history['id']['started']:
        tasks = [(x[:2]) for x in users.get_tasks(id)]
        if len(tasks) > 0:
            starting['id'] = True
            id_min['id'] = tasks[0][0]
            lst = ['/' + str(x[0] - id_min['id']) + ' ' + x[1] for x in tasks]
            bot.sendMessage(id, 'Select task to start')
            bot.sendMessage(id, '\n'.join(lst))
        else:
            bot.sendMessage(id, 'You have no tasks to do.')
    elif str.isnumeric(text[1:]) and starting['id'] and users.exist_task(int(text[1:]) + id_min['id']):
        history['id']['started'] = time_now()
        history['id']['id'] = int(text[1:]) + id_min['id']
        starting['id'] = False
        bot.sendMessage(id, 'Started!')
    elif text == 'Finish' and history['id']['started']:
        history['id']['ended'] = time_now()
        history['id']['user_id'] = id
        users.add_action(history['id'])
        adding['id'] = False
        starting['id'] = False
        history['id'] = {'started': None, 'ended': None, 'id': None}
        id_min['id'] = 0
        users.delete_task(id, users.get_task_name(history['id']['id']))
        bot.sendMessage(id, 'Great! You have completed this task!')
    else:
        if adding['id']:
            users.add_tasks(id, msg['text'].split('\n'))
            adding['id'] = False
        else:
            bot.sendMessage(
                id, 'I never chat to users, because my time is valuable. Your is tood:) ' +
                'Please choose any command.')


def time_now():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+03:00")


def on_chat_message(msg):
    id = msg['from']['id']
    if not users.exist_user(id):
        users.addUser(msg['from']['first_name'], id)
        adding['id'] = False
        starting['id'] = False
        history['id'] = {'started': None, 'ended': None, 'id': None}
        id_min['id'] = 0
    parseMessage(msg, id)


def startBot():
    ids = users.get_users()
    for id in ids:
        adding['id'] = False
        starting['id'] = False
        history['id'] = {'started': None, 'ended': None, 'id': None}
        id_min['id'] = 0
    with open('token', 'rt') as f:
        TOKEN = f.readline()
    bot = telepot.Bot(TOKEN)
    MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()
    print('Listening ...')
    return bot


try:
    os.environ['TZ'] = 'Europe/Kiev'
    users = Database('Users.db')
    bot = startBot()
    while 1:
        time.sleep(2)
finally:
    users.close()
