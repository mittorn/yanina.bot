#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from utils import *
from vk import config
import json
import requests
import re

imconfig = {'remixsid':''}
try:
	imconfig.update(load_object('imconfig'))
except:
	pass

USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.360"
# mailru chat flags
MAIL_CHAT_FLAG_ADMINS_CAN_INVITE_LINK = 32
MAIL_CHAT_FLAG_ADMINS_CAN_ADD_ADMINS = 16
MAIL_CHAT_FLAG_ONLY_ADMINS_CAN_CHANGE_TITLE = 8
MAIL_CHAT_FLAG_ONLY_ADMINS_CAN_INVITE = 1
MAIL_CHAT_FLAG_ONLY_ADMINS_CAN_PIN = 4
REAUTH_CODE=u'99b478ae0183d739b8'
class InvalidAuthException(Exception):
	pass
class ReauthException(Exception):
	pass

def login(login, password):
    result = None

    ip_h, lg_h, cookie = __get_h()
    remixlhk = re.findall('remixlhk=(?P<h>[A-Za-z0-9]+);', cookie)[1]
    remixstid = re.search('remixstid=(?P<h>[A-Za-z0-9_]+);', cookie).group('h')

    payload = {
        "act": "login",
        "role": "al_frame",
        "expire": "",
        "recapthca":"",
        "captcha_key": "",
        "captcha_sid": "",
        "_origin": "https://vk.com",
        "ip_h": ip_h,
        "lg_h": lg_h,
        "email": login,
        "pass": password,
        "utf-8": "1"
    }
    headers = {
        "Referer": "https://vk.com",
        "Origin": "https://vk.com",
        "Accept-Charset": "utf-8",
        "Cookie": "remixlang=0; remixlhk=%s; remixstid=%s; remixdt=0; remixflash=18.0.0; remixscreen_depth=24" % (remixlhk, remixstid),
        "User-Agent":USER_AGENT
    }
    
    r = requests.post("https://login.vk.com/?act=login", data=payload, headers=headers)
    r.raise_for_status()

    if "Set-Cookie" not in r.headers:
        raise InvalidAuthException("No Cookie")
    if r.status_code == 200:
        result = re.search('remixsid=([A-Za-z0-9]+)', r.headers["Set-Cookie"]).group().split("=")[1]
        if  result == "DELETED":
            raise InvalidAuthException("200: DELETED Session")
    else:
        raise InvalidAuthException("NON 200 CODE")
    return result


def __get_h():
    r = requests.get("https://vk.com/login")
    r.raise_for_status()

    ip_h = re.search('"ip_h" value="(?P<h>[A-Za-z0-9]+)"', r.text)
    lg_h = re.search('"lg_h" value="(?P<h>[A-Za-z0-9]+)"', r.text)

    return ip_h.group("h"), lg_h.group("h"), r.headers["Set-Cookie"]

def im_post(url, payload, headers = {}):
        headers_original = {
            "Origin": "https://vk.com",
            "Cookie" : "remixsslsid=1; remixsid=%s" % imconfig['remixsid'],
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4",
            "Pragma":"no-cache",
            "Cache-Control":"no-cache",
            "Accept-Charset": "utf-8",
            "User-Agent": USER_AGENT }
        headers_original.update(headers)
        r = requests.post(url, data=payload, headers=headers_original)
        r.raise_for_status()
        print(r.headers, r.text)
        r2 = requests.get('https://vk.com', headers=headers_original)
        print(r2.headers)
        return r

def im_parse(s):
	spl = s.split('<!>')
#	print spl
	error = spl[4]
	if int(error) != 0:
		ex = 'Unknown VK exception'
		try:
			ex  = spl[5].decode('utf-8')
		except Exception:
			pass
		if ex == REAUTH_CODE:
			raise ReauthException()
		raise Exception(ex)
	base = spl[5]
	if base[0] == '<':
		l = base.find('>')
		type = base[2:l]
		value = base[l+1:]
#		print type
		if type == 'json':
			return json.loads(value)
		if type == 'bool':
			return value == '1'
	return base


def im_request(chat_id, params):
	add = {"al":1,"hash":get_chat_hash(chat_id),"im_v":2,"gid":0}
	params.update(add)
#    print add
	try:
		return im_parse(im_post("https://vk.com/al_im.php",params).text)
	except ReauthException:
		imconfig['remixsid'] = login(config['login'],config['password'])
		save_object('imconfig',imconfig)
		im_request(chat_id,params)

def add_chat_bot(chat_id, bot_id):
	r = im_post("https://vk.com/al_groups.php",{"act":"a_search_chats_box","al":1,"group_id":-bot_id})
	start = r.text.find('add_hash')+11
	l = r.text[start:].find('"')
	hash = r.text[start:start+l]
	r = im_post("https://vk.com/al_im.php",{"act":"a_add_bots_to_chat","al":1, "add_hash":hash,"bot_id":bot_id,"peer_ids":chat_id})
	try:
		return im_parse(r.text)
	except ReauthException:
		imconfig['remixsid'] = login(config['login'],config['password'])
		save_object('imconfig',imconfig)
		add_chat_bot(chat_id,bot_id)
#    print r.text.encode('utf-8')

def get_chat_hash(chat_id):
    r = im_post("https://vk.com/al_im.php",{"act":"a_renew_hash","al":1,"peers":chat_id,"gid":0})
    start = r.text.find('":"')+3
    l = r.text[start:].find('"')
    hash = r.text[start:start+l]
    return hash

def get_chat_details(chat_id):
    return im_request(chat_id,{"act":"a_get_chat_details","chat":chat_id})

def toggle_admin(chat_id,member_id,is_admin):
    return im_request(chat_id,{"act":"a_toggle_admin","al":1,"hash":get_chat_hash(chat_id),"chat":chat_id, "mid":member_id,"is_admin":is_admin})

def toggle_community(chat_id,peer_id,state):
    return im_request(chat_id,{"act":"a_toggle_community", "peer_id":peer_id,"state":state})

def load_chat_info(chat_id):
    return im_request(chat_id,{"act":"a_load_chat_info","peer":chat_id})

def return_to_chat(chat_id):
    return im_request(chat_id,{"act":"a_return_to_chat","chat":chat_id-2000000000})

def change_caccess(chat_id,member_id,access):
    return im_request(chat_id,{"act":"a_change_caccess", "peer_id":chat_id,"member_id":member_id,"access":access})

def update_flags(chat_id,flags):
    return im_request(chat_id,{"act":"a_update_flags","chat":chat_id, "flags":flags})

def kick_user(chat_id,member_id):
    return im_request(chat_id,{"act":"a_kick_user","chat":chat_id, "mid":member_id})
