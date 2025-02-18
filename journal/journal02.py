#!/usr/bin/env python3

from tkinter import *  
from tkinter.ttk import Combobox, Radiobutton, Entry, Spinbox 
import tkinter.ttk as ttk
import datetime
from datetime import date
import ast
import winreg 
import psycopg2
from idlelib.tooltip import Hovertip
import subprocess
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

surnames = config['people']['engineers']
surnames = [element.strip("'[]") for element in surnames.split(", ")]

#Работа с буфером по клавишам Ctr-C, Ctr-V, Ctr-X
def _onKeyRelease(event):   
    ctrl = (event.state & 0x4) != 0
    if event.keycode==88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")
    if event.keycode==86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")
    if event.keycode==67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

def connect_database():
    #try:
    # Подключение к БД
    con = psycopg2.connect(
        database=config['data_base']['database'], 
        user=config['data_base']['user'], 
        password=config['data_base']['password'], 
        host=config['data_base']['host'], 
        port=config['data_base']['port'])
    print("Подключение к базе данных: ОК")
    #except:
    #    print("Не удалось подключиться к базе данных")


# Функция работы с комментариями по стендам
def comments(model, SN):
    connect_database()
    # Считывание комментариев по заданному SN
    try:
        cur = con.cursor()
        if SN == "ALL":
            cur.execute("SELECT date, time, author, commentary, serial_number, number_in_departament FROM public.comments ORDER BY (date, time) DESC;")
            rows = cur.fetchall()
        else:
            cur.execute("SELECT date, time, author, commentary FROM public.comments WHERE serial_number = \'%s\' ORDER BY (date, time) DESC;" %SN)
            rows = cur.fetchall()
        with open("comments.txt", 'w', encoding='utf-8') as f:
            for row in rows:
                f.write("\nДата: " + str(row[0]))
                f.write("\nВремя: " + str(row[1]))
                f.write("\nАвтор: " + str(row[2]))
                f.write("\nКомментарий: " + str(row[3]))
                f.write("\nСерийный: " + str(row[4]))
                f.write("\nПорядковый номер: " + str(row[5]))
                f.write("\n")
            con.close()
    except:
        print("Данные в таблице комментариев отсутствуют")
    subprocess.Popen("C:\\Windows\\notepad.exe D:\\myprogram\\bin\\journal\\comments.txt")

# Фукнция открытия карточки компьютера
def PC_card(model, SN, number_in_departament):
    window_card = Tk()
    window_card.bind_all("<Key>", _onKeyRelease, "+") 
    window_card.title("Карточка компьютера " + model)
    window_card.geometry("620x500")
    Label(window_card, text = ("Последние комментарии:")).place(x=10, y=90)
    text_card = Text(window_card, width=50, height=10)
    text_card.place(x=10, y=110)
    text_card.bind("<Button-3>")
    SUBD_get_PC(model, window_card, text_card, SN)
    Label(window_card, text = ("Ваш комментарий:")).place(x=10, y=300)
    text_wr = Text(window_card, width=50, height=5)
    text_wr.place(x=10, y=320)
    text_wr.bind("<Button-3>")
    Label(window_card, text = ("Новый IP:")).place(x=480, y=190)
    IP_new = Text(window_card, width=13, height=1)
    IP_new.place(x=480, y=215)
    IP_new.insert(1.0, '192.168.0.0')
    poverka_wr = Button(window_card, text="Записать", command = lambda: SUBD_push_one(window_card, IP_new, SN, model, pc))
    poverka_wr.place(x=490, y=240)
    btn_wr = Button(window_card, text="Отправить", command = lambda: SUBD_push(window_card, text_wr, model, combo, sel.get(), text_card, number_in_departament))
    btn_wr.place(x=350, y=420)
    lbl01 = Label(window_card, text = "Выберите фамилию:").place(x=10, y=420)
    combo = Combobox(window_card, width = 13, values = surnames)
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
def SUBD_get_PC(model, window_card, text_card, SN):
    connect_database()
    try:
    # Считывание данных ПК из таблицы pc
        cur = con.cursor()
        cur.execute("SELECT serial_number, name_pc, ip, alarms, radmin, windows, net_monitor, inkotex, other_soft FROM public.pc WHERE serial_number = \'%s\';" %SN)
        rows = cur.fetchall()
        for row in rows:
            Label(window_card, text = ("СН установки: " + row[0])).place(x=10, y=25)
            name_PC = row[1]
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
            btn_radmin.place(x=490, y=110)
            btn_ping = Button(window_card, text="Ping", command = lambda: subprocess.Popen('C:\\windows\\system32\\ping.exe %s '%ip_ad))
            btn_ping.place(x=490, y=145)
    except:
        Label(window_card, text = "Данные в таблице установок отсутсвуют!!!", foreground = 'red').place(x=10, y=25)

    try:
        # Считывание комментариев по данному компьютеру
        cur.execute("SELECT date, time, author, commentary FROM public.comments WHERE serial_number = \'%s\' ORDER BY (date, time);" %model)
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
def installation_card(model, SN, number_in_departament):
    window_card = Tk()
    window_card.bind_all("<Key>", _onKeyRelease, "+") 
    window_card.title("Карточка стенда " + model + "   SN " + SN)
    window_card.geometry("620x500")
    Label(window_card, text = ("Последние комментарии:")).place(x=10, y=90)
    text_card = Text(window_card, width=50, height=10)
    text_card.place(x=10, y=110)
    print('Im here')
    SUBD_get(window_card, text_card, SN)
    Label(window_card, text = ("Ваш комментарий:")).place(x=10, y=300)
    text_wr = Text(window_card, width=50, height=5)
    text_wr.place(x=10, y=320)
    Label(window_card, text = ("Новая дата:")).place(x=480, y=190)
    poverka_text = Text(window_card, width=10, height=1)
    poverka_text.place(x=480, y=215)
    poverka_text.insert(1.0, 'ГГГГ-ММ-ДД')
    poverka_wr = Button(window_card, text="Записать", command = lambda: SUBD_push_one(window_card, poverka_text, SN, number_in_departament, installations))
    poverka_wr.place(x=490, y=240)
    btn_wr = Button(window_card, text="Отправить", command = lambda: SUBD_push(window_card, text_wr, SN, combo, sel.get(), text_card, number_in_departament))
    btn_wr.place(x=350, y=420)
    lbl01 = Label(window_card, text = "Выберите фамилию:").place(x=10, y=420)
    combo = Combobox(window_card, width = 13, values = surnames)
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
        

# Функция записи комментариев в БД (установки)
def SUBD_push(window_card, text_wr, SN, combo, alarms, text_card, number_in_departament):
    connect_database()
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
        cur.execute("INSERT INTO public.comments (date, author, commentary, serial_number, time, alarms, number_in_departament) VALUES (%s, %s, %s, %s, %s, %s, %s);", (date, author, comment, SN, time, alarms, number_in_departament))
        if 'PC' in SN:
            cur.execute("UPDATE public.pc SET alarms=%s WHERE name_pc = %s; ", (alarms, SN))
        else:    
            cur.execute("UPDATE public.installations SET alarms=%s WHERE serial_number = %s; ", (alarms, SN))
        con.commit() 
        Label(window_card, text = "Данные успешно записаны!!!", foreground = 'green').place(x=10, y=450)
        #Считывание (обновление) данных в поле комментариев
        text_card.delete(1.0, END)
        cur.execute("SELECT date, time, author, commentary FROM public.comments WHERE serial_number = \'%s\' ORDER BY (date, time);" %SN)
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
    
# Функция записи даты поверки (и других одиночных полей)
def SUBD_push_one(window_card, data_bd, SN, number_in_departament, table):
    connect_database()
    try:
        #Запись комментария в таблицу БД
        date_usr =  data_bd.get(1.0, END).strip()
        if date_usr == "ГГГГ-ММ-ДД":
            Label(window_card, text = "Введите дату", foreground = 'red').place(x=480, y=270)
        else:
            try:
                date(int(date_usr[0:4]),int(date_usr[5:7]),int(date_usr[8:10]))
                Label(window_card, text = "Формат ок", foreground = 'green').place(x=480, y=270)
                cur = con.cursor()
                cur.execute("UPDATE public.installations SET poverka_date=%s WHERE serial_number = %s; ", (date_usr, SN))
                con.commit() 
                con.close()
                Label(window_card, text = "Дата записана", foreground = 'green').place(x=480, y=270)
            except:
                Label(window_card, text = "Не формат!", foreground = 'red').place(x=480, y=270)
        
    except:
        Label(window_card, text = "Не удалось записать данные в базу данных!!!", foreground = 'red').place(x=10, y=450)
        
       
# Функция получения данных из базы по установке
def SUBD_get(window_card, text_card, SN):
    connect_database()

    try:
        #Считывание данных установки из таблицы установок
        cur = con.cursor()
        cur.execute("SELECT serial_number, model, phases, alarms, inkotex, calibrovka, poverka, poverka_date FROM public.installations WHERE serial_number = \'%s\';" %SN)
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
            Label(window_card, text = ("Дата поверки \n счетчика: \n" + str(row[7]))).place(x=480, y=130)
    except:
        Label(window_card, text = "Данные в таблице установок отсутсвуют!!!", foreground = 'red').place(x=10, y=25)

    try:
        # Считывание комментариев по данной установке
        cur.execute("SELECT date, time, author, commentary FROM public.comments WHERE serial_number = \'%s\' ORDER BY (date, time), time;" %SN)
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

def button_color(SN, name_pc):
    try:
        connect_database()
        cur = con.cursor()
        cur.execute("SELECT alarms, (poverka_date - current_date) as poverka_days FROM public.installations WHERE serial_number = \'%s\';" %SN)
        rows = cur.fetchall()
        for row in rows:
            problems = row[0]
            poverka_days = row[1]
        
        if problems == "work":
            button_c = ('#D3D3D3')
        elif problems == "not_work":
            button_c = ('#FF0000')
        elif problems == "is_problems":
            button_c = ('#FFA500')
        else:
            button_c = ('#D3D3D3')
        if poverka_days >= 7:
            poverka_c = 'green'
        elif poverka_days > 0:
            poverka_c = 'orange'
        elif poverka_days <= 0:
            poverka_c = 'red'
        else:
            poverka_c = 'black'
        cur.execute("SELECT alarms FROM public.pc WHERE name_pc = \'%s\';" %name_pc)
        rows = cur.fetchall()
        for row in rows:
            problems = row[0]
        if problems == "work":
            button_pc = ('#D3D3D3')
        elif problems == "not_work":
            button_pc = ('#FF0000')
        elif problems == "is_problems":
            button_pc = ('#FFA500')
        else:
            button_pc = ('#D3D3D3')
        con.close()
        return(button_c, poverka_days, poverka_c, button_pc)
    except:
        Label(window, text = "Не удалось получить данные из базы данных!!!", bg = 'red').place(x=25, y=760)
   

#Main program
window = Tk()  
window.title("Виртуальный цех        (by Jamigo)")  
window.geometry('1400x800')
#Включаем подержку нажатий клавиш Ctr-C, Ctr-V, Ctr-X
window.bind_all("<Key>", _onKeyRelease, "+") 

#Дополнительные кнопки 
commentas = Button(window, text="Все комменты", width = 13, command = lambda: comments('080798', 'ALL'))
commentas.place(x=1270, y=20)
scheme_office_1 = Button(window, text="Схема стек.", width = 13, command = lambda: subprocess.Popen("C:\\Program Files\\OpenOffice 4\\program\\sdraw.exe D:\\myprogram\\bin\\journal\\scheme1.odg"))
scheme_office_1.place(x=1270, y=50)
scheme_office_2 = Button(window, text="Схема A2", width = 13, command = lambda: subprocess.Popen("C:\\Program Files\\OpenOffice 4\\program\\sdraw.exe D:\\myprogram\\bin\\journal\\scheme2.odg"))
scheme_office_2.place(x=1270, y=80)
history = Button(window, text="Изменения ПО", width = 13, command = lambda: subprocess.Popen("C:\\Windows\\notepad.exe D:\\myprogram\\bin\\journal\\history.txt"))
history.place(x=1270, y=110)
programs = Button(window, text="Программы", width = 13, command = lambda: subprocess.Popen("C:\\Windows\\explorer.exe D:\\MyProgram\\BIN\\dist"))
programs.place(x=1270, y=140)

#Элементы для лучшей визуализации
Right_wall = Canvas(window, width=10, height=1000, bg = 'green').place(x=1230, y=5)

#Элементы стенда №1 HX-8100 SN 080798
alarm_color = button_color('080798', 'PC1')
lbl_HX8100_3 = LabelFrame(window, text = "1 HX_1ф")
lbl_HX8100_3.place(x = 20, y=120, width = 250, heigh = 60)
HX8100_3_1 = Button(lbl_HX8100_3, text="1-48", width = 10, command = lambda: installation_card('HX8100','080798', '1'), bg = alarm_color[0])
HX8100_3_1.place(x=10, y=0)
HX8100_3_2 = Button(lbl_HX8100_3, text="49-96", width = 10, command = lambda: installation_card('HX8100','080798', '1'), bg = alarm_color[0])
HX8100_3_2.place(x=105, y=0)
HX8100_3_PC = Button(lbl_HX8100_3, text="ПК", width = 3, command = lambda: PC_card('PC1', '080798', '1'), bg = alarm_color[3])
HX8100_3_PC.place(x=200, y=0)
Hovertip(HX8100_3_1, ['HX-8100', ' SN080798'])
Hovertip(HX8100_3_2, ['HX-8100', ' SN080798'])
Hovertip(HX8100_3_PC, ['Windows XP', 'IP 192.168.0.202'])

#Элементы стенда №2 HX-8100_2
alarm_color = button_color('080799', 'PC2')
lbl_HX8100_2 = LabelFrame(window, text = "2 HX_1ф")
lbl_HX8100_2.place(x = 20, y=280, width = 250, heigh = 60)
HX8100_2_1 = Button(lbl_HX8100_2, text="1-48", width = 10, command = lambda: installation_card('HX8100', '080799', '2'), bg = alarm_color[0])
HX8100_2_1.place(x=50, y=0)
HX8100_2_2 = Button(lbl_HX8100_2, text="49-96", width = 10, command = lambda: installation_card('HX8100', '080799', '2'), bg = alarm_color[0])
HX8100_2_2.place(x=145, y=0)
HX8100_2_PC = Button(lbl_HX8100_2, text="ПК", width = 3, command = lambda: PC_card('PC2', '080799', '2'), bg = alarm_color[3])
HX8100_2_PC.place(x=10, y=0)
Hovertip(HX8100_2_1, ['HX-8100', ' SN080799'])
Hovertip(HX8100_2_2, ['HX-8100', ' SN080799'])
Hovertip(HX8100_2_PC, ['Windows XP', 'IP 192.168.0.163'])

#Элементы стенда №3 SY8125 SN703143
alarm_color = button_color('703143', 'PC3')
lbl_SY8125_1 = LabelFrame(window, text = "3 SY_1ф")
lbl_SY8125_1.place(x = 20, y=380, width = 150, heigh = 90)
poverka_SY8125_1 = Label(lbl_SY8125_1, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_SY8125_1.place(x=45, y=30)
SY8125_1 = Button(lbl_SY8125_1, text="1-24", width = 15, command = lambda: installation_card('SY8125', '703143', '3'), bg = alarm_color[0])
SY8125_1.place(x=10, y=0)
SY8125_1_PC = Button(lbl_SY8125_1, text="ПК", width = 3, command = lambda: PC_card('PC3', '703143', '3'), bg = alarm_color[3])
SY8125_1_PC.place(x=10, y=30)
Hovertip(SY8125_1, ['SY8125', ' SN703143'])
Hovertip(SY8125_1_PC, ['Windows XP', 'IP 192.168.0.242'])

#Элементы стенда №4 SY8125 SN703146
alarm_color = button_color('703146', 'PC4')
lbl_SY8125_2 = LabelFrame(window, text = "4 SY_1ф")
lbl_SY8125_2.place(x = 20, y=470, width = 150, heigh = 90)
poverka_SY8125_2 = Label(lbl_SY8125_2, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_SY8125_2.place(x=45, y=0)
SY8125_2 = Button(lbl_SY8125_2, text="1-24", width = 15, command = lambda: installation_card('SY8125', '703146', '4'), bg = alarm_color[0])
SY8125_2.place(x=10, y=30)
SY8125_2_PC = Button(lbl_SY8125_2, text="ПК", width = 3, command = lambda: PC_card('PC4', '703146', '4'), bg = alarm_color[3])
SY8125_2_PC.place(x=10, y=0)
Hovertip(SY8125_2, ['SY8125', ' SN703146'])
Hovertip(SY8125_2_PC, ['Windows XP', 'IP 192.168.0.97'])

#Элементы стенда №5 УАПС-1М SN000000
alarm_color = button_color('000000', 'PC5')
lbl_UAPS1M_5 = LabelFrame(window, text = "5 УАПС")
lbl_UAPS1M_5.place(x = 270, y=0, width = 80, heigh = 85)
UAPS1M_5 = Button(lbl_UAPS1M_5, text="Уст.", width = 3, command = lambda: installation_card('UAPS-1M', '000000', '5'), bg = alarm_color[0])
UAPS1M_5.place(x=20, y=00)
UAPS1M_5_1 = Button(lbl_UAPS1M_5, text="1-6", width = 3, command = lambda: installation_card('UAPS-1M', '000000', '5'), bg = alarm_color[0])
UAPS1M_5_1.place(x=40, y=30)
Hovertip(UAPS1M_5, ['УАПС-1М', ' SN000000'])
Hovertip(UAPS1M_5_1, ['УАПС-1М', ' SN000000'])

#Элементы стенда №6 УАПС-1М SN102
alarm_color = button_color('102', 'PC6')
lbl_UAPS1M_6 = LabelFrame(window, text = "6 УАПС")
lbl_UAPS1M_6.place(x = 350, y=0, width = 80, heigh = 85)
UAPS1M_6 = Button(lbl_UAPS1M_6, text="Уст.", width = 3, command = lambda: installation_card('UAPS-1M', '102', '6'), bg = alarm_color[0])
UAPS1M_6.place(x=20, y=00)
UAPS1M_6_1 = Button(lbl_UAPS1M_6, text="1-6", width = 3, command = lambda: installation_card('UAPS-1M', '102', '6'), bg = alarm_color[0])
UAPS1M_6_1.place(x=40, y=30)
UAPS1M_6_PC = Button(lbl_UAPS1M_6, text="ПК", width = 3, command = lambda: PC_card('PC6', '102', '6'), bg = alarm_color[3])
UAPS1M_6_PC.place(x=0, y=30)
Hovertip(UAPS1M_6, ['УАПС-1М', 'SN102'])
Hovertip(UAPS1M_6_1, ['УАПС-1М', 'SN102'])
Hovertip(UAPS1M_6_PC, ['Windows XP', 'IP 192.168.0.169'])

#Элементы стенда №7 УАПС-1М SN61207
alarm_color = button_color('61207', 'PC7')
lbl_UAPS1M_7 = LabelFrame(window, text = "7 УАПС")
lbl_UAPS1M_7.place(x = 440, y=0, width = 80, heigh = 85)
UAPS1M_7 = Button(lbl_UAPS1M_7, text="Уст.", width = 3, command = lambda: installation_card('UAPS-1M', '61207', '7'), bg = alarm_color[0])
UAPS1M_7.place(x=20, y=00)
UAPS1M_7_1 = Button(lbl_UAPS1M_7, text="1-6", width = 3, command = lambda: installation_card('UAPS-1M', '61207', '7'), bg = alarm_color[0])
UAPS1M_7_1.place(x=40, y=30)
UAPS1M_7_PC = Button(lbl_UAPS1M_7, text="ПК", width = 3, command = lambda: PC_card('PC7', '61207', '7'), bg = alarm_color[3])
UAPS1M_7_PC.place(x=0, y=30)
Hovertip(UAPS1M_7, ['УАПС-1М', 'SN61207'])
Hovertip(UAPS1M_7_1, ['УАПС-1М', 'SN61207'])
Hovertip(UAPS1M_7_PC, ['Windows XP', 'IP 192.168.0.37'])

#Элементы стенда №8 УАПС-1М SN109
alarm_color = button_color('109', 'PC8')
lbl_UAPS1M_8 = LabelFrame(window, text = "8 УАПС")
lbl_UAPS1M_8.place(x = 640, y=0, width = 80, heigh = 85)
UAPS1M_8 = Button(lbl_UAPS1M_8, text="Уст.", width = 3, command = lambda: installation_card('UAPS-1M', '109', '8'), bg = alarm_color[0])
UAPS1M_8.place(x=20, y=00)
UAPS1M_8_1 = Button(lbl_UAPS1M_8, text="1-6", width = 3, command = lambda: installation_card('UAPS-1M', '109', '8'), bg = alarm_color[0])
UAPS1M_8_1.place(x=40, y=30)
UAPS1M_8_PC = Button(lbl_UAPS1M_8, text="ПК", width = 3, command = lambda: PC_card('PC8', '109', '8'), bg = alarm_color[3])
UAPS1M_8_PC.place(x=0, y=30)
Hovertip(UAPS1M_8, ['УАПС-1М', 'SN109'])
Hovertip(UAPS1M_8_1, ['УАПС-1М', 'SN109'])
Hovertip(UAPS1M_8_PC, ['Windows 98', 'IP 192.168.0.17'])

#Элементы стенда №9 УАПС-1М SN050908
alarm_color = button_color('050908', 'PC9')
lbl_UAPS1M_9 = LabelFrame(window, text = "9 УАПС")
lbl_UAPS1M_9.place(x = 730, y=0, width = 80, heigh = 85)
UAPS1M_9 = Button(lbl_UAPS1M_9, text="Уст.", width = 3, command = lambda: installation_card('UAPS-1M', '050908', '9'), bg = alarm_color[0])
UAPS1M_9.place(x=20, y=00)
UAPS1M_9_1 = Button(lbl_UAPS1M_9, text="1-6", width = 3, command = lambda: installation_card('UAPS-1M', '050908', '9'), bg = alarm_color[0])
UAPS1M_9_1.place(x=40, y=30)
UAPS1M_9_PC = Button(lbl_UAPS1M_9, text="ПК", width = 3, command = lambda: PC_card('PC9', '050908', '9'), bg = alarm_color[3])
UAPS1M_9_PC.place(x=0, y=30)
Hovertip(UAPS1M_9, ['УАПС-1М', 'SN050908'])
Hovertip(UAPS1M_9_1, ['УАПС-1М', 'SN050908'])
Hovertip(UAPS1M_9_PC, ['Windows XP', 'IP 192.168.0.40'])

#Элементы стенда №10 HX8300 SN0807102
alarm_color = button_color('0807102', 'PC10')
lbl_HX8300_10 = LabelFrame(window, text = "10 HX_3ф")
lbl_HX8300_10.place(x = 350, y=120, width = 50, heigh = 320)
HX8300_10_1 = Button(lbl_HX8300_10, text="1-\n24", width = 3, height = 3, command = lambda: installation_card('HX8300','0807102', '10'), bg = alarm_color[0])
HX8300_10_1.place(x=5, y=30)
HX8300_10_2 = Button(lbl_HX8300_10, text="25-\n48", width = 3, height = 3, command = lambda: installation_card('HX8300','0807102', '10'), bg = alarm_color[0])
HX8300_10_2.place(x=5, y=95)
HX8300_10_3 = Button(lbl_HX8300_10, text="49-\n72", width = 3, height = 3, command = lambda: installation_card('HX8300','0807102', '10'), bg = alarm_color[0])
HX8300_10_3.place(x=5, y=160)
HX8300_10_4 = Button(lbl_HX8300_10, text="73-\n96", width = 3, height = 3, command = lambda: installation_card('HX8300','0807102', '10'), bg = alarm_color[0])
HX8300_10_4.place(x=5, y=225)
HX8300_10_PC = Button(lbl_HX8300_10, text="ПК", width = 3, command = lambda: PC_card('PC10','0807102', '10'), bg = alarm_color[3])
HX8300_10_PC.place(x=5, y=0)
Hovertip(HX8300_10_1, ['HX-8300', ' SN0807102'])
Hovertip(HX8300_10_2, ['HX-8300', ' SN0807102'])
Hovertip(HX8300_10_3, ['HX-8300', ' SN0807102'])
Hovertip(HX8300_10_4, ['HX-8300', ' SN0807102'])
Hovertip(HX8300_10_PC, ['Windows 7', 'IP 192.168.0.43'])

#Элементы стенда №11 HX8300 SN0807103
alarm_color = button_color('0807103', 'PC11')
lbl_HX8300_11 = LabelFrame(window, text = "11 HX_3ф")
lbl_HX8300_11.place(x = 350, y=440, width = 50, heigh = 320)
HX8300_11_1 = Button(lbl_HX8300_11, text="1-\n24", width = 3, height = 3, command = lambda: installation_card('HX8300','0807103', '11'), bg = alarm_color[0])
HX8300_11_1.place(x=5, y=30)
HX8300_11_2 = Button(lbl_HX8300_11, text="25-\n48", width = 3, height = 3, command = lambda: installation_card('HX8300','0807103', '11'), bg = alarm_color[0])
HX8300_11_2.place(x=5, y=95)
HX8300_11_3 = Button(lbl_HX8300_11, text="49-\n72", width = 3, height = 3, command = lambda: installation_card('HX8300','0807103', '11'), bg = alarm_color[0])
HX8300_11_3.place(x=5, y=160)
HX8300_11_4 = Button(lbl_HX8300_11, text="73-\n96", width = 3, height = 3, command = lambda: installation_card('HX8300','0807103', '11'), bg = alarm_color[0])
HX8300_11_4.place(x=5, y=225)
HX8300_11_PC = Button(lbl_HX8300_11, text="ПК", width = 3, command = lambda: PC_card('PC11','0807103', '11'), bg = alarm_color[3])
HX8300_11_PC.place(x=5, y=0)
Hovertip(HX8300_11_1, ['HX-8300', ' SN0807103'])
Hovertip(HX8300_11_2, ['HX-8300', ' SN0807103'])
Hovertip(HX8300_11_3, ['HX-8300', ' SN0807103'])
Hovertip(HX8300_11_4, ['HX-8300', ' SN0807103'])
Hovertip(HX8300_11_PC, ['Windows XP', 'IP нет данных'])

#Элементы стенда №12 CL3005-24 SN3028
alarm_color = button_color('3028', 'PC12')
lbl_CL3005_1 = LabelFrame(window, text = "12 CL_3ф")
lbl_CL3005_1.place(x = 420, y=100, width = 250, heigh = 90)
poverka_CL3005_1 = Label(lbl_CL3005_1, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_CL3005_1.place(x=10, y=10)
CL3005_1_1 = Button(lbl_CL3005_1, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3028', '12'), bg = alarm_color[0])
CL3005_1_1.place(x=10, y=30)
CL3005_1_2 = Button(lbl_CL3005_1, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3028', '12'), bg = alarm_color[0])
CL3005_1_2.place(x=105, y=30)
CL3005_1_ST = Button(lbl_CL3005_1, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3028', '12'), bg = alarm_color[0])
CL3005_1_ST.place(x=200, y=30)
CL3005_1_PC = Button(lbl_CL3005_1, text="ПК", width = 3, command = lambda: PC_card('PC12','3028', '12'), bg = alarm_color[3])
CL3005_1_PC.place(x=200, y=0)
Hovertip(CL3005_1_1, ['CL3005-24', ' SN3028'])
Hovertip(CL3005_1_2, ['CL3005-24', ' SN3028'])
Hovertip(CL3005_1_ST, ['CL3005-24', ' SN3028'])
Hovertip(CL3005_1_PC, ['Windows 7', 'IP 192.168.0.185'])

#Элементы стенда №13 CL3005-24 SN3042
alarm_color = button_color('3042', 'PC13')
lbl_CL3005_2 = LabelFrame(window, text = "13 CL_3ф")
lbl_CL3005_2.place(x = 670, y=100, width = 250, heigh = 90)
poverka_CL3005_2 = Label(lbl_CL3005_2, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_CL3005_2.place(x=10, y=10)
CL3005_2_1 = Button(lbl_CL3005_2, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3042', '13'), bg = alarm_color[0])
CL3005_2_1.place(x=10, y=30)
CL3005_2_2 = Button(lbl_CL3005_2, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3042', '13'), bg = alarm_color[0])
CL3005_2_2.place(x=105, y=30)
CL3005_2_ST = Button(lbl_CL3005_2, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3042', '13'), bg = alarm_color[0])
CL3005_2_ST.place(x=200, y=30)
CL3005_2_PC = Button(lbl_CL3005_2, text="ПК", width = 3, command = lambda: PC_card('PC13','3042', '13'), bg = alarm_color[3])
CL3005_2_PC.place(x=200, y=0)
Hovertip(CL3005_2_1, ['CL3005-24', ' SN3042'])
Hovertip(CL3005_2_1, ['CL3005-24', ' SN3042'])
Hovertip(CL3005_2_ST, ['CL3005-24', ' SN3042'])
Hovertip(CL3005_2_PC, ['Windows 7', 'IP 192.168.0.253'])

#Элементы стенда №14 CL1001 SN1009
alarm_color = button_color('1009', 'PC14')
lbl_CL1001_1 = LabelFrame(window, text = "14 CL_1ф")
lbl_CL1001_1.place(x = 450, y=190, width = 150, heigh = 90)
poverka_CL1001_1 = Label(lbl_CL1001_1, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_CL1001_1.place(x=45, y=30)
CL1001_1_1 = Button(lbl_CL1001_1, text="1-24", width = 10, command = lambda: installation_card('CL1001','1009', '14'), bg = alarm_color[0])
CL1001_1_1.place(x=50, y=0)
CL1001_1_ST = Button(lbl_CL1001_1, text="Уст.", width = 3, command = lambda: installation_card('CL1001','1009', '14'), bg = alarm_color[0])
CL1001_1_ST.place(x=10, y=0)
CL1001_1_PC = Button(lbl_CL1001_1, text="ПК", width = 3, command = lambda: PC_card('PC14','1009', '14'), bg = alarm_color[3])
CL1001_1_PC.place(x=10, y=30)
Hovertip(CL1001_1_1, ['CL3005-24', ' SN1009'])
Hovertip(CL1001_1_ST, ['CL3005-24', ' SN1009'])
Hovertip(CL1001_1_PC, ['Windows XP', 'IP 192.168.0.201'])

#Элементы стенда №15 CL1001 SN1008
alarm_color = button_color('1008', 'PC15')
lbl_CL1001_2 = LabelFrame(window, text = "15 CL_1ф")
lbl_CL1001_2.place(x = 450, y=280, width = 150, heigh = 90)
poverka_CL1001_2 = Label(lbl_CL1001_2, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_CL1001_2.place(x=10, y=10)
CL1001_2_1 = Button(lbl_CL1001_2, text="1-24", width = 10, command = lambda: installation_card('CL1001','1008', '15'), bg = alarm_color[0])
CL1001_2_1.place(x=10, y=30)
CL1001_2_ST = Button(lbl_CL1001_2, text="Уст.", width = 3, command = lambda: installation_card('CL1001','1008', '15'), bg = alarm_color[0])
CL1001_2_ST.place(x=110, y=30)
CL1001_2_PC = Button(lbl_CL1001_2, text="ПК", width = 3, command = lambda: PC_card('PC15','1008', '15'), bg = alarm_color[3])
CL1001_2_PC.place(x=110, y=0)
Hovertip(CL1001_2_1, ['CL3005-24', ' SN1008'])
Hovertip(CL1001_2_ST, ['CL3005-24', ' SN1008'])
Hovertip(CL1001_2_PC, ['Windows XP', 'IP 192.168.0.47'])

#Элементы стенда №16 SY8125 SN703154
alarm_color = button_color('703154', 'PC16')
lbl_SY8125_3 = LabelFrame(window, text = "16 SY_1ф")
lbl_SY8125_3.place(x = 605, y=190, width = 150, heigh = 80)
poverka_SY8125_3 = Label(lbl_SY8125_3, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_SY8125_3.place(x=0, y=30)
SY8125_3 = Button(lbl_SY8125_3, text="1-24", width = 10, command = lambda: installation_card('SY8125', '703154', '16'), bg = alarm_color[0])
SY8125_3.place(x=50, y=0)
SY8125_3_PC = Button(lbl_SY8125_3, text="ПК", width = 3, command = lambda: PC_card('PC16', '703154', '16'), bg = alarm_color[3])
SY8125_3_PC.place(x=10, y=0)
Hovertip(SY8125_3, ['SY8125', ' SN703154'])
Hovertip(SY8125_3_PC, ['Windows XP', 'IP 192.168.0.155'])

#Элементы стенда №17 SY8125 SN703152
alarm_color = button_color('703152', 'PC17')
lbl_SY8125_4 = LabelFrame(window, text = "17 SY_1ф")
lbl_SY8125_4.place(x = 760, y=190, width = 150, heigh = 80)
poverka_SY8125_4 = Label(lbl_SY8125_4, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_SY8125_4.place(x=0, y=30)
SY8125_4 = Button(lbl_SY8125_4, text="1-24", width = 10, command = lambda: installation_card('SY8125', '703152', '17'), bg = alarm_color[0])
SY8125_4.place(x=50, y=0)
SY8125_4_PC = Button(lbl_SY8125_4, text="ПК", width = 3, command = lambda: PC_card('PC17', '703152', '17'), bg = alarm_color[3])
SY8125_4_PC.place(x=10, y=0)
Hovertip(SY8125_4, ['SY8125', ' SN703152'])
Hovertip(SY8125_4_PC, ['Windows XP', 'IP 192.168.0.12'])

#Элементы стенда №18 SY8125 SN703153
alarm_color = button_color('703153', 'PC18')
lbl_SY8125_5 = LabelFrame(window, text = "18 SY_1ф")
lbl_SY8125_5.place(x = 605, y=285, width = 150, heigh = 85)
poverka_SY8125_5 = Label(lbl_SY8125_5, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_SY8125_5.place(x=50, y=10)
SY8125_5 = Button(lbl_SY8125_5, text="1-24", width = 10, command = lambda: installation_card('SY8125', '703153', '18'), bg = alarm_color[0])
SY8125_5.place(x=50, y=30)
SY8125_5_PC = Button(lbl_SY8125_5, text="ПК", width = 3, command = lambda: PC_card('PC18', '703153', '18'), bg = alarm_color[3])
SY8125_5_PC.place(x=10, y=30)
Hovertip(SY8125_5, ['SY8125', ' SN703153'])
Hovertip(SY8125_5_PC, ['Windows XP', 'IP 192.168.0.113'])

#Элементы стенда №19 SY8125 SN703151
alarm_color = button_color('703151', 'PC19')
lbl_SY8125_6 = LabelFrame(window, text = "19 SY_1ф")
lbl_SY8125_6.place(x = 760, y=285, width = 150, heigh = 85)
poverka_SY8125_6 = Label(lbl_SY8125_6, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_SY8125_6.place(x=50, y=10)
SY8125_6 = Button(lbl_SY8125_6, text="1-24", width = 10, command = lambda: installation_card('SY8125', '703151', '19'), bg = alarm_color[0])
SY8125_6.place(x=10, y=30)
SY8125_6_PC = Button(lbl_SY8125_6, text="ПК", width = 3, command = lambda: PC_card('PC19', '703151', '19'), bg = alarm_color[3])
SY8125_6_PC.place(x=105, y=30)
Hovertip(SY8125_5, ['SY8125', ' SN703151'])
Hovertip(SY8125_5_PC, ['Windows XP', 'IP 192.168.0.134'])

#Элементы стенда №20 CL3005-24 SN3035
alarm_color = button_color('3035', 'PC20')
lbl_CL3005_3 = LabelFrame(window, text = "20 CL_3ф")
lbl_CL3005_3.place(x = 570, y=370, width = 250, heigh = 90)
poverka_CL3005_3 = Label(lbl_CL3005_3, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_CL3005_3.place(x=45, y=30)
CL3005_3_1 = Button(lbl_CL3005_3, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3035', '20'), bg = alarm_color[0])
CL3005_3_1.place(x=40, y=0)
CL3005_3_2 = Button(lbl_CL3005_3, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3035', '20'), bg = alarm_color[0])
CL3005_3_2.place(x=135, y=0)
CL3005_3_ST = Button(lbl_CL3005_3, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3035', '20'), bg = alarm_color[0])
CL3005_3_ST.place(x=0, y=0)
CL3005_3_PC = Button(lbl_CL3005_3, text="ПК", width = 3, command = lambda: PC_card('PC20','3035', '20'), bg = alarm_color[3])
CL3005_3_PC.place(x=0, y=30)
Hovertip(CL3005_3_1, ['CL3005-24', ' SN3035'])
Hovertip(CL3005_3_2, ['CL3005-24', ' SN3035'])
Hovertip(CL3005_3_ST, ['CL3005-24', ' SN3035'])
Hovertip(CL3005_3_PC, ['Windows 7', 'IP 192.168.0.14'])

#Элементы стенда №21 CL3005-24 SN3036
alarm_color = button_color('3036', 'PC21')
lbl_CL3005_4 = LabelFrame(window, text = "21 CL_3ф")
lbl_CL3005_4.place(x = 570, y=460, width = 250, heigh = 90)
poverka_CL3005_4 = Label(lbl_CL3005_4, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_CL3005_4.place(x=10, y=10)
CL3005_4_1 = Button(lbl_CL3005_4, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3036', '21'), bg = alarm_color[0])
CL3005_4_1.place(x=0, y=30)
CL3005_4_2 = Button(lbl_CL3005_4, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3036', '21'), bg = alarm_color[0])
CL3005_4_2.place(x=95, y=30)
CL3005_4_ST = Button(lbl_CL3005_4, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3036', '21'), bg = alarm_color[0])
CL3005_4_ST.place(x=190, y=30)
CL3005_4_PC = Button(lbl_CL3005_4, text="ПК", width = 3, command = lambda: PC_card('PC21','3036', '21'), bg = alarm_color[3])
CL3005_4_PC.place(x=190, y=0)
Hovertip(CL3005_4_1, ['CL3005-24', ' SN3036'])
Hovertip(CL3005_4_2, ['CL3005-24', ' SN3036'])
Hovertip(CL3005_4_ST, ['CL3005-24', ' SN3036'])
Hovertip(CL3005_4_PC, ['Windows 7', 'IP 192.168.0.13'])

#Элементы стенда №22 CL3005-24 SN3032
alarm_color = button_color('3032', 'PC22')
lbl_CL3005_5 = LabelFrame(window, text = "22 CL_3ф")
lbl_CL3005_5.place(x = 500, y=550, width = 250, heigh = 90)
poverka_CL3005_5 = Label(lbl_CL3005_5, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_CL3005_5.place(x=45, y=30)
CL3005_5_1 = Button(lbl_CL3005_5, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3032', '22'), bg = alarm_color[0])
CL3005_5_1.place(x=50, y=0)
CL3005_5_2 = Button(lbl_CL3005_5, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3032', '22'), bg = alarm_color[0])
CL3005_5_2.place(x=145, y=0)
CL3005_5_ST = Button(lbl_CL3005_5, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3032', '22'), bg = alarm_color[0])
CL3005_5_ST.place(x=10, y=0)
CL3005_5_PC = Button(lbl_CL3005_5, text="ПК", width = 3, command = lambda: PC_card('PC22','3032', '22'), bg = alarm_color[3])
CL3005_5_PC.place(x=10, y=30)
Hovertip(CL3005_5_1, ['CL3005-24', ' SN3032'])
Hovertip(CL3005_5_2, ['CL3005-24', ' SN3032'])
Hovertip(CL3005_5_ST, ['CL3005-24', ' SN3032'])
Hovertip(CL3005_5_PC, ['Windows XP', 'IP 192.168.0.200'])

#Элементы стенда №23 CL1001-24 SN1015
alarm_color = button_color('1015', 'PC23')
lbl_CL1001_2 = LabelFrame(window, text = "23 CL_1ф")
lbl_CL1001_2.place(x = 480, y=640, width = 220, heigh = 70)
poverka_CL1001_2 = Label(lbl_CL1001_2, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_CL1001_2.place(x=10, y=25)
CL1001_3_1 = Button(lbl_CL1001_2, text="1-12", width = 6, command = lambda: installation_card('CL1001','1015', '23'), bg = alarm_color[0])
CL1001_3_1.place(x=90, y=0)
CL1001_3_2 = Button(lbl_CL1001_2, text="13-24", width = 6, command = lambda: installation_card('CL1001','1015', '23'), bg = alarm_color[0])
CL1001_3_2.place(x=150, y=0)
CL1001_3_ST = Button(lbl_CL1001_2, text="Уст.", width = 3, command = lambda: installation_card('CL1001','1015', '23'), bg = alarm_color[0])
CL1001_3_ST.place(x=10, y=0)
CL1001_3_PC = Button(lbl_CL1001_2, text="ПК", width = 3, command = lambda: PC_card('PC23','1015', '23'), bg = alarm_color[3])
CL1001_3_PC.place(x=50, y=0)
Hovertip(CL1001_3_1, ['CL1001-24', ' SN1015'])
Hovertip(CL1001_3_2, ['CL1001-24', ' SN1015'])
Hovertip(CL1001_3_ST, ['CL1001-24', ' SN1015'])
Hovertip(CL1001_3_PC, ['Windows 7', 'IP 192.168.0.100'])

#Элементы стенда №24 CL1005-48 SN1012
alarm_color = button_color('1012', 'PC24')
lbl_CL1005_1 = LabelFrame(window, text = "24 CL_1ф")
lbl_CL1005_1.place(x = 480, y=710, width = 220, heigh = 70)
poverka_CL1005_1 = Label(lbl_CL1005_1, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_CL1005_1.place(x=110, y=-5)
CL1005_1_1 = Button(lbl_CL1005_1, text="1-24", width = 6, command = lambda: installation_card('CL1001','1012', '24'), bg = alarm_color[0])
CL1005_1_1.place(x=110, y=15)
CL1005_1_2 = Button(lbl_CL1005_1, text="13-48", width = 6, command = lambda: installation_card('CL1001','1012', '24'), bg = alarm_color[0])
CL1005_1_2.place(x=10, y=15)
CL1005_1_ST = Button(lbl_CL1005_1, text="Уст.", width = 3, command = lambda: installation_card('CL1001','1012', '24'), bg = alarm_color[0])
CL1005_1_ST.place(x=170, y=15)
CL1005_1_PC = Button(lbl_CL1005_1, text="ПК", width = 3, command = lambda: PC_card('PC24','1012', '24'), bg = alarm_color[3])
CL1005_1_PC.place(x=70, y=15)
Hovertip(CL1005_1_1, ['CL1005-48', ' SN1012'])
Hovertip(CL1005_1_2, ['CL1005-48', ' SN1012'])
Hovertip(CL1005_1_ST, ['CL1005-48', ' SN1012'])
Hovertip(CL1005_1_PC, ['Windows XP', 'IP 192.168.0.245'])

#Элементы стенда №25 CL3005-24 SN3044
alarm_color = button_color('3044', 'PC25')
lbl_CL3005_6 = LabelFrame(window, text = "25 CL_3ф")
lbl_CL3005_6.place(x = 820, y=0, width = 250, heigh = 90)
poverka_CL3005_6 = Label(lbl_CL3005_6, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_CL3005_6.place(x=45, y=30)
CL3005_6_1 = Button(lbl_CL3005_6, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3044', '25'), bg = alarm_color[0])
CL3005_6_1.place(x=40, y=0)
CL3005_6_2 = Button(lbl_CL3005_6, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3044', '25'), bg = alarm_color[0])
CL3005_6_2.place(x=135, y=0)
CL3005_6_ST = Button(lbl_CL3005_6, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3044', '25'), bg = alarm_color[0])
CL3005_6_ST.place(x=0, y=0)
CL3005_6_PC = Button(lbl_CL3005_6, text="ПК", width = 3, command = lambda: PC_card('PC25','3044', '25'), bg = alarm_color[3])
CL3005_6_PC.place(x=0, y=30)
Hovertip(CL3005_6_1, ['CL3005-24', ' SN3044'])
Hovertip(CL3005_6_2, ['CL3005-24', ' SN3044'])
Hovertip(CL3005_6_ST, ['CL3005-24', ' SN3044'])
Hovertip(CL3005_6_PC, ['Windows 7', 'IP 192.168.0.247'])

#Элементы стенда №26 SY8126 SN 704202
alarm_color = button_color('704202', 'PC26')
lbl_SY8126_1 = LabelFrame(window, text = "26 SY_3ф")
lbl_SY8126_1.place(x = 970, y=190, width = 250, heigh = 90)
poverka_SY8126_1 = Label(lbl_SY8126_1, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_SY8126_1.place(x=45, y=30)
SY8126_1_1 = Button(lbl_SY8126_1, text="1-12", width = 10, command = lambda: installation_card('SY8126','704202', '26'), bg = alarm_color[0])
SY8126_1_1.place(x=50, y=0)
SY8126_1_2 = Button(lbl_SY8126_1, text="13-24", width = 10, command = lambda: installation_card('SY8126','704202', '26'), bg = alarm_color[0])
SY8126_1_2.place(x=145, y=0)
SY8126_1_ST = Button(lbl_SY8126_1, text="Уст.", width = 3, command = lambda: installation_card('SY8126','704202', '26'), bg = alarm_color[0])
SY8126_1_ST.place(x=10, y=0)
SY8126_1_PC = Button(lbl_SY8126_1, text="ПК", width = 3, command = lambda: PC_card('PC26','704202', '26'), bg = alarm_color[3])
SY8126_1_PC.place(x=10, y=30)
Hovertip(SY8126_1_1, ['SY8126', ' 704202'])
Hovertip(SY8126_1_2, ['SY8126', ' 704202'])
Hovertip(SY8126_1_ST, ['SY8126', ' 704202'])
Hovertip(SY8126_1_PC, ['Windows XP', 'IP 192.168.0.18'])

#Элементы стенда №27 SY8126 SN704203
alarm_color = button_color('704203', 'PC27')
lbl_SY8126_2 = LabelFrame(window, text = "27 SY_3ф")
lbl_SY8126_2.place(x = 970, y=280, width = 250, heigh = 90)
poverka_SY8126_2 = Label(lbl_SY8126_2, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_SY8126_2.place(x=10, y=10)
SY8126_2_1 = Button(lbl_SY8126_2, text="1-12", width = 10, command = lambda: installation_card('SY8126','704203', '27'), bg = alarm_color[0])
SY8126_2_1.place(x=10, y=30)
SY8126_2_2 = Button(lbl_SY8126_2, text="13-24", width = 10, command = lambda: installation_card('SY8126','704203', '27'), bg = alarm_color[0])
SY8126_2_2.place(x=105, y=30)
SY8126_2_ST = Button(lbl_SY8126_2, text="Уст.", width = 3, command = lambda: installation_card('SY8126','704203', '27'), bg = alarm_color[0])
SY8126_2_ST.place(x=200, y=30)
SY8126_2_PC = Button(lbl_SY8126_2, text="ПК", width = 3, command = lambda: PC_card('PC27','704203', '27'), bg = alarm_color[3])
SY8126_2_PC.place(x=200, y=0)
Hovertip(SY8126_2_1, ['SY8126', ' SN704203'])
Hovertip(SY8126_2_2, ['SY8126', ' SN704203'])
Hovertip(SY8126_2_ST, ['SY8126', ' SN704203'])
Hovertip(SY8126_2_PC, ['Windows XP', 'IP 192.168.0.16'])

#Элементы стенда №28 CL3005 SN3038
alarm_color = button_color('3038', 'PC28')
lbl_SY8126_3 = LabelFrame(window, text = "28 CL_3ф")
lbl_SY8126_3.place(x = 970, y=370, width = 250, heigh = 90)
poverka_SY8126_3 = Label(lbl_SY8126_3, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_SY8126_3.place(x=45, y=30)
SY8126_3_1 = Button(lbl_SY8126_3, text="1-12", width = 10, command = lambda: installation_card('CL3005','3038', '28'), bg = alarm_color[0])
SY8126_3_1.place(x=50, y=0)
SY8126_3_2 = Button(lbl_SY8126_3, text="13-24", width = 10, command = lambda: installation_card('CL3005','3038', '28'), bg = alarm_color[0])
SY8126_3_2.place(x=145, y=0)
SY8126_3_ST = Button(lbl_SY8126_3, text="Уст.", width = 3, command = lambda: installation_card('CL3005','3038', '28'), bg = alarm_color[0])
SY8126_3_ST.place(x=10, y=0)
SY8126_3_PC = Button(lbl_SY8126_3, text="ПК", width = 3, command = lambda: PC_card('PC28','3038', '28'), bg = alarm_color[3])
SY8126_3_PC.place(x=10, y=30)
Hovertip(SY8126_3_1, ['CL30005', ' SN3038'])
Hovertip(SY8126_3_2, ['CL30005', ' SN3038'])
Hovertip(SY8126_3_ST, ['CL30005', ' SN3038'])
Hovertip(SY8126_3_PC, ['Windows XP', 'IP 192.168.0.101'])

#Элементы стенда №29 SY8126 SN704204
alarm_color = button_color('704204', 'PC29')
lbl_SY8126_2 = LabelFrame(window, text = "29 SY_3ф")
lbl_SY8126_2.place(x = 970, y=460, width = 250, heigh = 90)
poverka_SY8126_2 = Label(lbl_SY8126_2, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_SY8126_2.place(x=10, y=10)
SY8126_2_1 = Button(lbl_SY8126_2, text="1-12", width = 10, command = lambda: installation_card('SY8126','704204', '29'), bg = alarm_color[0])
SY8126_2_1.place(x=10, y=30)
SY8126_2_2 = Button(lbl_SY8126_2, text="13-24", width = 10, command = lambda: installation_card('SY8126','704204', '29'), bg = alarm_color[0])
SY8126_2_2.place(x=105, y=30)
SY8126_2_ST = Button(lbl_SY8126_2, text="Уст.", width = 3, command = lambda: installation_card('SY8126','704204', '29'), bg = alarm_color[0])
SY8126_2_ST.place(x=200, y=30)
SY8126_2_PC = Button(lbl_SY8126_2, text="ПК", width = 3, command = lambda: PC_card('PC29','704204', '29'), bg = alarm_color[3])
SY8126_2_PC.place(x=200, y=0)
Hovertip(SY8126_2_1, ['SY8126', ' SN704204'])
Hovertip(SY8126_2_2, ['SY8126', ' SN704204'])
Hovertip(SY8126_2_ST, ['SY8126', ' SN704204'])
Hovertip(SY8126_2_PC, ['Windows 10', 'нет данных'])

#Элементы стенда №30 CL3005-24 SN3030
alarm_color = button_color('3030', 'PC30')
lbl_CL3005_7 = LabelFrame(window, text = "30 CL_3ф")
lbl_CL3005_7.place(x = 970, y=550, width = 250, heigh = 90)
poverka_CL3005_7 = Label(lbl_CL3005_7, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_CL3005_7.place(x=45, y=30)
CL3005_7_1 = Button(lbl_CL3005_7, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3030', '30'), bg = alarm_color[0])
CL3005_7_1.place(x=50, y=0)
CL3005_7_2 = Button(lbl_CL3005_7, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3030', '30'), bg = alarm_color[0])
CL3005_7_2.place(x=145, y=0)
CL3005_7_ST = Button(lbl_CL3005_7, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3030', '30'), bg = alarm_color[0])
CL3005_7_ST.place(x=10, y=0)
CL3005_7_PC = Button(lbl_CL3005_7, text="ПК", width = 3, command = lambda: PC_card('PC30','3030', '30'), bg = alarm_color[3])
CL3005_7_PC.place(x=10, y=30)
Hovertip(CL3005_7_1, ['CL3005-24', ' SN3030'])
Hovertip(CL3005_7_2, ['CL3005-24', ' SN3030'])
Hovertip(CL3005_7_ST, ['CL3005-24', ' SN3030'])
Hovertip(CL3005_7_PC, ['Windows 7', 'IP 192.168.0.180'])

#Элементы стенда №31 CL3005-24 SN3029
alarm_color = button_color('3029', 'PC31')
lbl_CL3005_8 = LabelFrame(window, text = "31 CL_3ф")
lbl_CL3005_8.place(x = 970, y=640, width = 250, heigh = 90)
poverka_CL3005_8 = Label(lbl_CL3005_8, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_CL3005_8.place(x=10, y=10)
CL3005_8_1 = Button(lbl_CL3005_8, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3029', '31'), bg = alarm_color[0])
CL3005_8_1.place(x=10, y=30)
CL3005_8_2 = Button(lbl_CL3005_8, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3029', '31'), bg = alarm_color[0])
CL3005_8_2.place(x=105, y=30)
CL3005_8_ST = Button(lbl_CL3005_8, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3029', '31'), bg = alarm_color[0])
CL3005_8_ST.place(x=200, y=30)
CL3005_8_PC = Button(lbl_CL3005_8, text="ПК", width = 3, command = lambda: PC_card('PC31','3029', '31'), bg = alarm_color[3])
CL3005_8_PC.place(x=200, y=0)
Hovertip(CL3005_8_1, ['CL3005-24', 'SN3029'])
Hovertip(CL3005_8_2, ['CL3005-24', 'SN3029'])
Hovertip(CL3005_8_ST, ['CL3005-24', 'SN3029'])
Hovertip(CL3005_8_PC, ['Windows 7', 'IP 192.168.0.111'])

#Элементы стенда №32 Merkury_210 SN025
alarm_color = button_color('025', 'PC32')
lbl_Merkury_210 = LabelFrame(window, text = "32")
lbl_Merkury_210.place(x = 710, y=720, width = 60, heigh = 60)
Merkury_210 = Button(lbl_Merkury_210, text="1-6", width = 3, command = lambda: installation_card('Merkury_210','025', '32'), bg = alarm_color[0])
Merkury_210.place(x=10, y=0)
Hovertip(Merkury_210, ['Merkury_210', 'SN025'])

#Элементы стенда №33 Merkury_210 SN018
alarm_color = button_color('018', 'PC33')
lbl_Merkury_210 = LabelFrame(window, text = "33")
lbl_Merkury_210.place(x = 780, y=720, width = 60, heigh = 60)
Merkury_210 = Button(lbl_Merkury_210, text="1-6", width = 3, command = lambda: installation_card('Merkury_210','018', '33'), bg = alarm_color[0])
Merkury_210.place(x=10, y=0)
Hovertip(Merkury_210, ['Merkury_210', 'SN025'])

#Элементы стенда №34 Functional_3ph SN000001
alarm_color = button_color('000001', 'PC34')
lbl_Functional_3ph_1 = LabelFrame(window, text = "34")
lbl_Functional_3ph_1.place(x = 130, y=640, width = 90, heigh = 60)
Functional_3ph_1 = Button(lbl_Functional_3ph_1, text="1", width = 3, command = lambda: installation_card('Functional_3ph', '000001', '34'), bg = alarm_color[0])
Functional_3ph_1.place(x=10, y=0)
Functional_3ph_PC_1 = Button(lbl_Functional_3ph_1, text="ПК", width = 3, command = lambda: PC_card('PC34', '000001', '34'), bg = alarm_color[3])
Functional_3ph_PC_1.place(x=50, y=00)
Hovertip(Functional_3ph_1, ['Functional_3ph', '000001'])
Hovertip(Functional_3ph_PC_1, ['Windows 7', 'IP 192.168.194.19'])

#Элементы стенда №35 Functional_3ph SN000035
alarm_color = button_color('000035', 'PC35')
lbl_Functional_3ph_2 = LabelFrame(window, text = "35")
lbl_Functional_3ph_2.place(x = 20, y=640, width = 90, heigh = 60)
Functional_3ph_2 = Button(lbl_Functional_3ph_2, text="1", width = 3, command = lambda: installation_card('Functional_3ph','000035', '35'), bg = alarm_color[0])
Functional_3ph_2.place(x=10, y=0)
Functional_3ph_PC_2 = Button(lbl_Functional_3ph_2, text="ПК", width = 3, command = lambda: PC_card('PC35','000035', '35'), bg = alarm_color[3])
Functional_3ph_PC_2.place(x=50, y=0)
Hovertip(Functional_3ph_2, ['Functional_3ph', '000035'])
Hovertip(Functional_3ph_PC_2, ['Windows 7', 'IP 000.000.000.000'])

#Элементы стенда №36 Functional_1ph SN061101401
alarm_color = button_color('061101401', 'PC36')
lbl_Functional_1ph_1 = LabelFrame(window, text = "36")
lbl_Functional_1ph_1.place(x = 130, y=700, width = 90, heigh = 60)
Functional_1ph_1 = Button(lbl_Functional_1ph_1, text="1", width = 3, command = lambda: installation_card('Functional_1ph','061101401', '36'), bg = alarm_color[0])
Functional_1ph_PC_3 = Button(lbl_Functional_1ph_1, text="ПК", width = 3, command = lambda: PC_card('PC36','061101401', '36'), bg = alarm_color[3])
Functional_1ph_PC_3.place(x=50, y=0)
Functional_1ph_1.place(x=10, y=0)
Hovertip(Functional_1ph_1, ['Functional_1ph', '061101401'])
Hovertip(Functional_1ph_PC_3, ['Windows 7', 'IP 0.0.0.0'])

#Элементы стенда №37 Functional_1ph SN000037
alarm_color = button_color('000037', 'PC37')
lbl_Functional_1ph_2 = LabelFrame(window, text = "37")
lbl_Functional_1ph_2.place(x = 20, y=700, width = 90, heigh = 60)
Functional_1ph_2 = Button(lbl_Functional_1ph_2, text="1", width = 3, command = lambda: installation_card('Functional_1ph','000037', '37'), bg = alarm_color[0])
Functional_1ph_2.place(x=10, y=0)
Functional_1ph_2_PC_4 = Button(lbl_Functional_1ph_2, text="ПК", width = 3, command = lambda: PC_card('PC37','000037', '37'), bg = alarm_color[3])
Functional_1ph_2_PC_4.place(x=50, y=00)
Hovertip(Functional_1ph_2, ['Functional_1ph', '000037'])
Hovertip(Functional_1ph_2_PC_4, ['Windows 7', 'IP 000.000.000.000'])

#Элементы стенда №38 Functional_1ph SN000038
alarm_color = button_color('000038', 'PC38')
lbl_Functional_1ph_1 = LabelFrame(window, text = "38")
lbl_Functional_1ph_1.place(x = 1130, y=730, width = 90, heigh = 60)
Functional_1ph_1 = Button(lbl_Functional_1ph_1, text="1", width = 3, command = lambda: installation_card('Functional_1ph','000038', '38'), bg = alarm_color[0])
Functional_1ph_PC_3 = Button(lbl_Functional_1ph_1, text="ПК", width = 3, command = lambda: PC_card('PC38','000038', '38'), bg = alarm_color[3])
Functional_1ph_PC_3.place(x=5, y=0)
Functional_1ph_1.place(x=45, y=0)
Hovertip(Functional_1ph_1, ['Functional_1ph', '000038'])
Hovertip(Functional_1ph_PC_3, ['Windows XP', 'IP 192.168.0.243'])


#Элементы стенда №39 Rele_201TLO SN000039
alarm_color = button_color('000039', 'PC39')
lbl_Rele_201TLO = LabelFrame(window, text = "39, 40")
lbl_Rele_201TLO.place(x = 20, y=10, width = 150, heigh = 60)
Rele_201TLO = Button(lbl_Rele_201TLO, text="1", width = 3, command = lambda: installation_card('Rele_201TLO','000039', '39'), bg = alarm_color[0])
Rele_201TLO.place(x=50, y=0)
Rele_201TLO_PC = Button(lbl_Rele_201TLO, text="ПК", width = 3, command = lambda: PC_card('PC39','000039', '39'), bg = alarm_color[3])
Rele_201TLO_PC.place(x=10, y=0)
Hovertip(Rele_201TLO, ['Rele_201TLO', '000039'])
Hovertip(Rele_201TLO_PC, ['Windows XP', 'IP 192.168.0.131'])

#Элементы стенда №40 Modem_PLC_201TLO SN000040
alarm_color = button_color('000040', 'PC39')
Modem_201TLO = Button(lbl_Rele_201TLO, text="1", width = 3, command = lambda: installation_card('Modem_201TLO','000040', '40'), bg = alarm_color[0])
Modem_201TLO.place(x=90, y=0)
Hovertip(Modem_201TLO, ['Modem_201TLO', '000040'])

#Элементы стенда №41 CL1000 SN1017
alarm_color = button_color('1017', 'PC41')
lbl_CL1000 = LabelFrame(window, text = "41 CL_1ф")
lbl_CL1000.place(x = 410, y=500, width = 50, heigh = 180)
poverka_CL1000 = Label(lbl_CL1000, text = ("Пов.:\n" + str(alarm_color[1])) , fg = alarm_color[2])
poverka_CL1000.place(x=5, y=110)
CL1000_1 = Button(lbl_CL1000, text="1-6", width = 3, command = lambda: installation_card('CL1000','1017', '41'), bg = alarm_color[0])
CL1000_1.place(x=5, y=5)
CL1000_ST = Button(lbl_CL1000, text="Уст.", width = 3, command = lambda: installation_card('CL1000','1017', '41'), bg = alarm_color[0])
CL1000_ST.place(x=5, y=40)
CL1000_PC = Button(lbl_CL1000, text="ПК", width = 3, command = lambda: PC_card('PC41','1017', '41'), bg = alarm_color[3])
CL1000_PC.place(x=5, y=75)
Hovertip(CL1000_1, ['CL1000', '1017'])
Hovertip(CL1000_ST, ['CL1000', '1017'])
Hovertip(CL1000_PC, ['Windows 7', 'IP 192.168.0.207'])

#Элементы стенда №49 SY8126 SN0808169
alarm_color = button_color('0808169', 'PC49')
lbl_SY8126_3 = LabelFrame(window, text = "49 SY_3ф")
lbl_SY8126_3.place(x = 1270, y=280, width = 100, heigh = 270)
poverka_SY8126_3 = Label(lbl_SY8126_3, text = ("Поверка: \n" + str(alarm_color[1])) , fg = alarm_color[2])
poverka_SY8126_3.place(x=10, y=170)
progon_SY8126_3 = Label(lbl_SY8126_3, text = ("Стенд рядом\n с прогоном" ))
progon_SY8126_3.place(x=0, y=210)
SY8126_3_1 = Button(lbl_SY8126_3, text="1 \n-12", width = 3, height = 3, command = lambda: installation_card('SY8126','0808169', '49'), bg = alarm_color[0])
SY8126_3_1.place(x=10, y=70)
SY8126_3_2 = Button(lbl_SY8126_3, text="13 \n-24", width = 3, height = 3, command = lambda: installation_card('SY8126','0808169', '49'), bg = alarm_color[0])
SY8126_3_2.place(x=10, y=5)
SY8126_3_ST = Button(lbl_SY8126_3, text="Уст.", width = 3, command = lambda: installation_card('SY8126','0808169', '49'), bg = alarm_color[0])
SY8126_3_ST.place(x=10, y=135)
SY8126_3_PC = Button(lbl_SY8126_3, text="ПК", width = 3, command = lambda: PC_card('PC49','0808169', '49'), bg = alarm_color[3])
SY8126_3_PC.place(x=45, y=135)
Hovertip(SY8126_3_1, ['SY8126', ' SN0808169'])
Hovertip(SY8126_3_2, ['SY8126', ' SN0808169'])
Hovertip(SY8126_3_ST, ['SY8126', ' SN0808169'])
Hovertip(SY8126_3_PC, ['Windows XP', 'IP 192.168.0.11'])

#Элементы стенда №90 CL3005-24 SN3036
alarm_color = button_color('3027', 'PC90')
lbl_CL3005_9 = LabelFrame(window, text = "90 Ремонт_группа")
lbl_CL3005_9.place(x = 1250, y=700, width = 150, heigh = 90)
poverka_CL3005_9 = Label(lbl_CL3005_9, text = ("Поверка: " + str(alarm_color[1])) , fg = alarm_color[2])
poverka_CL3005_9.place(x=0, y=10)
CL3005_9_1 = Button(lbl_CL3005_9, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3027', '90'), bg = alarm_color[0])
CL3005_9_1.place(x=5, y=30)
CL3005_9_ST = Button(lbl_CL3005_9, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3027', '90'), bg = alarm_color[0])
CL3005_9_ST.place(x=110, y=30)
CL3005_9_PC = Button(lbl_CL3005_9, text="ПК", width = 3, command = lambda: PC_card('PC90','3027', '90'), bg = alarm_color[3])
CL3005_9_PC.place(x=110, y=0)
Hovertip(CL3005_9_1, ['CL3005-24', ' SN3027'])
Hovertip(CL3005_9_ST, ['CL3005-24', ' SN3036'])
Hovertip(CL3005_9_PC, ['Windows 2000', 'IP 0.0.0.0'])

window.mainloop()


