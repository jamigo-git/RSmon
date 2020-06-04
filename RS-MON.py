import tkinter.ttk as ttk
from tkinter import *  
from tkinter.ttk import Combobox, Button, Radiobutton, Label, Entry, Spinbox
import serial
import time
import ast
import winreg 

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

k_OPT_inter = '1A'
v_opt_inter_0 = '00'
v_opt_inter_1 = '01'
v_opt_inter_2 = '02'
v_opt_inter_3 = '03'
v_opt_inter_4 = '04'
v_opt_inter_5 = '05'
v_opt_inter_6 = '06'

k_Impuls_out = '02'
v_Aplus = '01' 
v_Aminus = '03'
v_Rplus = '02'
v_Rminus = '04'

k_Interface = '19'
v_CAN_ON = '00'
v_RS485_ON = '01'

k_VCC_inter = '14'
v_5V_ON = '00'
v_5V_OFF = '01'

k_Inter_counter = '1B'
v_CAN_OFF = '00'
v_CAN0_ON = '01'
v_CAN1_ON = '02'
Opros = '00'

white = True

connected = 0
data=0
amount = 0
parcel_rx_up = str('0')
parcel_tx = str('0')

speeds = ['1200','2400', '4800', '9600', '19200', '38400', '57600', '115200']

#Функция записи данных в реестр (последняя отправленная посылка, выбранный COM-порт)
def winreestr_push(parcel,comport):
    keyValue = 'Software\\RSMON'
    software_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software')
    winreg.CreateKey(software_key, 'RSMON')
    rsmon_key = winreg.OpenKey(software_key, 'RSMON', 0, winreg.KEY_ALL_ACCESS)
    #winreg.CreateKeyEx(rsmon_key, "last_parcel")
    winreg.SetValueEx(rsmon_key, "last_parcel" , None, winreg.REG_SZ, parcel)
    #winreg.CreateKeyEx(rsmon_key, "last_com")
    winreg.SetValueEx(rsmon_key, "last_com" , None, winreg.REG_SZ, comport)
    winreg.CloseKey(rsmon_key)

#Функция получения данных из реестра (последняя отправленная посылка, выбранный COM-порт)
def winreestr_pull():
    keyValue = 'Software\\RSMON'
    try:
        rsmon_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\RSMON')
        parcel = winreg.QueryValueEx(rsmon_key, "last_parcel")
        comport = winreg.QueryValueEx(rsmon_key, "last_com")
    except Exception:
        parcel = ("5555555500000000", 1) # при получении из реестра значения ключа получаем похожий кортеж
        comport = ("COM1", 1)            # при получении из реестра значения ключа получаем похожий кортеж
    return (parcel,comport)


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

#Функция выводит в правый угол ошибку в случае сбоя инициализации COM-порта
def com_port_bad():
    self.lbl_number_of_plate = Label(lbl_rx_data_dc, text = "Не удалось открыть COM-порт\nПовторите попытку снова\n                \n                \n                  \n                \n                 ", foreground = 'red')
    self.lbl_number_of_plate.place(x=5, y=25)

#Класс циклично отправляет посылки пока не нажата клавиша Стоп
class cycle_tx():
    def __init__(self):
        self.white = True
        self.second = 0
        btn_cycle = Button(window, text="Цикл", command = self.serial_tx_cycle).place(x=115, y=240)
        btn_stop = Button(window, text="Стоп", command = self.serial_stop).place(x=215, y=240)
        self.time = None
    #Метод цикличной отправки/приема пакетов и отображения полученных данных
    def serial_tx_cycle(self): 
        ser = serial.Serial(combo.get(), combo1.get(), timeout = 0.1)
        winreestr_push(txt.get(), combo.get()) # записываем в реестр отправлемую посылку и выбранный COM-порт
        self.second +=1
        ser.write(controller_crc_function(txt.get()))
        lbl_parcel_tx = Label(window, text = txt.get()).place(x=200, y=290)
        serial_rx(ser, txt.get())
        if self.white == True: # Индикация циклической посылки
            white = Canvas(window, width=10, height=10, bg = 'white')
            white.place(x=330, y=245)
            self.white = False
        else:
            white = Canvas(window, width=10, height=10, bg = 'black')
            white.place(x=330, y=245)
            self.white = True
        self.time = window.after(100, self.serial_tx_cycle) #здесь устанавливается время между посылками (по умолчанию задал 0.1с)

    #Метод отключает цикл отправки пакетов
    def serial_stop(self): 
        if self.time is not None:
            window.after_cancel(self.time)
            self.time = None
        else:
            return
            
#Функция отправляет заданное количество посылок, берет значения из поля тхт  
def serial_tx(): 
    try:
        ser = serial.Serial(combo.get(), combo1.get(), timeout = 0.1)
        amount = int(number_of_parcel.get())
        parcel = str(txt.get())
        winreestr_push(parcel, combo.get())
        lbl_parcel_tx = Label(window, text = 00000000000000)
        lbl_parcel_tx = Label(window, text = txt.get()).place(x=200, y=290)
        while amount != 0:
            ser.write(controller_crc_function(txt.get()))
            amount-=1
        serial_rx(ser,parcel)
    except Exception:
        comport_bad()

#Функция отправляет заранее определенный код используется для заранее обозначенных клавиш
def serial_tx_code(parcel_full): 
    try:
        ser = serial.Serial(combo.get(), combo1.get(), timeout = 0.1)
        amount = int(number_of_parcel.get())
        lbl_parcel_tx = Label(window, text = 00000000000000)
        lbl_parcel_tx = Label(window, text = parcel_full).place(x=200, y=290)
        while amount != 0:
            ser.write(controller_crc_function(parcel_full))
            amount-=1
        serial_rx(ser,parcel_full)
    except Exception:
        comport_bad()
    
        
#Функция чтения данных из COM-порта и приведения их в нормальный вид
def serial_rx(ser, parcel_tx):
    display_data_rx = ser.read(20)      #читаем 20 байт данных с порта
    parcel_hex = display_data_rx.hex()  #Переводим полученные данные в HEX-формат (убираем /x)
    parcel_hex = parcel_hex[18:]              #Удаляем отправленную посылку из принятых данных
    parcel_rx_up = parcel_hex.upper()   #Переводим все буквы в верхний регистр (для удобства)
    lbl_parcel_rx = Label(window, text = "                                 ")
    lbl_parcel_rx.place(x=200, y=320)
    lbl_parcel_rx = Label(window, text = parcel_rx_up) #Выводим в пользовательский интерфейс
    lbl_parcel_rx.place(x=200, y=320) 
    ser.close()
    rx_dc1 = rx_dc(parcel_rx_up, parcel_tx)
    rx_dc1.crc_plata(parcel_rx_up)
   
    
#Класс дешифровки принятых данных и вывода их в поле "Принятые данные"
class rx_dc():
    def __init__(self, parcel_rx_up, parcel_tx):
        self.lbl_komanda_dc = Label(lbl_rx_data_dc, text = "")
        self.lbl_komanda_dc.place(x=5, y=65)
        self.lbl_number_of_plate = Label(lbl_rx_data_dc, text = "")
        self.lbl_number_of_plate.place(x=5, y=25)
        self.lbl_version_po = Label(lbl_rx_data_dc, text = "")
        self.lbl_version_po.place(x=5, y=45)
        self.lbl_komanda = Label(lbl_rx_data_dc, text = "")
        self.lbl_komanda.place(x=5, y=45)
        self.lbl_PXIN = Label(lbl_rx_data_dc, text = "")
        self.lbl_PXIN.place(x=5, y=125)

        commands_1 = ('01', '02', '04', '06', '19', '14', '1A', '1B')
        if parcel_rx_up[4:6] == '':
            self.lbl_number_of_plate = Label(lbl_rx_data_dc, text = "Нет связи с платой!!!\n                \n                \n                \n                  \n                \n                 ", foreground = 'red')
            self.lbl_number_of_plate.place(x=5, y=25)
            return
        number_of_plate = parcel_rx_up[4:6]
        self.lbl_number_of_plate = Label(lbl_rx_data_dc, text = ("Адрес платы: " + str(int(number_of_plate, 16)).zfill(2) + '      '))
        self.lbl_number_of_plate.place(x=5, y=25)
        komanda_tx = parcel_tx[10:12]
        if komanda_tx == '00' :
            version_po = int(parcel_rx_up[8:10], 16)
            self.lbl_version_po = Label(lbl_rx_data_dc, text = ("Версия ПО:  " + str(version_po) + "     "))
            self.lbl_version_po.place(x=5, y=45)
            self.lbl_komanda = Label(lbl_rx_data_dc, text = "Команда: 00       ")
            self.lbl_komanda.place(x=5, y=65)
            self.lbl_komanda_dc = Label(lbl_rx_data_dc, text = "связь с       \nконтроллером       \n              \n               ")
            self.lbl_komanda_dc.place(x=5, y=85)
            
        elif commands_1.count(komanda_tx) != 0: #Сравнение отправленной посылки идет в шестнадцатеричной системе
            self.PXIN = str(parcel_rx_up[10:12]).zfill(2)
            komanda_rx = parcel_rx_up[6:8]
            komanda_rx = int(komanda_rx, 16)
            komanda_rx = str(komanda_rx).zfill(2)
            self.lbl_komanda = Label(lbl_rx_data_dc, text = ("Команда: " + komanda_rx + ' (Dec)'))
            self.lbl_komanda.place(x=5, y=45)

            if komanda_rx == '01': #Сравнение принятой посылки идет в десятичной системе
                self.lbl_komanda_dc['text'] = "управление     \nCAN-интерфейсом \n            "
                self.PXIN_dc()
                self.lbl_PXIN = Label(lbl_rx_data_dc, text = self.PXIN_state, foreground = 'green')
                self.lbl_PXIN.place(x=5, y=125)
                    
            elif komanda_rx == '02':
                self.lbl_komanda_dc['text'] = "управление     \nкоммутацией имп.\nвыходов     "
                self.PXIN_dc()
                self.lbl_PXIN = Label(lbl_rx_data_dc, text = self.PXIN_state, foreground = 'green')
                self.lbl_PXIN.place(x=5, y=125)

                
            elif komanda_rx == '04':
                self.lbl_komanda_dc['text'] = "перезапуск    \nUSB-интерфейсов    \nCAN-RS485_"
                self.PXIN_dc()
                self.lbl_PXIN = Label(lbl_rx_data_dc, text = self.PXIN_state, foreground = 'green')
                self.lbl_PXIN.place(x=5, y=125)
                
            elif komanda_rx == '06':
                self.lbl_komanda_dc['text'] = "управление     \nCAN-интерфейсом  n\____________"
                self.PXIN_dc()
                self.lbl_PXIN = Label(lbl_rx_data_dc, text = self.PXIN_state, foreground = 'green')
                self.lbl_PXIN.place(x=5, y=125)
                
            elif komanda_rx == '25':
                self.lbl_komanda_dc['text'] = "переключение     \nинтерфейсов      \nCAN->RS, RS->CAN  "
                if self.PXIN == '00':
                    self.lbl_PXIN = Label(lbl_rx_data_dc, text = "CAN ON          ", foreground = 'green')
                    self.lbl_PXIN.place(x=5, y=125)
                elif self.PXIN == '01':
                    self.lbl_PXIN = Label(lbl_rx_data_dc, text = "RS-485 ON       ", foreground = 'green')
                    self.lbl_PXIN.place(x=5, y=125)
                else:
                    self.lbl_PXIN = Label(lbl_rx_data_dc, text = "Ошибка распознания", foreground = 'red')
                    self.lbl_PXIN.place(x=5, y=125)
                
            elif komanda_rx == '20':
                self.lbl_komanda_dc['text'] = "упр. питанием  \nCAN-интерфейса  \nсчетчика     "
                self.PXIN_dc()
                self.lbl_PXIN = Label(lbl_rx_data_dc, text = self.PXIN_state, foreground = 'green')
                self.lbl_PXIN.place(x=5, y=125)
                
                
            elif komanda_rx == '26':
               
                self.lbl_komanda_dc['text'] = "переключение    \nоптических       \nинтерфейсов      "
                self.PXIN_dc()
                self.lbl_PXIN = Label(lbl_rx_data_dc, text = self.PXIN_state, foreground = 'green')
                self.lbl_PXIN.place(x=5, y=125)
              
            elif komanda_rx == '27':
                self.lbl_komanda_dc['text'] = "выбор интерфейса \nэлектросчетчика \n                "
                self.PXIN_dc()
                self.lbl_PXIN = Label(lbl_rx_data_dc, text = self.PXIN_state, foreground = 'green')
                self.lbl_PXIN.place(x=5, y=125)
                 
    def PXIN_dc(self): # Функция дешифрует биты порта PXIN ответной посылки контроллера 
        PXINb = int(self.PXIN,16)
        Interface = ''
        Impuls_out = ''
        PXIN_state = ''
        _5v_bit_up = (PXINb & 8)

        inter_bits = PXINb &  4
        t_inter_bits = PXINb & 112
        CAN_inters = 4
        CAN_inter = 64
        CAN_inter_0 = 96
        CAN_inter_1 = 80
        
        RS_inter = 101
        RS_inter_0 = 96
        RS_inter_1 = 80

        impuls_bits = PXINb & 3
        
        Aplus = 1
        Aminus = 0
        Rplus = 3
        Rminus = 2
        
        if _5v_bit_up != 0:
            _5v_bit = ' 5V OFF '     
        else:
            _5v_bit = ' 5V ON '
            
        if CAN_inters == inter_bits:
            if CAN_inter == t_inter_bits:
                Interface = ' CAN '
            elif CAN_inter_1 == t_inter_bits:
                Interface = ' CAN1 '
            elif CAN_inter_0 == t_inter_bits:
                Interface = ' CAN0 '

        if inter_bits == 0:
            if RS_inter == t_inter_bits:
                Interface = ' RS485 '
            elif RS_inter_0 == t_inter_bits:
                Interface = ' RS485_0 '
            elif RS_inter_1 == t_inter_bits:
                Interface = ' RS485_1 '

        if Aplus == impuls_bits:
            Impuls_out = ' A+     '
        elif Aminus == impuls_bits:
            Impuls_out = ' A-     '
        elif Rplus == impuls_bits:
            Impuls_out = ' R+     '
        elif Rminus == impuls_bits:
            Impuls_out = ' R-     '
        self.PXIN_state = _5v_bit + Interface + Impuls_out
        return (self.PXIN_state)
    
    def komanda_03_dc(parcel_rx_up):
        lbl_komanda_dc = Label(lbl_rx_data_dc, text = "выбор счит.   \nканала таймера   ").place(x=5, y=65)
       

    def crc_plata(self, parcel_rx_up): #функция вычисляет CRC принятой посылки и выводит значение проверки
        crc256_rx = parcel_rx_up[12:14]
        crc256_chk = hex(sum(bytes.fromhex(parcel_rx_up[0:12])) % 256)[2:] #Вычисляем контрольную сумму по модулю 256, убираем 0x перед шестнадцатеричным числом
        if crc256_rx == crc256_chk.upper():
            lbl_crc = Label(lbl_rx_data_dc, text = "CRC: ОК   ", foreground = 'Green').place(x=5, y=5)
        else:
            lbl_crc = Label(lbl_rx_data_dc, text = "CRC: BAD  ", foreground = 'Red').place(x=5, y=5)
    

#Main program
window = Tk()  
window.title("Программа для проверки плат коммутации Incotex (by Jamigo)")  
window.geometry('600x500')
window.bind_all("<Key>", _onKeyRelease, "+") #Включаем подержку нажатий клавиш Ctr-C, Ctr-V, Ctr-X

sel_interface = IntVar()
sel_interface.set(1)
lbl_inter = LabelFrame(window, text='Интерфейсы')
lbl_inter.place(x=5, y=0, width = 200)
rad1 = Radiobutton(lbl_inter, text='CAN', value=1, variable=sel_interface)
rad1.pack(side=LEFT)
#rad2 = Radiobutton(lbl_inter, text='RS-485', value=2, variable=sel_interface)
#rad2.pack(side=LEFT)  

sel_CRC = IntVar()
lbl_CRC = LabelFrame(window, text = "CRC")
lbl_CRC.place(x = 5, y=50, width = 300)
rad_controller = Radiobutton(lbl_CRC, text='Контроллер', value=1, variable=sel_CRC)
rad_controller.pack(side=LEFT)
#rad_counter = Radiobutton(lbl_CRC, text='Счетчик', value=2, variable=sel_CRC)
#rad_counter.pack(side=LEFT)                
#rad_wocrc = Radiobutton(lbl_CRC, text='Без CRC', value=3, variable=sel_CRC)
#rad_wocrc.pack(side=LEFT)
sel_CRC.set(1)


reestr_com = winreestr_pull()[1]       # присваиваем переменной кортеж значений (0-последняя посылка из реестра (кортеж), 1-последний выбраный COM-порт (кортеж))

lbl0 = Label(window, text = "Выберите COM-порт:").place(x=15, y=100)
combo = Combobox(window, values = serial_ports())
combo.place(x=15, y=120)
combo.bind('<<ComboboxSelected>>', com_port_state) #вызываем функцию отображения состояния порта
combo.set(reestr_com[0])   # устанавливае при запуске программы значение COM-порта из реестра

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

reestr_parcel = winreestr_pull()[0] # забираем из кортежа (при получении из реестра (parcel, 1)) значение parcel
txt = Entry(window, width=30)  # поле для ввода посылки
txt.place(x=15, y=210) 
txt.delete(0, "end")
txt.insert(0, reestr_parcel[0])        
txt.focus()                   # при запуске программы фокусируемся в данном поле

menu = Menu(tearoff=0) #пункты меню всплывающего в текстовом поле при нажатии правой клавиши
menu.add_command(label='Копировать', command = lambda: txt.event_generate("<<Copy>>"))
menu.add_command(label="Вставить", command = lambda: txt.event_generate("<<Paste>>"))
menu.add_command(label="Вырезать", command = lambda: txt.event_generate("<<Cut>>"))
txt.bind("<Button-3>", mouse_button3) #нажатие на правую клавишу вызывает функцию всплывающего меню

btn_send = Button(window, text="Отправить", command = serial_tx).place(x=15, y=240)
cycle = cycle_tx() # активируем класс с кнопками "Цикл" и "Стоп" см. выше


lbl3 = Label(window, text = 'Отправленные данные:').place(x=15, y=290)
lbl4 = Label(window, text = 'Принятые данные:').place(x=15, y=320)

lbl_optic = LabelFrame(window, text = "Опт. интерфейсы")
lbl_optic.place(x = 420, y=190, width = 130, heigh = 150)
btn_CAN_01 = Button(lbl_optic, text="Opto1 ", command = lambda: serial_tx_code(Parcel(k_OPT_inter, v_opt_inter_1)), width = 5).place(x=5, y=0)
btn_CAN_02 = Button(lbl_optic, text="Opto2 ", command = lambda: serial_tx_code(Parcel(k_OPT_inter, v_opt_inter_2)), width = 5).place(x=5, y=30)
btn_CAN_03 = Button(lbl_optic, text="Opto3 ", command = lambda: serial_tx_code(Parcel(k_OPT_inter, v_opt_inter_3)), width = 5).place(x=5, y=60)
btn_CAN_04 = Button(lbl_optic, text="Opto4 ", command = lambda: serial_tx_code(Parcel(k_OPT_inter, v_opt_inter_4)), width = 5).place(x=5, y=90)
btn_CAN_05 = Button(lbl_optic, text="Opto5 ", command = lambda: serial_tx_code(Parcel(k_OPT_inter, v_opt_inter_5)), width = 5).place(x=65, y=0)
btn_CAN_06 = Button(lbl_optic, text="Opto6 ", command = lambda: serial_tx_code(Parcel(k_OPT_inter, v_opt_inter_6)), width = 5).place(x=65, y=30)
btn_CAN_06 = Button(lbl_optic, text="OFF ", command = lambda: serial_tx_code(Parcel(k_OPT_inter, v_opt_inter_0)), width = 5).place(x=65, y=60)

lbl_impuls_out = LabelFrame(window, text = "Имп. выходы")
lbl_impuls_out.place(x = 15, y=350, width = 120, heigh = 145)
btn_Aplus = Button(lbl_impuls_out, text="А+ ", command = lambda: serial_tx_code(Parcel(k_Impuls_out,v_Aplus))).place(x=5, y=0)
btn_Aminus = Button(lbl_impuls_out, text="А- ", command = lambda: serial_tx_code(Parcel(k_Impuls_out,v_Aminus))).place(x=5, y=30)
btn_Rplus = Button(lbl_impuls_out, text="R+ ", command = lambda: serial_tx_code(Parcel(k_Impuls_out,v_Rplus))).place(x=5, y=60)
btn_Rminus = Button(lbl_impuls_out, text="R- ", command = lambda: serial_tx_code(Parcel(k_Impuls_out,v_Rminus))).place(x=5, y=90)

lbl_interface = LabelFrame(window, text = "Интер. CAN-RS")
lbl_interface.place(x = 150, y=350, width = 120, heigh = 145)
btn_CAN_ON = Button(lbl_interface, text="CAN_ON ", command = lambda: serial_tx_code(Parcel(k_Interface, v_CAN_ON))).place(x=5, y=0)
btn_RS485_ON = Button(lbl_interface, text="RS485_ON ", command = lambda: serial_tx_code(Parcel(k_Interface, v_RS485_ON))).place(x=5, y=30)
btn_5V_ON = Button(lbl_interface, text="5V ON Сч", command = lambda: serial_tx_code(Parcel(k_VCC_inter, v_5V_ON))).place(x=5, y=60)
btn_5V_OFF = Button(lbl_interface, text="5V OFF Сч", command = lambda: serial_tx_code(Parcel(k_VCC_inter, v_5V_OFF))).place(x=5, y=90)

lbl_CAN = LabelFrame(window, text = "CAN-плата")
lbl_CAN.place(x = 285, y=350, width = 130, heigh = 145)
btn_CAN_01 = Button(lbl_CAN, text="CAN1 ", command = lambda: serial_tx_code(Parcel(k_CAN_inter, v_interface_1)), width = 5).place(x=5, y=0)
btn_CAN_02 = Button(lbl_CAN, text="CAN2 ", command = lambda: serial_tx_code(Parcel(k_CAN_inter, v_interface_2)), width = 5).place(x=5, y=30)
btn_CAN_03 = Button(lbl_CAN, text="CAN3 ", command = lambda: serial_tx_code(Parcel(k_CAN_inter, v_interface_3)), width = 5).place(x=5, y=60)
btn_CAN_04 = Button(lbl_CAN, text="CAN4 ", command = lambda: serial_tx_code(Parcel(k_CAN_inter, v_interface_4)), width = 5).place(x=5, y=90)
btn_CAN_05 = Button(lbl_CAN, text="CAN5 ", command = lambda: serial_tx_code(Parcel(k_CAN_inter, v_interface_5)), width = 5).place(x=65, y=0)
btn_CAN_06 = Button(lbl_CAN, text="CAN6 ", command = lambda: serial_tx_code(Parcel(k_CAN_inter, v_interface_6)), width = 5).place(x=65, y=30)

lbl_counter = LabelFrame(window, text = "Инт. счетчик")
lbl_counter.place(x = 420, y=350, width = 130, heigh = 110)
btn_CAN_OFF = Button(lbl_counter, text="Inter_All_OFF ", command = lambda: serial_tx_code(Parcel(k_Inter_counter, v_CAN_OFF))).place(x=5, y=0)
btn_CAN0_ON = Button(lbl_counter, text="Int_0_ON ", command = lambda: serial_tx_code(Parcel(k_Inter_counter, v_CAN0_ON))).place(x=5, y=30)
btn_CAN1_ON = Button(lbl_counter, text="Int_1_ON ", command = lambda: serial_tx_code(Parcel(k_Inter_counter, v_CAN1_ON))).place(x=5, y=60)

btn_opros = Button(window, text="Опросить ", command = lambda: serial_tx_code(Parcel(Opros,Opros)))
btn_opros.place(x=430, y=465)


lbl_rx_data_dc = LabelFrame(window, text = "Принятые данные")
lbl_rx_data_dc.place(x = 420, y=0, width = 150, heigh = 180)


window.mainloop()


