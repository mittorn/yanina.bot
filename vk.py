from utils import *
import requests
import time
lp_modes = aenum('LP_PAGE','LP_GROUP')
call_modes = aenum('CALL_NORMAL', 'CALL_AUDIO' ,'CALL_GROUP', 'CALL_BROWSER')
api_versions = { CALL_NORMAL : '5.95', CALL_AUDIO : '5.71', CALL_GROUP : '5.50' }
api_tokens = {}

def vk_call(mode,method,specparam, ignore = False):
	try:
		param = {}
		if mode == CALL_BROWSER:
			raise Exception('Not implemented yet')
		if mode in api_versions:
			param['v'] = api_versions[mode]
		if mode in api_tokens:
			param['access_token'] = api_tokens[mode]
		param.update(specparam)
		headers = {}
		if mode == CALL_AUDIO:
			headers['User-Agent'] = 'VKAndroidApp/4.38-816 (Android 6.0; SDK 23; x86; Google Nexus 5X; ru)'
		result = requests.post('https://api.vk.com/method/%s'%method, data=param, headers = {'User-Agent':'VKAndroidApp/4.38-816 (Android 6.0; SDK 23; x86; Google Nexus 5X; ru)'}).json()
		if not 'response' in result:
			raise Exception(result['error']['error_msg'])
		return result['response']
	except Exception as e:
		if not ignore:
			raise e

def _load_config():
	global config
	config = load_json('vk')
	api_tokens[CALL_NORMAL] = config['token_normal']
	api_tokens[CALL_AUDIO] = config['token_audio']
	api_tokens[CALL_GROUP] = config['token_group']
_load_config()