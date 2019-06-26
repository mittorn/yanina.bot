# coding: utf-8
import os, sys, types
import imp
from vk import config
cmd_commands = {}
cmd_admcommands = {}
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
	global cmd_modules, cmd_commands, cmd_admcommands, cmd_helps, cmd_imports, cmd_instance
	cmd_instance += 1
	if not cmd_imports:
		cmd_imports = __import__('command_imports')

	for modname in filter(lambda x: x and x[-3:] == ".py", os.listdir("bot_commands")):
		try:
			module = imp.load_source('cmd_'+str(cmd_instance)+'_'+modname[0:-3],'bot_commands/'+modname)
			cmd_modules.append(module)
		except Exception as e:
			print('Loading '+ modname + ': ' + str(e))

	for m in cmd_modules:
		try:
			v = m.__dict__
			for d in v:
				f = v[d]
				if not type(f) is types.FunctionType:continue
				if not f.__doc__:continue
				doc = f.__doc__.decode('utf-8').split(' ')
				if doc[0] =='cmd':
					l = doc[1].split(',')
					for c in l:
						cmd_commands[c] = f
					if len(doc) > 2:
						cmd_helps.append(', '.join(l) + ' - ' + (' '.join(doc[2:])))
				if doc[0] == 'admin':
					l = doc[1].split(',')
					for c in l:
						cmd_admcommands[c] = f

			d1 = {}
			d1.update(cmd_imports.__dict__)
			d1.update(m.__dict__)
			m.__dict__.update(d1)
		except Exception:
			print(e)

def unload_commands():
#	global cmd_commands, cmd_modules, cmd_helps, cmd_imports
	cmd_commands.clear()
	cmd_admcommands.clear()
	del cmd_helps[:]
	for module in cmd_modules:
		n = '' + module.__name__
		shit = []
		for d in module.__dict__:
			shit.append(d)
		for s in shit:
			module.__dict__.pop(s)
		del sys.modules[n]
		del module
	del cmd_modules[:]

def reload_commands():
	try:
		unload_commands()
	except Exception:
		cmd_commands.clear()
		cmd_admcommands.clear()
		del cmd_helps[:]
		del cmd_modules[:]

	load_commands()

def handle_command(peer,cmd,text,msg):
	if msg['from_id'] in config['owners'] and cmd in cmd_admcommands:
		cmd_admcommands[cmd](peer,text,msg)

	if cmd in cmd_commands:
		cmd_commands[cmd](peer,text,msg)
