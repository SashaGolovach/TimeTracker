import telepot
import time
from telepot.loop import MessageLoop
from api import Database
import pickle


mode = False


def parseMessage(msg, id):
    global mode
    text = msg['text']
    if text.startswith('/empty'):
        users.emptyTasks(id)
    elif text.startswith('/add'):
        bot.sendMessage(id, 'Enter your tasks here')
        mode = True
    elif text.startswith('/update'):
        pass
    elif text.startswith('/tasks'):
        tasks = [x[0] for x in users.getTasks(id)]
        bot.sendMessage(id, '\n'.join(tasks))
    elif text.startswith('/help'):
        bot.sendMessage(id, 'I can\'t help you now')
    else:
        if mode:
            users.addTasks(id, msg['text'].split('\n'))
            mode = False
        else:
            bot.sendMessage(id, 'Please choose any command')


def on_chat_message(msg):
    id = msg['from']['id']
    if not users.exist(id):
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
