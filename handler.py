# coding: utf-8
from lp import *
from command import *
import threading
import sys, os
from Queue import Queue

def handle_msg(msg):
#	try:
		message = vk_call(CALL_NORMAL,'messages.getById',{'message_ids':msg[0],'extended':1})['items'][0]
		print message
		handle_command(msg[1], msg[2], msg[3], message)
#	except Exception as e:
#		pass

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
	for i in range(config['num_threads']):
		t = threading.Thread(target=worker)
		t.start()
		threads.append(t)
