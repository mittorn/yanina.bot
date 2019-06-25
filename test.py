from lp import *
import im
import threading
import random
print('test')

try:
	hybrid = load_object('hybrid')
except Exception as e:
	print('Warning: failed to load peer connections:',e)
	hybrid = {}

def mon_lp():
	global convid
	lp_start(LP_GROUP)
	while True:
		updates = lp_wait(LP_GROUP)
		for u in updates:
			print u
			try:
				if u['type'] == 'message_new':
					from_id = u['object']['from_id']
					if from_id == config['page_id']:
						parse_id = int(u['object']['text'].split('|')[1].split(']')[0])
						hybrid[parse_id] = u['object']['peer_id']
						save_object("hybrid", hybrid)
			except Exception as e:
				print e
thread = threading.Thread(target=mon_lp, args=())
thread.daemon = True
thread.start();

def mon_request(peer_id):
	try:
		im.add_chat_bot(peer_id, -config['group_id'])
	except Exception as e:
		print e
	message_id = vk_call(CALL_NORMAL,'messages.send', {'peer_id':peer_id, 'random_id':random.random(),'message':'[club'+str(config['group_id'])+'|'+str(peer_id)+']'})
	time.sleep(1)
	vk_call(CALL_NORMAL,'messages.delete', {'message_ids':str(message_id),'delete_for_all':1}, True)

def send_text(peer_id, text):
	vk_call(CALL_GROUP,'messages.send', {'peer_id':hybrid[peer_id],'message':text})

def mon_page():
	lp_start(LP_PAGE)
	while True:
		updates = lp_wait(LP_PAGE)
		for u in updates:
			print u
			if u[0] == 4:
				message_id = u[1]
				flags = u[2]
				peer_id = u[3]
				ts = u[4]
				title = u[5]
				text = u[6]
				if text == 'test':
					mon_request(peer_id)
				if text == 'test2':
					send_text(peer_id,'passed')
mon_page()