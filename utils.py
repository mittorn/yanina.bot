try:
	import cPickle as pickle
except Exception:
	import pickle
import json
import inspect
import sys
import os
import threading
# shitty json does not work with utf-8
def unicodeWrap(x):
	if isinstance(x,dict):
		return {key : unicodeWrap(x[key]) for key in x}
	elif isinstance(x,list):
		return [unicodeWrap(l) for l in x]
	return tounicode(x)

def D(x = None, **kw):
	if x == None:
		x = kw
	if isinstance(x,dict):
		return DictWrap(x)
	elif isinstance(x,list):
		return [D(l) for l in x]
	return tostr(x)

class DictWrap:
	"this wraps dict into object-like structure (dict.child1.child2)"
	def __init__(self,d):
		if not isinstance(d,dict):
			t = "dictwrap from " + str(d) + " " +str(type(d))
			print(t)
			raise Exception(t)
		self.__dict__['_dict'] = d

	def __getattr__(self,name):
		# shortcut for json
		if name == '_json':
			return json.dumps(unicodeWrap(self._dict), ensure_ascii = False)
		try:
			return D(self._dict[name])
		except KeyError:
			# if d.attr
			return None
			# if attr in d and d.attr
			# raise AttributeError(name)
	def __getitem__(self,name):
		if isinstance(name,dict):
			print name
		if isinstance(name, int):
			return self._dict.keys()[name]
		return D(self._dict[name])
	def __setitem__(self,x,y):
		return self._dict.__setitem__(x,todict(y))
	def __setattr__(self,x,y):
		return self._dict.__setitem__(x,todict(y))
	def __repr__(self):
		return self._dict.__repr__()
	def __str__(self):
		return self._dict.__str__()
	def __dir__(self):
		return self._dict.__dir__()
	def __contains__(self,k):
		return self._dict.__contains__(k)
	def __iter__(self):
		for key in self._dict:
			yield (key, self._dict[key])

def todict(x):
	if isinstance(x,DictWrap):
		return x._dict
	return x

def aenum(*s):
	"C-style enum (automatic counting)"
	module = inspect.stack()[1][0].f_globals
	i = 0
	reverse = {}
	for e in s:
		module[e] = i
		reverse[i] = e
		i += 1
	return reverse

def nenum(**s):
	"C-style enum"
	module = inspect.stack()[1][0].f_globals
	reverse = {}
	for e in s:
		module[e] = s[e]
		reverse[s[e]] = e
	return reverse

def tostr(x):
	if sys.version_info[0] == 2 and isinstance(x,unicode):
		return x.encode('utf-8')
	return x
def tounicode(x):
	if sys.version_info[0] == 2 and isinstance(x,str):
		return x.decode('utf-8')
	return x

file_locks = {}

def flock(name):
	if not name in file_locks:
		file_locks[name] = threading.Lock()
	l = file_locks[name]
	l.acquire()
	return l

def save_object(name, obj):
	try:
		fname = 'data/'+name+'.pkl'
		l = flock(name)
		f = open(fname + '.new', 'wb')
		pickle.dump(obj, f, 2)
		f.close()
		os.remove(fname)
		os.rename(fname + '.new',fname)
	finally:
		l.release()

def load_object(name):
	try:
		fname = 'data/'+name+'.pkl'
		l = flock(fname)
		f = open(fname,'rb')
		obj = pickle.load(f)
		f.close()
	finally:
		l.release()
	return obj

def load_json(name):
	try:
		fname = 'config/'+name+'.json'
		l = flock(fname)
		f = open(fname,'r')
	
		obj = json.load(f)
		f.close()
	finally:
		l.release()
	return DictWrap(obj)

def save_json(name, obj):
	try:
		if isinstance(obj,DictWrap):
			obj = obj._dict
		fname = 'config/'+name+'.json'
		l = flock(fname)
		f = open(fname + '.new', 'w')
		json.dump(obj, f, 2)
		f.close()
		os.remove(fname)
		os.rename(fname+'.new', fname)
	finally:
		l.release()