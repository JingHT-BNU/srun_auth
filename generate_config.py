import random


url = input('auth server (without protocol): ')
if url[-1] == '/':
    url = url[:-1]
ip = input('your ip (not necessary): ')
user = input('user name: ')
password = input('password: ')
callback_number = '11240'
for _ in range(16):
    callback_number += str(random.randint(0,9))
f = open('config.py', 'w+')
f.write(f"""init_url = '{url}'
ip = '{ip}'  # blank for autonomous
type = '1'  # 1 for computer and 0 for mobile phone
username = '{user}'
password = '{password}'
callback_number = {callback_number}  # a random 21-digits number, starts with 11240""")
f.close()
