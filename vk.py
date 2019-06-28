from utils import *
import requests
import time
lp_modes = aenum('LP_PAGE','LP_GROUP')
call_modes = aenum('CALL_NORMAL', 'CALL_AUDIO' ,'CALL_GROUP', 'CALL_BROWSER')
api_versions = { CALL_NORMAL : '5.95', CALL_AUDIO : '5.71', CALL_GROUP : '5.95' }
api_tokens = {}
config = {}

def vk_call(mode,method,specparam, ignore = False):
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
		result = requests.post('https://api.vk.com/method/%s'%method, data=param, headers = {'User-Agent':'VKAndroidApp/4.38-816 (Android 6.0; SDK 23; x86; Google Nexus 5X; ru)'}).json()
		if not 'response' in result:
			raise Exception(result['error']['error_msg'])
		return result['response']
	except Exception as e:
		if not ignore:
			raise e

def load_config():
	global config
	newconfig = load_json('vk')
	config.update(newconfig)
	api_tokens[CALL_NORMAL] = config['token_normal']
	api_tokens[CALL_AUDIO] = config['token_audio']
	api_tokens[CALL_GROUP] = config['token_group']





import httplib, urlparse

LIMIT = '----------lImIt_of_THE_fIle_eW_$'
class VkUploader:
	def __init__(self,url,name,fname,mime):
		parsed = urlparse.urlparse(url)
		self.con = httplib.HTTPSConnection(parsed.netloc)
		self.con.putrequest('POST', '%s?%s' % (parsed.path, parsed.query)) #, headers={'Host': parsed.netloc})
		self.con.putheader('content-type', 'multipart/form-data; boundary=%s' % LIMIT)
		s = ''
		s +=('--'+LIMIT+'\r\n')
		s +=('Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (name, fname))
		s +=('Content-Type: %s\r\n\r\n' % mime)
		self.con.putheader('Transfer-Encoding', 'chunked')
		self.con.endheaders()
		self.write(s)
		del s,parsed

	def write(self,data):
		if len(data):
			self.con.send(str(hex(len(data)))[2:]+'\r\n')
			self.con.send(data)
			self.con.send('\r\n')
	def finish(self):
		self.write('\r\n--'+LIMIT+'--\r\n\r\n')
		self.con.send('0\r\n\r\n')
		s = json.loads(self.con.getresponse().read())
		del self.con
		return s


load_config()