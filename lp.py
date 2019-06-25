from vk import *
_longpolls = {}

def lp_start(mode):
	if mode == LP_PAGE:
		_longpolls[mode] = vk_call(CALL_NORMAL, 'messages.getLongPollServer', {'lp_version':3})
		_longpolls[mode]['server'] = 'https://'+_longpolls[mode]['server']
	if mode == LP_GROUP:
		_longpolls[mode] = vk_call(CALL_GROUP, 'groups.getLongPollServer', {'group_id':config['group_id']})

def lp_wait(mode):
	try:
		longpoll = _longpolls[mode]
		response = requests.get('{server}?act=a_check&key={key}&ts={ts}&wait=90'.format(server=longpoll['server'], key=longpoll['key'], ts=longpoll['ts'])).json()
		listen = {'result':None,'ts':longpoll['ts']}
#	print response
		longpoll['ts'] = response['ts']
#	for result in response['updates']:
#		if result[0] == 4:
#			listen = {'result':result, 'ts':responce['ts']}
		return response['updates']
	except Exception as e:
		print('Longpoll expeption '+str(e))
		lp_start(mode)
		time.sleep(10)
	return []
