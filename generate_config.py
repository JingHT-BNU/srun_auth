import random


url = input('auth server for wired connection (without protocol): ')
url_wireless = input('auth server for wireless connection (without protocol): ')
_switch = input('wired connection? (yes/no/auto)') == 'yes'
if _switch == 'yes':
    switch = True
elif _switch == 'no':
    switch = False
else:
    switch = None

ip = input('your ip (not necessary): ')
user = input('user name: ')
password = input('password: ')
callback_number = '11240'
for _ in range(16):
    callback_number += str(random.randint(0,9))
f = open('config.py', 'w+')
f.write(f"""init_url = '{url}'
init_url_wireless = '{url_wireless}'
switch = {switch}
ip = '{ip}'  # blank for autonomous
type = '1'  # 1 for computer and 0 for mobile phone
username = '{user}'
password = '{password}'
callback_number = {callback_number}  # a random 21-digits number, starts with 11240""")
f.close()
