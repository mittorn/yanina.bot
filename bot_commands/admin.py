# coding: utf-8
def isadmin(m):
	return m['from_id'] in config['owners']

def cmdeval(p,t,m):
	"admin eval,ебал,евал"
	if isadmin(m):
		vk_send(p,str(eval(t)))
	else:
		vk_send(p,u'нахуй')
