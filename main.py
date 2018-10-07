import telepot
from pprint import pprint
from telepot.loop import MessageLoop


def handle(msg):
    pprint(msg)


bot = telepot.Bot('699222682:AAHbzs4gCAEBFFS7eOJAvmCiQIy4AxMnshA')
MessageLoop(bot, handle).run_as_thread()
while 1:
    pass
