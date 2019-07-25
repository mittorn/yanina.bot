#-*- coding: utf-8 -*-
import datetime
def format_weather(city):
	weather = DictWrap(requests.get('http://api.openweathermap.org/data/2.5/weather', params={'lang':'ru', 'units': 'metric', 'APPID': 'ef23e5397af13d705cfb244b33d04561', 'q':city}).json())
	try:
		msg=""
		msg+="Погода в " + str(weather.sys.country) + "/" + weather.name + ":\n"
		msg+='&#8195;•Температура: ' + str(weather.main.temp) + '°C\n'
		#msg+='&#8195;&#8195;Максимальная температура: ' + str(weather["main"]["temp_max"]) + '°C\n'
		#msg+='&#8195;&#8195;Минимальная температура: ' + str(weather["main"]["temp_min"]) + '°C\n'
		msg+='&#8195;•Скорость ветра: ' + str(weather.wind.speed) + ' м/с\n'
		msg+='&#8195;•Влажность: ' + str(weather.main.humidity) + '%\n'
		msg+='&#8195;•Состояние: ' + str(weather.weather[0].description) + "\n"
		msg+='&#8195;•Давление: ' + ('%0.2f' % (float(weather.main.pressure)/1000*750.06))+"\n"
		msg+='Время обновления: ' + datetime.datetime.fromtimestamp(weather["dt"]).strftime('%I:%M%p');
		return msg
	except AttributeError:
		return None
def translit(x):
	symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
           u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")

	tr = {ord(a):ord(b) for a, b in zip(*symbols)}

# for Python 2.*:
# tr = dict( [ (ord(a), ord(b)) for (a, b) in zip(*symbols) ] )

	return tounicode(x).translate(tr)  # looks good

def weather(p,t,m):
	"cmd погода Погода по OWM"
	msg = format_weather(t)
	if msg == None:
		msg = format_weather(translit(t))
	if msg == None:
		vk_send(p,'Я не нашла населённый пункт '+t)
		return
	vk_send(p,msg)
		#apisay('Если город не в РФ, пиши английское название',toho,'')
