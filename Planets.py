from tkinter import *
from math import *

#Повернуть точку х, у относительно x0, y0
def point_rotate(x0, y0, x, y, dalfa):
	r = sqrt((x-x0)*(x-x0)+(y-y0)*(y-y0))
	alfa = atan2(y-y0, x-x0)
	beta = alfa + dalfa
	x = x0 + r*cos(beta)
	y = y0 + r*sin(beta)
	return x, y

#Повернуть круг "Планету"
def oval_rotate(oval_id, x0, y0, dalfa):
	x1, y1, x2, y2 = canv.coords(oval_id)
	centr_x, centr_y = (x1+x2)/2, (y1+y2)/2
	delta_x, delta_y = abs(x1-x2)/2, abs(y1-y2)/2
	centr_x, centr_y = point_rotate(x0, y0, centr_x, centr_y, dalfa)
	x1, y1 = centr_x - delta_x, centr_y - delta_y
	x2, y2 = centr_x + delta_x, centr_y + delta_y
	canv.coords(oval_id, x1, y1, x2, y2)

#Повернуть линию или полигон с произвольным количеством вершин ***
def obj_rotate(obj_id, x0, y0, dalfa):
	obj_crds = canv.coords(obj_id)
	for coord_num in range( len(obj_crds)//2):
		x, y = obj_crds[coord_num*2], obj_crds[coord_num*2 + 1]
		x, y = point_rotate(x0, y0, x, y, dalfa)
		obj_crds[coord_num*2] = x;   obj_crds[coord_num*2 + 1] = y
	canv.coords(obj_id, *obj_crds)     
	
#Общий класс графического обьекта (Планет)
class Planet:
	def __init__(self, form, center= [0,0], templ = [-1,-1, 1, 1], scale = 10,
		     fill_color = "white", bg_color = "black", line_width = 1,
		     beg_pos = [0,0], speed = 1, angle = 0,
		     path = [], path_center = [0,0]):
				 
		#Внутренние переменные
		self.form = form
		self.path = path
		self.angle = angle
		self.center = []
		self.center.append( center[0] + beg_pos[0] )
		self.center.append( center[1] + beg_pos[1] )
		self.path_center = []
		self.speed = speed
		self.path_center.append( path_center[0])
		self.path_center.append( path_center[1])
		self.node_num = 0
		
		#Масштабировать объект
		self.templ =[]
		for templ_num in range(len(templ)):
			center_num = templ_num % 2
			self.templ.append( self.center[center_num] + templ[templ_num]*scale ) 
			       
		#Создать графический объект 
		if form == "oval":
			self.obj = canv.create_oval( *self.templ, fill=fill_color)
			
	#Сдвинуть по заданному смещению 
	def shift(self, step_x, step_y ):
		canv.move( self.obj, step_x, step_y  )
		self.center[0] += step_x
		self.center[1] += step_y
		
	#Повернуть относительно произвольной точки 
	def rotate( self, delta_grad, x0, y0 ):
		delta_fi = pi*delta_grad/180

		if self.form == "oval":
			oval_rotate(self.obj, x0, y0, delta_fi)
		else:
			obj_rotate(self.obj, x0, y0, delta_fi)

		self.angle += delta_fi
		self.center[0], self.center[1] = point_rotate(x0, y0, self.center[0], self.center[1], delta_fi)

	#Переместить в заданную точку траектории без проверки
	def jump( self, node_num ):
		if self.path == []:  return
		self.node_num = node_num
		
		#Сместить главный центр
		node_x = self.path[ node_num ][0] + self.path_center[0]
		node_y = self.path[ node_num ][1] + self.path_center[1]
		old_x, old_y = self.center
				
		step_x = node_x - old_x
		step_y = node_y - old_y
		self.shift( step_x, step_y )
		
		if node_num == len(self.path)-1:  return
		
		next_x, next_y = self.path[ node_num + 1]
		next_x += self.path_center[0]
		next_y += self.path_center[1]

		new_angle = atan2( next_y - node_y, next_x - node_x )
		delta_grad = (new_angle - self.angle)*180/pi
		self.rotate( delta_grad, *self.center )
		
	#Сдвинуть по направлению движения 
	def move( self, cycle = 0):
		#Движение если нет траектории
		if self.path == []:
			step_x = self.speed*cos(self.angle)
			step_y = self.speed*sin(self.angle)
			self.shift( step_x, step_y )
			return
		#Движение если есть траектории
		node_num = self.node_num + self.speed
		if cycle == 0:
			if node_num < 0: node_num = 0
			elif node_num >= len(self.path): node_num = len(self.path) -1
		else:
			if node_num < 0: node_num += len(self.path)
			if node_num >= len(self.path):
				node_num = len(self.path)-1 if cycle==0 else node_num % len(self.path)
		#Выполнить перемещение
		if node_num != self.node_num:
			self.jump( node_num )
			
#Функции, формирующие меню информации 	
def mercury_menu():
	mercury_menu = Toplevel(root)
	mercury_menu.resizable(width = False, height = False)
	canv_1 = Canvas(mercury_menu, width=500, height=350, bg = 'black')
	canv_1.create_text(250,20,text = "Меркурий:", fill = "white", font =("Times",15))
	canv_1.create_text(200,50,text = "Орбитальные и физические характеристики:", fill = "white", font =("Times",15))
	canv_1.create_text(160,70,text = "Радиус орбиты = 2439,7 ± 1,0 км; ", fill = "white", font =("Times",15))
	canv_1.create_text(110,90,text = "Масса = 3.33×10²³ кг; ", fill = "white", font =("Times",15))
	canv_1.create_text(120,110,text = "Плотность = 5,43 г/см³; ", fill = "white", font =("Times",15))
	canv_1.create_text(145,130,text = "Период вращения = 58,65 сут; ", fill = "white", font =("Times",15))
	canv_1.create_text(143,150,text = "Период обращения — 88 сут; ", fill = "white", font =("Times",15))
	canv_1.create_text(110,170,text = "Наклон орбиты — 7°; ", fill = "white", font =("Times",15))
	canv_1.create_text(190,190,text = "Среднее расстояние от солнца - 0,39 а.е; ", fill = "white", font =("Times",15))
	canv_1.create_text(145,210,text = "Средняя температура - 67 °C ; ", fill = "white", font =("Times",15))
	canv_1.create_text(95,230,text = "Состав Атмосферы:", fill = "white", font =("Times",15))
	canv_1.create_text(95,250,text = "Кислород 42,0%:", fill = "white", font =("Times",15))
	canv_1.create_text(80,270,text = "Натрий 29,0%", fill = "white", font =("Times",15))
	canv_1.create_text(85,290,text = "Водород 22,0%", fill = "white", font =("Times",15))
	canv_1.create_text(63,310,text = "Гелий 6%", fill = "white", font =("Times",15))
	canv_1.create_text(95,330,text = "Калий 0,5 и д.р %", fill = "white", font =("Times",15))
	canv_1.pack()
def venera_menu():
	venera_menu = Toplevel(root)
	venera_menu.resizable(width = False, height = False)
	canv_2 = Canvas(venera_menu, width=500, height=350, bg = 'black')
	canv_2.create_text(250,20,text = "Венера:", fill = "white", font =("Times",15))
	canv_2.create_text(200,50,text = "Орбитальные и физические характеристики:", fill = "white", font =("Times",15))
	canv_2.create_text(138,70,text = "Радиус орбиты = 6051,8 км; ", fill = "white", font =("Times",15))
	canv_2.create_text(110,90,text = "Масса = 4.87×10²⁴ кг; ", fill = "white", font =("Times",15))
	canv_2.create_text(120,110,text = "Плотность = 5,24 г/см³; ", fill = "white", font =("Times",15))
	canv_2.create_text(140,130,text = "Период вращения = 243 сут; ", fill = "white", font =("Times",15))
	canv_2.create_text(158,150,text = "Период обращения — 224,7 сут; ", fill = "white", font =("Times",15))
	canv_2.create_text(120,170,text = "Наклон орбиты — 3,4°; ", fill = "white", font =("Times",15))
	canv_2.create_text(192,190,text = "Среднее расстояние от солнца - 0,72 а.е; ", fill = "white", font =("Times",15))
	canv_2.create_text(152,210,text = "Средняя температура - 463 °C ; ", fill = "white", font =("Times",15))
	canv_2.create_text(92,230,text = "Состав Атмосферы:", fill = "white", font =("Times",15))
	canv_2.create_text(125,250,text = "Углекислого газа 96,5 %:", fill = "white", font =("Times",15))
	canv_2.create_text(85,270,text = "Азот 3,5% и д.р ", fill = "white", font =("Times",15))
	canv_2.pack()
	
def earth_menu():
	earth_menu = Toplevel(root)
	earth_menu.resizable(width = False, height = False)
	canv_3 = Canvas(earth_menu, width=500, height=350, bg = 'black')
	canv_3.create_text(250,20,text = "Земля:", fill = "white", font =("Times",15))
	canv_3.create_text(200,50,text = "Орбитальные и физические характеристики:", fill = "white", font =("Times",15))
	canv_3.create_text(150,70,text = "Радиус орбиты = 149,6 млн км; ", fill = "white", font =("Times",15))
	canv_3.create_text(108,90,text = "Масса = 5,97×10²⁴ кг; ", fill = "white", font =("Times",15))
	canv_3.create_text(118,110,text = "Плотность = 5,52 г/см³; ", fill = "white", font =("Times",15))
	canv_3.create_text(185,130,text = "Период вращения = 23 ч. 26 мин. 4 сек; ", fill = "white", font =("Times",15))
	canv_3.create_text(155,150,text = "Период обращения — 365,3 сут; ", fill = "white", font =("Times",15))
	canv_3.create_text(128,170,text = "Наклон орбиты — 23,44°; ", fill = "white", font =("Times",15))
	canv_3.create_text(190,190,text = "Среднее расстояние от солнца - 1,00 а.е; ", fill = "white", font =("Times",15))
	canv_3.create_text(145,210,text = "Средняя температура - 14 °C ; ", fill = "white", font =("Times",15))
	canv_3.create_text(92,230,text = "Состав Атмосферы:", fill = "white", font =("Times",15))
	canv_3.create_text(88,250,text = "Кислород 21 %:", fill = "white", font =("Times",15))
	canv_3.create_text(85,270,text = "Азот 78% и д.р ", fill = "white", font =("Times",15))
	canv_3.pack()

def mars_menu():
	mars_menu = Toplevel(root)
	mars_menu.resizable(width = False, height = False)
	canv_4 = Canvas(mars_menu, width=500, height=350, bg = 'black')
	canv_4.create_text(250,20,text = "Марс:", fill = "white", font =("Times",15))
	canv_4.create_text(200,50,text = "Орбитальные и физические характеристики:", fill = "white", font =("Times",15))
	canv_4.create_text(130,70,text = "Радиус орбиты = 3390 км; ", fill = "white", font =("Times",15))
	canv_4.create_text(108,90,text = "Масса = 6.42×10²³ кг; ", fill = "white", font =("Times",15))
	canv_4.create_text(118,110,text = "Плотность = 3,93 г/см³; ", fill = "white", font =("Times",15))
	canv_4.create_text(156,130,text = "Период вращения = 24 ч 37 мин; ", fill = "white", font =("Times",15))
	canv_4.create_text(153,150,text = "Период обращения — 686,9 сут; ", fill = "white", font =("Times",15))
	canv_4.create_text(122,170,text = "Наклон орбиты — 1,85°; ", fill = "white", font =("Times",15))
	canv_4.create_text(190,190,text = "Среднее расстояние от солнца - 1,52 а.е; ", fill = "white", font =("Times",15))
	canv_4.create_text(155,210,text = "Средняя температура - -63,1 °C ; ", fill = "white", font =("Times",15))
	canv_4.create_text(92,230,text = "Состав Атмосферы:", fill = "white", font =("Times",15))
	canv_4.create_text(105,250,text = "Углекислый газ 95%:", fill = "white", font =("Times",15))
	canv_4.create_text(115,270,text = "Молекулярный газ 2,8%", fill = "white", font =("Times",15))
	canv_4.create_text(80,290,text = "Аргон 2% и д.р ", fill = "white", font =("Times",15))
	canv_4.pack()

def upiter_menu():
	upiter_menu = Toplevel(root)
	upiter_menu.resizable(width = False, height = False)
	canv_5 = Canvas(upiter_menu, width=500, height=350, bg = 'black')
	canv_5.create_text(250,20,text = "Юпитер:", fill = "white", font =("Times",15))
	canv_5.create_text(200,50,text = "Орбитальные и физические характеристики:", fill = "white", font =("Times",15))
	canv_5.create_text(155,70,text = "Радиус орбиты = 69911 ± 6 км; ", fill = "white", font =("Times",15))
	canv_5.create_text(108,90,text = "Масса = 1.9×10²⁷ кг; ", fill = "white", font =("Times",15))
	canv_5.create_text(128,110,text = "Плотность = 1330 кг/м3; ", fill = "white", font =("Times",15))
	canv_5.create_text(176,130,text = "Период вращения = 9 ч 55 мин 29 с; ", fill = "white", font =("Times",15))
	canv_5.create_text(165,150,text = "Период обращения — 11,86 года; ", fill = "white", font =("Times",15))
	canv_5.create_text(128,170,text = "Наклон орбиты — 1,30°; ", fill = "white", font =("Times",15))
	canv_5.create_text(195,190,text = "Среднее расстояние от солнца - 5,20 а.е; ", fill = "white", font =("Times",15))
	canv_5.create_text(160,210,text = "Средняя температура - -108  °C ; ", fill = "white", font =("Times",15))
	canv_5.create_text(92,230,text = "Состав Атмосферы:", fill = "white", font =("Times",15))
	canv_5.create_text(143,250,text = "Молекулярный водород 90%:", fill = "white", font =("Times",15))
	canv_5.create_text(95,270,text = "Гелий около 10%", fill = "white", font =("Times",15))
	canv_5.pack()

def saturn_menu():
	saturn_menu = Toplevel(root)
	saturn_menu.resizable(width = False, height = False)
	canv_6 = Canvas(saturn_menu, width=500, height=350, bg = 'black')
	canv_6.create_text(250,20,text = "Сатурн:", fill = "white", font =("Times",15))
	canv_6.create_text(200,50,text = "Орбитальные и физические характеристики:", fill = "white", font =("Times",15))
	canv_6.create_text(145,70,text = "Радиус орбиты =  60 300 км; ", fill = "white", font =("Times",15))
	canv_6.create_text(108,90,text = "Масса = 5.6×10²⁶ кг; ", fill = "white", font =("Times",15))
	canv_6.create_text(123,110,text = "Плотность = 690 кг/м3; ", fill = "white", font =("Times",15))
	canv_6.create_text(181,130,text = "Период вращения = 10 ч 40 мин 30 с; ", fill = "white", font =("Times",15))
	canv_6.create_text(165,150,text = "Период обращения — 29,46 года; ", fill = "white", font =("Times",15))
	canv_6.create_text(128,170,text = "Наклон орбиты — 2,50°; ", fill = "white", font =("Times",15))
	canv_6.create_text(195,190,text = "Среднее расстояние от солнца - 9,54 а.е; ", fill = "white", font =("Times",15))
	canv_6.create_text(160,210,text = "Средняя температура - -139  °C ; ", fill = "white", font =("Times",15))
	canv_6.create_text(92,230,text = "Состав Атмосферы:", fill = "white", font =("Times",15))
	canv_6.create_text(143,250,text = "Молекулярный водород 96%:", fill = "white", font =("Times",15))
	canv_6.create_text(89,270,text = "Гелий около 4%", fill = "white", font =("Times",15))
	canv_6.pack()

def uran_menu():
	uran_menu = Toplevel(root)
	uran_menu.resizable(width = False, height = False)
	canv_7 = Canvas(uran_menu, width=500, height=350, bg = 'black')
	canv_7.create_text(250,20,text = "Уран:", fill = "white", font =("Times",15))
	canv_7.create_text(200,50,text = "Орбитальные и физические характеристики:", fill = "white", font =("Times",15))
	canv_7.create_text(140,70,text = "Радиус орбиты =  25 360 км; ", fill = "white", font =("Times",15))
	canv_7.create_text(108,90,text = "Масса = 8.68×10²⁵ кг; ", fill = "white", font =("Times",15))
	canv_7.create_text(123,110,text = "Плотность = 1710 кг/м3; ", fill = "white", font =("Times",15))
	canv_7.create_text(157,130,text = "Период вращения = 17 ч 14 мин; ", fill = "white", font =("Times",15))
	canv_7.create_text(160,150,text = "Период обращения — 84,01 года; ", fill = "white", font =("Times",15))
	canv_7.create_text(122,170,text = "Наклон орбиты — 0,77°; ", fill = "white", font =("Times",15))
	canv_7.create_text(195,190,text = "Среднее расстояние от солнца - 19,18 а.е; ", fill = "white", font =("Times",15))
	canv_7.create_text(158,210,text = "Средняя температура -  -197  °C ; ", fill = "white", font =("Times",15))
	canv_7.create_text(92,230,text = "Состав Атмосферы:", fill = "white", font =("Times",15))
	canv_7.create_text(143,250,text = "Молекулярный водород 72%:", fill = "white", font =("Times",15))
	canv_7.create_text(61,270,text = "Метан 2%", fill = "white", font =("Times",15))
	canv_7.create_text(93,290,text = "Гелий около 26%", fill = "white", font =("Times",15))
	canv_7.pack()
	
def neptun_menu():
	neptun_menu = Toplevel(root)
	neptun_menu.resizable(width = False, height = False)
	canv_8 = Canvas(neptun_menu, width=500, height=350, bg = 'black')
	canv_8.create_text(250,20,text = "Нептун:", fill = "white", font =("Times",15))
	canv_8.create_text(200,50,text = "Орбитальные и физические характеристики:", fill = "white", font =("Times",15))
	canv_8.create_text(140,70,text = "Радиус орбиты =  24 622 км; ", fill = "white", font =("Times",15))
	canv_8.create_text(108,90,text = "Масса = 1.02×10²⁶ кг; ", fill = "white", font =("Times",15))
	canv_8.create_text(123,110,text = "Плотность = 2300 кг/м3; ", fill = "white", font =("Times",15))
	canv_8.create_text(157,130,text = "Период вращения = 16 ч 03 мин; ", fill = "white", font =("Times",15))
	canv_8.create_text(165,150,text = "Период обращения — 164,79 года; ", fill = "white", font =("Times",15))
	canv_8.create_text(122,170,text = "Наклон орбиты — 1,77°; ", fill = "white", font =("Times",15))
	canv_8.create_text(195,190,text = "Среднее расстояние от солнца - 30,06 а.е; ", fill = "white", font =("Times",15))
	canv_8.create_text(158,210,text = "Средняя температура -  -201  °C ; ", fill = "white", font =("Times",15))
	canv_8.create_text(92,230,text = "Состав Атмосферы:", fill = "white", font =("Times",15))
	canv_8.create_text(143,250,text = "Молекулярный водород 80%:", fill = "white", font =("Times",15))
	canv_8.create_text(95,270,text = "Метан около 1,5%", fill = "white", font =("Times",15))
	canv_8.create_text(93,290,text = "Гелий около 19%", fill = "white", font =("Times",15))
	canv_8.pack()


#Запус окна и настройка
root = Tk()
root.resizable(width = False, height = False)

mainmenu = Menu(root)
root.config(menu = mainmenu)

#Формирует меню выбора информации интересующей планеты
filemenu = Menu(mainmenu, tearoff = 0)
filemenu.add_command(label = "Мercury", command = mercury_menu)
filemenu.add_command(label = "Venera", command = venera_menu)
filemenu.add_command(label = "Earth", command = earth_menu)
filemenu.add_command(label = "Мars", command = mars_menu)
filemenu.add_command(label = "Upiter", command = upiter_menu)
filemenu.add_command(label = "Saturn", command = saturn_menu)
filemenu.add_command(label = "Uran", command = uran_menu)
filemenu.add_command(label = "Neptun", command = neptun_menu)
mainmenu.add_cascade(label = "Info Planet", menu  = filemenu)

canv = Canvas(root, width=1000, height=1000, bg = 'black')
canv.pack()

#Формирование "обьекта" планет и их пути

sun = Planet("oval", center = [500,500], scale = 30, fill_color = "yellow")

mercury_path = [ [ 100*sin(2*pi*fi/200), - 100*cos(2*pi*fi/200) ] for fi in range(200)]
mercury = Planet("oval", scale = 5, fill_color = "#737B83",
	     speed = 2, path = mercury_path, path_center = [500,500])

venera_path = [ [ 140*sin(2*pi*fi/300), - 140*cos(2*pi*fi/300) ] for fi in range(300)]
venera = Planet("oval", scale = 10, fill_color = "#D1C981",
	       speed = 2, path = venera_path, path_center = [500,500])

earth_path = [ [ 200*sin(2*pi*fi/400), - 200*cos(2*pi*fi/400) ] for fi in range(400)]
earth = Planet("oval", scale = 14, fill_color = "#62EAE3",
	       speed = 2, path = earth_path, path_center = [500,500])

mars_path = [ [ 245*sin(2*pi*fi/500), - 245*cos(2*pi*fi/500) ] for fi in range(500)]
mars = Planet("oval", scale = 12, fill_color = "#E03609",
	       speed = 2, path = mars_path, path_center = [500,500])

upiter_path = [ [ 300*sin(2*pi*fi/600), - 300*cos(2*pi*fi/600) ] for fi in range(600)]
upiter = Planet("oval", scale = 25, fill_color = "#CC7119",
	       speed = 2, path = upiter_path, path_center = [500,500])
	      
saturn_path = [ [ 345*sin(2*pi*fi/700), - 365*cos(2*pi*fi/700) ] for fi in range(700)]
saturn = Planet("oval", scale = 20, fill_color = "#DFA771",
	       speed = 2, path = saturn_path, path_center = [500,500])
	       
uran_path = [ [ 405*sin(2*pi*fi/800), - 405*cos(2*pi*fi/800) ] for fi in range(800)]
uran = Planet("oval", scale = 15, fill_color = "#24CC8E",
	       speed = 2, path = uran_path, path_center = [500,500])
	       
neptun_path = [ [ 445*sin(2*pi*fi/900), - 445*cos(2*pi*fi/900) ] for fi in range(900)]
neptun = Planet("oval", scale = 15, fill_color = "#ABCAD0",
	       speed = 2, path = neptun_path, path_center = [500,500])
	      
#Осуществляет движение планет по орбите	       	       
def disp_rotate( ):
	mercury.move(1)
	venera.move(1)
	earth.move(1)
	mars.move(1)
	upiter.move(1)
	saturn.move(1)
	uran.move(1)
	neptun.move(1)
	canv.after(38, disp_rotate)

disp_rotate() 
root.mainloop()
