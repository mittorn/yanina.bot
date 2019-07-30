# coding: utf-8
from module_imports import *
import random

@cmd('кто', 'кого')
def who(p,t,m):
	'Выбор случайного участника беседы'
	users = vkpage.messages.getConversationMembers(peer_id=p, fields='id,first_name_acc,last_name_acc')
	rand = random.randint(0, len(users.profiles)-1)
	u = users.profiles[rand]
	if m.text.split(' ')[1] == 'кого':
		name = u.first_name_acc + ' ' + u.last_name_acc
	else:
		name = u.first_name + ' ' + u.last_name
	vk_send(p,'Я думаю, что ' + t.replace('?','') + ' у нас ' + '[id'+str(u.id)+'|'+name+']')
	

@cmd('бутылка')
def bottle(p,t,m):
	users = vkpage.messages.getConversationMembers(peer_id=p, fields='id,first_name_acc,last_name_acc')
	rand = random.randint(0, len(users.profiles)-1)
	u = users.profiles[rand]
	name = u.first_name + ' ' + u.last_name

	
	msg1 = ["Разминай анус","Присаживайся","Хорошего сидеть","Обутылен","Надеюсь, это приятно","Главное, что я не присяду","Тебе норм... Наверное","Теперь ты точно Россиянин","Оххх я не завидую тебе"]
	msg2 = ['Я уверена, на бутылке у нас','На бутылке у нас', 'Бутылку в зад у нас получает', 'Я уверена, на бутылке у нас']
	isis = 'Бинго!<br>Изысканная бутылка достаётся'
	bank = 'Ууупс<br>Бутылки кончились, остались банки<br>Следовательно, на банку у нас сядет'
	r = random.randint(0,7)
	if r == 1:
		vk_send(p,bank +' [id'+str(u.id)+'|'+name+']\n' + random.choice(msg1) + '\nГлавное чтоб не лопнула!','photo353166779_456284069')
	elif r == 2:
		vk_send(p,isis +' [id'+str(u.id)+'|'+name+']\n' + random.choice(msg1),'photo353166779_456284070')
	else:
		vk_send(p,random.choice(msg2) +' [id'+str(u.id)+'|'+name+']\n' + random.choice(msg1),'photo353166779_456284068')

@cmd('когда')
def when(p,t,m):
	'Выбор случайной даты'
	months = ['сентября','октября','ноября','декабря','января','февраля','марта','апреля','мая','июня','июля','августа']
	if random.randint(0,5):
		vk_send(p, random.choice(['Я уверена, ','Я думаю, ']) + t.replace('?','') +' '+ str(random.randint(1,31))+' '+random.choice(months)+' '+str(random.randint(2018,2050)))
	else:
		vk_send(p, random.choice(['Когда рак на горе свистнет','Никогда']))

@cmd('выбери')
def choice(p,t,m):
	'выбор'
	vk_send(p,random.choice([a for f in t.split(', ') for a in f.split(' или ')]))

@cmd('инфа')
def infa(p,t,m):
	'Проверяет инфу'
	vk_send(p, 'Вероятность того, что ' + t + ' равна ' + str(random.randint(0,146))+'%')
