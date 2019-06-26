# coding: utf-8

def help(p,text,msg):
	"cmd помощь,help Список комманд"
	vk_send(p,'Реализовано:\n'+('\n'.join(cmd_helps)))

def test(p,t,m):
	"cmd тест Просто тест"
	vk_send(p,'тест')