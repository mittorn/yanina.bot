# coding: utf-8
from module_imports import *

from hybrid import mon_request

@cmd('помощь', 'help')
def help(p,text,msg):
	'Список комманд'
	vk_send(p,'Реализовано:\n'+('\n'.join(mod_cmdhelps)))

@cmd('тест')
def test(p,t,m):
	'Просто тест'
	vk_send(p,'тест')

@cmd('связь')
def connect(p,t,m):
	'Повторно связать страницу и группу (если бота кикнули)'
	mon_request(p)

@cmd('reload', 'обновись', admin=True)
def reload(p,t,m):
	load_config()
	print('перезагрузка команд')
	reload_modules()
	print('done')

