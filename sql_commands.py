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
SELECT name from Tasks WHERE user_id = {id}
'''
