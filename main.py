import telepot
import time
from telepot.loop import MessageLoop
from api import Database
import pickle
import datetime


adding = False
starting = False
id_min = 0
history = {'started': None, 'ended': None, 'id': None}


def parseMessage(msg, id):
    global adding
    global starting
    global id_min
    global history
    text = msg['text']
    if text == '/start':
        reply_markup = {'keyboard': [['Start', 'Finish']],
                        "one_time_keyboard": False, "resize_keyboard": True}
        bot.sendMessage(id, 'Hello!',
                        reply_markup=reply_markup)
    elif text == '/empty':
        users.empty_tasks(id)
    elif text == '/add':
        bot.sendMessage(id, 'Enter your tasks here')
        adding = True
    elif text == '/update':
        pass
    elif text == '/tasks':
        tasks = [x[1] for x in users.get_tasks(id)]
        if len(tasks) > 0:
            bot.sendMessage(id, '\n'.join(tasks))
        else:
            bot.sendMessage(id, 'You have no tasks to do.')
    elif text == '/help':
        bot.sendMessage(id, 'I can\'t help you now')
    elif text == 'Start':
        tasks = [(x[:2]) for x in users.get_tasks(id)]
        if len(tasks) > 0:
            starting = True
            id_min = tasks[0][0]
            lst = ['/' + str(x[0] - id_min) + ' ' + x[1] for x in tasks]
            bot.sendMessage(id, '\n'.join(lst))
        else:
            bot.sendMessage(id, 'You have no tasks to do.')
    elif str.isnumeric(text[1:]) and starting and users.exist_task(int(text[1:]) + id_min):
        history['started'] = time_now()
        history['id'] = int(text[1:]) + id_min
        bot.sendMessage(id, 'Started!')
    elif text == 'Finish' and history['started']:
        history['ended'] = time_now()
        users.add_action(history)
        bot.sendMessage(id, 'Great! You have completed this task!')
    else:
        if adding:
            users.add_tasks(id, msg['text'].split('\n'))
            adding = False
        else:
            bot.sendMessage(id, 'Please choose any command')


def time_now():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+03:00")


def on_chat_message(msg):
    id = msg['from']['id']
    if not users.exist_user(id):
        users.addUser('Sasha', id)
    parseMessage(msg, id)


def startBot():
    with open('token', 'rt') as f:
        TOKEN = f.readline()
    bot = telepot.Bot(TOKEN)
    MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()
    print('Listening ...')
    return bot


try:
    users = Database('Users.db')
    bot = startBot()
    while 1:
        time.sleep(2)
finally:
    users.close()
