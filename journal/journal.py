import tkinter.ttk as ttk
from tkinter import *  
from tkinter.ttk import Combobox, Radiobutton, Label, Entry, Spinbox
import time
import datetime
import ast
import winreg 
import psycopg2

surname = ['Рожков В.А.', 'Алексеев Н.И.', 'Коротаев А.А.', 'Ямалеев И.О.']

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

# Функция открытия карточки стенда
def installation_card(model, SN):
   
    window_card = Tk()
    window_card.title("Карточка стенда " + model + "   SN " + SN)
    window_card.geometry("600x500")
    Label(window_card, text = ("Последние комментарии:")).place(x=10, y=90)
    text_card = Text(window_card, width=50, height=10)
    text_card.place(x=10, y=110)
    #scroll = Scrollbar(window_card, command=text_card.yview, width=50)
    #scroll.place(x=530, y=110)
    SUBD_get(window_card, text_card, SN)
    Label(window_card, text = ("Ваш комментарий:")).place(x=10, y=300)
    text_wr = Text(window_card, width=50, height=5)
    text_wr.place(x=10, y=320)
    btn_wr = Button(window_card, text="Отправить", command = lambda: SUBD_push(window_card, text_wr, SN, combo))
    btn_wr.place(x=350, y=420)
    lbl01 = Label(window_card, text = "Выберите фамилию:").place(x=10, y=420)
    combo = Combobox(window_card, width = 13, values = surname)
    combo.place(x=150, y=420)
    combo.current(3)


# Функция записи данных в БД
def SUBD_push(window_card, text_wr, SN, combo):
    try:
        # Подключение к БД
        
        con = psycopg2.connect(
          database="Virtual_department", 
          user="postgres", 
          password="777#igra", 
          host="127.0.0.1", 
          port="5432")
        Label(window_card, text = "Подключение к базе данных: ОК", foreground = 'green').place(x=10, y=450)
    except:
        Label(window_card, text = "Подключение к базе данных отсутсвует", foreground = 'red').place(x=10, y=450)
    try:
        #Запись комментария в таблицу БД
        cur = con.cursor()
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        author = combo.get()
        comment = text_wr.get(1.0, END).strip()
        cur.execute("INSERT INTO public.comments (date, author, commentary, serial_number) VALUES (%s, %s, %s, %s);", (date, author, comment, SN))
        con.commit() 
        Label(window_card, text = "Данные успешно записаны!!!", foreground = 'green').place(x=10, y=450)
    except:
        Label(window_card, text = "Не удалось записать данные в базу данных!!!", foreground = 'red').place(x=10, y=450)
    

# Функция получения данных из базы
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
        cur.execute("SELECT serial_number, model, phases FROM public.installations WHERE serial_number = \'%s\';" %SN)
        rows = cur.fetchall()
        for row in rows:
            Label(window_card, text = ("Serial_number: " + row[0])).place(x=10, y=25)
            Label(window_card, text = ("Model: " + row[1])).place(x=10, y=45)
            Label(window_card, text = ("Phases: " + row[2])).place(x=10, y=65)
    except:
        Label(window_card, text = "Данные в таблице установок отсутсвуют!!!", foreground = 'red').place(x=10, y=25)

    try:
        # Считывание комментариев по данной установке
        cur.execute("SELECT date, author, commentary FROM public.comments WHERE serial_number = \'%s\';" %SN)
        rows = cur.fetchall()
        for row in rows:
            text_card.insert(1.0, "\nДата: " + str(row[0]))
            text_card.insert(1.0, "\nАвтор: " + row[1])
            text_card.insert(1.0, "\nКомментарий: " + row[2])
            text_card.insert(1.0, "\n")
        con.close()
    except:
        text_card.insert(1.0, "Данные в таблице комментариев отсутствуют")


    

#Main program
window = Tk()  
window.title("Виртуальный цех сборки электросчетчиков (by Jamigo)")  
window.geometry('1200x780')
#Включаем подержку нажатий клавиш Ctr-C, Ctr-V, Ctr-X
window.bind_all("<Key>", _onKeyRelease, "+") 

#Элементы стенда №1 HX-8100_3
lbl_HX8100_3 = LabelFrame(window, text = "1")
lbl_HX8100_3.place(x = 20, y=120, width = 250, heigh = 60)
HX8100_3_1 = Button(lbl_HX8100_3, text="1-48", width = 10, command = lambda: installation_card('HX8100','080798'))
HX8100_3_1.place(x=10, y=0)
HX8100_3_2 = Button(lbl_HX8100_3, text="49-96", width = 10, command = lambda: installation_card('HX8100','080798'))
HX8100_3_2.place(x=105, y=0)
HX8100_3_PC = Button(lbl_HX8100_3, text="ПК", width = 3, command = lambda: PC_card('PC1'))
HX8100_3_PC.place(x=200, y=0)

#Элементы стенда №2 HX-8100_2
lbl_HX8100_2 = LabelFrame(window, text = "2")
lbl_HX8100_2.place(x = 20, y=280, width = 250, heigh = 60)
HX8100_2_1 = Button(lbl_HX8100_2, text="1-48", width = 10, command = lambda: installation_card('HX8100', '080799'))
HX8100_2_1.place(x=50, y=0)
HX8100_2_2 = Button(lbl_HX8100_2, text="49-96", width = 10, command = lambda: installation_card('HX8100', '080799'))
HX8100_2_2.place(x=145, y=0)
HX8100_2_PC = Button(lbl_HX8100_2, text="ПК", width = 3, command = lambda: PC_card('PC2'))
HX8100_2_PC.place(x=10, y=0)

#Элементы стенда №3 SY8125 SN703143
lbl_SY8125_1 = LabelFrame(window, text = "3")
lbl_SY8125_1.place(x = 20, y=380, width = 150, heigh = 90)
SY8125_1 = Button(lbl_SY8125_1, text="1-24", width = 10, command = lambda: installation_card('SY8125', '703143'))
SY8125_1.place(x=50, y=0)
SY8125_1_PC = Button(lbl_SY8125_1, text="ПК", width = 3, command = lambda: PC_card('PC3'))
SY8125_1_PC.place(x=10, y=30)

#Элементы стенда №4 SY8125 SN703146
lbl_SY8125_2 = LabelFrame(window, text = "4")
lbl_SY8125_2.place(x = 20, y=470, width = 150, heigh = 90)
SY8125_2 = Button(lbl_SY8125_2, text="1-24", width = 10, command = lambda: installation_card('SY8125', '703146'))
SY8125_2.place(x=50, y=30)
SY8125_2_PC = Button(lbl_SY8125_2, text="ПК", width = 3, command = lambda: PC_card('PC4'))
SY8125_2_PC.place(x=10, y=0)

#Элементы стенда №5 УАПС-1М SN000000
lbl_UAPS1M_5 = LabelFrame(window, text = "5")
lbl_UAPS1M_5.place(x = 270, y=0, width = 80, heigh = 85)
UAPS1M_5 = Button(lbl_UAPS1M_5, text="Уст.", width = 3, command = lambda: installation_card('UAPS-1M', '000000'))
UAPS1M_5.place(x=20, y=00)
UAPS1M_5 = Button(lbl_UAPS1M_5, text="1-6", width = 3, command = lambda: installation_card('UAPS-1M', '000000'))
UAPS1M_5.place(x=40, y=30)

#Элементы стенда №6 УАПС-1М SN102
lbl_UAPS1M_6 = LabelFrame(window, text = "6")
lbl_UAPS1M_6.place(x = 350, y=0, width = 80, heigh = 85)
UAPS1M_6 = Button(lbl_UAPS1M_6, text="Уст.", width = 3, command = lambda: installation_card('UAPS-1M', '102'))
UAPS1M_6.place(x=20, y=00)
UAPS1M_6 = Button(lbl_UAPS1M_6, text="1-6", width = 3, command = lambda: installation_card('UAPS-1M', '102'))
UAPS1M_6.place(x=40, y=30)
UAPS1M_6_PC = Button(lbl_UAPS1M_6, text="ПК", width = 3, command = lambda: PC_card('PC6'))
UAPS1M_6_PC.place(x=0, y=30)

#Элементы стенда №7 УАПС-1М SN61207
lbl_UAPS1M_7 = LabelFrame(window, text = "7")
lbl_UAPS1M_7.place(x = 440, y=0, width = 80, heigh = 85)
UAPS1M_7 = Button(lbl_UAPS1M_7, text="Уст.", width = 3, command = lambda: installation_card('UAPS-1M', '61207'))
UAPS1M_7.place(x=20, y=00)
UAPS1M_7 = Button(lbl_UAPS1M_7, text="1-6", width = 3, command = lambda: installation_card('UAPS-1M', '61207'))
UAPS1M_7.place(x=40, y=30)
UAPS1M_7_PC = Button(lbl_UAPS1M_7, text="ПК", width = 3, command = lambda: PC_card('PC7'))
UAPS1M_7_PC.place(x=0, y=30)

#Элементы стенда №8 УАПС-1М SN109
lbl_UAPS1M_8 = LabelFrame(window, text = "8")
lbl_UAPS1M_8.place(x = 640, y=0, width = 80, heigh = 85)
UAPS1M_8 = Button(lbl_UAPS1M_8, text="Уст.", width = 3, command = lambda: installation_card('UAPS-1M', '109'))
UAPS1M_8.place(x=20, y=00)
UAPS1M_8 = Button(lbl_UAPS1M_8, text="1-6", width = 3, command = lambda: installation_card('UAPS-1M', '109'))
UAPS1M_8.place(x=40, y=30)
UAPS1M_8_PC = Button(lbl_UAPS1M_8, text="ПК", width = 3, command = lambda: PC_card('PC8'))
UAPS1M_8_PC.place(x=0, y=30)

#Элементы стенда №9 УАПС-1М SN050908
lbl_UAPS1M_9 = LabelFrame(window, text = "9")
lbl_UAPS1M_9.place(x = 730, y=0, width = 80, heigh = 85)
UAPS1M_9 = Button(lbl_UAPS1M_9, text="Уст.", width = 3, command = lambda: installation_card('UAPS-1M', '050908'))
UAPS1M_9.place(x=20, y=00)
UAPS1M_9 = Button(lbl_UAPS1M_9, text="1-6", width = 3, command = lambda: installation_card('UAPS-1M', '050908'))
UAPS1M_9.place(x=40, y=30)
UAPS1M_9_PC = Button(lbl_UAPS1M_9, text="ПК", width = 3, command = lambda: PC_card('PC9'))
UAPS1M_9_PC.place(x=0, y=30)

#Элементы стенда №10 HX8300 SN0807102
lbl_HX8300_10 = LabelFrame(window, text = "10")
lbl_HX8300_10.place(x = 350, y=120, width = 50, heigh = 320)
HX8300_10_1 = Button(lbl_HX8300_10, text="1-\n24", width = 3, height = 3, command = lambda: installation_card('HX8300','0807102'))
HX8300_10_1.place(x=5, y=30)
HX8300_10_2 = Button(lbl_HX8300_10, text="25-\n48", width = 3, height = 3, command = lambda: installation_card('HX8300','0807102'))
HX8300_10_2.place(x=5, y=95)
HX8300_10_3 = Button(lbl_HX8300_10, text="49-\n72", width = 3, height = 3, command = lambda: installation_card('HX8300','0807102'))
HX8300_10_3.place(x=5, y=160)
HX8300_10_4 = Button(lbl_HX8300_10, text="73-\n96", width = 3, height = 3, command = lambda: installation_card('HX8300','0807102'))
HX8300_10_4.place(x=5, y=225)
HX8300_10_PC = Button(lbl_HX8300_10, text="ПК", width = 3, command = lambda: PC_card('PC10'))
HX8300_10_PC.place(x=5, y=0)

#Элементы стенда №11 HX8300 SN0807103
lbl_HX8300_11 = LabelFrame(window, text = "11")
lbl_HX8300_11.place(x = 350, y=440, width = 50, heigh = 320)
HX8300_11_1 = Button(lbl_HX8300_11, text="1-\n24", width = 3, height = 3, command = lambda: installation_card('HX8300','0807103'))
HX8300_11_1.place(x=5, y=30)
HX8300_11_2 = Button(lbl_HX8300_11, text="25-\n48", width = 3, height = 3, command = lambda: installation_card('HX8300','0807103'))
HX8300_11_2.place(x=5, y=95)
HX8300_11_3 = Button(lbl_HX8300_11, text="49-\n72", width = 3, height = 3, command = lambda: installation_card('HX8300','0807103'))
HX8300_11_3.place(x=5, y=160)
HX8300_11_4 = Button(lbl_HX8300_11, text="73-\n96", width = 3, height = 3, command = lambda: installation_card('HX8300','0807103'))
HX8300_11_4.place(x=5, y=225)
HX8300_11_PC = Button(lbl_HX8300_11, text="ПК", width = 3, command = lambda: PC_card('PC11'))
HX8300_11_PC.place(x=5, y=0)

#Элементы стенда №12 CL3005-24 SN 3028
lbl_CL3005_1 = LabelFrame(window, text = "12")
lbl_CL3005_1.place(x = 450, y=100, width = 250, heigh = 90)
CL3005_1_1 = Button(lbl_CL3005_1, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3028'))
CL3005_1_1.place(x=10, y=15)
CL3005_1_2 = Button(lbl_CL3005_1, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3028'))
CL3005_1_2.place(x=105, y=15)
CL3005_1_ST = Button(lbl_CL3005_1, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3028'))
CL3005_1_ST.place(x=200, y=30)
CL3005_1_PC = Button(lbl_CL3005_1, text="ПК", width = 3, command = lambda: PC_card('PC12'))
CL3005_1_PC.place(x=200, y=0)

#Элементы стенда №13 CL3005-24 SN 3042
lbl_CL3005_2 = LabelFrame(window, text = "13")
lbl_CL3005_2.place(x = 700, y=100, width = 250, heigh = 90)
CL3005_2_1 = Button(lbl_CL3005_2, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3042'))
CL3005_2_1.place(x=10, y=15)
CL3005_2_2 = Button(lbl_CL3005_2, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3042'))
CL3005_2_2.place(x=105, y=15)
CL3005_2_ST = Button(lbl_CL3005_2, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3042'))
CL3005_2_ST.place(x=200, y=30)
CL3005_2_PC = Button(lbl_CL3005_2, text="ПК", width = 3, command = lambda: PC_card('PC13'))
CL3005_2_PC.place(x=200, y=0)

#Элементы стенда №14 CL1001 SN 1009
lbl_CL1001_1 = LabelFrame(window, text = "14")
lbl_CL1001_1.place(x = 450, y=190, width = 150, heigh = 90)
CL1001_1_1 = Button(lbl_CL1001_1, text="1-24", width = 10, command = lambda: installation_card('CL1001','1009'))
CL1001_1_1.place(x=50, y=15)
CL1001_1_ST = Button(lbl_CL1001_1, text="Уст.", width = 3, command = lambda: installation_card('CL1001','1009'))
CL1001_1_ST.place(x=10, y=30)
CL1001_1_PC = Button(lbl_CL1001_1, text="ПК", width = 3, command = lambda: PC_card('PC14'))
CL1001_1_PC.place(x=10, y=0)

#Элементы стенда №15 CL1001 SN 1008
lbl_CL1001_2 = LabelFrame(window, text = "15")
lbl_CL1001_2.place(x = 450, y=280, width = 150, heigh = 90)
CL1001_2_1 = Button(lbl_CL1001_2, text="1-24", width = 10, command = lambda: installation_card('CL1001','1008'))
CL1001_2_1.place(x=10, y=15)
CL1001_2_ST = Button(lbl_CL1001_2, text="Уст.", width = 3, command = lambda: installation_card('CL1001','1008'))
CL1001_2_ST.place(x=110, y=30)
CL1001_2_PC = Button(lbl_CL1001_2, text="ПК", width = 3, command = lambda: PC_card('PC15'))
CL1001_2_PC.place(x=110, y=0)

#Элементы стенда №16 SY8125 SN703154
lbl_SY8125_3 = LabelFrame(window, text = "16")
lbl_SY8125_3.place(x = 605, y=200, width = 150, heigh = 60)
SY8125_3 = Button(lbl_SY8125_3, text="1-24", width = 10, command = lambda: installation_card('SY8125', '703154'))
SY8125_3.place(x=50, y=0)
SY8125_3_PC = Button(lbl_SY8125_3, text="ПК", width = 3, command = lambda: PC_card('PC16'))
SY8125_3_PC.place(x=10, y=0)

#Элементы стенда №17 SY8125 SN703152
lbl_SY8125_4 = LabelFrame(window, text = "17")
lbl_SY8125_4.place(x = 760, y=200, width = 150, heigh = 60)
SY8125_4 = Button(lbl_SY8125_4, text="1-24", width = 10, command = lambda: installation_card('SY8125', '703152'))
SY8125_4.place(x=50, y=0)
SY8125_4_PC = Button(lbl_SY8125_4, text="ПК", width = 3, command = lambda: PC_card('PC17'))
SY8125_4_PC.place(x=10, y=0)

#Элементы стенда №18 SY8125 SN703153
lbl_SY8125_5 = LabelFrame(window, text = "18")
lbl_SY8125_5.place(x = 605, y=290, width = 150, heigh = 60)
SY8125_5 = Button(lbl_SY8125_5, text="1-24", width = 10, command = lambda: installation_card('SY8125', '703153'))
SY8125_5.place(x=50, y=0)
SY8125_5_PC = Button(lbl_SY8125_5, text="ПК", width = 3, command = lambda: PC_card('PC18'))
SY8125_5_PC.place(x=10, y=0)

#Элементы стенда №19 SY8125 SN703151
lbl_SY8125_6 = LabelFrame(window, text = "19")
lbl_SY8125_6.place(x = 760, y=290, width = 150, heigh = 60)
SY8125_6 = Button(lbl_SY8125_6, text="1-24", width = 10, command = lambda: installation_card('SY8125', '703151'))
SY8125_6.place(x=50, y=0)
SY8125_6_PC = Button(lbl_SY8125_6, text="ПК", width = 3, command = lambda: PC_card('PC19'))
SY8125_6_PC.place(x=10, y=0)

#Элементы стенда №20 CL3005-24 SN 3035
lbl_CL3005_3 = LabelFrame(window, text = "20")
lbl_CL3005_3.place(x = 570, y=370, width = 250, heigh = 90)
CL3005_3_1 = Button(lbl_CL3005_3, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3035'))
CL3005_3_1.place(x=40, y=15)
CL3005_3_2 = Button(lbl_CL3005_3, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3035'))
CL3005_3_2.place(x=135, y=15)
CL3005_3_ST = Button(lbl_CL3005_3, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3035'))
CL3005_3_ST.place(x=0, y=0)
CL3005_3_PC = Button(lbl_CL3005_3, text="ПК", width = 3, command = lambda: PC_card('PC20'))
CL3005_3_PC.place(x=0, y=30)

#Элементы стенда №21 CL3005-24 SN 3036
lbl_CL3005_4 = LabelFrame(window, text = "21")
lbl_CL3005_4.place(x = 570, y=460, width = 250, heigh = 90)
CL3005_4_1 = Button(lbl_CL3005_4, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3036'))
CL3005_4_1.place(x=0, y=15)
CL3005_4_2 = Button(lbl_CL3005_4, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3036'))
CL3005_4_2.place(x=95, y=15)
CL3005_4_ST = Button(lbl_CL3005_4, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3036'))
CL3005_4_ST.place(x=190, y=0)
CL3005_4_PC = Button(lbl_CL3005_4, text="ПК", width = 3, command = lambda: PC_card('PC21'))
CL3005_4_PC.place(x=190, y=30)

#Элементы стенда №22 CL3005-24 SN 3032
lbl_CL3005_5 = LabelFrame(window, text = "22")
lbl_CL3005_5.place(x = 500, y=550, width = 250, heigh = 90)
CL3005_5_1 = Button(lbl_CL3005_5, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3032'))
CL3005_5_1.place(x=50, y=15)
CL3005_5_2 = Button(lbl_CL3005_5, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3032'))
CL3005_5_2.place(x=145, y=15)
CL3005_5_ST = Button(lbl_CL3005_5, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3032'))
CL3005_5_ST.place(x=10, y=0)
CL3005_5_PC = Button(lbl_CL3005_5, text="ПК", width = 3, command = lambda: PC_card('PC22'))
CL3005_5_PC.place(x=10, y=30)

#Элементы стенда №23 CL1001 SN 1015
lbl_CL1001_2 = LabelFrame(window, text = "23")
lbl_CL1001_2.place(x = 480, y=650, width = 220, heigh = 60)
CL1001_2_1 = Button(lbl_CL1001_2, text="1-12", width = 6, command = lambda: installation_card('CL1001','1015'))
CL1001_2_1.place(x=90, y=0)
CL1001_2_2 = Button(lbl_CL1001_2, text="13-24", width = 6, command = lambda: installation_card('CL1001','1015'))
CL1001_2_2.place(x=150, y=0)
CL1001_2_ST = Button(lbl_CL1001_2, text="Уст.", width = 3, command = lambda: installation_card('CL1001','1015'))
CL1001_2_ST.place(x=10, y=0)
CL1001_2_PC = Button(lbl_CL1001_2, text="ПК", width = 3, command = lambda: PC_card('PC23'))
CL1001_2_PC.place(x=50, y=0)

#Элементы стенда №24 CL1005-48 SN 1012
lbl_CL1005_1 = LabelFrame(window, text = "24")
lbl_CL1005_1.place(x = 480, y=720, width = 220, heigh = 60)
CL1005_1_1 = Button(lbl_CL1005_1, text="1-24", width = 6, command = lambda: installation_card('CL1001','1012'))
CL1005_1_1.place(x=110, y=0)
CL1005_1_2 = Button(lbl_CL1005_1, text="13-48", width = 6, command = lambda: installation_card('CL1001','1012'))
CL1005_1_2.place(x=10, y=0)
CL1005_1_ST = Button(lbl_CL1005_1, text="Уст.", width = 3, command = lambda: installation_card('CL1001','1012'))
CL1005_1_ST.place(x=170, y=0)
CL1005_1_PC = Button(lbl_CL1005_1, text="ПК", width = 3, command = lambda: PC_card('PC24'))
CL1005_1_PC.place(x=70, y=0)

#Элементы стенда №25 CL3005-24 SN 3044
lbl_CL3005_6 = LabelFrame(window, text = "25")
lbl_CL3005_6.place(x = 820, y=0, width = 250, heigh = 90)
CL3005_6_1 = Button(lbl_CL3005_6, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3044'))
CL3005_6_1.place(x=40, y=15)
CL3005_6_2 = Button(lbl_CL3005_6, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3044'))
CL3005_6_2.place(x=135, y=15)
CL3005_6_ST = Button(lbl_CL3005_6, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3044'))
CL3005_6_ST.place(x=0, y=0)
CL3005_6_PC = Button(lbl_CL3005_6, text="ПК", width = 3, command = lambda: PC_card('PC25'))
CL3005_6_PC.place(x=0, y=30)

#Элементы стенда №26 SY8126 SN 704202
lbl_SY8126_1 = LabelFrame(window, text = "26")
lbl_SY8126_1.place(x = 950, y=225, width = 250, heigh = 90)
SY8126_1_1 = Button(lbl_SY8126_1, text="1-12", width = 10, command = lambda: installation_card('SY8126','704202'))
SY8126_1_1.place(x=50, y=15)
SY8126_1_2 = Button(lbl_SY8126_1, text="13-24", width = 10, command = lambda: installation_card('SY8126','704202'))
SY8126_1_2.place(x=145, y=15)
SY8126_1_ST = Button(lbl_SY8126_1, text="Уст.", width = 3, command = lambda: installation_card('SY8126','704202'))
SY8126_1_ST.place(x=10, y=0)
SY8126_1_PC = Button(lbl_SY8126_1, text="ПК", width = 3, command = lambda: PC_card('PC26'))
SY8126_1_PC.place(x=10, y=30)

#Элементы стенда №27 SY8126 SN 704203
lbl_SY8126_2 = LabelFrame(window, text = "27")
lbl_SY8126_2.place(x = 950, y=315, width = 250, heigh = 90)
SY8126_2_1 = Button(lbl_SY8126_2, text="1-12", width = 10, command = lambda: installation_card('SY8126','704203'))
SY8126_2_1.place(x=10, y=15)
SY8126_2_2 = Button(lbl_SY8126_2, text="13-24", width = 10, command = lambda: installation_card('SY8126','704203'))
SY8126_2_2.place(x=105, y=15)
SY8126_2_ST = Button(lbl_SY8126_2, text="Уст.", width = 3, command = lambda: installation_card('SY8126','704203'))
SY8126_2_ST.place(x=200, y=30)
SY8126_2_PC = Button(lbl_SY8126_2, text="ПК", width = 3, command = lambda: PC_card('PC27'))
SY8126_2_PC.place(x=200, y=0)

#Элементы стенда №28 SY8126 SN 704205
lbl_SY8126_3 = LabelFrame(window, text = "28")
lbl_SY8126_3.place(x = 950, y=405, width = 250, heigh = 90)
SY8126_3_1 = Button(lbl_SY8126_3, text="1-12", width = 10, command = lambda: installation_card('SY8126','704205'))
SY8126_3_1.place(x=50, y=15)
SY8126_3_2 = Button(lbl_SY8126_3, text="13-24", width = 10, command = lambda: installation_card('SY8126','704205'))
SY8126_3_2.place(x=145, y=15)
SY8126_3_ST = Button(lbl_SY8126_3, text="Уст.", width = 3, command = lambda: installation_card('SY8126','704205'))
SY8126_3_ST.place(x=10, y=0)
SY8126_3_PC = Button(lbl_SY8126_3, text="ПК", width = 3, command = lambda: PC_card('PC28'))
SY8126_3_PC.place(x=10, y=30)

#Элементы стенда №29 SY8126 SN 704204
lbl_SY8126_2 = LabelFrame(window, text = "29")
lbl_SY8126_2.place(x = 950, y=495, width = 250, heigh = 90)
SY8126_2_1 = Button(lbl_SY8126_2, text="1-12", width = 10, command = lambda: installation_card('SY8126','704204'))
SY8126_2_1.place(x=10, y=15)
SY8126_2_2 = Button(lbl_SY8126_2, text="13-24", width = 10, command = lambda: installation_card('SY8126','704204'))
SY8126_2_2.place(x=105, y=15)
SY8126_2_ST = Button(lbl_SY8126_2, text="Уст.", width = 3, command = lambda: installation_card('SY8126','704204'))
SY8126_2_ST.place(x=200, y=30)
SY8126_2_PC = Button(lbl_SY8126_2, text="ПК", width = 3, command = lambda: PC_card('PC29'))
SY8126_2_PC.place(x=200, y=0)

#Элементы стенда №30 CL3005-24 SN 3030
lbl_CL3005_7 = LabelFrame(window, text = "30")
lbl_CL3005_7.place(x = 950, y=590, width = 250, heigh = 90)
CL3005_7_1 = Button(lbl_CL3005_7, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3030'))
CL3005_7_1.place(x=50, y=15)
CL3005_7_2 = Button(lbl_CL3005_7, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3030'))
CL3005_7_2.place(x=145, y=15)
CL3005_7_ST = Button(lbl_CL3005_7, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3030'))
CL3005_7_ST.place(x=10, y=0)
CL3005_7_PC = Button(lbl_CL3005_7, text="ПК", width = 3, command = lambda: PC_card('PC30'))
CL3005_7_PC.place(x=10, y=30)

#Элементы стенда №31 CL3005-24 SN 3029
lbl_CL3005_8 = LabelFrame(window, text = "31")
lbl_CL3005_8.place(x = 950, y=685, width = 250, heigh = 90)
CL3005_8_1 = Button(lbl_CL3005_8, text="1-12", width = 10, command = lambda: installation_card('CL3005-24','3029'))
CL3005_8_1.place(x=10, y=15)
CL3005_8_2 = Button(lbl_CL3005_8, text="13-24", width = 10, command = lambda: installation_card('CL3005-24','3029'))
CL3005_8_2.place(x=105, y=15)
CL3005_8_ST = Button(lbl_CL3005_8, text="Уст.", width = 3, command = lambda: installation_card('CL3005-24','3029'))
CL3005_8_ST.place(x=200, y=30)
CL3005_8_PC = Button(lbl_CL3005_8, text="ПК", width = 3, command = lambda: PC_card('PC31'))
CL3005_8_PC.place(x=200, y=0)


window.mainloop()


