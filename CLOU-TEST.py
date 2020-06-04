import tkinter.ttk as ttk
from tkinter import *  
from tkinter.ttk import Combobox, Button, Radiobutton, Label, Entry, Spinbox
import serial
import time
import winreg



version_reply = '81161720434C333131563220342E3233'
stop_parcel = '8110200749FF818110200846FF00818110200847FF00808110200849FF8E8110200863FF00A4812000263500103FFFFFFFFFFFFF00405000000000000000000000000000320000006400005A'



start_st_parcel = '8110200749FF818110200846FF00818110200847FF00808110200849FF8E8110200863FF00A4812000263500'
first_st_parcel = 'FFFFFFFFFFFFF004'
second_st_parcel = '00000'
end_st_parcel = '00000032000000640000'

current_values = ('0', '0.02', '0.05', '0.1', '0.25', '0.5', '1', '2.5', '5', '10', '25', '60', '100')
current_0A = ('500','0000')
current_002A = ('510','0002')
current_005A = ('520','0005')
current_01A = ('530','000A')
current_025A = ('540','0019')
current_05A = ('550','0032')
current_1A = ('560','0064')
current_2_5A = ('570','00FA')
current_5A = ('580','01F4')
current_10A = ('590','03E8')
current_25A = ('5A0','09C4')
current_60A = ('5B0','1770')
current_100A = ('5C0','2710')
current_dict = {'0':current_0A, '0.02':current_002A, '0.05':current_005A, '0.1':current_01A,
                '0.25':current_025A, '0.5':current_05A, '1':current_1A, '2.5':current_2_5A,
                '5':current_5A, '10':current_10A, '25':current_25A, '60':current_60A, '100':current_100A}

voltage_0V = ('0','0000000')
voltage_57V =('0','039B333')
voltage_230V =('2','0E60000')
voltage_270V =('3', '112D999')
voltage_dict = {1:voltage_57V, 2:voltage_230V, 3:voltage_270V}

phase_ALL = '103'
phase_A = '113'
phase_B = '123'
phase_C = '133'

speeds = ['1200','2400', '4800', '9600', '19200', '38400', '57600', '115200']


#Функция записи данных в реестр (последняя отправленная посылка, выбранный COM-порт)
def winreestr_push(comport):
    software_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software')
    winreg.CreateKey(software_key, 'CL3000')
    rsmon_key = winreg.OpenKey(software_key, 'CL3000', 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(rsmon_key, "last_com" , None, winreg.REG_SZ, comport)
    winreg.CloseKey(rsmon_key)

#Функция получения данных из реестра (последняя отправленная посылка, выбранный COM-порт)
def winreestr_pull():
    try:
        rsmon_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\CL3000')
        comport = winreg.QueryValueEx(rsmon_key, "last_com")
    except Exception:
        comport = ("COM1", 1)            # при получении из реестра значения ключа получаем похожий кортеж
    return (comport)

#Функция получения данных из реестра (если стоит программ 3ph-поверка Inkotex)
def winreestr_pull_inkotex():
    try:
        rsmon_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Incotex\\3Ph_pm\\Clou_v4.23')
        comport = winreg.QueryValueEx(rsmon_key, "Clou_COM")
    except Exception:
        comport = ("COM1", 1)            # при получении из реестра значения ключа получаем похожий кортеж
    combo.set(comport[0])


#Функция собирает посылку в зависимости от нажатых клавиш и выбора платы
def Parcel_func():
    phase = str(sel_phase.get())
    voltage = voltage_dict[sel_voltage.get()]
    current = current_dict[spinbox_current.get()]
    angle = hex(int(spinbox_angle.get()))[2:]
    angle = angle.zfill(3)
    parcel = start_st_parcel + phase + first_st_parcel + voltage[0] + current[0]+ voltage[1] + current [1]+ second_st_parcel + angle.upper() + end_st_parcel
    parcel_crc = parcel_crc_function(parcel)
    parcel_full = bytes.fromhex(parcel + parcel_crc)
    return parcel_full

def get_value():
    print('Значение спинбокс ток get: ', spinbox_current.get(), type( spinbox_current.get()))
    print('Значение тока 1: ', current_dict[spinbox_current.get()][0], type(current_dict[spinbox_current.get()][0]))
    print('Значение тока 2: ', current_dict[spinbox_current.get()][1], type (current_dict[spinbox_current.get()][1]))
    print('Значение напряжения 1: ', voltage_dict[sel_voltage.get()][0], type(voltage_dict[sel_voltage.get()][0]))
    print('Значение напряжения 2: ', voltage_dict[sel_voltage.get()][1], type(voltage_dict[sel_voltage.get()][1]))
    print('Значение фазы: ', sel_phase.get(), type(str(sel_phase.get())))
    print('Значение угла: ', hex(int(spinbox_angle.get()))[2:], type(hex(int(spinbox_angle.get()))))

    
def parcel_crc_function(parcel):                   #Функция вычисляет контрольную сумму посылки и добавляет ее к исходным данным
    xor8 = bytes.fromhex(parcel)
    z = 0
    for i in xor8:
        if z == 0:
            k = xor8[0]
            z+=1
        else:
            k = i^k
    k = hex(k).upper()[2:]
    parcel_crc = k.zfill(2)
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
        com_port_state = Canvas(window, width=10, height=10, bg = 'green')
        com_port_state.place(x=400, y=40)
    else:
        com_port_state = Canvas(window, width=10, height=10, bg = 'red')
        com_port_state.place(x=400, y=40)


#Функция отправляет посылку установке
def serial_tx(parcel):
    try:
        lbl_error_com = Label(lbl_rx_data_dc, text = "                                                    \n                \n                \n                  \n                \n                 ", foreground = 'red')
        lbl_error_com.place(x=5, y=5)
        ser = serial.Serial(combo.get(), combo1.get(), timeout = 0.1)
        winreestr_push(combo.get())
        ser.write(parcel)
       # serial_rx(ser,parcel)
    except Exception:
        lbl_error_com = Label(lbl_rx_data_dc, text = "Не удалось открыть COM-порт\nПовторите попытку снова\n                \n                \n                  \n                \n                 ", foreground = 'red')
        lbl_error_com.place(x=5, y=5)

        
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
   
    
#Main program
    
window = Tk()  
window.title("Программа для диагностики устновок CLOU 3F (by Jamigo)")  
window.geometry('600x500')

btn_opros = Button(window, text="Из реестра", command = winreestr_pull_inkotex)
btn_opros.place(x=390, y=35)

reestr = winreestr_pull()       # присваиваем переменной кортеж значений (0-последняя посылка из реестра (кортеж), 1-последний выбраный COM-порт (кортеж))

lbl0 = Label(window, text = "Выберите COM-порт:").place(x=15, y=15)
combo = Combobox(window, values = serial_ports())
combo.place(x=15, y=35)
combo.bind('<<ComboboxSelected>>', com_port_state) #вызываем функцию отображения состояния порта
combo.set(reestr[0])   # устанавливае при запуске программы значение COM-порта из реестра

lbl01 = Label(window, text = "Выберите скорость:").place(x=200, y=15)
combo1 = Combobox(window, values = speeds)
combo1.place(x=200, y=35)
combo1.current(3)

lbl_current = LabelFrame(window, text = "Установите параметры тока")
lbl_current.place(x=15, y=70, width = 350, heigh = 60)

spinbox_current = Spinbox(lbl_current, values = current_values, width=5) #модуль для выбора количества посылок
spinbox_current.place(x=5,y=5)
spinbox_current.delete(00,"end")                            #удаление всех элементов из модуля, для установки значения по умолчанию
spinbox_current.insert(0,0)                                #установка значения по умолчанию 1
lbl_current_A = Label(lbl_current, text="Ток, А")
lbl_current_A.place(x=90, y=5)

spinbox_angle = Spinbox(lbl_current, from_=0, to=360, width=5) #модуль для выбора количества посылок
spinbox_angle.place(x=170,y=5)
spinbox_angle.delete(0,"end")                            #удаление всех элементов из модуля, для установки значения по умолчанию
spinbox_angle.insert(0,0)                                #установка значения по умолчанию 1
lbl_angle = Label(lbl_current, text="Угол")
lbl_angle.place(x=260, y=5)


lbl_phase = LabelFrame(window, text = "Выберите задействованные фазы")
lbl_phase.place(x=15, y=135, width = 350, heigh = 60)

sel_phase = IntVar()
sel_phase.set(103)
rad_A = Radiobutton(lbl_phase, text='A', value=113, variable=sel_phase)
rad_A.place(x=5,y=5)
rad_B = Radiobutton(lbl_phase, text='B', value=123, variable=sel_phase)
rad_B.place(x=45,y=5)
rad_C = Radiobutton(lbl_phase, text='C', value=133, variable=sel_phase)
rad_C.place(x=85,y=5)
rad_ABC = Radiobutton(lbl_phase, text='ABC', value=103, variable=sel_phase)
rad_ABC.place(x=125,y=5)


lbl_voltage = LabelFrame(window, text = "Установите параметры напряжения")
lbl_voltage.place(x=15, y=200, width = 350, heigh = 60)

sel_voltage = IntVar()
sel_voltage.set(2)
rad_voltage_57V = Radiobutton(lbl_voltage, text='57В', value=1, variable=sel_voltage)
rad_voltage_57V.place(x=5,y=5)
rad_voltage_220V = Radiobutton(lbl_voltage, text='220В', value=2, variable=sel_voltage)
rad_voltage_220V.place(x=65,y=5)
rad_voltage_270V = Radiobutton(lbl_voltage, text='270В', value=3, variable=sel_voltage)
rad_voltage_270V.place(x=125,y=5)

btn_send = Button(window, text="Запустить", command = lambda: serial_tx(Parcel_func()))
btn_send.place(x=15, y=290)
btn_stop = Button(window, text="Остановить", command = lambda: serial_tx(bytes.fromhex(stop_parcel)))
btn_stop.place(x=250, y=290)

lbl_version = LabelFrame(window, text = "Версия ПО установки")
lbl_version.place(x = 420, y=250, width = 155, heigh = 180)
lbl_develop = Label(lbl_version, text = "В разработке")
lbl_develop.place(x=5, y=5)

btn_opros = Button(lbl_version, text="Опросить ", command = lambda: serial_tx(bytes.fromhex(version_reply)))
btn_opros.pack(side = BOTTOM)

lbl_rx_data_dc = LabelFrame(window, text = "Принятые данные (в разработке)")
lbl_rx_data_dc.place(x=15, y=320, width = 350, heigh = 140)


window.mainloop()


