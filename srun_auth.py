import requests
import time
import re
from encryption.srun_md5 import *
from encryption.srun_sha1 import *
from encryption.srun_base64 import *
from encryption.srun_xencode import *
from config import *
import socket
def _t():
	return str(int(time.time() * 1000))

header={
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0'
}
url = ''
if not init_url_wireless and not init_url:
	print('init url not found')
	exit(1)
if switch:
	url = init_url_wireless
elif switch is None:
	from detect_connection import detect_network_type_multilingual
	result = detect_network_type_multilingual()
	if result and isinstance(result, dict):
		if result.get('ethernet', False):
			url = init_url
		elif result.get('wifi', False):
			url = init_url_wireless
else:
	url = init_url
if not url:
	if init_url_wireless and not init_url:
		url = init_url_wireless
	else:
		url = init_url


get_challenge_api = f"http://{url}/cgi-bin/get_challenge"
srun_portal_api = f"http://{url}/cgi-bin/srun_portal"
n = '200'
ac_id='1'
enc = "srun_bx1"
t = _t()
callback = f'jQuery{callback_number}_{t}'
get_info_api = f"http://{url}/cgi-bin/rad_user_info?callback=" + callback

if not ip:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		s.connect(('172.16.202.202', 80))
		ip = s.getsockname()[0]
	finally:
		s.close()

def get_chksum():
	chkstr = token+username
	chkstr += token+hmd5
	chkstr += token+ac_id
	chkstr += token+ip
	chkstr += token+n
	chkstr += token+type
	chkstr += token+i
	return chkstr

def get_info():
	info_temp={
		"username":username,
		"password":password,
		"ip":ip,
		"acid":ac_id,
		"enc_ver":enc
	}
	i=re.sub("'",'"',str(info_temp))
	i=re.sub(" ",'',i)
	return i

def get_token():
	global token
	get_challenge_params={
		"callback": callback,
		"username":username,
		"ip":ip,
		"_":str(int(t)+1),
	}
	get_challenge_res=requests.get(get_challenge_api,params=get_challenge_params,headers=header)
	token=re.search('"challenge":"(.*?)"',get_challenge_res.text).group(1)

def do_complex_work():
	global i,hmd5,chksum
	i=get_info()
	i="{SRBX1}"+get_base64(get_xencode(i,token))
	hmd5=get_md5(password,token)
	chksum=get_sha1(get_chksum())

def login():
	srun_portal_params={
	'callback': callback,
	'action':'login',
	'username':username,
	'password':'{MD5}'+hmd5,
	'ac_id':ac_id,
	'ip':ip,
	'chksum':chksum,
	'info':i,
	'n':n,
	'type':type,
	'os':'windows+10',
	'name':'windows',
	'double_stack':'0',
	'_': _t()
	}
	srun_portal_res=requests.get(srun_portal_api,params=srun_portal_params,headers=header)
	print(srun_portal_res.text)

if __name__ == '__main__':
	get_token()
	do_complex_work()
	login()
	res = requests.get(get_info_api, headers=header)
	print(eval(res.text[42:-1])['error'])
