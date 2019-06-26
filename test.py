from lp import *
import im
import threading
import random
import sys
import os
from Queue import Queue
print('test')

try:
	hybrid = load_object('hybrid')
except Exception as e:
	print('Warning: failed to load peer connections:',e)
	hybrid = {}


convid = 0
def mon_lp():
	global convid
	lp_start(LP_GROUP)
	while True:
		updates = lp_wait(LP_GROUP)
		for u in updates:
				print u
			#try:
				if u['type'] == 'message_new':
					from_id = u['object']['from_id']
					convid = u['object']['conversation_message_id']
					if from_id == config['page_id']:
						parse_id = int(u['object']['text'].split('|')[1].split(']')[0])
						hybrid[parse_id] = u['object']['peer_id']
						save_object("hybrid", hybrid)
		#	except Exception as e:
		#		print str(e)
thread = threading.Thread(target=mon_lp, args=())
thread.daemon = True
thread.start();

def mon_request(peer_id):
	try:
		im.add_chat_bot(peer_id, -config['group_id'])
	except Exception as e:
		#print e
		pass
	message_id = vk_call(CALL_NORMAL,'messages.send', {'peer_id':peer_id, 'random_id':random.random(),'message':'[club'+str(config['group_id'])+'|'+str(peer_id)+']'})
	time.sleep(1)
	vk_call(CALL_NORMAL,'messages.delete', {'message_ids':str(message_id),'delete_for_all':1}, True)

def send_text(peer_id, text):
	vk_call(CALL_GROUP,'messages.send', {'peer_id':hybrid[peer_id], 'random_id':random.random(),'message':text})

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
				if text == 'test3':
					vk_call(CALL_GROUP,'messages.send', {'peer_id':hybrid[peer_id], 'random_id':random.random(),'message':'test_', 'forward_messages': str(convid)+','+str(convid-1)})
#					vk_call(CALL_GROUP,'messages.send', {'peer_id':hybrid[peer_id], 'random_id':random.random(),'message':'test_', 'reply_to': str(convid)})
				if text == 'test4':
					msg_queue.put(message_id)



def handle_msg(msg):
	message = vk_call(CALL_NORMAL,'messages.getById',{'message_ids':msg,'extended':1})['items'][0]
	print message
	send_text(message['peer_id'], 'handled')

def worker():
    while True:
        item = msg_queue.get()
        if item is None:
            break
        handle_msg(item)
        msg_queue.task_done()

msg_queue = Queue()
threads = []
for i in range(config['num_threads']):
	t = threading.Thread(target=worker)
	t.start()
	threads.append(t)
try:
	mon_page()
except KeyboardInterrupt:
	os._exit(0)