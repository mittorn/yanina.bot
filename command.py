# coding: utf-8
import os, sys, types

cmd_commands = {}
cmd_helps = []
cmd_modules = []

#print sys.getdefaultencoding()
def force_utf8():
	import imp
	_sys_org = imp.load_dynamic('_sys_org', 'sys')
	_sys_org.setdefaultencoding('utf-8')
	del _sys_org

#force_utf8()
#print sys.getdefaultencoding()
cmd_imports = None

def load_commands():
	global cmd_modules, cmd_commands, cmd_helps, cmd_imports
	if not cmd_imports:
		cmd_imports = __import__('command_imports')
	p = sys.path
	sys.path = ['bot_commands/']
	cmd_modules = [__import__(module[0:-3]) for module in filter(lambda x: x and x[-3:] == ".py", os.listdir("bot_commands"))]
	sys.path = p

	for m in cmd_modules:
		v = m.__dict__
		for d in v:
			f = v[d]
			if not type(f) is types.FunctionType:
				continue
			if not hasattr(f,'__doc__'):
				continue
			doc = f.__doc__.split(' ')
#			print doc
			if doc[0] != 'cmd':
				continue
			l = doc[1].split(',')
			for c in l:
				cmd_commands[c] = f
			cmd_helps.append(', '.join(l) + ' - ' + (' '.join(doc[2:])))
#		print vk.__dict__
		m.__dict__.update(cmd_imports.__dict__)
#		print vk.__dict__['cmd']

def unload_commands():
	global cmd_commands, cmd_modules, cmd_helps, cmd_imports
	cmd_commands = {}
	cmd_helps = []
	for module in cmd_modules:
		for d in cmd_imports.__dict__:
			if d in module.__dict__:
				module.__dict__.pop(d)
		del module
	cmd_modules = []

def reload_commands():
	unload_commands()
	load_commands()

def handle_command(peer,cmd,text,msg):
	cmd = cmd.encode('utf-8')

	if cmd in cmd_commands:
		cmd_commands[cmd](peer,text,msg)
