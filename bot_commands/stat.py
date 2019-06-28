# coding:utf-8
import psutil, time
from datetime import timedelta

start_time = time.time()
def stat(p,t,m):
	"cmd стат Статистика крекера"
	text = u'[ Статистика ]<br>Система:<br>&#8195;Процессоры:<br>'
	for idx, cpu in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
		text += u'&#8195;&#8195;Процессор №'+str(idx+1)+': '+str(cpu)+'%<br>'
	mem = psutil.virtual_memory()
	MB = 1024 * 1024
	text += u'&#8195;ОЗУ:<br>&#8195;&#8195;Всего: '+str(int(mem.total / MB))+u'MB<br>&#8195;&#8195;Использовано: '+str(int((mem.total - mem.available) / MB))+u'MB<br>&#8195;&#8195;Свободно: '+str(int(mem.available / MB))+u'MB<br>&#8195;&#8195;Использовано ботом: '+str(int(psutil.Process().memory_info().vms / MB))+u'MB<br>&#8195;'
	end_time = time.time()
	text += u'Бот:<br>&#8195;&#8195;Время работы: '+str(timedelta(seconds=end_time - start_time))
	text += u'\nВерсия python:\n'+str(sys.version)
	vk_send(p,text)
