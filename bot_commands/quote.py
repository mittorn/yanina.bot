# coding:utf-8
import random

def init():
	global face, jpeg
	import freetype
	from tjpgwrap import TurboJPEG
	jpeg = TurboJPEG('/usr/lib/libturbojpeg.so')
	face = freetype.Face("font.ttf")
	face.set_char_size( 1000 )

jpeg = None
face = None
space_size = 10
yspace = 10
cspace = 2
def create_image(w,h):
	return [[0]*w*3 for i in range(h)]

def render_text(image, x, y, text, width, height, r, g, b):
	lstart = x
	hmax = 0
	for c in text:
		if c == ' ':
			x += space_size
			continue
		face.load_char(c)
		bitmap = face.glyph.bitmap
		w =	bitmap.width
		if x + w > width or c == '\n':
			x = lstart
			y += hmax + yspace
			hmax = 0
		if w == 0:
			continue
		h = len(bitmap.buffer)/w
		if h > hmax: hmax = h
		try:
			for i in range(h):
				for j in range(w):
					l = int(bitmap.buffer[i*w+j])
					if l:
						image[y - face.glyph.bitmap_top+i][(x+j)*3] = int(r * l)
						image[y - face.glyph.bitmap_top+i][(x+j)*3+1] = int(g * l)
						image[y - face.glyph.bitmap_top+i][(x+j)*3+2] = int(b * l)
						
		except Exception:
			pass
		x += w + cspace
	return y + hmax
def compress_image(img,w,h,f):
	from png import Writer
	w = Writer(w, h, greyscale = False)
	w.write(f,img)
	
def render_jpg(img,x,y,jpg):
	data, w, h = jpeg.decode(jpg)

	for i in range(h):
		for j in range(w*3):
			img[y+i][x+j] = ord(data[i*w*3+j])
	del data

def quote(p,t,m):
	"cmd цытата,цитата Всратая цытата"
	if not jpeg:init()

	server = vk_call(CALL_GROUP,'photos.getMessagesUploadServer',{'peer_id':hybrid[p]})
	attachments = []

	for fwd in m['fwd_messages']:
		w = 500 + len(fwd['text'])/7
		img = create_image(w,1024)
		if fwd['from_id'] > 0:
			u = vk_call(CALL_GROUP,'users.get',{'user_ids':fwd['from_id'],'fields':'photo_100'})[0]
			name = u['first_name']+' '+u['last_name']
		else:
			u = vk_call(CALL_NORMAL,'groups.getById',{'group_ids':-fwd['from_id'],'fields':'photo_100'})[0]
			name = u['name']
		try:
			render_jpg(img, 30, 60, requests.get(u['photo_100']).content)
		except Exception:
			pass
		face.set_char_size( 1000 )
		y = render_text(img,120,50,fwd['text'],w-50,1024,1,1,1) + 50
		print u
		face.set_char_size( 1500 )
		y = render_text(img, w - 300, y,  name, w, 1024,random.uniform(0.4,1),random.uniform(0.4,1),random.uniform(0.4,1)) + 50
		if y > 1024: y = 1024
		f = VkUploader(server['upload_url'],'photo','photo.png','image/png')
		compress_image(img[0:y],w,y,f)
		for i in img:del i[:]
		del img[:]
		j = f.finish()

		print j
		rr = vk_call(CALL_GROUP,'photos.saveMessagesPhoto',j)
		del f
		attachments.append('photo'+str(rr[0]['owner_id'])+'_'+str(rr[0]['id']))
	vk_send(p,'',','.join(attachments)),
