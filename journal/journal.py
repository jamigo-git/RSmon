from tkinter import *  
from tkinter.ttk import Combobox, Radiobutton, Label, Entry, Spinbox
import tkinter.ttk as ttk
import datetime
import ast
import winreg 
import psycopg2
from idlelib.tooltip import Hovertip
import subprocess

surname = ['Рожков В.А.', 'Алексеев Н.И.', 'Коротаев А.А.', 'Ямалеев И.О.', 'Голованов А.С.']

#Работа с буфером по клавишам Ctr-C, Ctr-V, Ctr-X
def _onKeyRelease(event):   
    ctrl = (event.state & 0x4) != 0
    if event.keycode==88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")
    if event.keycode==86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")
    if event.keycode==67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

# Функция отрабатывает нажатие ПКМ на текстовом поле и выводит меню        
def mouse_button3(event): 
    global x,y
    x = event.x
    y = event.y
    menu.post(event.x_root, event.y_root)

# Функция запуска Radmin с параметрами подключения.
def radmin_start(IP):
    subprocess.Popen('C:\\Program Files\\Radmin Viewer 3\\Radmin.exe')

# Фукнция открытия карточки компьютера
def PC_card(model, IP, SN):
    window_card = Tk()
    window_card.title("Карточка компьютера " + model + "   IP " + IP)
    window_card.geometry("620x500")
    Label(window_card, text = ("Последние комментарии:")).place(x=10, y=90)
    text_card = Text(window_card, width=50, height=10)
    text_card.place(x=10, y=110)
    SUBD_get_PC(window_card, text_card, SN, IP)
    Label(window_card, text = ("Ваш комментарий:")).place(x=10, y=300)
    text_wr = Text(window_card, width=50, height=5)
    text_wr.place(x=10, y=320)
    btn_wr = Button(window_card, text="Отправить", command = lambda: SUBD_push_PC(window_card, text_wr, SN, combo, sel.get(), text_card))
    btn_wr.place(x=350, y=420)
    lbl01 = Label(window_card, text = "Выберите фамилию:").place(x=10, y=420)
    combo = Combobox(window_card, width = 13, values = surname)
    combo.place(x=150, y=420)
    combo.current(3)
    lbl_alarms = LabelFrame(window_card, text = "Состояние")
    lbl_alarms.place(x = 470, y=300, width = 140, height = 120)
    sel = IntVar(lbl_alarms)
    sel.set(1)
    rad_alarm1 = Radiobutton(lbl_alarms, text='В работе', variable=sel, value=1)
    rad_alarm1.place(x=5, y=0)
    rad_alarm2 = Radiobutton(lbl_alarms, text='Не работает', variable=sel, value=2)
    rad_alarm2.place(x=5, y=30)                
    rad_alarm3 = Radiobutton(lbl_alarms, text='Есть проблемы', variable=sel, value=3)
    rad_alarm3.place(x=5, y=60)

#Функция получения данных о компьютере из БД
def SUBD_get_PC(window_card, text_card, SN, IP):
    try:
        # Подключение к БД
        con = psycopg2.connect(
        database="Virtual_department", 
        user="postgres", 
        password="777#igra", 
        host="127.0.0.1", 
        port="5432")
        label_dbsuc = Label(window_card, text = "Подключение к базе данных: ОК", foreground = 'green')
        label_dbsuc.place(x=10, y=5)

    except:
        label_dbsuc = Label(window_card, text = "Не удалось подключиться к базе денных", foreground = 'red')
        label_dbsuc.place(x=10, y=5)

    try:
    # Считывание данных установки из таблицы установок
        cur = con.cursor()
        cur.execute("SELECT serial_number, name_pc, ip, alarms, radmin, windows, net_monitor, inkotex, other_soft FROM public.pc WHERE serial_number = \'%s\';" %SN)
        rows = cur.fetchall()
        for row in rows:
            Label(window_card, text = ("СН установки: " + row[0])).place(x=10, y=25)
            Label(window_card, text = ("Номер ПК: " + row[1])).place(x=10, y=45)
            Label(window_card, text = ("IP-адрес: " + row[2])).place(x=10, y=65)
            ip_ad = row[2]
            print(ip_ad)
            if row[3] == 'work':
                Label(window_card, text = ("Состояние: " + row[3]), foreground = 'green').place(x=200, y=25)
            elif row[3] == 'not_work':
                Label(window_card, text = ("Состояние: " + row[3]), foreground = 'red').place(x=200, y=25)
            elif row[3] == 'is_problems':
                Label(window_card, text = ("Состояние: " + row[3]), foreground = 'orange').place(x=200, y=25)
            else:
                Label(window_card, text = ("Состояние: нет"), foreground = 'red').place(x=200, y=25)
            Label(window_card, text = ("Radmin: " + row[4])).place(x=200, y=45)
            Label(window_card, text = ("Windows: " + row[5])).place(x=200, y=65)
            Label(window_card, text = ("Net Monitor 2: " + row[6])).place(x=390, y=65)
            Label(window_card, text = ("Инкотекс: " + row[7])).place(x=390, y=25)
            Label(window_card, text = ("Другие: " + row[8])).place(x=390, y=45)
            btn_radmin = Button(window_card, text="Radmin", command = lambda: subprocess.Popen('C:\\Program Files\\Radmin Viewer 3\\Radmin.exe /connect:%s:4899 '%ip_ad))
            btn_radmin.place(x=520, y=125)
    except:
        Label(window_card, text = "Данные в таблице установок отсутсвуют!!!", foreground = 'red').place(x=10, y=25)

    try:
        # Считывание комментариев по данному компьютеру
        cur.execute("SELECT date, time, author, commentary FROM public.comments WHERE serial_number = \'%s\' ORDER BY date;" %SN)
        rows = cur.fetchall()
        for row in rows:
            text_card.insert(1.0, "\nДата: " + str(row[0]))
            text_card.insert(1.0, "\nВремя: " + str(row[1]))
            text_card.insert(1.0, "\nАвтор: " + row[2])
            text_card.insert(1.0, "\nКомментарий: " + row[3])
            text_card.insert(1.0, "\n")
        con.close()
    except:
        text_card.insert(1.0, "Данные в таблице комментариев отсутствуют")


# Функция открытия карточки стенда
def installation_card(model, SN):
    window_card = Tk()
    window_card.title("Карточка стенда " + model + "   SN " + SN)
    window_card.geometry("620x500")
    Label(window_card, text = ("Последние комментарии:")).place(x=10, y=90)
    text_card = Text(window_card, width=50, height=10)
    text_card.place(x=10, y=110)
    #scroll = Scrollbar(window_card, command=text_card.yview, width=50)
    #scroll.place(x=530, y=110)
    SUBD_get(window_card, text_card, SN)
    Label(window_card, text = ("Ваш комментарий:")).place(x=10, y=300)
    text_wr = Text(window_card, width=50, height=5)
    text_wr.place(x=10, y=320)
    btn_wr = Button(window_card, text="Отправить", command = lambda: SUBD_push(window_card, text_wr, SN, combo, sel.get(), text_card))
    btn_wr.place(x=350, y=420)
    lbl01 = Label(window_card, text = "Выберите фамилию:").place(x=10, y=420)
    combo = Combobox(window_card, width = 13, values = surname)
    combo.place(x=150, y=420)
    combo.current(3)
    lbl_alarms = LabelFrame(window_card, text = "Состояние")
    lbl_alarms.place(x = 470, y=300, width = 140, height = 120)
    sel = IntVar(lbl_alarms)
    sel.set(1)
    rad_alarm1 = Radiobutton(lbl_alarms, text='В работе', variable=sel, value=1)
    rad_alarm1.place(x=5, y=0)
    rad_alarm2 = Radiobutton(lbl_alarms, text='Не работает', variable=sel, value=2)
    rad_alarm2.place(x=5, y=30)                
    rad_alarm3 = Radiobutton(lbl_alarms, text='Есть проблемы', variable=sel, value=3)
    rad_alarm3.place(x=5, y=60)
        

# Функция записи данных в БД (установки)
def SUBD_push(window_card, text_wr, SN, combo, alarms, text_card):
    print(alarms)
    try:
        # Подключение к БД
        con = psycopg2.connect(
          database="Virtual_department", 
          user="postgres", 
          password="777#igra", 
          host="127.0.0.1", 
          port="5432")
        Label(window_card, text = "Подключение к базе данных: ОК            ", foreground = 'green').place(x=10, y=450)
    except:
        Label(window_card, text = "Подключение к базе данных отсутсвует", foreground = 'red').place(x=10, y=450)
    try:
        #Запись комментария в таблицу БД
        if alarms == 1:
            alarms = 'work'
        elif alarms == 2:
            alarms = 'not_work'
        else:
            alarms = 'is_problems'
        cur = con.cursor()
      
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        time = datetime.datetime.now().strftime("%H:%M:%S")    
        author = combo.get()
        comment = text_wr.get(1.0, END).strip()
        cur.execute("INSERT INTO public.comments (date, author, commentary, serial_number, time, alarms) VALUES (%s, %s, %s, %s, %s, %s);", (date, author, comment, SN, time, alarms))
        cur.execute("UPDATE public.installations SET alarms=%s WHERE serial_number = %s; ", (alarms, SN))
        con.commit() 
        Label(window_card, text = "Данные успешно записаны!!!", foreground = 'green').place(x=10, y=450)
        #Считывание (обновление) данных в поле комментариев
        text_card.delete(1.0, END)
        cur.execute("SELECT date, time, author, commentary FROM public.comments WHERE serial_number = \'%s\' ORDER BY date;" %SN)
        rows = cur.fetchall()
        for row in rows:
            text_card.insert(1.0, "\nДата: " + str(row[0]))
            text_card.insert(1.0, "\nВремя: " + str(row[1]))
            text_card.insert(1.0, "\nАвтор: " + row[2])
            text_card.insert(1.0, "\nКомментарий: " + row[3])
            text_card.insert(1.0, "\n")
        con.close()
    except:
        Label(window_card, text = "Не удалось записать данные в базу данных!!!", foreground = 'red').place(x=10, y=450)
    

# Функция получения данных из базы по установке
def SUBD_get(window_card, text_card, SN):
    try:
        # Подключение к БД
        con = psycopg2.connect(
          database="Virtual_department", 
          user="postgres", 
          password="777#igra", 
          host="127.0.0.1", 
          port="5432")
        label_dbsuc = Label(window_card, text = "Подключение к базе данных: ОК", foreground = 'green')
        label_dbsuc.place(x=10, y=5)

    except:
        label_dbsuc = Label(window_card, text = "Не удалось подключиться к базе денных", foreground = 'red')
        label_dbsuc.place(x=10, y=5)

    try:
        # Считывание данных установки из таблицы установок
        cur = con.cursor()
        cur.execute("SELECT serial_number, model, phases, alarms, inkotex, calibrovka, poverka FROM public.installations WHERE serial_number = \'%s\';" %SN)
        rows = cur.fetchall()
        for row in rows:
            Label(window_card, text = ("Серийный номер: " + row[0])).place(x=10, y=25)
            Label(window_card, text = ("Модель стенда: " + row[1])).place(x=10, y=45)
            Label(window_card, text = ("Количество фаз: " + row[2])).place(x=10, y=65)
            if row[3] == 'work':
                Label(window_card, text = ("Текущее состояние: " + row[3]), foreground = 'green').place(x=250, y=25)
            elif row[3] == 'not_work':
                Label(window_card, text = ("Текущее состояние: " + row[3]), foreground = 'red').place(x=250, y=25)
            elif row[3] == 'is_problems':
                Label(window_card, text = ("Текущее состояние: " + row[3]), foreground = 'orange').place(x=250, y=25)
            else:
                Label(window_card, text = ("Текущее состояние: не удалось получить"), foreground = 'red').place(x=250, y=25)
            if row[4] == True:
                Label(window_card, text = "Доработка Инкотекс: имеется").place(x=250, y=45)
            elif row[4] == False:
                Label(window_card, text = "Доработка Инкотекс: отсутствует").place(x=250, y=45)
            else:
                Label(window_card, text = "Доработка Инкотекс: данные отсутствуют").place(x=250, y=45)
            Label(window_card, text = ("Счетчики калибровка: " + row[5])).place(x=250, y=65)
            Label(window_card, text = ("Счетчики поверка: " + row[6])).place(x=250, y=85)
    except:
        Label(window_card, text = "Данные в таблице установок отсутсвуют!!!", foreground = 'red').place(x=10, y=25)

    try:
        # Считывание комментариев по данной установке
        cur.execute("SELECT date, time, author, commentary FROM public.comments WHERE serial_number = \'%s\' ORDER BY date;" %SN)
        rows = cur.fetchall()
        for row in rows:
            text_card.insert(1.0, "\nДата: " + str(row[0]))
            text_card.insert(1.0, "\nВремя: " + str(row[1]))
            text_card.insert(1.0, "\nАвтор: " + row[2])
            text_card.insert(1.0, "\nКомментарий: " + row[3])
            text_card.insert(1.0, "\n")
        con.close()
    except:
        text_card.insert(1.0, "Данные в таблице комментариев отсутствуют")

def button_color(SN):
    try:
        con = psycopg2.connect(
        database="Virtual_department", 
        user="postgres", 
        password="777#igra", 
        host="127.0.0.1", 
        port="5432")
        cur = con.cursor()
        cur.execute("SELECT alarms FROM public.installations WHERE serial_number = \'%s\';" %SN)
        rows = cur.fetchall()
        for row in rows:
            if row[0] == "work":
                return ('#D3D3D3')
            elif row[0] == "not_work":
                return ('#FF0000')
            elif row[0] == "is_problems":
                return('#FFA500')
            else:
                return('#D3D3D3')
        con.close()
    except:
        Label(window, text = "Не удалось получить данные из базы данных!!!", bg = 'red').place(x=25, y=760)
   

#Main program
window = Tk()  
window.title("Виртуальный цех        (by Jamigo)")  
window.geometry('1250x780')
#Включаем подержку нажатий клавиш Ctr-C, Ctr-V, Ctr-X
window.bind_all("<Key>", _onKeyRelease, "+") 


#Элементы стенда №1 HX-8100 SN 080798
alarm_color = button_color('080798')
lbl_HX8100_3 = LabelFrame(window, text = "1")
lbl_HX8100_3.place(x = 20, y=120, width = 250, heigh = 60)
HX8100_3_1 = Button(lbl_HX8100_3, text="1-48", width = 10, command = lambda: installation_card('HX8100','080798'), bg = alarm_color)
HX8100_3_1.place(x=10, y=0)
HX8100_3_2 = Button(lbl_HX8100_3, text="49-96", width = 10, command = lambda: installation_card('HX8100','080798'), bg = alarm_color)
HX8100_3_2.place(x=105, y=0)
HX8100_3_PC = Button(lbl_HX8100_3, text="ПК", width = 3, command = lambda: PC_card('PC1', '192.168.0.202', '080798'), bg = alarm_color)
HX8100_3_PC.place(x=200, y=0)
Hovertip(HX8100_3_1, ['HX-8100', ' SN080798'])
Hovertip(HX8100_3_2, ['HX-8100', ' SN080798'])
Hovertip(HX8100_3_PC, ['Windows XP', 'IP 192.168.0.202'])

#Элементы стенда №2 HX-8100_2
alarm_color = button_color('080799')
lbl_HX8100_2 = LabelFrame(window, text = "2")
lbl_HX8100_2.place(x = 20, y=280, width = 250, heigh = 60)
HX8100_2_1 = Button(lbl_HX8100_2, text="1-48", width = 10, command = lambda: installation_card('HX8100', '080799'), bg = alarm_color)
HX8100_2_1.place(x=50, y=0)
HX8100_2_2 = Button(lbl_HX8100_2, text="49-96", width = 10, command = lambda: installation_card('HX8100', '080799'), bg = alarm_color)
HX8100_2_2.place(x=145, y=0)
HX8100_2_PC = Button(lbl_HX8100_2, text="ПК", width = 3, command = lambda: PC_card('PC2', '192.168.0.163', '080799'), bg = alarm_color)
HX8100_2_PC.place(x=10, y=0)
Hovertip(HX8100_2_1, ['HX-8100', ' SN080799'])
Hovertip(HX8100_2_2, ['HX-8100', ' SN080799'])
Hovertip(HX8100_2_PC, ['Windows XP', 'IP 192.168.0.163'])

#Элементы стенда №3 SY8125 SN703143
alarm_color = button_color('703143')
lbl_SY8125_1 = LabelFrame(window, text = "3")
lbl_SY8125_1.place(x = 20, y=380, width = 150, heigh = 90)
SY8125_1 = Button(lbl_SY8125_1, text="1-24", width = 10, command = lambda: installation_card('SY8125', '703143'), bg = alarm_color)
SY8125_1.place(x=50, y=0)
SY8125_1_PC = Button(lbl_SY8125_1, text="ПК", width = 3, command = lambda: PC_card('PC3', '192.168.0.242', '703143'), bg = alarm_color)
SY8125_1_PC.place(x=10, y=30)
Hovertip(SY8125_1, ['SY8125', ' SN703143'])
Hovertip(SY8125_1_PC, ['Windows XP', 'IP 192.168.0.242'])

#Элементы стенда №4 SY8125 SN703146
alarm_color = button_color('703146')
lbl_SY8125_2 = LabelFrame(window, text = "4")
lbl_SY8125_2.place(x = 20, y=470, width = 150, heigh = 90)
SY8125_2 = Button(lbl_SY8125_2, text="1-24", width = 10, command = lambda: installation_card('SY8125', '703146'), bg = alarm_color)
SY8125_2.place(x=50, y=30)
SY8125_2_PC = Button(lbl_SY8125_2, text="ПК", width = 3, command = lambda: PC_card('PC4', '192.168.0.97', '703146'), bg = alarm_color)
SY8125_2_PC.place(x=10, y=0)
Hovertip(SY8125_2, ['SY8125', ' SN703146'])
Hovertip(SY8125_2_PC, ['Windows XP', 'IP 192.168.0.97'])

#Элементы стенда №5 УАПС-1М SN000000
alarm_color = button_color('000000')
lbl_UAPS1M_5 = LabelFrame(window, text = "5")
lbl_UAPS1M_5.place(x = 270, y=0, width = 80, heigh = 85)
UAPS1M_5 = Button(lbl_UAPS1M_5, text="Уст.", width = 3, command = lambda: installation_card('UAPS-1M', '000000'), bg = alarm_color)
UAPS1M_5.place(x=20, y=00)
UAPS1M_5_1 = Button(lbl_UAPS1M_5, text="1-6", width = 3, command = lambda: installation_card('UAPS-1M', '000000'), bg = alarm_color)
UAPS1M_5_1.place(x=40, y=30)
Hovertip(UAPS1M_5, ['УАПС-1М', ' SN000000'])
Hovertip(UAPS1M_5_1, ['УАПС-1М', ' SN000000'])

#Элементы стенда №6 УАПС-1М SN102
alarm_color = button_color('102')
lbl_UAPS1M_6 = LabelFrame(window, text = "6")
lbl_UAPS1M_6.place(x = 350, y=0, width = 80, heigh = 85)
UAPS1M_6 = Button(lbl_UAPS1M_6, text="Уст.", width = 3, command = lambda: installation_card('UAPS-1M', '102'), bg = alarm_color)
UAPS1M_6.place(x=20, y=00)
UAPS1M_6_1 = Button(lbl_UAPS1M_6, text="1-6", width = 3, command = lambda: installation_card('UAPS-1M', '102'), bg = alarm_color)
UAPS1M_6_1.place(x=40, y=30)
UAPS1M_6_PC = Button(lbl_UAPS1M_6, text="ПК", width = 3, command = lambda: PC_card('PC6', '192.168.0.169', '102'), bg = alarm_color)
UAPS1M_6_PC.place(x=0, y=30)
Hovertip(UAPS1M_6, ['УАПС-1М', 'SN102'])
Hovertip(UAPS1M_6_1, ['УАПС-1М', 'SN102'])
Hovertip(UAPS1M_6_PC, ['Windows XP', 'IP 192.168.0.169'])

#Элементы стенда №7 УАПС-1М SN61207
alarm_color = button_color('61207')
lbl_UAPS1M_7 = LabelFrame(window, text = "7")
lbl_UAPS1M_7.place(x = 440, y=0, width = 80, heigh = 85)
UAPS1M_7 = Button(lbl_UAPS1M_7, text="Уст.", width = 3, command = lambda: installation_card('UAPS-1M', '61207'), bg = alarm_color)
UAPS1M_7.place(x=20, y=00)
UAPS1M_7_1 = Button(lbl_UAPS1M_7, text="1-6", width = 3, command = lambda: installation_card('UAPS-1M', '61207'), bg = alarm_color)
UAPS1M_7_1.place(x=40, y=30)
UAPS1M_7_PC = Button(lbl_UAPS1M_7, text="ПК", width = 3, command = lambda: PC_card('PC7', '192.168.0.37', '61207'), bg = alarm_color)
UAPS1M_7_PC.place(x=0, y=30)
Hovertip(UAPS1M_7, ['УАПС-1М', 'SN61207'])
Hovertip(UAPS1M_7_1, ['УАПС-1М', 'SN61207'])
Hovertip(UAPS1M_7_PC, ['Windows XP', 'IP 192.168.0.37'])

#Элементы стенда №8 УАПС-1М SN109
alarm_color = button_color('109')
lbl_UAPS1M_8 = LabelFrame(window, text = "8")
lbl_UAPS1M_8.place(x = 640, y=0, width = 80, heigh = 85)
UAPS1M_8 = Button(lbl_UAPS1M_8, text="Уст.", width = 3, command = lambda: installation_card('UAPS-1M', '109'), bg = alarm_color)
UAPS1M_8.place(x=20, y=00)
UAPS1M_8_1 = Button(lbl_UAPS1M_8, text="1-6", width = 3, command = lambda: installation_card('UAPS-1M', '109'), bg = alarm_color)
UAPS1M_8_1.place(x=40, y=30)
UAPS1M_8_PC = Button(lbl_UAPS1M_8, text="ПК", width = 3, command = lambda: PC_card('PC8', '192.168.0.17', '109'), bg = alarm_color)
UAPS1M_8_PC.place(x=0, y=30)
Hovertip(UAPS1M_8, ['УАПС-1М', 'SN109'])
Hovertip(UAPS1M_8_1, ['УАПС-1М', 'SN109'])
Hovertip(UAPS1M_8_PC, ['Windows 98', 'IP 192.168.0.17'])

#Элементы стенда №9 УАПС-1М SN050908
alarm_color = button_color('050908')
lbl_UAPS1M_9 = LabelFrame(window, text = "9")
lbl_UAPS1M_9.place(x = 730, y=0, width = 80, heigh = 85)
UAPS1M_9 = Button(lbl_UAPS1M_9, text="Уст.", width = 3, command = lambda: installation_card('UAPS-1M', '050908'), bg = alarm_color)
UAPS1M_9.place(x=20, y=00)
UAPS1M_9_1 = Button(lbl_UAPS1M_9, text="1-6", width = 3, command = lambda: installation_card('UAPS-1M', '050908'), bg = alarm_color)
UAPS1M_9_1.place(x=40, y=30)
UAPS1M_9_PC = Button(lbl_UAPS1M_9, text="ПК", width = 3, command = lambda: PC_card('PC9', '192.168.0.40', '050908'), bg = alarm_color)
UAPS1M_9_PC.place(x=0, y=30)
Hovertip(UAPS1M_9, ['УАПС-1М', 'SN050908'])
Hovertip(UAPS1M_9_1, ['УАПС-1М', 'SN050908'])
Hovertip(UAPS1M_9_PC, ['Windows XP', 'IP 192.168.0.40'])

#Элементы стенда №10 HX8300 SN0807102
alarm_color = button_color('0807102')
lbl_HX8300_10 = LabelFrame(window, text = "10")
lbl_HX8300_10.place(x = 350, y=120, width = 50, heigh = 320)
HX8300_10_1 = Button(lbl_HX8300_10, text="1-\n24", width = 3, height = 3, command = lambda: installation_card('HX8300','0807102'), bg = alarm_color)
HX8300_10_1.place(x=5, y=30)
HX8300_10_2 = Button(lbl_HX8300_10, text="25-\n48", width = 3, height = 3, command = lambda: installation_card('HX8300','0807102'), bg = alarm_color)
HX8300_10_2.place(x=5, y=95)
HX8300_10_3 = Button(lbl_HX8300_10, text="49-\n72", width = 3, height = 3, command = lambda: installation_card('HX8300','0807102'), bg = alarm_color)
HX8300_10_3.place(x=5, y=160)
HX8300_10_4 = Button(lbl_HX8300_10, text="73-\n96", width = 3, height = 3, command = lambda: installation_card('HX8300','0807102'), bg = alarm_color)
HX8300_10_4.place(x=5, y=225)
HX8300_10_PC = Button(lbl_HX8300_10, text="ПК", width = 3, command = lambda: PC_card('PC10', '192.168.0.43','0807102'), bg = alarm_color)
HX8300_10_PC.place(x=5, y=0)
Hovertip(HX8300_10_1, ['HX-8300', ' SN0807102'])
Hovertip(HX8300_10_2, ['HX-8300', ' SN0807102'])
Hovertip(HX8300_10_3, ['HX-8300', ' SN0807102'])
Hovertip(HX8300_10_4, ['HX-8300', ' SN0807102'])
Hovertip(HX8300_10_PC, ['Windows 7', 'IP 192.168.0.43'])

#Элементы стенда №11 HX8300 SN0807103
alarm_color = button_color('0807103')
lbl_HX8300_11 = LabelFrame(window, text = "11")
lbl_HX8300_11.place(x = 350, y=440, width = 50, heigh = 320)
HX8300_11_1 = Button(lbl_HX8300_11, text="1-\n24", width = 3, height = 3, command = lambda: installation_card('HX8300','0807103'), bg = alarm_color)
HX8300_11_1.place(x=5, y=30)
HX8300_11_2 = Button(lbl_HX8300_11, text="25-\n48", width = 3, height = 3, command = lambda: installation_card('HX8300','0807103'), bg = alarm_color)
HX8300_11_2.place(x=5, y=95)
HX8300_11_3 = Button(lbl_HX8300_11, text="49-\n72", width = 3, height = 3, command = lambda: installation_card('HX8300','0807103'), bg = alarm_color)
HX8300_11_3.place(x=5, y=160)
HX8300_11_4 = Button(lbl_HX8300_11, text="73-\n96", width = 3, height = 3, command = lambda: installation_card('HX8300','0807103'), bg = alarm_color)
HX8300_11_4.place(x=5, y=225)
HX8300_11_PC = Button(lbl_HX8300_11, text="ПК", width = 3, command = lambda: PC_card('PC11', '000.000.000.000','0807103'), bg = alarm_color)
HX8300_11_PC.place(x=5, y=0)
Hovertip(HX8300_11_1, ['HX-8300', ' SN0807103'])
Hovertip(HX8300_11_2, ['HX-8300', ' SN0807103'])
Hovertip(HX8300_11_3, ['HX-8300', ' SN0807103'])
Hovertip(HX8300_11_4, ['HX-8300', ' SN0807103'])
Hovertip(HX8300_11_PC, ['Windows XP', 'IP нет данных'])

#Элементы стенда №12 CL3005-24 SN3028
alarm_color = button_color('3028')
lbl_CL3005_1 = LabelFrame(window, text = "12")
lbl_CL3005_1.place(x = 450, y=100, width = 250, heigh = 90)
CL3005_1_1 = Button(lbl_CL3005_1, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3028'), bg = alarm_color)
CL3005_1_1.place(x=10, y=15)
CL3005_1_2 = Button(lbl_CL3005_1, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3028'), bg = alarm_color)
CL3005_1_2.place(x=105, y=15)
CL3005_1_ST = Button(lbl_CL3005_1, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3028'), bg = alarm_color)
CL3005_1_ST.place(x=200, y=30)
CL3005_1_PC = Button(lbl_CL3005_1, text="ПК", width = 3, command = lambda: PC_card('PC12', '192.168.0.185','3028'), bg = alarm_color)
CL3005_1_PC.place(x=200, y=0)
Hovertip(CL3005_1_1, ['CL3005-24', ' SN3028'])
Hovertip(CL3005_1_2, ['CL3005-24', ' SN3028'])
Hovertip(CL3005_1_ST, ['CL3005-24', ' SN3028'])
Hovertip(CL3005_1_PC, ['Windows 7', 'IP 192.168.0.185'])

#Элементы стенда №13 CL3005-24 SN3042
alarm_color = button_color('3042')
lbl_CL3005_2 = LabelFrame(window, text = "13")
lbl_CL3005_2.place(x = 700, y=100, width = 250, heigh = 90)
CL3005_2_1 = Button(lbl_CL3005_2, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3042'), bg = alarm_color)
CL3005_2_1.place(x=10, y=15)
CL3005_2_2 = Button(lbl_CL3005_2, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3042'), bg = alarm_color)
CL3005_2_2.place(x=105, y=15)
CL3005_2_ST = Button(lbl_CL3005_2, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3042'), bg = alarm_color)
CL3005_2_ST.place(x=200, y=30)
CL3005_2_PC = Button(lbl_CL3005_2, text="ПК", width = 3, command = lambda: PC_card('PC13', '192.168.0.253','3042'), bg = alarm_color)
CL3005_2_PC.place(x=200, y=0)
Hovertip(CL3005_2_1, ['CL3005-24', ' SN3042'])
Hovertip(CL3005_2_1, ['CL3005-24', ' SN3042'])
Hovertip(CL3005_2_ST, ['CL3005-24', ' SN3042'])
Hovertip(CL3005_2_PC, ['Windows 7', 'IP 192.168.0.253'])

#Элементы стенда №14 CL1001 SN1009
alarm_color = button_color('1009')
lbl_CL1001_1 = LabelFrame(window, text = "14")
lbl_CL1001_1.place(x = 450, y=190, width = 150, heigh = 90)
CL1001_1_1 = Button(lbl_CL1001_1, text="1-24", width = 10, command = lambda: installation_card('CL1001','1009'), bg = alarm_color)
CL1001_1_1.place(x=50, y=15)
CL1001_1_ST = Button(lbl_CL1001_1, text="Уст.", width = 3, command = lambda: installation_card('CL1001','1009'), bg = alarm_color)
CL1001_1_ST.place(x=10, y=0)
CL1001_1_PC = Button(lbl_CL1001_1, text="ПК", width = 3, command = lambda: PC_card('PC14', '192.168.0.201','1009'), bg = alarm_color)
CL1001_1_PC.place(x=10, y=30)
Hovertip(CL1001_1_1, ['CL3005-24', ' SN1009'])
Hovertip(CL1001_1_ST, ['CL3005-24', ' SN1009'])
Hovertip(CL1001_1_PC, ['Windows XP', 'IP 192.168.0.201'])

#Элементы стенда №15 CL1001 SN1008
alarm_color = button_color('1008')
lbl_CL1001_2 = LabelFrame(window, text = "15")
lbl_CL1001_2.place(x = 450, y=280, width = 150, heigh = 90)
CL1001_2_1 = Button(lbl_CL1001_2, text="1-24", width = 10, command = lambda: installation_card('CL1001','1008'), bg = alarm_color)
CL1001_2_1.place(x=10, y=15)
CL1001_2_ST = Button(lbl_CL1001_2, text="Уст.", width = 3, command = lambda: installation_card('CL1001','1008'), bg = alarm_color)
CL1001_2_ST.place(x=110, y=30)
CL1001_2_PC = Button(lbl_CL1001_2, text="ПК", width = 3, command = lambda: PC_card('PC15', '192.168.0.47','1008'), bg = alarm_color)
CL1001_2_PC.place(x=110, y=0)
Hovertip(CL1001_2_1, ['CL3005-24', ' SN1008'])
Hovertip(CL1001_2_ST, ['CL3005-24', ' SN1008'])
Hovertip(CL1001_2_PC, ['Windows XP', 'IP 192.168.0.47'])

#Элементы стенда №16 SY8125 SN703154
alarm_color = button_color('703154')
lbl_SY8125_3 = LabelFrame(window, text = "16")
lbl_SY8125_3.place(x = 605, y=200, width = 150, heigh = 60)
SY8125_3 = Button(lbl_SY8125_3, text="1-24", width = 10, command = lambda: installation_card('SY8125', '703154'), bg = alarm_color)
SY8125_3.place(x=50, y=0)
SY8125_3_PC = Button(lbl_SY8125_3, text="ПК", width = 3, command = lambda: PC_card('PC16', '192.168.0.155', '703154'), bg = alarm_color)
SY8125_3_PC.place(x=10, y=0)
Hovertip(SY8125_3, ['SY8125', ' SN703154'])
Hovertip(SY8125_3_PC, ['Windows XP', 'IP 192.168.0.155'])

#Элементы стенда №17 SY8125 SN703152
alarm_color = button_color('703152')
lbl_SY8125_4 = LabelFrame(window, text = "17")
lbl_SY8125_4.place(x = 760, y=200, width = 150, heigh = 60)
SY8125_4 = Button(lbl_SY8125_4, text="1-24", width = 10, command = lambda: installation_card('SY8125', '703152'), bg = alarm_color)
SY8125_4.place(x=50, y=0)
SY8125_4_PC = Button(lbl_SY8125_4, text="ПК", width = 3, command = lambda: PC_card('PC17', '192.168.0.197', '703152'), bg = alarm_color)
SY8125_4_PC.place(x=10, y=0)
Hovertip(SY8125_4, ['SY8125', ' SN703152'])
Hovertip(SY8125_4_PC, ['Windows XP', 'IP 192.168.0.197'])

#Элементы стенда №18 SY8125 SN703153
alarm_color = button_color('703153')
lbl_SY8125_5 = LabelFrame(window, text = "18")
lbl_SY8125_5.place(x = 605, y=290, width = 150, heigh = 60)
SY8125_5 = Button(lbl_SY8125_5, text="1-24", width = 10, command = lambda: installation_card('SY8125', '703153'), bg = alarm_color)
SY8125_5.place(x=50, y=0)
SY8125_5_PC = Button(lbl_SY8125_5, text="ПК", width = 3, command = lambda: PC_card('PC18', '192.168.0.113', '703153'), bg = alarm_color)
SY8125_5_PC.place(x=10, y=0)
Hovertip(SY8125_5, ['SY8125', ' SN703153'])
Hovertip(SY8125_5_PC, ['Windows XP', 'IP 192.168.0.113'])

#Элементы стенда №19 SY8125 SN703151
alarm_color = button_color('703151')
lbl_SY8125_6 = LabelFrame(window, text = "19")
lbl_SY8125_6.place(x = 760, y=290, width = 150, heigh = 60)
SY8125_6 = Button(lbl_SY8125_6, text="1-24", width = 10, command = lambda: installation_card('SY8125', '703151'), bg = alarm_color)
SY8125_6.place(x=50, y=0)
SY8125_6_PC = Button(lbl_SY8125_6, text="ПК", width = 3, command = lambda: PC_card('PC19', '192.168.0.134', '703151'), bg = alarm_color)
SY8125_6_PC.place(x=10, y=0)
Hovertip(SY8125_5, ['SY8125', ' SN703151'])
Hovertip(SY8125_5_PC, ['Windows XP', 'IP 192.168.0.134'])

#Элементы стенда №20 CL3005-24 SN3035
alarm_color = button_color('3035')
lbl_CL3005_3 = LabelFrame(window, text = "20")
lbl_CL3005_3.place(x = 570, y=370, width = 250, heigh = 90)
CL3005_3_1 = Button(lbl_CL3005_3, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3035'), bg = alarm_color)
CL3005_3_1.place(x=40, y=15)
CL3005_3_2 = Button(lbl_CL3005_3, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3035'), bg = alarm_color)
CL3005_3_2.place(x=135, y=15)
CL3005_3_ST = Button(lbl_CL3005_3, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3035'), bg = alarm_color)
CL3005_3_ST.place(x=0, y=0)
CL3005_3_PC = Button(lbl_CL3005_3, text="ПК", width = 3, command = lambda: PC_card('PC20', '192.168.0.14','3035'), bg = alarm_color)
CL3005_3_PC.place(x=0, y=30)
Hovertip(CL3005_3_1, ['CL3005-24', ' SN3035'])
Hovertip(CL3005_3_2, ['CL3005-24', ' SN3035'])
Hovertip(CL3005_3_ST, ['CL3005-24', ' SN3035'])
Hovertip(CL3005_3_PC, ['Windows 7', 'IP 192.168.0.14'])

#Элементы стенда №21 CL3005-24 SN3036
alarm_color = button_color('3036')
lbl_CL3005_4 = LabelFrame(window, text = "21")
lbl_CL3005_4.place(x = 570, y=460, width = 250, heigh = 90)
CL3005_4_1 = Button(lbl_CL3005_4, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3036'), bg = alarm_color)
CL3005_4_1.place(x=0, y=15)
CL3005_4_2 = Button(lbl_CL3005_4, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3036'), bg = alarm_color)
CL3005_4_2.place(x=95, y=15)
CL3005_4_ST = Button(lbl_CL3005_4, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3036'), bg = alarm_color)
CL3005_4_ST.place(x=190, y=30)
CL3005_4_PC = Button(lbl_CL3005_4, text="ПК", width = 3, command = lambda: PC_card('PC21', '192.168.0.13','3036'), bg = alarm_color)
CL3005_4_PC.place(x=190, y=0)
Hovertip(CL3005_4_1, ['CL3005-24', ' SN3036'])
Hovertip(CL3005_4_2, ['CL3005-24', ' SN3036'])
Hovertip(CL3005_4_ST, ['CL3005-24', ' SN3036'])
Hovertip(CL3005_4_PC, ['Windows 7', 'IP 192.168.0.13'])

#Элементы стенда №22 CL3005-24 SN3032
alarm_color = button_color('3032')
lbl_CL3005_5 = LabelFrame(window, text = "22")
lbl_CL3005_5.place(x = 500, y=550, width = 250, heigh = 90)
CL3005_5_1 = Button(lbl_CL3005_5, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3032'), bg = alarm_color)
CL3005_5_1.place(x=50, y=15)
CL3005_5_2 = Button(lbl_CL3005_5, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3032'), bg = alarm_color)
CL3005_5_2.place(x=145, y=15)
CL3005_5_ST = Button(lbl_CL3005_5, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3032'), bg = alarm_color)
CL3005_5_ST.place(x=10, y=0)
CL3005_5_PC = Button(lbl_CL3005_5, text="ПК", width = 3, command = lambda: PC_card('PC22', '192.168.0.200','3032'), bg = alarm_color)
CL3005_5_PC.place(x=10, y=30)
Hovertip(CL3005_5_1, ['CL3005-24', ' SN3032'])
Hovertip(CL3005_5_2, ['CL3005-24', ' SN3032'])
Hovertip(CL3005_5_ST, ['CL3005-24', ' SN3032'])
Hovertip(CL3005_5_PC, ['Windows XP', 'IP 192.168.0.200'])

#Элементы стенда №23 CL1001-24 SN1015
alarm_color = button_color('1015')
lbl_CL1001_2 = LabelFrame(window, text = "23")
lbl_CL1001_2.place(x = 480, y=650, width = 220, heigh = 60)
CL1001_3_1 = Button(lbl_CL1001_2, text="1-12", width = 6, command = lambda: installation_card('CL1001','1015'), bg = alarm_color)
CL1001_3_1.place(x=90, y=0)
CL1001_3_2 = Button(lbl_CL1001_2, text="13-24", width = 6, command = lambda: installation_card('CL1001','1015'), bg = alarm_color)
CL1001_3_2.place(x=150, y=0)
CL1001_3_ST = Button(lbl_CL1001_2, text="Уст.", width = 3, command = lambda: installation_card('CL1001','1015'), bg = alarm_color)
CL1001_3_ST.place(x=10, y=0)
CL1001_3_PC = Button(lbl_CL1001_2, text="ПК", width = 3, command = lambda: PC_card('PC23', '192.168.0.100','1015'), bg = alarm_color)
CL1001_3_PC.place(x=50, y=0)
Hovertip(CL1001_3_1, ['CL1001-24', ' SN1015'])
Hovertip(CL1001_3_2, ['CL1001-24', ' SN1015'])
Hovertip(CL1001_3_ST, ['CL1001-24', ' SN1015'])
Hovertip(CL1001_3_PC, ['Windows 7', 'IP 192.168.0.100'])

#Элементы стенда №24 CL1005-48 SN1012
alarm_color = button_color('1012')
lbl_CL1005_1 = LabelFrame(window, text = "24")
lbl_CL1005_1.place(x = 480, y=720, width = 220, heigh = 60)
CL1005_1_1 = Button(lbl_CL1005_1, text="1-24", width = 6, command = lambda: installation_card('CL1001','1012'), bg = alarm_color)
CL1005_1_1.place(x=110, y=0)
CL1005_1_2 = Button(lbl_CL1005_1, text="13-48", width = 6, command = lambda: installation_card('CL1001','1012'), bg = alarm_color)
CL1005_1_2.place(x=10, y=0)
CL1005_1_ST = Button(lbl_CL1005_1, text="Уст.", width = 3, command = lambda: installation_card('CL1001','1012'), bg = alarm_color)
CL1005_1_ST.place(x=170, y=0)
CL1005_1_PC = Button(lbl_CL1005_1, text="ПК", width = 3, command = lambda: PC_card('PC24', '192.168.0.245','1012'), bg = alarm_color)
CL1005_1_PC.place(x=70, y=0)
Hovertip(CL1005_1_1, ['CL1005-48', ' SN1012'])
Hovertip(CL1005_1_2, ['CL1005-48', ' SN1012'])
Hovertip(CL1005_1_ST, ['CL1005-48', ' SN1012'])
Hovertip(CL1005_1_PC, ['Windows XP', 'IP 192.168.0.245'])

#Элементы стенда №25 CL3005-24 SN3044
alarm_color = button_color('3044')
lbl_CL3005_6 = LabelFrame(window, text = "25")
lbl_CL3005_6.place(x = 820, y=0, width = 250, heigh = 90)
CL3005_6_1 = Button(lbl_CL3005_6, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3044'), bg = alarm_color)
CL3005_6_1.place(x=40, y=15)
CL3005_6_2 = Button(lbl_CL3005_6, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3044'), bg = alarm_color)
CL3005_6_2.place(x=135, y=15)
CL3005_6_ST = Button(lbl_CL3005_6, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3044'), bg = alarm_color)
CL3005_6_ST.place(x=0, y=0)
CL3005_6_PC = Button(lbl_CL3005_6, text="ПК", width = 3, command = lambda: PC_card('PC25', '192.168.0.247','3044'), bg = alarm_color)
CL3005_6_PC.place(x=0, y=30)
Hovertip(CL3005_6_1, ['CL3005-24', ' SN3044'])
Hovertip(CL3005_6_2, ['CL3005-24', ' SN3044'])
Hovertip(CL3005_6_ST, ['CL3005-24', ' SN3044'])
Hovertip(CL3005_6_PC, ['Windows 7', 'IP 192.168.0.247'])

#Элементы стенда №26 SY8126 SN 704202
alarm_color = button_color('704202')
lbl_SY8126_1 = LabelFrame(window, text = "26")
lbl_SY8126_1.place(x = 970, y=200, width = 250, heigh = 90)
SY8126_1_1 = Button(lbl_SY8126_1, text="1-12", width = 10, command = lambda: installation_card('SY8126','704202'), bg = alarm_color)
SY8126_1_1.place(x=50, y=15)
SY8126_1_2 = Button(lbl_SY8126_1, text="13-24", width = 10, command = lambda: installation_card('SY8126','704202'), bg = alarm_color)
SY8126_1_2.place(x=145, y=15)
SY8126_1_ST = Button(lbl_SY8126_1, text="Уст.", width = 3, command = lambda: installation_card('SY8126','704202'), bg = alarm_color)
SY8126_1_ST.place(x=10, y=0)
SY8126_1_PC = Button(lbl_SY8126_1, text="ПК", width = 3, command = lambda: PC_card('PC26', '192.168.0.112','704202'), bg = alarm_color)
SY8126_1_PC.place(x=10, y=30)
Hovertip(SY8126_1_1, ['SY8126', ' 704202'])
Hovertip(SY8126_1_2, ['SY8126', ' 704202'])
Hovertip(SY8126_1_ST, ['SY8126', ' 704202'])
Hovertip(SY8126_1_PC, ['Windows XP', 'IP 192.168.0.112'])

#Элементы стенда №27 SY8126 SN704203
alarm_color = button_color('704203')
lbl_SY8126_2 = LabelFrame(window, text = "27")
lbl_SY8126_2.place(x = 970, y=300, width = 250, heigh = 90)
SY8126_2_1 = Button(lbl_SY8126_2, text="1-12", width = 10, command = lambda: installation_card('SY8126','704203'), bg = alarm_color)
SY8126_2_1.place(x=10, y=15)
SY8126_2_2 = Button(lbl_SY8126_2, text="13-24", width = 10, command = lambda: installation_card('SY8126','704203'), bg = alarm_color)
SY8126_2_2.place(x=105, y=15)
SY8126_2_ST = Button(lbl_SY8126_2, text="Уст.", width = 3, command = lambda: installation_card('SY8126','704203'), bg = alarm_color)
SY8126_2_ST.place(x=200, y=30)
SY8126_2_PC = Button(lbl_SY8126_2, text="ПК", width = 3, command = lambda: PC_card('PC27', '192.168.0.16','704203'), bg = alarm_color)
SY8126_2_PC.place(x=200, y=0)
Hovertip(SY8126_2_1, ['SY8126', ' SN704203'])
Hovertip(SY8126_2_2, ['SY8126', ' SN704203'])
Hovertip(SY8126_2_ST, ['SY8126', ' SN704203'])
Hovertip(SY8126_2_PC, ['Windows XP', 'IP 192.168.0.16'])

#Элементы стенда №28 SY8126 SN704205
alarm_color = button_color('704205')
lbl_SY8126_3 = LabelFrame(window, text = "28")
lbl_SY8126_3.place(x = 970, y=380, width = 250, heigh = 90)
SY8126_3_1 = Button(lbl_SY8126_3, text="1-12", width = 10, command = lambda: installation_card('SY8126','704205'), bg = alarm_color)
SY8126_3_1.place(x=50, y=15)
SY8126_3_2 = Button(lbl_SY8126_3, text="13-24", width = 10, command = lambda: installation_card('SY8126','704205'), bg = alarm_color)
SY8126_3_2.place(x=145, y=15)
SY8126_3_ST = Button(lbl_SY8126_3, text="Уст.", width = 3, command = lambda: installation_card('SY8126','704205'), bg = alarm_color)
SY8126_3_ST.place(x=10, y=0)
SY8126_3_PC = Button(lbl_SY8126_3, text="ПК", width = 3, command = lambda: PC_card('PC28', '192.168.0.101','704205'), bg = alarm_color)
SY8126_3_PC.place(x=10, y=30)
Hovertip(SY8126_3_1, ['SY8126', ' SN704205'])
Hovertip(SY8126_3_2, ['SY8126', ' SN704205'])
Hovertip(SY8126_3_ST, ['SY8126', ' SN704205'])
Hovertip(SY8126_3_PC, ['Windows XP', 'IP 192.168.0.101'])

#Элементы стенда №29 SY8126 SN704204
alarm_color = button_color('704204')
lbl_SY8126_2 = LabelFrame(window, text = "29")
lbl_SY8126_2.place(x = 970, y=480, width = 250, heigh = 90)
SY8126_2_1 = Button(lbl_SY8126_2, text="1-12", width = 10, command = lambda: installation_card('SY8126','704204'), bg = alarm_color)
SY8126_2_1.place(x=10, y=15)
SY8126_2_2 = Button(lbl_SY8126_2, text="13-24", width = 10, command = lambda: installation_card('SY8126','704204'), bg = alarm_color)
SY8126_2_2.place(x=105, y=15)
SY8126_2_ST = Button(lbl_SY8126_2, text="Уст.", width = 3, command = lambda: installation_card('SY8126','704204'), bg = alarm_color)
SY8126_2_ST.place(x=200, y=30)
SY8126_2_PC = Button(lbl_SY8126_2, text="ПК", width = 3, command = lambda: PC_card('PC29', '000.000.000.000','704204'), bg = alarm_color)
SY8126_2_PC.place(x=200, y=0)
Hovertip(SY8126_2_1, ['SY8126', ' SN704204'])
Hovertip(SY8126_2_2, ['SY8126', ' SN704204'])
Hovertip(SY8126_2_ST, ['SY8126', ' SN704204'])
Hovertip(SY8126_2_PC, ['Windows 10', 'нет данных'])

#Элементы стенда №30 CL3005-24 SN3030
alarm_color = button_color('3030')
lbl_CL3005_7 = LabelFrame(window, text = "30")
lbl_CL3005_7.place(x = 970, y=570, width = 250, heigh = 90)
CL3005_7_1 = Button(lbl_CL3005_7, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3030'), bg = alarm_color)
CL3005_7_1.place(x=50, y=15)
CL3005_7_2 = Button(lbl_CL3005_7, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3030'), bg = alarm_color)
CL3005_7_2.place(x=145, y=15)
CL3005_7_ST = Button(lbl_CL3005_7, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3030'), bg = alarm_color)
CL3005_7_ST.place(x=10, y=0)
CL3005_7_PC = Button(lbl_CL3005_7, text="ПК", width = 3, command = lambda: PC_card('PC30', '192.168.0.180','3030'), bg = alarm_color)
CL3005_7_PC.place(x=10, y=30)
Hovertip(CL3005_7_1, ['CL3005-24', ' SN3030'])
Hovertip(CL3005_7_2, ['CL3005-24', ' SN3030'])
Hovertip(CL3005_7_ST, ['CL3005-24', ' SN3030'])
Hovertip(CL3005_7_PC, ['Windows 7', 'IP 192.168.0.180'])

#Элементы стенда №31 CL3005-24 SN3029
alarm_color = button_color('3029')
lbl_CL3005_8 = LabelFrame(window, text = "31")
lbl_CL3005_8.place(x = 970, y=685, width = 250, heigh = 90)
CL3005_8_1 = Button(lbl_CL3005_8, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3029'), bg = alarm_color)
CL3005_8_1.place(x=10, y=15)
CL3005_8_2 = Button(lbl_CL3005_8, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3029'), bg = alarm_color)
CL3005_8_2.place(x=105, y=15)
CL3005_8_ST = Button(lbl_CL3005_8, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3029'), bg = alarm_color)
CL3005_8_ST.place(x=200, y=30)
CL3005_8_PC = Button(lbl_CL3005_8, text="ПК", width = 3, command = lambda: PC_card('PC31', '192.168.0.111','3029'), bg = alarm_color)
CL3005_8_PC.place(x=200, y=0)
Hovertip(CL3005_8_1, ['CL3005-24', 'SN3029'])
Hovertip(CL3005_8_2, ['CL3005-24', 'SN3029'])
Hovertip(CL3005_8_ST, ['CL3005-24', 'SN3029'])
Hovertip(CL3005_8_PC, ['Windows 7', 'IP 192.168.0.111'])

#Элементы стенда №32 Merkury_210 SN025
alarm_color = button_color('025')
lbl_Merkury_210 = LabelFrame(window, text = "32")
lbl_Merkury_210.place(x = 710, y=720, width = 60, heigh = 60)
Merkury_210 = Button(lbl_Merkury_210, text="1-6", width = 3, command = lambda: installation_card('Merkury_210','025'), bg = alarm_color)
Merkury_210.place(x=10, y=0)
Hovertip(Merkury_210, ['Merkury_210', 'SN025'])

#Элементы стенда №33 Merkury_210 SN018
alarm_color = button_color('018')
lbl_Merkury_210 = LabelFrame(window, text = "33")
lbl_Merkury_210.place(x = 780, y=720, width = 60, heigh = 60)
Merkury_210 = Button(lbl_Merkury_210, text="1-6", width = 3, command = lambda: installation_card('Merkury_210','018'), bg = alarm_color)
Merkury_210.place(x=10, y=0)
Hovertip(Merkury_210, ['Merkury_210', 'SN025'])

#Элементы стенда №34 Functional_3ph SN000001
alarm_color = button_color('000001')
lbl_Functional_3ph_1 = LabelFrame(window, text = "34")
lbl_Functional_3ph_1.place(x = 120, y=670, width = 90, heigh = 60)
Functional_3ph_1 = Button(lbl_Functional_3ph_1, text="1", width = 3, command = lambda: installation_card('Functional_3ph', '000001'), bg = alarm_color)
Functional_3ph_1.place(x=10, y=0)
Functional_3ph_PC_1 = Button(lbl_Functional_3ph_1, text="ПК", width = 3, command = lambda: PC_card('PC34', '192.168.194.19', '000001'), bg = alarm_color)
Functional_3ph_PC_1.place(x=50, y=00)
Hovertip(Functional_3ph_1, ['Functional_3ph', '000001'])
Hovertip(Functional_3ph_PC_1, ['Windows 7', 'IP 192.168.194.19'])

#Элементы стенда №35 Functional_3ph SN000002
alarm_color = button_color('000002')
lbl_Functional_3ph_2 = LabelFrame(window, text = "35")
lbl_Functional_3ph_2.place(x = 10, y=670, width = 90, heigh = 60)
Functional_3ph_2 = Button(lbl_Functional_3ph_2, text="1", width = 3, command = lambda: installation_card('Functional_3ph','000002'), bg = alarm_color)
Functional_3ph_2.place(x=10, y=0)
Functional_3ph_PC_2 = Button(lbl_Functional_3ph_2, text="ПК", width = 3, command = lambda: PC_card('PC35', '000.000.000.000','000002'), bg = alarm_color)
Functional_3ph_PC_2.place(x=50, y=00)
Hovertip(Functional_3ph_2, ['Functional_3ph', '000002'])
Hovertip(Functional_3ph_PC_2, ['Windows 7', 'IP 000.000.000.000'])

#Элементы стенда №36 Functional_1ph SN061101401
alarm_color = button_color('061101401')
lbl_Functional_1ph_1 = LabelFrame(window, text = "36")
lbl_Functional_1ph_1.place(x = 120, y=720, width = 90, heigh = 60)
Functional_1ph_1 = Button(lbl_Functional_1ph_1, text="1", width = 3, command = lambda: installation_card('Functional_1ph','061101401'), bg = alarm_color)
Functional_1ph_PC_3 = Button(lbl_Functional_1ph_1, text="ПК", width = 3, command = lambda: PC_card('PC36', '000.000.000.000','061101401'), bg = alarm_color)
Functional_1ph_PC_3.place(x=50, y=00)
Functional_1ph_1.place(x=10, y=0)
Hovertip(Functional_1ph_1, ['Functional_1ph', '061101401'])
Hovertip(Functional_1ph_PC_3, ['Windows 7', 'IP 000.000.000.000'])

#Элементы стенда №37 Functional_1ph SN000004
alarm_color = button_color('000004')
lbl_Functional_1ph_2 = LabelFrame(window, text = "37")
lbl_Functional_1ph_2.place(x = 10, y=720, width = 90, heigh = 60)
Functional_1ph_2 = Button(lbl_Functional_1ph_2, text="1", width = 3, command = lambda: installation_card('Functional_1ph','000004'), bg = alarm_color)
Functional_1ph_2.place(x=10, y=0)
Functional_1ph_2_PC_4 = Button(lbl_Functional_1ph_2, text="ПК", width = 3, command = lambda: PC_card('PC37', '000.000.000.000','000004'), bg = alarm_color)
Functional_1ph_2_PC_4.place(x=50, y=00)
Hovertip(Functional_1ph_2, ['Functional_1ph', '000004'])
Hovertip(Functional_1ph_2_PC_4, ['Windows 7', 'IP 000.000.000.000'])

window.mainloop()


