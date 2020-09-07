# -*- coding: utf-8 -*-
import serial
import time
import _winreg
import Tkinter
import ttk
import struct
from Tkinter import *
from ttk import *
import CRC16_MODBUS
from CRC16_MODBUS import *

speeds = ['1200','2400', '4800', '9600', '19200', '38400', '57600', '115200']
version_reply = ''
parcel1 = '00000000'
stop_parcel_old = 'FEFEFEFEFE01FF1302303030303030303030303030307217FEFEFEFEFE01A900070717FEFEFEFEFE01A900070717F9F9F9F9F9B110000200102013880000000000000000000000000000000000000000000000002EE05DC000007CB2'
stop_parcel = stop_parcel_old.decode("hex")
header = 'F9F9F9F9F9'
start_st_parcel = 'B11000020010201388'
first_st_parcel = '0000000000'
second_st_parcel= '0000000000000000'
end_st_parcel = '000000002EE05DC00000'
current_values = ('0', '0.25', '0.5', '1', '2.5', '5', '10', '25', '60')
current_0A =   ('9', '000000')
current_025A = ('8', '0009C4')
current_05A =  ('7', '001388')
current_1A =   ('6', '002710')
current_2_5A = ('5', '0061A8')
current_5A =   ('4', '00C350')
current_10A =  ('3', '0186A0')
current_25A =  ('2', '03D090')
current_60A =  ('1', '0927C0')

current_dict = {'0':current_0A, '0.25':current_025A, '0.5':current_05A, '1':current_1A, '2.5':current_2_5A, '5':current_5A, '10':current_10A, '25':current_25A, '60':current_60A}

voltage_0V = ('0000')
voltage_57V =('1644')
voltage_230V =('59D8')
voltage_270V =('6978')
voltage_dict = {1:voltage_57V, 2:voltage_230V, 3:voltage_270V}


#write data in window_installations registry
def winreestr_push(comport):
    software_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software')
    _winreg.CreateKey(software_key, 'SY1ph')
    rsmon_key = _winreg.OpenKey(software_key, 'SY1ph', 0, _winreg.KEY_ALL_ACCESS)
    _winreg.SetValueEx(rsmon_key, "last_com" , None, _winreg.REG_SZ, comport)
    _winreg.CloseKey(rsmon_key)

#read data data from window_installations registry
def winreestr_pull():
    try:
        rsmon_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software\\SY1ph')
        comport = _winreg.QueryValueEx(rsmon_key, "last_com")
    except Exception:
        print ('Com-port from window_installations registry unavailable, will use COM1 as default!!!')
        comport = ("COM1", 1)
    
    return (comport)

#read data from window_installations registry Inkotex 3ph
def winreestr_pull_inkotex():
    try:
        rsmon_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software\\Incotex\\1Ph_pm\\Songyang')
        comport = _winreg.QueryValueEx(rsmon_key, "Songyang_Com")
        rsmon_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software\\Incotex\\1Ph_pm')
        comport_commutation = _winreg.QueryValueEx(rsmon_key, "ConnDev_COM")
        comport_PM = _winreg.QueryValueEx(rsmon_key, "PM_COM")
        comport_IRda = _winreg.QueryValueEx(rsmon_key, "IrDA_COM")
        lbl_com_clou = Label(window_installation, text = ("Установка: " +  str(comport[0]))).place(x=380, y=100)
        lbl_com_commutation = Label(window_installation, text = ("Плата коммутации: " +  str(comport_commutation[0]))).place(x=380, y=120)
        lbl_com_IRda = Label(window_installation, text = ("IRda: " +  str(comport_IRda[0]))).place(x=380, y=140)
        lbl_com_PM = Label(window_installation, text = ("Интерфейс счетчиков: " +  str(comport_PM[0]))).place(x=380, y=160)
    except Exception:
        comport = ("COM1", 1)
        combo.set(comport[0])
        lbl_com_clou = Label(window_installation, text = ("Не удалось получить данные!!!" )).place(x=380, y=100)
    
#Funcion collect parcel for RS232
def Parcel_func():
    voltage = voltage_dict[sel_voltage.get()]
    current = current_dict[spinbox_current.get()]
    angle = str(hex(int(spinbox_angle.get())*100))[2:]
    angle = angle.zfill(4)
    parcel = start_st_parcel + voltage + first_st_parcel + current[1] + second_st_parcel + angle.upper() + end_st_parcel
    parcel_crc = mainfunction(parcel)
    parcel_full = (header + parcel + parcel_crc.zfill(4))
    parcel1 = '4942303' + current[0] + '0D'
    print parcel_full
    print parcel1
    return (parcel_full.decode("hex"), parcel1.decode("hex"))

#Funcion find all com-ports in system and list result
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

#Function check choosen com-port state using CD
def com_port_state(ser):
    ser = serial.Serial(combo.get(), combo1.get())
    if ser.getCD() == True:
        com_port_state = Canvas(window_installation, width=10, height=10, bg = 'green')
        com_port_state.place(x=180, y=20)
    else:
        com_port_state = Canvas(window_installation, width=10, height=10, bg = 'red')
        com_port_state.place(x=180, y=20)

#Function send parcel in RS232
def serial_tx(parcel):
    try:
        parcel0 = '4D53300D'
        lbl_error_com = Label(lbl_rx_data_dc, text = "                                                    \n                \n                \n                  \n                \n                 ", foreground = 'red')
        lbl_error_com.place(x=5, y=5)
        ser = serial.Serial(combo.get(), combo1.get(), timeout = 0.1)
        winreestr_push(combo.get())
        ser.setDTR(True)
        ser.setRTS(False)
        ser.write(parcel0.decode("hex"))
        time.sleep(1)
        ser.write(parcel[1])
        time.sleep(1)
        ser.write(parcel[0])
        ser.close()
      
    except Exception:
        lbl_error_com = Label(lbl_rx_data_dc, text = "Can't open COM-port\nplease try again\n                \n                \n                  \n                \n                 ", foreground = 'red')
        lbl_error_com.place(x=5, y=5)

window_installation = Tk()  
window_installation.title("Program for diagnostic CLOU 1F (by Jamigo)")  
window_installation.geometry('600x600')

btn_opros = Button(window_installation, text="Из реестра", command = winreestr_pull_inkotex)
btn_opros.place(x=390, y=35)

reestr = winreestr_pull()       # присваиваем переменной кортеж значений (0-последняя посылка из реестра (кортеж), 1-последний выбраный COM-порт (кортеж))

lbl0 = Label(window_installation, text = "Выберите COM-порт:").place(x=15, y=15)
combo = Combobox(window_installation, values = serial_ports())
combo.place(x=15, y=35)
combo.bind('<<ComboboxSelected>>', com_port_state) #вызываем функцию отображения состояния порта
combo.set(reestr[0])   # устанавливае при запуске программы значение COM-порта из реестра

lbl01 = Label(window_installation, text = "Выберите скорость:").place(x=200, y=15)
combo1 = Combobox(window_installation, values = speeds)
combo1.place(x=200, y=35)
combo1.current(3)

lbl_current = LabelFrame(window_installation, text = "Установите параметры тока")
lbl_current.place(x=15, y=70, width = 350, heigh = 60)

spinbox_current = Spinbox(lbl_current, values = current_values, width=5) #модуль для выбора тока
spinbox_current.place(x=5,y=5)
spinbox_current.delete(00,"end")                            #удаление всех элементов из модуля, для установки значения по умолчанию
spinbox_current.insert(0,0)                                #установка значения по умолчанию 1
lbl_current_A = Label(lbl_current, text="Ток, А")
lbl_current_A.place(x=90, y=5)

spinbox_angle = Spinbox(lbl_current, from_=0, to=360, width=5) #модуль для выбора угла фи
spinbox_angle.place(x=170,y=5)
spinbox_angle.delete(0,"end")                            #удаление всех элементов из модуля, для установки значения по умолчанию
spinbox_angle.insert(0,0)                                #установка значения по умолчанию 1
lbl_angle = Label(lbl_current, text="Угол")
lbl_angle.place(x=260, y=5)

lbl_voltage = LabelFrame(window_installation, text = "Установите параметры напряжения")
lbl_voltage.place(x=15, y=200, width = 350, heigh = 60)

sel_voltage = IntVar()
sel_voltage.set(2)
rad_voltage_57V = Radiobutton(lbl_voltage, text='57В', value=1, variable=sel_voltage)
rad_voltage_57V.place(x=5,y=5)
rad_voltage_220V = Radiobutton(lbl_voltage, text='220В', value=2, variable=sel_voltage)
rad_voltage_220V.place(x=65,y=5)
rad_voltage_270V = Radiobutton(lbl_voltage, text='270В', value=3, variable=sel_voltage)
rad_voltage_270V.place(x=125,y=5)

btn_send = Button(window_installation, text="Запустить", command = lambda: serial_tx(Parcel_func()))
btn_send.place(x=15, y=290)
btn_stop = Button(window_installation, text="Остановить", command = lambda: serial_tx((stop_parcel, '000000'.decode("hex"))))
btn_stop.place(x=250, y=290)

lbl_version = LabelFrame(window_installation, text = "Версия ПО установки")
lbl_version.place(x = 420, y=310, width = 155, heigh = 150)

lbl_rx_data_dc = LabelFrame(window_installation, text = "Принятые со счетчика (CL311v2) данные")
lbl_rx_data_dc.place(x=15, y=320, width = 350, heigh = 240)

window_installation.mainloop()
