from lp import *
import im
import threading, time, random
from handler import enqueue_msg
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
			print(u)
			try:
				if u.type == 'message_new':
					from_id = u.object.from_id
					convid = u.object.conversation_message_id
					if from_id == config.page_id:
						parse_id = int(u.object.text.split('|')[1].split(']')[0])
						hybrid[parse_id] = u.object.peer_id
						save_object("hybrid", hybrid)
			except Exception as e:
				print(str(e))
def mon_start():
	thread = threading.Thread(target=mon_lp, args=())
	thread.daemon = True
	thread.start();

def mon_request(peer_id):
	try:
		im.add_chat_bot(peer_id, -config.group_id)
	except Exception as e:
		print('Failed to add bot: ',e)
	message_id = vkpage.messages.send(peer_id=peer_id, random_id=random.random(),message='[club'+str(config['group_id'])+'|'+str(peer_id)+']')
	time.sleep(1)
	try:
		vkpage.messages.delete(message_ids=str(message_id),delete_for_all=1)
	except Exception:
		pass

def vk_send(peer_id, text, attachments = None):
	if not peer_id in hybrid:
		mon_request(peer_id)
		time.sleep(2)
	params = D(peer_id=hybrid[peer_id], random_id=random.random(),message=text)
	if attachments:
		params.attachment = attachments
	vkgroup.messages.send(params)

def mon_page():
	lp_start(LP_PAGE)
	while True:
		updates = lp_wait(LP_PAGE)
		for u in updates:
			#print(json.dumps(u,ensure_ascii=False).encode('utf-8'))
			if u[0] == 4:
				message_id = u[1]
				flags = u[2]
				peer_id = u[3]
				ts = u[4]
				title = u[5]
				text = u[6]
				spl = text.split(' ')
				if tostr(tounicode(spl[0]).lower()) in config.names:
					try:
						enqueue_msg((message_id,peer_id,spl[1],text[len(spl[0])+len(spl[1])+2:]))
					except Exception:
						pass
