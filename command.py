# coding: utf-8
import os, sys, types
import imp
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
cmd_instance = 0

def load_commands():
	global cmd_modules, cmd_commands, cmd_helps, cmd_imports, cmd_instance
	cmd_instance += 1
	if not cmd_imports:
		cmd_imports = __import__('command_imports')
#	p = sys.path
#	sys.path = ['bot_commands/']
	for modname in filter(lambda x: x and x[-3:] == ".py", os.listdir("bot_commands")):
		module = imp.load_source('cmd_'+str(cmd_instance)+'_'+modname[0:-3],'bot_commands/'+modname)
#		reload(module)
#		del module
#		del sys.modules[modname[0:-3]]
#		del sys.modules[modname[0:-3]]
#		try:
#			reload(module)
#		except Exception:
#			pass
#		module = __import__(modname[0:-3])
		cmd_modules.append(module)
#	sys.path = p

	for m in cmd_modules:
		print m.__name__, m
		v = m.__dict__
		for d in v:
			f = v[d]
			if not type(f) is types.FunctionType:
				continue
			if not hasattr(f,'__doc__'):
				continue
			if not f.__doc__:
				continue
			doc = f.__doc__.decode('utf-8').split(' ')
			print doc
			if doc[0] != 'cmd':
				continue
			l = doc[1].split(',')
			for c in l:
				cmd_commands[c] = f
			if len(doc) > 2:
				cmd_helps.append(', '.join(l) + ' - ' + (' '.join(doc[2:])))
#		print vk.__dict__
		d1 = {}
		d1.update(cmd_imports.__dict__)
		d1.update(m.__dict__)
		m.__dict__.update(d1)
#		print vk.__dict__['cmd']

def unload_commands():
	global cmd_commands, cmd_modules, cmd_helps, cmd_imports
	cmd_commands.clear()
	del cmd_helps[:]
#	p = sys.path
#	sys.path = ['bot_commands/']
	for module in cmd_modules:
#		for d in cmd_imports.__dict__:
#			if d in module.__dict__:
#				module.__dict__.pop(d)
#		reload(module)
		n = '' + module.__name__
		shit = []
		for d in module.__dict__:
			shit.append(d)
		for s in shit:
			module.__dict__.pop(s)
		del sys.modules[n]
		del module
#		sys.modules.pop(n)
	del cmd_modules[:]
#	sys_path = p
#	cmd_modules = []

def reload_commands():
	unload_commands()
	load_commands()

def handle_command(peer,cmd,text,msg):
	cmd = cmd

	if cmd in cmd_commands:
		cmd_commands[cmd](peer,text,msg)
