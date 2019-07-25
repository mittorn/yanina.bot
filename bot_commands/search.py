# coding:utf-8
def video(p,t,m):
	"cmd видео,видосы Поиск видео"
	res = vkpage.video.search(adult=1,q=t,count=10)
	attachments = ','.join([ 'video'+str(i.owner_id)+'_'+str(i.id) for i in res.items])
	vk_send(p,'Видео по вашему запросу',attachments)
	
def film(p,t,m):
	"cmd фильмы,кино Поиск фильмов"
	res = vkpage.video.search(adult=1,q=t,count=10,filters='long')
	attachments = ','.join([ 'video'+str(i.owner_id)+'_'+str(i.id) for i in res.items])
	vk_send(p,'Фильмы по вашему запросу',attachments)

def pron(p,t,m):
	"cmd порно,порево,порище Поиск порно"
	res1 = vkpage.video.search(adult=1,q=t,count=200,filters='mp4')
	res2 = vkpage.video.search(adult=0,q=t,count=200,filters='mp4')
	list1 = [ 'video'+str(i.owner_id)+'_'+str(i.id) for i in res1.items]
	list2 = [ 'video'+str(i.owner_id)+'_'+str(i.id) for i in res2.items]
	list3 = []
	for i in list1:
		if not i in list2:list3.append(i)

	vk_send(p,'Дрочите на здоровье',','.join(list3))

def photo(p,t,m):
	"cmd фото Поиск фото (не ожидайте релевантных результатов)"
	res = vkpage.photos.search(q=t,count=10)
	attachments = ','.join([ 'photo'+str(i.owner_id)+'_'+str(i.id) for i in res.items])
	vk_send(p,'Фото по вашему запросу',attachments)

def docs(p,t,m):
	"cmd доки Поиск документов"
	res = vkpage.docs.search(q=t,count=10)
	attachments = ','.join([ 'doc'+str(i.owner_id)+'_'+str(i.id) for i in res.items])
	vk_send(p,'Доки по вашему запросу',attachments)

def music(p,t,m):
	"cmd музыка Поиск музыки"
	res1 = vkaudio.audio.search(q=t,count=10,sort=2)
	res2 = vkaudio.audio.search(q=t,count=10)
	attachments1 = [ 'audio'+str(i.owner_id)+'_'+str(i.id) for i in res1.items]
	attachments2 = [ 'audio'+str(i.owner_id)+'_'+str(i.id) for i in res2.items]
	for a in attachments2:
		if not a in attachments1:
			attachments1.append(a)
	vk_send(p,'Музыка по вашему запросу',','.join(attachments1))

def gif(p,t,m):
	"cmd гиф,гифки,gif Поиск гифок"
	res = vkpage.docs.search(q=t +' ' +'.gif',count=200)
#	print(json.dumps(res,ensure_ascii=False))
	attachments = ','.join([ 'doc'+str(i.owner_id)+'_'+str(i.id) for i in res.items if i.ext == 'gif'][0:10])
	vk_send(p,'Гифки по вашему запросу',attachments)
