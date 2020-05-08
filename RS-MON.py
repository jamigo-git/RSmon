from tkinter import *  
from tkinter.ttk import *
from tkinter import Tk, Frame, Menu
import serial
import time


#def counter_crc_funcion():
    
def _onKeyRelease(event):   #Работа с буфером по клавишам Ctr-C, Ctr-V, Ctr-X
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

def serial_ports(): #Funcrion find all com-ports in Windows
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

Aplus = '5555555500020100' 
Aminus = '5555555500020300'
Rplus = '5555555500020200'
Rminus = '5555555500020400'
CAN_ON = '5555555500190000'
RS485_ON = '5555555500190100'
CAN_OFF = '55555555001B0000'
CAN0_ON = '55555555001B0100'
CAN1_ON = '55555555001B0200'
connected = 0
data=0
amount = 0
stop = 0

speeds = ['1200','2400', '4800', '9600', '19200', '38400', '57600', '115200']

def serial_tx_cycle(): #Функция отправляет 1000 посылок, берет значения из поля тхт
    ser = serial.Serial(combo.get(), combo1.get())
    ser.write(controller_crc_function(txt.get()))
    lbl_parcel_tx = Label(window, text = txt.get()).place(x=250, y=290)
    if stop == False:
        window.after(1000, serial_tx_cycle)
    else:
        ser.close()
        return

def serial_tx(): #Функция отправляет заданное количество посылок, берет значения из поля тхт
    ser = serial.Serial(combo.get(), combo1.get())
    amount = int(number_of_parcel.get())
    while amount != 0:
        ser.write(controller_crc_function(txt.get()))
        display = txt.get()
        lbl_parcel_tx = Label(window, text = 00000000000000)
        lbl_parcel_tx = Label(window, text = display).place(x=250, y=290)
        amount -=1
        display_data_rx =ser.read(20)
        print(display_data_rx)
        
        lbl_parcel_rx = Label(window, text = display_data_rx)
    ser.close()

def serial_tx_code(parcel): #Функция отправляет заранее определенный код
    ser = serial.Serial(combo.get(), combo1.get(), timeout = 1)
    amount = int(number_of_parcel.get())
    while amount!=0:
        ser.write(controller_crc_function(parcel))
        lbl_parcel_tx = Label(window, text = 00000000000000)
        lbl_parcel_tx = Label(window, text = parcel).place(x=250, y=290)
        amount-=1
        display_data_rx = ser.read(20)      #читаем 20 байт данных с порта
        parcel_hex = display_data_rx.hex()  #Переводим полученные данные в HEX-формат (убираем /x)
        parcel_hex = parcel_hex[18:]              #Удаляем отправленную посылку из принятых данных
        parcel_rx_up = parcel_hex.upper()   #Переводим все буквы в верхний регистр (для удобства)
        lbl_parcel_rx = Label(window, text = parcel_rx_up).place(x=250, y=320) #Выводим в пользовательский интерфейс
    ser.close()
    

def serial_stop(): #Функция отключает общение с COM-портом
    stop = True
   
window = Tk()  #Main program
window.title("Программа для проверки доработок Incotex")  
window.geometry('600x500')
window.bind_all("<Key>", _onKeyRelease, "+") #Включаем подержку нажатий клавиш Ctr-C, Ctr-V, Ctr-X

sel_interface = IntVar()
sel_interface.set(1)
lbl_inter = LabelFrame(window, text='Интерфейсы')
lbl_inter.pack(fill=X)
rad1 = Radiobutton(lbl_inter, text='CAN', value=1, variable=sel_interface)
rad1.pack(side=LEFT)
rad2 = Radiobutton(lbl_inter, text='RS-485', value=2, variable=sel_interface)
rad2.pack(side=LEFT)  

sel_CRC = IntVar()
lbl_CRC = LabelFrame(window, text = "CRC")
lbl_CRC.pack(fill=X)
rad_controller = Radiobutton(lbl_CRC, text='Контроллер', value=1, variable=sel_CRC)
rad_controller.pack(side=LEFT)
rad_counter = Radiobutton(lbl_CRC, text='Счетчик', value=2, variable=sel_CRC)
rad_counter.pack(side=LEFT)                
rad_wocrc = Radiobutton(lbl_CRC, text='Без CRC', value=3, variable=sel_CRC)
rad_wocrc.pack(side=LEFT)
sel_CRC.set(1)

lbl0 = Label(window, text = "Выберите COM-порт:").place(x=15, y=100)
combo = Combobox(window)
combo.place(x=15, y=120)
combo['values'] = (serial_ports())
combo.current(0)

lbl01 = Label(window, text = "Выберите скорость:").place(x=200, y=100)
combo1 = Combobox(window)
combo1.place(x=200, y=120)
combo1['values'] = (speeds)
combo1.current(3)

lbl2 = Label(window, text = "Отправка произвольной посылки:").place(x=15, y=150)
number_of_parcel = Spinbox(window, from_=1, to=20, width=5) #модуль для выбора количества посылок
number_of_parcel.place(x=15,y=180)
number_of_parcel.delete(0,"end")                            #удаление всех элементов из модуля, для установки значения по умолчанию
number_of_parcel.insert(0,1)                                #установка значения по умолчанию 1
lbl_number_of_parcel = Label(window, text="Кол-во повторов").place(x=100, y=180)

number_of_plate = Spinbox(window, from_=0, to=256, width=5) #модуль для выбора количества посылок
number_of_plate.place(x=220,y=180)
number_of_plate.delete(0,"end")                            #удаление всех элементов из модуля, для установки значения по умолчанию
number_of_plate.insert(0,0)                                #установка значения по умолчанию 1
lbl_number_of_plate = Label(window, text="Номер платы").place(x=310, y=180)

txt = Entry(window, width=30)  # поле для ввода посылки
txt.place(x=15, y=210) 
txt.focus()                   # при запуске программы фокусируемся в данном поле

menu = Menu(tearoff=0) #пункты меню всплывающего в текстовом поле при нажатии правой клавиши
menu.add_command(label='Копировать', command = lambda: txt.event_generate("<<Copy>>"))
menu.add_command(label="Вставить", command = lambda: txt.event_generate("<<Paste>>"))
menu.add_command(label="Вырезать", command = lambda: txt.event_generate("<<Cut>>"))
txt.bind("<Button-3>", mouse_button3) #нажатие на правую клавишу вызывает функцию всплывающего меню

btn_send = Button(window, text="Отправить", command = serial_tx).place(x=270, y=210)
btn_cycle = Button(window, text="Цикл", command = serial_tx_cycle).place(x=370, y=210)
btn_stop = Button(window, text="Стоп", command = serial_stop).place(x=470, y=210)

lbl3 = Label(window, text = 'Отправленные данные:').place(x=15, y=290)
lbl4 = Label(window, text = 'Принятые данные:').place(x=15, y=320)

btn_Aplus = Button(window, text="А+ ", command = lambda: serial_tx_code(Aplus)).place(x=15, y=350)
btn_Aminus = Button(window, text="А- ", command = lambda: serial_tx_code(Aminus)).place(x=15, y=380)
btn_Rplus = Button(window, text="R+ ", command = lambda: serial_tx_code(Rplus)).place(x=15, y=410)
btn_Rminus = Button(window, text="R- ", command = lambda: serial_tx_code(Rminus)).place(x=15, y=440)
btn_CAN_ON = Button(window, text="CAN_ON ", command = lambda: serial_tx_code(CAN_ON)).place(x=150, y=350)
btn_CAN_OFF = Button(window, text="CAN_OFF ", command = lambda: serial_tx_code(CAN_OFF)).place(x=150, y=380)
btn_RS485_ON = Button(window, text="RS485_ON ", command = lambda: serial_tx_code(RS485_ON)).place(x=150, y=410)
btn_CAN0_ON = Button(window, text="CAN0_ON ", command = lambda: serial_tx_code(CAN0_ON)).place(x=150, y=440)
btn_CAN1_ON = Button(window, text="CAN1_ON ", command = lambda: serial_tx_code(CAN1_ON)).place(x=285, y=350)


window.mainloop()


