from utils import *
import requests
import time
lp_modes = aenum('LP_PAGE','LP_GROUP')
call_modes = aenum('CALL_NORMAL', 'CALL_AUDIO' ,'CALL_GROUP', 'CALL_BROWSER')
api_versions = { CALL_NORMAL : '5.95', CALL_AUDIO : '5.71', CALL_GROUP : '5.95' }
api_tokens = {}
config = {}

class VkException(Exception):
	def __init__(self, code, message):
		self.code = code
		Exception.__init__(self,message)

class NoSuchMethodException(VkException):
	"for vkwrap"
	pass

def vk_call(mode,method,specparam, ignore = False):
	"make request, check for errors, return response"

	class NeverMatch(Exception):
		pass

	try:
		param = {}
		if mode == CALL_BROWSER:
			raise Exception('Not implemented yet')
		if mode in api_versions:
			param['v'] = api_versions[mode]
		if mode in api_tokens:
			param['access_token'] = api_tokens[mode]
		param.update(specparam)
		headers = {}
		if mode == CALL_AUDIO:
			headers['User-Agent'] = 'VKAndroidApp/4.38-816 (Android 6.0; SDK 23; x86; Google Nexus 5X; ru)'
		result = requests.post('https://api.vk.com/method/%s'%method, data=param, headers = headers)
		result.raise_for_status()
		json = result.json()
		if not 'response' in json:
			code = json['error']['error_code']
			if code == 3: 
				raise NoSuchMethodException(json['error']['error_msg'])
			if code in (6,9):
				# cool-down this thread
				time.sleep(10)
				r = vk_call(mode,method,specparam, ignore)
				time.sleep(10)
				return r
			if code == 3: 
				raise NoSuchMethodException(code,json['error']['error_msg'])
			raise VkException(code,json['error']['error_msg'])
		return json['response']
	except (Exception if ignore else NeverMatch) as e:
		pass

def load_config():
	global config
	newconfig = load_json('vk')
	config.update(newconfig)
	api_tokens[CALL_NORMAL] = config['token_normal']
	api_tokens[CALL_AUDIO] = config['token_audio']
	api_tokens[CALL_GROUP] = config['token_group']




try:
	import httplib
except Exception:
	import http.client as httplib
LIMIT = '----------lImIt_of_THE_fIle_eW_$'

class VkUploader:
	"file-like uploader"
	def __init__(self,url,name,fname,mime):
		server = url.split('/')[2]
		
		self.con = httplib.HTTPSConnection(server)
		self.con.putrequest('POST', url[8+len(server):])
		self.con.putheader('content-type', 'multipart/form-data; boundary=%s' % LIMIT)
		s = ''
		s +=('--'+LIMIT+'\r\n')
		s +=('Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (name, fname))
		s +=('Content-Type: %s\r\n\r\n' % mime)
		self.con.putheader('Transfer-Encoding', 'chunked')
		self.con.endheaders()
		self.write(s.encode('ascii'))
		del s

	def write(self,data):
		if len(data):
			self.con.send(bytes((str(hex(len(data)))[2:]+'\r\n').encode('ascii')))
			self.con.send(bytes(data))
			self.con.send(b'\r\n')
	def finish(self):
		self.write(b'\r\n--'+LIMIT.encode('ascii')+b'--\r\n\r\n')
		self.con.send(b'0\r\n\r\n')
		s = json.loads(self.con.getresponse().read())
		del self.con
		return s


class DictWrap:
	"this wraps dict into object-like structure (dict.child1.child2)"
	def __init__(self,d):
		self._dict = d

	def _wrap(self,i):
		"traverse children if needed"
		if isinstance(i, list):
			return [self._wrap(l) for l in i]
		if isinstance(i, dict):
			return DictWrap(i)
		return i

	def __getattr__(self,name):
		# shortcut for json
		if name == '_json':
			return json.dumps(self._dict, ensure_ascii = False)
		try:
			return self._wrap(self._dict[name])
		except KeyError:
			raise AttributeError(name)
	def __getitem__(self,name):
		if isinstance(name, int):
			return self._dict.keys()[name]
		return self._dict[name]
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

class VKWrap:
	"wrap vk api into object-like structure (vkwrap.docs.search(q='',count=1).items[0].owner_id)"
	class _submethod:
		def __init__(self,mode, name):
			self._mode = mode
			self._name = name
		def __getattr__(self,name):
			def call(**args):
				try:
					return DictWrap(vk_call(self._mode, self._name +'.'+ name, args))
				except NoSuchMethodException:
					raise AttributeError(name)
			return call
	def __init__(self,mode):
		self._mode = mode
	def __getattr__(self,name):
		return self._submethod(self._mode, name)

vkpage = VKWrap(CALL_NORMAL)
vkaudio = VKWrap(CALL_AUDIO)
vkgroup = VKWrap(CALL_GROUP)

load_config()

