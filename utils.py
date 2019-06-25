import cPickle as pickle
import json
import inspect
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


def save_object(name, obj):
	f = open('data/'+name+'.pkl', 'wb')
	pickle.dump(obj, f, 2)
	f.close()

def load_object(name):
	f = open('data/'+name+'.pkl','rb')
	obj = pickle.load(f)
	f.close()
	return obj

def load_json(name):
	f = open('config/'+name+'.json','r')
	obj = json.load(f)
	f.close()
	return obj

def save_json(name, obj):
	f = open('config/'+name+'.json', 'w')
	json.dump(obj, f, 2)
	f.close()