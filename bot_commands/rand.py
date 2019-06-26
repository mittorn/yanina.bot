# coding: utf-8
import random

def who(p,t,m):
	"cmd кто,кого Выбор случайного участника беседы"
	print p
	users = vk_call(CALL_NORMAL,'messages.getConversationMembers', {'peer_id': p, 'fields':'id,first_name_acc,last_name_acc'})
	print users
	rand = random.randint(0, len(users['profiles'])-1)
	u = users['profiles'][rand]
	if m['text'].split(' ')[1] == u'кого':
		name = u['first_name_acc'] + ' ' + u['last_name_acc']
	else:
		name = u['first_name'] + ' ' + u['last_name']
	vk_send(p,u'Я думаю, что ' + t.replace('?','') + u' у нас ' + '[id'+str(u['id'])+'|'+name+']')

def when(p,t,m):
	"cmd когда Выбор случайной даты"
	months = [u'сентября',u'октября',u'ноября',u'декабря',u'января',u'февраля',u'марта',u'апреля',u'мая',u'июня',u'июля',u'августа']
	if random.randint(0,5):
		vk_send(p, random.choice([u'Я уверена, ',u'Я думаю, ']) + t.replace('?','') +' '+ str(random.randint(1,31))+' '+random.choice(months)+' '+str(random.randint(2018,2050)))
	else:
		vk_send(p, random.choice([u'Когда рак на гаре свистнет',u'Никогда']))

def infa(p,t,m):
	"cmd инфа Проверяет инфу"
	vk_send(p, u'Вероятность того, что ' + t + u' равна ' + str(random.randint(0,146))+'%')