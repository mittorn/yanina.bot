# coding: utf-8
from module_imports import *
def isadmin(m):
	return m['from_id'] in config['owners']

@cmd('eval', 'ебал', 'евал', admin=True)
def cmdeval(p,t,m):
	if isadmin(m):
		vk_send(p,str(eval(t)))
	else:
		vk_send(p,u'нахуй')

