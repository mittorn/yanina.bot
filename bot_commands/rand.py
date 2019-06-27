# coding: utf-8
import random

def who(p,t,m):
	"cmd кто,кого Выбор случайного участника беседы"
	users = vk_call(CALL_NORMAL,'messages.getConversationMembers', {'peer_id': p, 'fields':'id,first_name_acc,last_name_acc'})
	rand = random.randint(0, len(users['profiles'])-1)
	u = users['profiles'][rand]
	if m['text'].split(' ')[1] == u'кого':
		name = u['first_name_acc'] + ' ' + u['last_name_acc']
	else:
		name = u['first_name'] + ' ' + u['last_name']
	vk_send(p,u'Я думаю, что ' + t.replace('?','') + u' у нас ' + '[id'+str(u['id'])+'|'+name+']')
	

def bottle(p,t,m):
	"cmd бутылка"
	users = vk_call(CALL_NORMAL,'messages.getConversationMembers', {'peer_id': p, 'fields':'id,first_name_acc,last_name_acc'})
	rand = random.randint(0, len(users['profiles'])-1)
	u = users['profiles'][rand]
	if m['text'].split(' ')[1] == u'кого':
		name = u['first_name_acc'] + ' ' + u['last_name_acc']
	else:
		name = u['first_name'] + ' ' + u['last_name']

	
	msg1 = ["Разминай анус","Присаживайся","Хорошего сидеть","Обутылен","Надеюсь, это приятно","Главное, что я не присяду","Тебе норм... Наверное","Теперь ты точно Россиянин","Оххх я не завидую тебе"]
	msg2 = ['Я уверена, на бутылке у нас','На бутылке у нас', 'Бутылку в зад у нас получает', 'Я уверена, на бутылке у нас']
	isis = u'Бинго!<br>Изысканная бутылка достаётся'
	bank = u'Ууупс<br>Бутылки кончились, остались банки<br>Следовательно, на банку у нас сядет'
	r = random.randint(0,7)
	if r == 1:
		vk_send(p,bank +' [id'+str(u['id'])+'|'+name+']\n' + random.choice(msg1).decode('utf-8') + u'\nГлавное чтоб не лопнула!','photo353166779_456284069')
	elif r == 2:
		vk_send(p,isis +' [id'+str(u['id'])+'|'+name+']\n' + random.choice(msg1).decode('utf-8'),'photo353166779_456284070')
	else:
		vk_send(p,random.choice(msg2).decode('utf-8') +' [id'+str(u['id'])+'|'+name+']\n' + random.choice(msg1).decode('utf-8'),'photo353166779_456284068')

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