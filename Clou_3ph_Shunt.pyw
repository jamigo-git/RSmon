# -*- coding: utf-8 -*-
import serial
import time
import _winreg
import Tkinter
import ttk
import struct
from Tkinter import *
from ttk import *

speeds = ['1200','2400', '4800', '38400', '19200', '38400', '57600', '115200']
version_reply = '81161720434C333131563220342E3233'
stop_parcel_old = '8101070EA3054480070B3F3F0167'
stop_parcel_old_0 = '81010746A305063F804F1200009F240000000000804F1200009F240000000000FF00000000FC00000000FC00000000FC00000000FA00000000FA00000000FA0000000000FFD9'
stop_parcel = stop_parcel_old.decode("hex")
stop_parcel_0 = stop_parcel_old_0.decode("hex")
start_st_parcel = '010748A305463F804F1200009F240000000000'
end_st_parcel = '20A1070007033F3F'
current_values = ('0', '0.1', '0.25', '0.5', '1', '2.5', '5', '10', '25', '60', '100')
current_0A =   ('00000000FC')
current_01A =  ('E8030000FC')
current_025A = ('C3090000FC')
current_05A =  ('87130000FC')
current_1A =   ('0F270000FC')
current_2_5A = ('A7610000FC')
current_5A =   ('4FC30000FC')
current_10A =  ('9F860100FC')
current_25A =  ('8FD00300FC')
current_60A =  ('BF270900FC')
current_100A = ('3F420F00FC')
current_dict = {'0':current_0A, '0.1':current_01A,
                '0.25':current_025A, '0.5':current_05A, '1':current_1A, '2.5':current_2_5A,
                '5':current_5A, '10':current_10A, '25':current_25A, '60':current_60A, '100':current_100A}

voltage_0V = ('00000000FC')
voltage_57V =('E8CD0800FC')
voltage_230V =('5F182300FC')
voltage_270V =('54F02900FC')
voltage_dict = {1:voltage_57V, 2:voltage_230V, 3:voltage_270V}

#write data in window_installations registry
def winreestr_push(comport):
    software_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software')
    _winreg.CreateKey(software_key, 'CL3000')
    rsmon_key = _winreg.OpenKey(software_key, 'CL3000', 0, _winreg.KEY_ALL_ACCESS)
    _winreg.SetValueEx(rsmon_key, "last_com" , None, _winreg.REG_SZ, comport)
    _winreg.CloseKey(rsmon_key)

#read data data from window_installations registry
def winreestr_pull():
    try:
        rsmon_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software\\CL3000')
        comport = _winreg.QueryValueEx(rsmon_key, "last_com")
        print comport
    except Exception:
        print 'Com-port from window_installations registry unavailable, will use COM1 as default!!!'
        comport = ("COM1", 1)
    return (comport)

#read data from window_installations registry Inkotex 3ph
def winreestr_pull_inkotex():
    try:
        rsmon_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software\\Incotex\\3Ph_pm\\Clou_Shunt')
        comport = _winreg.QueryValueEx(rsmon_key, "Clou_COM")
        rsmon_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software\\Incotex\\3Ph_pm')
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
    
def places_func():
        
    first_12 = str(hex(cvar1.get()|cvar2.get()|cvar3.get()|cvar4.get()|cvar5.get()|cvar6.get()|cvar7.get()|cvar8.get()|cvar9.get()|cvar10.get()|cvar11.get()|cvar12.get()))[2:]
    print first_12.zfill(3)
    second_12 = str(hex(cvar13.get()|cvar14.get()|cvar15.get()|cvar16.get()|cvar17.get()|cvar18.get()|cvar19.get()|cvar20.get()|cvar21.get()|cvar22.get()|cvar23.get()|cvar24.get()))[2:]
    print second_12.zfill(3)
    parcel = '400115C2FF0C000000000000000000'+ second_12.zfill(3) + first_12.zfill(3) + '01'
    parcel = '81' + parcel + parcel_crc_function(parcel)
    print parcel
    return parcel.decode("hex")


#Функция вычисляет контрольную сумму посылки и добавляет ее к исходным данным
def parcel_crc_function(parcel):                   
    xor8 = bytearray(parcel.decode("hex"))
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

#Funcion collect parcel for RS232
def Parcel_func():
    voltage = voltage_dict[sel_voltage.get()]
    current = current_dict[spinbox_current.get()]
    if sel_phase.get() == 1:
        current_A = current
        current_B = current_0A
        current_C = current_0A
    elif sel_phase.get() == 2:
        current_A = current_0A
        current_B = current
        current_C = current_0A
    elif sel_phase.get() == 3:
        current_A = current_0A
        current_B = current_0A
        current_C = current
    else:
        current_A = current
        current_B = current
        current_C = current

    angle_A = str(hex(int(spinbox_angle.get())*10000))[3:]
    angle_A = angle_A.zfill(6)
    angle_A = angle_A[4:]+angle_A[2:4]+angle_A[:2]+'00'
    if spinbox_angle < 120:
        angle_B = str(hex((int(spinbox_angle.get())+240)*10000))[3:]
        angle_B = angle_B.zfill(6)
        angle_B = angle_B[4:]+angle_B[2:4]+angle_B[:2]+'00'
    else:
        angle_B = str(hex((int(spinbox_angle.get())-120)*10000))[3:]
        angle_B = angle_B.zfill(6)
        angle_B = angle_B[4:]+angle_B[2:4]+angle_B[:2]+'00'
    if spinbox_angle < 240:
        angle_C = str(hex((int(spinbox_angle.get())+120)*10000))[3:]
        angle_C = angle_C.zfill(6)
        angle_C = angle_C[4:]+angle_C[2:4]+angle_C[:2]+'00'
    else:
        angle_C = str(hex((int(spinbox_angle.get())-240)*10000))[3:]
        angle_C = angle_C.zfill(6)
        angle_C = angle_C[4:]+angle_C[2:4]+angle_C[:2]+'00'
    parcel = start_st_parcel + angle_C.upper() + angle_B.upper() + angle_A.upper() + "FF" + voltage*3 + current_C + current_B + current_A + end_st_parcel
    parcel_crc = parcel_crc_function(parcel)
    parcel_full = ('81' + parcel + parcel_crc)
    print parcel_full
    return parcel_full.decode("hex")

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
        lbl_error_com = Label(lbl_rx_data_dc, text = "                                                    \n                \n                \n                  \n                \n                 ", foreground = 'red')
        lbl_error_com.place(x=5, y=5)
        ser = serial.Serial(combo.get(), combo1.get(), timeout = 0.1)
        winreestr_push(combo.get())
        if parcel == stop_parcel:
            ser.write(stop_parcel_0)
            time.sleep(0.5)
        ser.write(parcel)
        
     
    except Exception:
        lbl_error_com = Label(lbl_rx_data_dc, text = "Can't open COM-port\nplease try again\n                \n                \n                  \n                \n                 ", foreground = 'red')
        lbl_error_com.place(x=5, y=5)


   
def serial_tx_ver(parcel):
    try:
        ser = serial.Serial(combo.get(), 38400, timeout = 1)
        if parcel == 1:
            ser.setDTR(False)
            ser.setRTS(True)
            parcel_send = '81300706C9F8'
            parcel_full = parcel_send.decode("hex")
            ser.write(parcel_full)
            serial_rx_ver(ser)                   
            ser.close()
                
        elif parcel == 2:
            ser.setDTR(True)
            ser.setRTS(False) 
            parcel_send = '8122011684FF0CFFFFFFFFFFFFFFFFFFFFFFFF1400568122011684FF0CFFFFFFFFFFFFFFFFFFFFFFFF1400568122011684FF0CFFFFFFFFFFFFFFFFFFFFFFFF14005681300706C9F8'
            parcel_full = parcel_send.decode("hex")
            ser.write(parcel_full)
            serial_rx_ver(ser)
            ser.close()
    except Exception:
        lbl_error_com = Label(lbl_version, text = "Can't open com-port\ntry again\n                \n                              \n                                      ", foreground = 'red')
        lbl_error_com.place(x=5, y=5)

def serial_rx_ver(ser):
    try:
        display_data_rx1 = ser.read(23)
        display_data_rx = display_data_rx1[4:13]
        if display_data_rx == b'':
            lbl_parcel_rx = Label(lbl_version, text = "                                 \n                            \n                               ")
            lbl_parcel_rx.place(x=5, y=5)
            lbl_parcel_rx = Label(lbl_version, text = 'No data!!!\n try to reboot managment block', foreground = 'red') 
            lbl_parcel_rx.place(x=5, y=5)
        else:
            lbl_parcel_rx = Label(lbl_version, text = "                                 \n                  \n                    ")
            lbl_parcel_rx.place(x=5, y=5)
            lbl_parcel_rx = Label(lbl_version, text = display_data_rx) 
            lbl_parcel_rx.place(x=5, y=5)
            lbl_parcel_rx = Label(lbl_version, text = "                                 ")
            lbl_parcel_rx.place(x=5, y=20)
            lbl_parcel_rx = Label(lbl_version, text = 'Firmware version                  \n                            ') 
            lbl_parcel_rx.place(x=5, y=20)
    except Exception:
        lbl_error_com = Label(lbl_version, text = "No data!!\ntry connection\ncom-port settings\n                ", foreground = 'red')
        lbl_error_com.place(x=5, y=5)
    ser.close()

window_installation = Tk()  
window_installation.title("Program for diagnostic CLOU SHUNT 3F XP (by Jamigo)")  
window_installation.geometry('600x600')

btn_opros = Button(window_installation, text="Из реестра", command = winreestr_pull_inkotex)
btn_opros.place(x=390, y=35)

reestr = winreestr_pull()       # присваиваем переменной кортеж значений (0-последняя посылка из реестра (кортеж), 1-последний выбраный COM-порт (кортеж))
lbl0 = Label(window_installation, text = "Выберите COM-порт:").place(x=15, y=15)
combo = Combobox(window_installation, values = serial_ports())
combo.place(x=15, y=35)
combo.bind('<<ComboboxSelected>>', com_port_state) #вызываем функцию отображения состояния порта
combo.set(reestr[0])   

lbl01 = Label(window_installation, text = "Выберите скорость:").place(x=200, y=15)
combo1 = Combobox(window_installation, values = speeds)
combo1.place(x=200, y=35)
combo1.current(3)

lbl_current = LabelFrame(window_installation, text = "Установите параметры тока")
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


lbl_phase = LabelFrame(window_installation, text = "Выберите задействованные фазы")
lbl_phase.place(x=15, y=135, width = 350, heigh = 60)

sel_phase = IntVar()
sel_phase.set(4)
rad_A = Radiobutton(lbl_phase, text='A', value=1, variable=sel_phase)
rad_A.place(x=5,y=5)
rad_B = Radiobutton(lbl_phase, text='B', value=2, variable=sel_phase)
rad_B.place(x=45,y=5)
rad_C = Radiobutton(lbl_phase, text='C', value=3, variable=sel_phase)
rad_C.place(x=85,y=5)
rad_ABC = Radiobutton(lbl_phase, text='ABC', value=4, variable=sel_phase)
rad_ABC.place(x=125,y=5)

lbl_voltage = LabelFrame(window_installation, text = "Установите параметры напряжения")
lbl_voltage.place(x=15, y=200, width = 350, heigh = 60)

sel_voltage = IntVar()
sel_voltage.set(2)
rad_voltage_57V = Radiobutton(lbl_voltage, text='57В', value=1, variable=sel_voltage)
rad_voltage_57V.place(x=5,y=5)
rad_voltage_220V = Radiobutton(lbl_voltage, text='230В', value=2, variable=sel_voltage)
rad_voltage_220V.place(x=65,y=5)
rad_voltage_270V = Radiobutton(lbl_voltage, text='270В', value=3, variable=sel_voltage)
rad_voltage_270V.place(x=125,y=5)

btn_send = Button(window_installation, text="Запустить", command = lambda: serial_tx(Parcel_func()))
btn_send.place(x=15, y=290)
btn_stop = Button(window_installation, text="Остановить", command = lambda: serial_tx((stop_parcel)))
btn_stop.place(x=250, y=290)

lbl_version = LabelFrame(window_installation, text = "Версия ПО установки")
lbl_version.place(x = 420, y=210, width = 155, heigh = 150)

btn_opros = Button(lbl_version, text="Опросить счетчик", command = lambda: serial_tx_ver(1))
btn_opros.pack(side = BOTTOM)

lbl_places = LabelFrame(window_installation, text = "Выберите места")
lbl_places.place(x=15, y=370, width = 500, heigh = 120)

cvar1 = IntVar()
cvar1.set(0)
c1 = Checkbutton(lbl_places, text="1", variable=cvar1, onvalue=1, offvalue=0)
c1.place(x=5,y=5)
cvar2 = IntVar()
cvar2.set(0)
c2 = Checkbutton(lbl_places, text="2", variable=cvar2, onvalue=2, offvalue=0)
c2.place(x=45,y=5)
cvar3 = IntVar()
cvar3.set(0)
c3 = Checkbutton(lbl_places, text="3", variable=cvar3, onvalue=4, offvalue=0)
c3.place(x=85,y=5)
cvar4 = IntVar()
cvar4.set(0)
c4 = Checkbutton(lbl_places, text="4", variable=cvar4, onvalue=8, offvalue=0)
c4.place(x=125,y=5)
cvar5 = IntVar()
cvar5.set(0)
c5 = Checkbutton(lbl_places, text="5", variable=cvar5, onvalue=16, offvalue=0)
c5.place(x=165,y=5)
cvar6 = IntVar()
cvar6.set(0)
c6 = Checkbutton(lbl_places, text="6", variable=cvar6, onvalue=32, offvalue=0)
c6.place(x=205,y=5)
cvar7 = IntVar()
cvar7.set(0)
c7 = Checkbutton(lbl_places, text="7", variable=cvar7, onvalue=64, offvalue=0)
c7.place(x=5,y=35)
cvar8 = IntVar()
cvar8.set(0)
c8 = Checkbutton(lbl_places, text="8", variable=cvar8, onvalue=128, offvalue=0)
c8.place(x=45,y=35)
cvar9 = IntVar()
cvar9.set(0)
c9 = Checkbutton(lbl_places, text="9", variable=cvar9, onvalue=256, offvalue=0)
c9.place(x=85,y=35)
cvar10 = IntVar()
cvar10.set(0)
c10 = Checkbutton(lbl_places, text="10", variable=cvar10, onvalue=512, offvalue=0)
c10.place(x=125,y=35)
cvar11 = IntVar()
cvar11.set(0)
c11 = Checkbutton(lbl_places, text="11", variable=cvar11, onvalue=1024, offvalue=0)
c11.place(x=165,y=35)
cvar12 = IntVar()
cvar12.set(0)
c12 = Checkbutton(lbl_places, text="12", variable=cvar12, onvalue=2048, offvalue=0)
c12.place(x=205,y=35)

cvar13 = IntVar()
cvar13.set(0)
c13 = Checkbutton(lbl_places, text="13", variable=cvar13, onvalue=1, offvalue=0)
c13.place(x=255,y=5)
cvar14 = IntVar()
cvar14.set(0)
c14 = Checkbutton(lbl_places, text="14", variable=cvar14, onvalue=2, offvalue=0)
c14.place(x=295,y=5)
cvar15 = IntVar()
cvar15.set(0)
c15 = Checkbutton(lbl_places, text="15", variable=cvar15, onvalue=4, offvalue=0)
c15.place(x=335,y=5)
cvar16 = IntVar()
cvar16.set(0)
c16 = Checkbutton(lbl_places, text="16", variable=cvar16, onvalue=8, offvalue=0)
c16.place(x=375,y=5)
cvar17 = IntVar()
cvar17.set(0)
c17 = Checkbutton(lbl_places, text="17", variable=cvar17, onvalue=16, offvalue=0)
c17.place(x=415,y=5)
cvar18 = IntVar()
cvar18.set(0)
c18 = Checkbutton(lbl_places, text="18", variable=cvar18, onvalue=32, offvalue=0)
c18.place(x=455,y=5)
cvar19 = IntVar()
cvar19.set(0)
c19 = Checkbutton(lbl_places, text="19", variable=cvar19, onvalue=64, offvalue=0)
c19.place(x=255,y=35)
cvar20 = IntVar()
cvar20.set(0)
c20 = Checkbutton(lbl_places, text="20", variable=cvar20, onvalue=128, offvalue=0)
c20.place(x=295,y=35)
cvar21 = IntVar()
cvar21.set(0)
c21 = Checkbutton(lbl_places, text="21", variable=cvar21, onvalue=256, offvalue=0)
c21.place(x=335,y=35)
cvar22 = IntVar()
cvar22.set(0)
c22 = Checkbutton(lbl_places, text="22", variable=cvar22, onvalue=512, offvalue=0)
c22.place(x=375,y=35)
cvar23 = IntVar()
cvar23.set(0)
c23 = Checkbutton(lbl_places, text="23", variable=cvar23, onvalue=1024, offvalue=0)
c23.place(x=415,y=35)
cvar24 = IntVar()
cvar24.set(0)
c24 = Checkbutton(lbl_places, text="24", variable=cvar24, onvalue=2048, offvalue=0)
c24.place(x=455,y=35)

btn_send = Button(lbl_places, text="Включить", command = lambda: serial_tx(places_func()))
btn_send.place(x=15, y=65)

lbl_rx_data_dc = LabelFrame(window_installation, text = "Доп. информация")
lbl_rx_data_dc.place(x = 10, y=500, width = 250, heigh = 90)

window_installation.mainloop()
