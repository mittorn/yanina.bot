# coding: utf-8
from module_imports import *
import threading
import re

try:
	from urllib import unquote
except Exception:
	from urllib.parse import unquote

import requests
import traceback
import time
HEADERS_GOOGLE = {'User-Agent':'LG8700/1.0 UP.Browser/6.2.3.9 (GUI) MMP/2.0'}
HEADERS_YANDEX_SMART ={'User-Agent': 'Opera/9.80 (Android; Opera Mini/36.2.2254/119.132; U; id) Presto/2.12.423 Version/12.16'}
HEADERS_YANDEX_TOUCH ={'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4=7.1.2; en-us) AppleWebKit/633.1 (KHTML, like Gecko) Version/5.0 UCBrowser/12.7.0.398 U3/0.8.0 Mobile Safari/633.1'}
types_img = ('jpg', 'bmp', 'png', 'jpeg', 'x-ms-bmp')
types_doc = ('gif',)
match_gtag = re.compile(r'<a class="image" href="([^"]*)"')
match_gurl = re.compile(r'imgurl=(.*?)&imgrefurl')
match_type = re.compile(r'image/(.*)')
match_yurl = re.compile(r'img_url=([^&]*)&')
match_ytag = re.compile(r'<a class="serp-item" href="([^"]*)"')
match_ydata= re.compile(r" data-bem='([^']*)' ")
match_ydvid= re.compile(r' data-video="([^"]*)" ')
match_ypic = re.compile(r' href="\/images\/search\?text\=([^"]*)">')
match_ycaptcha_key = re.compile(r'<input class="form__key" type="hidden" name="key" value="([^"]*)"')
match_ycaptcha_retpath = re.compile(r'<input class="form__retpath" type="hidden" name="retpath" value="([^"]*)"')
match_ycaptcha_src = re.compile(r'<img class="image form__image" src="([^"]*)"')
ycaptchas = {}

@cmd('як')
def ysolve(p,t,m):
	if not p in ycaptchas:
		return
	r = ycaptchas[p]
	r.update({'rep':t})
	ysearch(p,tostr(requests.get('https://yandex.ru/checkcaptcha',r, headers=HEADERS_YANDEX_SMART).text))
	
def ycaptcha(p,page):
	ycaptchas[p] = {'key':match_ycaptcha_key.findall(page)[0],'retpath':match_ycaptcha_retpath.findall(page)[0].replace('&amp;','&')}
	server_img = vkgroup.photos.getMessagesUploadServer(peer_id=hybrid[p])
	f = VkUploader(server_img.upload_url,'photo','photo.png','image/png')
	r = requests.get(match_ycaptcha_src.findall(page)[0],stream=True,headers=HEADERS_YANDEX_SMART)
	for chunk in r.iter_content(chunk_size=1000):
		f.write(chunk)
	rr = vkgroup.photos.saveMessagesPhoto(f.finish())
	vk_send(p,'Введите "Ян як (текст капчи)','photo'+str(rr[0].owner_id)+'_'+str(rr[0].id))
			
	
@cmd('яндекс', 'тындекс')
def yadv_main(p,t,m):
	'поиск в тындексе с описанием'
	page = tostr(requests.get('https://yandex.ru/images/touch/search',{'text':t,'rpt':'image_smart','p':0},headers=HEADERS_YANDEX_TOUCH).text)
	yadv(p,page)

def get_single_photo(m):
	w = 0
	url = None
	try:
		ph = m.attachments[0].photo
	except Exception:
		ph = m.fwd_messages[0].attachments[0].photo
	for s in ph.sizes:
		if s.width > w:
			w = s.width
			url = s.url
	return url

@cmd('что')
def ypic(p,t,m):
	'распознаванте картинки через яндекс'
	page = tostr(requests.get('https://yandex.ru/images/search?url='+get_single_photo(m)+'&rpt=imageview').text)
	
	#f=open('ya.txt','wb')
	#f.write(page)
	#f.close()

	r = match_ypic.findall(page)
	vk_send(p,'Возможно это:\n' + ('\n'.join(['* '+unquote(t) for t in r])))

@cmd('чоита')
def yadv_pic(p,t,m):
	'поиск в тындексе по картинке'
	page = requests.get('https://yandex.ru/images/touch/search',{'text':'','rpt':'imagelike','url':get_single_photo(m)},headers=HEADERS_YANDEX_TOUCH).text.encode('utf-8')
	yadv(p,page)

def yadv(p,page):
	#f=open('ya.txt','wb')
	#f.write(page)
	#f.close()
	#print page
	images=[]
	ydata=match_ydata.findall(page)
	if len(ydata) == 0:
		ycaptcha(p,page)
		return
	#vk_send(p,str(ydata)[0:4000])
	serp = []
	for d in ydata:
		try:
			j = json.loads(d.replace('&amp;','&'))
			if 'serp-item' in j:
				url = j['serp-item']['preview'][0]['origin']['url']
				title = None
				try:
					title = tostr(j['serp-item']['snippet']['title'])
				except Exception:
					pass
				images.append((url,title))
		except Exception:
			continue
	#vk_send(p,str(images)[0:4000])
	groupupload(p,images,'Результаты поиска изображений в Yandex:')

@cmd('яв', 'явидео')
def yvid(p,t,m):
	'видео со внешних ресурсов из тындекса'
	page = tostr(requests.get('https://yandex.ru/video/touch/search',{'text':t,'p':0},headers=HEADERS_YANDEX_TOUCH).text)
	f=open('ya.txt','wb')
	f.write(page)
	f.close()
	#print page
	images=[]
	ydata=match_ydvid.findall(page)
	if len(ydata) == 0:
		ycaptcha(p,page)
		return
	#vk_send(p,str(ydata)[0:4000])
	videos = []
	for d in ydata:
		try:
			j = json.loads(d.replace('&amp;','&').replace('&quot;','"'))
			videos.append(j['url'])
		except Exception as e:
			print e 
	#vk_send(p,str(videos)[0:4000])
	attachments = []
	for v in videos:
		try:
			f = vkpage.video.save(is_private=1,link=v)
			time.sleep(1)
			t = requests.get(f.upload_url)
			print t.text
			while 'Too much requests' in tostr(t.text):
				time.sleep(5)
				t = requests.get(f.upload_url)
			if not 'response' in t.json():
				print v
				continue
			attachments.append('video'+str(f.owner_id)+'_'+str(f.video_id)+'_'+f.access_key)
			if len(attachments) > 10:
				break
		except Exception as e:
			print e
	vk_send(p,'Видео из поиска яндекса',','.join(attachments))

@cmd('я', 'ты')
def ysearch(p,t,m):
	'поиск в тындексе'
	page = tostr(requests.get('https://yandex.ru/images/smart/search',{'text':t,'rpt':'image_smart','p':0},headers=HEADERS_YANDEX_SMART).text)
	images=[]
	r = match_ytag.findall(page)
	if len(r) == 0:
		ycaptcha(p,page)
		return
	for a in r:
		url=a.replace('&amp;','&')
		f=match_yurl.findall(url)
		try:
			images.append((unquote(f[0]),None))
		except Exception:
			continue
	#vk_send(p,str(images))
	groupupload(p,images, 'Картинки из яндекса')

@cmd('g', 'г', 'гы')
def gsearch(p,t,m):
	'поиск в кукле'
	page = tostr(requests.get('https://www.google.by/search',{'q':t,'source':'lnms','tbm':'isch'},headers=HEADERS_GOOGLE).text)

	r = match_gtag.findall(page)
	#vk_send(p,str(r)[0:1000])
	
	images=[]
	for a in r:
		url=a.replace('&amp;','&')
		f=match_gurl.findall(url)
		try:
			images.append((unquote(f[0]),None))
		except Exception as e:
			print(e)
			continue
	groupupload(p,images, 'Картинки из злого гуголя')

def groupupload(p,images,title = ''):
	server_img = vkgroup.photos.getMessagesUploadServer(peer_id=hybrid[p])
	server_doc = vkgroup.docs.getMessagesUploadServer(peer_id=hybrid[p])
	attachments = []
	threads = []
	isDone = [False]
	text = [title]
	def done():
		if isDone[0]:
			return
		isDone[0] = True
		vk_send(p,text,','.join(attachments)),
		
	def newthread():
		if len(images) > 0 and len(attachments) < 10 and not isDone[0]:
			t =threading.Thread(target=imgthread,args=(images.pop(),))
			t.start()
			threads.append(t)
	def imgthread(img):
		r = None
		try:
			r = requests.get(img[0],verify=False,stream=True,timeout=5)
			imgtype = match_type.findall(r.headers['Content-Type'])[0]
			doc = False
			if imgtype in types_doc:
				doc = True
				f = VkUploader(server_doc.upload_url,'file','file.gif','image/'+imgtype)
			elif imgtype in types_img:
				f = VkUploader(server_img.upload_url,'photo','photo.'+imgtype,'image/'+imgtype)
			else: raise Exception()
			for chunk in r.iter_content(chunk_size=1000):
				f.write(chunk)
				if isDone[0]: raise Exception()
			vkfile = f.finish()
			if doc:
				#print vkfile
				rr = vkgroup.docs.save(vkfile)
				#print rr
				attachments.append('doc'+str(rr.doc.owner_id)+'_'+str(rr.doc.id))
			else:
				rr = vkgroup.photos.saveMessagesPhoto(vkfile)
				attachments.append('photo'+str(rr[0].owner_id)+'_'+str(rr[0].id))
			if img[1]:
				text[0] = text[0] + '\n' + str(len(attachments))+'. ' +img[1]
		except Exception as e:
			#print(traceback.print_exc(e))
			newthread()
			
		if len(attachments) == 10:done()
		if r:r.close()
		threads.remove(threading.current_thread())
		if len(threads) == 0:done()
	for i in range(10):
		newthread()
	time.sleep(5)
	if len(threads) == 0:
		done()
	else:
		time.sleep(15)
		done()

