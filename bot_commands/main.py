# coding: utf-8

from hybrid import mon_request

def help(p,text,msg):
	"cmd помощь,help Список комманд"
	vk_send(p,u'Реализовано:\n'+('\n'.join(cmd_helps)))

def test(p,t,m):
	"cmd тест Просто тест"
	vk_send(p,'тест')

def connect(p,t,m):
	"cmd связь Повторно связать страницу и группу (если бота кикнули)"
	mon_request(p)

def reload(p,t,m):
	"admin reload,обновись"
	load_config()
	print('перезагрузка команд')
	reload_commands()
	print('done')
