from sql_commands import *
import mysql.connector


class Database():

    def __init__(self, path):
        self.conn = mysql.connector.connect(
            user='root', password='hrefsrc08', host='localhost', database='TimeTrackingAppDB')
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def emptyTasks(self, user_id):
        self.cur.execute(empty_tasks.format(id=user_id))

    def addTasks(self, user_id, args):
        for name in args:
            self.cur.execute(add_tasks.format(name=name, id=user_id))

    def getTasks(self, user_id):
        self.cur.execute(get_tasks.format(id=user_id))
        return self.cur.fetchall()

    def exist(self, user_id):
        self.cur.execute(exists.format(id=user_id))
        return len(self.cur.fetchall()) > 0

    def addUser(self, name, user_id):
        self.cur.execute(add_user.format(name=name, id=user_id))
