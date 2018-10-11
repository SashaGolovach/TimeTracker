from sql_commands import *
import mysql.connector
import Calendar


class Database():

    def __init__(self, path):
        self.conn = mysql.connector.connect(
            user='root', password='hrefsrc08', host='localhost', database='TimeTrackingAppDB')
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def empty_tasks(self, user_id):
        self.cur.execute(empty_tasks.format(id=user_id))

    def add_tasks(self, user_id, args):
        for name in args:
            self.cur.execute(add_tasks.format(name=name, id=user_id))

    def get_tasks(self, user_id):
        self.cur.execute(get_tasks.format(id=user_id))
        return self.cur.fetchall()

    def exist_user(self, user_id):
        self.cur.execute(exists.format(id=user_id))
        return len(self.cur.fetchall()) > 0

    def exist_task(self, task_id):
        self.cur.execute(exists_task.format(id=task_id))
        return len(self.cur.fetchall()) > 0

    def get_task_name(self, task_id):
        self.cur.execute(get_task_name_command.format(task_id=task_id))
        return self.cur.fetchall()[0][0]

    def add_action(self, info):
        self.cur.execute(add_action.format(
            started=info['started'], ended=info['ended'], task_id=info['id']))
        Calendar.update(info['started'], info['ended'],
                        self.get_task_name(info['id']), info['user_id'])

    def addUser(self, name, user_id):
        self.cur.execute(add_user.format(name=name, id=user_id))

    def get_users(self):
        self.cur.execute(get_users_command.format())
        return self.cur.fetchall()
