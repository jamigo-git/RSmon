from tkinter import *  
from tkinter.ttk import Combobox, Button, Radiobutton, Label, Entry, Spinbox
from tkinter import Tk, Frame, Menu
import serial
import time


#Переменные и константы
Start = '55555555'
Stop = '00'
Number_plate = '00'

k_CAN_inter = '01'
v_interface_1 = '01'
v_interface_2 = '02'
v_interface_3 = '03'
v_interface_4 = '04'
v_interface_5 = '05'
v_interface_6 = '06'

k_Impuls_out = '02'
v_Aplus = '01' 
v_Aminus = '03'
v_Rplus = '02'
v_Rminus = '04'

k_Interface = '19'
v_CAN_ON = '00'
v_RS485_ON = '01'

k_Inter_counter = '1B'
v_CAN_OFF = '00'
v_CAN0_ON = '01'
v_CAN1_ON = '02'

Opros = '00'


connected = 0
data=0
amount = 0
stop = False
flag = 0
speeds = ['1200','2400', '4800', '9600', '19200', '38400', '57600', '115200']



#Функция собирает посылку в зависимости от нажатых клавиш и выбора платы
def Parcel(komanda, value):
    Number_plate = hex(int(number_of_plate.get()))[2:]
    parcel_full = Start + str(Number_plate).zfill(2) + komanda + value + Stop
    return parcel_full

#def counter_crc_funcion():
    
#Работа с буфером по клавишам Ctr-C, Ctr-V, Ctr-X
def _onKeyRelease(event):   
    ctrl = (event.state & 0x4) != 0
    if event.keycode==88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")
    if event.keycode==86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")
    if event.keycode==67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")
        
def mouse_button3(event): # Функция отрабатывает нажатие ПКМ на текстовом поле и выводит меню
    global x,y
    x = event.x
    y = event.y
    menu.post(event.x_root, event.y_root)

def controller_crc_function(parcel):                   #Функция вычисляет контрольную сумму посылки и добавляет ее к исходным данным
    crc256 = hex(sum(bytes.fromhex(parcel)) % 256)[2:] #Вычисляем контрольную сумму по модулю 256, убираем 0x перед шестнадцатеричным числом
    parcel_crc = bytes.fromhex(parcel + str(crc256))   #Добавляем контрольную сумму к нашей строке и переводим в байты
    return (parcel_crc)

#Функция находит все свободные COM-порты в системе и добавляет их в список result
def serial_ports(): 
    ports = ['COM%s' % (i + 1) for i in range(256)]
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

#Функция проверяет состояние выбранного COM-порта
def com_port_state(ser):
    ser = serial.Serial(combo.get(), combo1.get())
    if ser.cd == True: # Если на линии обнаружен CD - рисуем зеленый квадрат
        com_port_state = Canvas(window, width=10, height=10, bg = 'green').place(x=400, y=125)
    else:
        com_port_state = Canvas(window, width=10, height=10, bg = 'red').place(x=400, y=125)
        
#Функция циклично отправляет посылки пока не нажата клавиша Стоп
def serial_tx_cycle(): 
    ser = serial.Serial(combo.get(), combo1.get(), timeout = 0.1)
    ser.write(controller_crc_function(txt.get()))
    lbl_parcel_tx = Label(window, text = txt.get()).place(x=200, y=290)
    serial_rx(ser)
    if stop == False:
        end = window.after(1000, serial_tx_cycle)
            
#Функция отправляет заданное количество посылок, берет значения из поля тхт  
def serial_tx(): 
    ser = serial.Serial(combo.get(), combo1.get(), timeout = 0.1)
    amount = int(number_of_parcel.get())
    parcel = str(txt.get())
    lbl_parcel_tx = Label(window, text = 00000000000000)
    lbl_parcel_tx = Label(window, text = txt.get()).place(x=200, y=290)
    while amount != 0:
        ser.write(controller_crc_function(txt.get()))
        amount-=1
        serial_rx(ser)

#Функция отправляет заранее определенный код используется для заранее обозначенных клавиш
def serial_tx_code(parcel_full): 
    ser = serial.Serial(combo.get(), combo1.get(), timeout = 0.1)
    amount = int(number_of_parcel.get())
    lbl_parcel_tx = Label(window, text = 00000000000000)
    lbl_parcel_tx = Label(window, text = parcel_full).place(x=200, y=290)
    while amount != 0:
        ser.write(controller_crc_function(parcel_full))
        amount-=1
        serial_rx(ser)
        
#Функция чтения данных из COM-порта и приведения их в нормальный вид
def serial_rx(ser):
    display_data_rx = ser.read(20)      #читаем 20 байт данных с порта
    parcel_hex = display_data_rx.hex()  #Переводим полученные данные в HEX-формат (убираем /x)
    parcel_hex = parcel_hex[18:]              #Удаляем отправленную посылку из принятых данных
    parcel_rx_up = parcel_hex.upper()   #Переводим все буквы в верхний регистр (для удобства)
    lbl_parcel_rx = Label(window, text = parcel_rx_up).place(x=200, y=320) #Выводим в пользовательский интерфейс
    ser.close()

#Функция отключает цикл отправки пакетов
def serial_stop(): 
    global flag
    global stop
    if flag != 2:
        if stop == False:
            stop = True
            flag = 1
            btn_stop_mark = Canvas(window, width=10, height=10, bg="red").place(x=320, y=245)
        else:
            stop = False
            flag = 2
            btn_stop_mark = Canvas(window, width=10, height=10, bg="green").place(x=320, y=245)
    flag = 0
        
#Main program
window = Tk()  
window.title("Программа для проверки доработок Incotex")  
window.geometry('600x500')
window.bind_all("<Key>", _onKeyRelease, "+") #Включаем подержку нажатий клавиш Ctr-C, Ctr-V, Ctr-X

sel_interface = IntVar()
sel_interface.set(1)
lbl_inter = LabelFrame(window, text='Интерфейсы')
lbl_inter.place(x=5, y=0, width = 200)
rad1 = Radiobutton(lbl_inter, text='CAN', value=1, variable=sel_interface)
rad1.pack(side=LEFT)
rad2 = Radiobutton(lbl_inter, text='RS-485', value=2, variable=sel_interface)
rad2.pack(side=LEFT)  

sel_CRC = IntVar()
lbl_CRC = LabelFrame(window, text = "CRC")
lbl_CRC.place(x = 5, y=50, width = 300)
rad_controller = Radiobutton(lbl_CRC, text='Контроллер', value=1, variable=sel_CRC)
rad_controller.pack(side=LEFT)
rad_counter = Radiobutton(lbl_CRC, text='Счетчик', value=2, variable=sel_CRC)
rad_counter.pack(side=LEFT)                
rad_wocrc = Radiobutton(lbl_CRC, text='Без CRC', value=3, variable=sel_CRC)
rad_wocrc.pack(side=LEFT)
sel_CRC.set(1)

lbl0 = Label(window, text = "Выберите COM-порт:").place(x=15, y=100)
combo = Combobox(window, values = serial_ports())
combo.place(x=15, y=120)
combo.current(0)
combo.bind('<<ComboboxSelected>>', com_port_state) #вызываем функцию отображения состояния порта

lbl01 = Label(window, text = "Выберите скорость:").place(x=200, y=100)
combo1 = Combobox(window, values = speeds)
combo1.place(x=200, y=120)
combo1.current(3)

lbl2 = Label(window, text = "Отправка произвольной посылки:").place(x=15, y=150)
number_of_parcel = Spinbox(window, from_=1, to=20, width=5) #модуль для выбора количества посылок
number_of_parcel.place(x=15,y=180)
number_of_parcel.delete(0,"end")                            #удаление всех элементов из модуля, для установки значения по умолчанию
number_of_parcel.insert(0,1)                                #установка значения по умолчанию 1
lbl_number_of_parcel = Label(window, text="Кол-во повторов").place(x=100, y=180)

number_of_plate = Spinbox(window, from_=0, to=256, width=5) #модуль для выбора количества посылок
number_of_plate.place(x=220,y=180)
number_of_plate.delete(00,"end")                            #удаление всех элементов из модуля, для установки значения по умолчанию
number_of_plate.insert(0,00)                                #установка значения по умолчанию 1
lbl_number_of_plate = Label(window, text="Номер платы").place(x=310, y=180)


txt = Entry(window, width=30)  # поле для ввода посылки
txt.place(x=15, y=210) 
txt.delete(0, "end")
txt.insert(0, 5555555500000000)
txt.focus()                   # при запуске программы фокусируемся в данном поле

menu = Menu(tearoff=0) #пункты меню всплывающего в текстовом поле при нажатии правой клавиши
menu.add_command(label='Копировать', command = lambda: txt.event_generate("<<Copy>>"))
menu.add_command(label="Вставить", command = lambda: txt.event_generate("<<Paste>>"))
menu.add_command(label="Вырезать", command = lambda: txt.event_generate("<<Cut>>"))
txt.bind("<Button-3>", mouse_button3) #нажатие на правую клавишу вызывает функцию всплывающего меню

btn_send = Button(window, text="Отправить", command = serial_tx).place(x=15, y=240)
btn_cycle = Button(window, text="Цикл", command = serial_tx_cycle).place(x=115, y=240)
btn_stop = Button(window, text="Стоп", command = serial_stop).place(x=215, y=240)

lbl3 = Label(window, text = 'Отправленные данные:').place(x=15, y=290)
lbl4 = Label(window, text = 'Принятые данные:').place(x=15, y=320)

btn_Aplus = Button(window, text="А+ ", command = lambda: serial_tx_code(Parcel(k_Impuls_out,v_Aplus))).place(x=15, y=350)
btn_Aminus = Button(window, text="А- ", command = lambda: serial_tx_code(Parcel(k_Impuls_out,v_Aminus))).place(x=15, y=380)
btn_Rplus = Button(window, text="R+ ", command = lambda: serial_tx_code(Parcel(k_Impuls_out,v_Rplus))).place(x=15, y=410)
btn_Rminus = Button(window, text="R- ", command = lambda: serial_tx_code(Parcel(k_Impuls_out,v_Rminus))).place(x=15, y=440)

btn_CAN_ON = Button(window, text="CAN_ON ", command = lambda: serial_tx_code(Parcel(k_Interface, v_CAN_ON))).place(x=150, y=350)
btn_RS485_ON = Button(window, text="RS485_ON ", command = lambda: serial_tx_code(Parcel(k_Interface, v_RS485_ON))).place(x=150, y=380)
btn_opros = Button(window, text="Опросить ", command = lambda: serial_tx_code(Parcel(Opros,Opros))).place(x=150, y=440)

btn_CAN_01 = Button(window, text="CAN1 ", command = lambda: serial_tx_code(Parcel(k_CAN_inter, v_interface_1)), width = 5).place(x=285, y=350)
btn_CAN_02 = Button(window, text="CAN2 ", command = lambda: serial_tx_code(Parcel(k_CAN_inter, v_interface_2)), width = 5).place(x=285, y=380)
btn_CAN_03 = Button(window, text="CAN3 ", command = lambda: serial_tx_code(Parcel(k_CAN_inter, v_interface_3)), width = 5).place(x=285, y=410)
btn_CAN_04 = Button(window, text="CAN4 ", command = lambda: serial_tx_code(Parcel(k_CAN_inter, v_interface_4)), width = 5).place(x=285, y=440)
btn_CAN_05 = Button(window, text="CAN5 ", command = lambda: serial_tx_code(Parcel(k_CAN_inter, v_interface_5)), width = 5).place(x=345, y=350)
btn_CAN_06 = Button(window, text="CAN6 ", command = lambda: serial_tx_code(Parcel(k_CAN_inter, v_interface_6)), width = 5).place(x=345, y=380)

btn_CAN_OFF = Button(window, text="CAN_All_OFF ", command = lambda: serial_tx_code(Parcel(k_Inter_counter, v_CAN_OFF))).place(x=420, y=350)
btn_CAN0_ON = Button(window, text="CAN0_ON ", command = lambda: serial_tx_code(Parcel(k_Inter_counter, v_CAN0_ON))).place(x=420, y=380)
btn_CAN1_ON = Button(window, text="CAN1_ON ", command = lambda: serial_tx_code(k_Inter_counter, v_CAN1_ON)).place(x=420, y=410)


window.mainloop()


