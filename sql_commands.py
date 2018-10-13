add_user = '''
INSERT INTO Users (name, id) VALUES ('{name}', {id})
'''
exists = '''
SELECT name, id FROM Users WHERE id = {id}
'''
add_tasks = '''
INSERT INTO Tasks (name, user_id) Values ('{name}', {id})
'''

empty_tasks = '''
DELETE FROM Tasks WHERE user_id = {id}
'''

get_tasks = '''
SELECT * from Tasks WHERE user_id = {id}
'''
exists_task = '''
SELECT * FROM Tasks WHERE id = {id}
'''
add_action = '''
INSERT INTO Actions (started, ended, task_id) VALUES ('{started}', '{ended}', {task_id})
'''

get_task_name_command = '''
SELECT name from Tasks WHERE id = {task_id}
'''

get_users_command = '''
SELECT id from Users
'''
delete_task_command = '''
DELETE FROM Tasks WHERE user_id = {id} and name = {name}
'''
