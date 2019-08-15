# coding: utf-8
import os, sys, types
import imp
from utils import *
from vk import config
mod_commands = D()
loaded_modules = []
mod_cmdhelps = []
mod_imports = None
mod_instance = 0

def load_modules(p=0):
	global mod_instance, mod_imports
	print loaded_modules
	mod_instance += 1
	if not mod_imports:
		mod_imports = __import__('module_imports')

	for modname in filter(lambda x: x and x[-3:] == ".py", os.listdir("modules")):
		print modname
		try:
			module = imp.load_source('mod_'+str(mod_instance)+'_'+modname[0:-3],'modules/'+modname)
			loaded_modules.append(module)
		except Exception as e:
			print('Loading '+ modname + ': ' + str(e))

	for m in loaded_modules:
		try:
			d1 = {}
			d1.update(mod_imports.__dict__)
			d1.update(m.__dict__)
			m.__dict__.update(d1)
		except Exception as e:
			print(e)

def unload_modules():
	mod_commands._dict.clear()
	for module in loaded_modules:
		n = '' + module.__name__
		shit = []
		for d in module.__dict__:
			shit.append(d)
		for s in shit:
			module.__dict__.pop(s)
		del sys.modules[n]
		del module
		del shit[:]
	del loaded_modules[:]

def reload_modules(p=0):
	print 'b'
	try:
		unload_modules()
		print 'a'
	except Exception as e:
		print(e)
		mod_commands._dict.clear()
		del loaded_modules[:]
	print 'l'
	load_modules()
	print 'd'

def handle_command(peer,cmd,text,msg):
	if not cmd in mod_commands:
		return False
	c = mod_commands[cmd]
	if c.admin and not msg.from_id in config.owners:
		return False
	mod_commands[cmd].func(peer,text,msg)
	return True

def cmd(*names,**parms):
	def deco(func):
		ac = func.__code__.co_argcount
		if ac > 3: raise Exception('@cmd: bad function '+str(func))
		elif ac == 3:
			f = func
		else:
			def f(p,t,m):
				d = (p,t,m)[0:ac]
				func(*d)
	
		parms['func'] = f
		if func.__doc__:
			parms['help'] = func.__doc__
			mod_cmdhelps.append(', '.join(names) + ' - ' + func.__doc__)
		for name in names:
			mod_commands[name] = parms
		return f
			
	return deco