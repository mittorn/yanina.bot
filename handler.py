# coding: utf-8
from lp import *
from command import *
import threading
import sys, os
try:
	from Queue import Queue
except Exception:
	from queue import Queue
import traceback
def handle_msg(msg):
	try:
		message = vkpage.messages.getById(message_ids=msg[0],extended=1,fields='first_name,last_name').items[0]
		message.cmd = msg[2]
		print(message._json)

		handle_command(msg[1], msg[2], msg[3], message)
	except Exception as e:
		print('Handle: ',traceback.print_exc(e))

def enqueue_msg(msg):
	msg_queue.put(msg)

def worker():
    while True:
        item = msg_queue.get()
        if item is None:
            break
        handle_msg(item)
        msg_queue.task_done()

msg_queue = Queue()
threads = []

def handler_start():
	for i in range(config.num_threads):
		t = threading.Thread(target=worker)
		t.start()
		threads.append(t)
