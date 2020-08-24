#C:\Users\v.rojkov.NPF-MOSSAR\AppData\Local\Programs\Python\Python38-32\Scripts\;C:\Users\v.rojkov.NPF-MOSSAR\AppData\Local\Programs\Python\Python38-32\;
# -*- coding: utf-8 -*-
import serial
import time
import _winreg
import Tkinter
import ttk
import struct
from Tkinter import *
from ttk import *


speeds = ['1200','2400', '4800', '9600', '19200', '38400', '57600', '115200']

version_reply = '81161720434C333131563220342E3233'
stop_parcel_old = '8110200749FF818110200846FF00818110200847FF00808110200849FF8E8110200863FF00A4812000263500103FFFFFFFFFFFFF00405000000000000000000000000000320000006400005A'
stop_parcel = stop_parcel_old.decode("hex")

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


#write data in windows registry
def winreestr_push(comport):
    software_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software')
    _winreg.CreateKey(software_key, 'CL3000')
    rsmon_key = _winreg.OpenKey(software_key, 'CL3000', 0, _winreg.KEY_ALL_ACCESS)
    _winreg.SetValueEx(rsmon_key, "last_com" , None, _winreg.REG_SZ, comport)
    _winreg.CloseKey(rsmon_key)

#read data data from windows registry
def winreestr_pull():
    try:
        rsmon_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software\\CL3000')
        comport = _winreg.QueryValueEx(rsmon_key, "last_com")
    except Exception:
        print ('Com-port from windows registry unavailable, will use COM1 as default!!!')
        comport = ("COM1", 1)
    
    return (comport)

#read data from windows registry Inkotex 3ph
def winreestr_pull_inkotex():
    #try:
    rsmon_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software\\Incotex\\3Ph_pm\\Clou_v4.23')
    comport = _winreg.QueryValueEx(rsmon_key, "Clou_COM")
    rsmon_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software\\Incotex\\3Ph_pm')
    comport_commutation = _winreg.QueryValueEx(rsmon_key, "ConnDev_COM")
    comport_PM = _winreg.QueryValueEx(rsmon_key, "PM_COM")
    comport_IRda = _winreg.QueryValueEx(rsmon_key, "IrDA_COM")
    #except Exception:
     #   comport = ("COM1", 1)
    combo.set(comport[0])
    lbl_com_clou = Label(window, text = ("Установка: " +  str(comport[0]))).place(x=380, y=100)
    lbl_com_commutation = Label(window, text = ("Плата коммутации: " +  str(comport_commutation[0]))).place(x=380, y=120)
    lbl_com_IRda = Label(window, text = ("IRda: " +  str(comport_IRda[0]))).place(x=380, y=140)
    lbl_com_PM = Label(window, text = ("Интерфейс счетчиков: " +  str(comport_PM[0]))).place(x=380, y=160)
    

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
    phase = str(sel_phase.get())
    voltage = voltage_dict[sel_voltage.get()]
    current = current_dict[spinbox_current.get()]
    angle = hex(int(spinbox_angle.get()))[2:]
    angle = angle.zfill(3)
    parcel = start_st_parcel + phase + first_st_parcel + voltage[0] + current[0]+ voltage[1] + current [1]+ second_st_parcel + angle.upper() + end_st_parcel
    parcel_crc = parcel_crc_function(parcel)
    parcel_full = (parcel + parcel_crc)
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
    """if ser.cd == True:
        com_port_state = Canvas(window, width=10, height=10, bg = 'green')
        com_port_state.place(x=400, y=40)
    else:
        com_port_state = Canvas(window, width=10, height=10, bg = 'red')
        com_port_state.place(x=400, y=40)"""

#Function send parcel in RS232
def serial_tx(parcel):
    try:
        lbl_error_com = Label(lbl_rx_data_dc, text = "                                                    \n                \n                \n                  \n                \n                 ", foreground = 'red')
        lbl_error_com.place(x=5, y=5)
        ser = serial.Serial(combo.get(), combo1.get(), timeout = 0.1)
        winreestr_push(combo.get())
        ser.setDTR(True)
        ser.setRTS(False)
        ser.write(parcel)
      
    except Exception:
        lbl_error_com = Label(lbl_rx_data_dc, text = "Can't open COM-port\nplease try again\n                \n                \n                  \n                \n                 ", foreground = 'red')
        lbl_error_com.place(x=5, y=5)


def serial_rx_UIPQ(parcel_tx):
    ser = serial.Serial(combo.get(), 9600, timeout = 1)
    ser.write(parcel_tx.decode("hex"))
    display_data_UIPQ = ser.read(77)      #read 75 bites from com-port
    parcel_hex = bytearray(display_data_UIPQ)
    
    F_all =  [parcel_hex[6], parcel_hex[7]]
    F_all = struct.unpack('H', bytearray(F_all))
    Ua = [parcel_hex[23], parcel_hex[24], parcel_hex[25],'\x00']
    Ua = str(struct.unpack('I', bytearray(Ua))).strip('(,)')
    Ia = [parcel_hex[26], parcel_hex[27], parcel_hex[28],'\x00']
    Ia = str(struct.unpack('I', bytearray(Ia))).strip('(,)')
    Ub = [parcel_hex[29], parcel_hex[30], parcel_hex[31],'\x00']
    Ub = str(struct.unpack('I', bytearray(Ub))).strip('(,)')
    Ib = [parcel_hex[32], parcel_hex[33], parcel_hex[34],'\x00']
    Ib = str(struct.unpack('I', bytearray(Ib))).strip('(,)')
    Uc = [parcel_hex[35], parcel_hex[36], parcel_hex[37],'\x00']
    Uc = str(struct.unpack('I', bytearray(Uc))).strip('(,)')
    Ic = [parcel_hex[38], parcel_hex[39], parcel_hex[40],'\x00']
    Ic = str(struct.unpack('I', bytearray(Ic))).strip('(,)')
    Fi_Ua = [parcel_hex[41], parcel_hex[42], parcel_hex[43],'\x00']
    Fi_Ua = str(struct.unpack('I', bytearray(Fi_Ua))).strip('(,)')
    Fi_Ia = [parcel_hex[44], parcel_hex[45], parcel_hex[46],'\x00']
    Fi_Ia = str(struct.unpack('I', bytearray(Fi_Ia))).strip('(,)')
    Fi_Ub = [parcel_hex[47], parcel_hex[48], parcel_hex[49],'\x00']
    Fi_Ub = str(struct.unpack('I', bytearray(Fi_Ub))).strip('(,)')
    Fi_Ib = [parcel_hex[50], parcel_hex[51], parcel_hex[52],'\x00']
    Fi_Ib = str(struct.unpack('I', bytearray(Fi_Ib))).strip('(,)')
    Fi_Uc = [parcel_hex[53], parcel_hex[54], parcel_hex[55],'\x00']
    Fi_Uc = str(struct.unpack('I', bytearray(Fi_Uc))).strip('(,)')
    Fi_Ic = [parcel_hex[56], parcel_hex[57], parcel_hex[58],'\x00']
    Fi_Ic = str(struct.unpack('I', bytearray(Fi_Ic))).strip('(,)')
    Pa = [parcel_hex[59], parcel_hex[60], parcel_hex[61],'\x00']
    Pa = str(struct.unpack('I', bytearray(Pa))).strip('(,)')
    Pb = [parcel_hex[62], parcel_hex[63], parcel_hex[64],'\x00']
    Pb = str(struct.unpack('I', bytearray(Pb))).strip('(,)')
    Pc = [parcel_hex[65], parcel_hex[66], parcel_hex[67],'\x00']
    Pc = str(struct.unpack('I', bytearray(Pc))).strip('(,)')
    Ra = [parcel_hex[68], parcel_hex[69], parcel_hex[70],'\x00']
    Ra = str(struct.unpack('I', bytearray(Ra))).strip('(,)')
    Rb = [parcel_hex[71], parcel_hex[72], parcel_hex[73],'\x00']
    Rb = str(struct.unpack('I', bytearray(Rb))).strip('(,)')
    Rc = [parcel_hex[74], parcel_hex[75], parcel_hex[76],'\x00']
    Rc = str(struct.unpack('I', bytearray(Rc))).strip('(,)')
    lbl_clear = Label(lbl_rx_data_dc, text = ('                                                     \n                                                            \n                                                         \n                                                        \n                                                                 \n                                                           \n                                                                   \n                                                                          ')).place(x=5, y=5) 
    lbl_Ua = Label(lbl_rx_data_dc, text = ('Ua = ' + str(int(Ua)/10**int(parcel_hex[14])) + ' В')).place(x=5, y=5)
    lbl_Ub = Label(lbl_rx_data_dc, text = ('Ub = ' + str(int(Ub)/10**int(parcel_hex[15])) + ' В')).place(x=5, y=45)
    lbl_Uc = Label(lbl_rx_data_dc, text = ('Uc = ' + str(int(Uc)/10**int(parcel_hex[16])) + ' В')).place(x=5, y=85)
    lbl_Ia = Label(lbl_rx_data_dc, text = ('Ia = ' + str(float(Ia)/10**int(parcel_hex[17])) + ' А')).place(x=5, y=25)
    lbl_Ib = Label(lbl_rx_data_dc, text = ('Ib = ' + str(float(Ia)/10**int(parcel_hex[18])) + ' А')).place(x=5, y=65)
    lbl_Ic = Label(lbl_rx_data_dc, text = ('Ic = ' + str(float(Ia)/10**int(parcel_hex[19])) + ' А')).place(x=5, y=105)
    lbl_Fi_Ua = Label(lbl_rx_data_dc, text = ('Q_Ua = ' + str(int(Fi_Ua)/1000) + ' \x60')).place(x=105, y=5)
    lbl_Fi_Ub = Label(lbl_rx_data_dc, text = ('Q_Ub = ' + str(int(Fi_Ub)/1000) + ' \x60')).place(x=105, y=45)
    lbl_Fi_Uc = Label(lbl_rx_data_dc, text = ('Q_Uc = ' + str(int(Fi_Uc)/1000) + ' \x60')).place(x=105, y=85)
    lbl_Fi_Ia = Label(lbl_rx_data_dc, text = ('Q_Ia = ' + str(int(Fi_Ia)/1000) + ' \x60')).place(x=105, y=25)
    lbl_Fi_Ib = Label(lbl_rx_data_dc, text = ('Q_Ib = ' + str(int(Fi_Ib)/1000) + ' \x60')).place(x=105, y=65)
    lbl_Fi_Ic = Label(lbl_rx_data_dc, text = ('Q_Ic = ' + str(int(Fi_Ic)/1000) + ' \x60')).place(x=105, y=105)
    lbl_Pa = Label(lbl_rx_data_dc, text = ('Pa = ' + str(int(Pa)/10**int(parcel_hex[20])) + ' Вт')).place(x=205, y=5)
    lbl_Pb = Label(lbl_rx_data_dc, text = ('Pb = ' + str(int(Pb)/10**int(parcel_hex[21])) + ' Вт')).place(x=205, y=45)
    lbl_Pc = Label(lbl_rx_data_dc, text = ('Pc = ' + str(int(Pc)/10**int(parcel_hex[22])) + ' Вт')).place(x=205, y=85)
    lbl_Ra = Label(lbl_rx_data_dc, text = ('Ra = ' + str(int(Ra)/10**int(parcel_hex[20])) + ' Вт')).place(x=205, y=25)
    lbl_Rb = Label(lbl_rx_data_dc, text = ('Rb = ' + str(int(Rb)/10**int(parcel_hex[21])) + ' Вт')).place(x=205, y=65)
    lbl_Rc = Label(lbl_rx_data_dc, text = ('Rc = ' + str(int(Rc)/10**int(parcel_hex[22])) + ' Вт')).place(x=205, y=105)
    ser.close()
   

def serial_tx_ver(parcel):
    
    ser = serial.Serial(combo.get(), 9600, timeout = 1)
    if parcel == 1:
        ser.setDTR(False)
        ser.setRTS(True)
        parcel_send = '8116052033'
        parcel_full = parcel_send.decode("hex")
        ser.write(parcel_full)
        serial_rx_ver(ser)                   
        ser.close()
            
    elif parcel == 2:
        ser.setDTR(True)
        ser.setRTS(False) 
        parcel_send = '812000065670'
        parcel_full = parcel_send.decode("hex")
        ser.write(parcel_full)
        serial_rx_ver(ser)
        ser.close()

    
    #except Exception:
      #  lbl_error_com = Label(lbl_version, text = "Can't open com-port\ntry again\n                \n                              \n                                      ", foreground = 'red')
      #  lbl_error_com.place(x=5, y=5)

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

#Main program
    
window = Tk()  
window.title("Program for diagnostic CLOU 3F --special for Windows XP (by Jamigo)")  
window.geometry('600x600')

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
btn_stop = Button(window, text="Остановить", command = lambda: serial_tx((stop_parcel)))
btn_stop.place(x=250, y=290)

lbl_version = LabelFrame(window, text = "Версия ПО установки")
lbl_version.place(x = 420, y=310, width = 155, heigh = 150)

btn_opros = Button(lbl_version, text="Опросить счетчик", command = lambda: serial_tx_ver(1))
btn_opros.pack(side = BOTTOM)

btn_opros = Button(lbl_version, text="Опросить блок уп", command = lambda: serial_tx_ver(2))
btn_opros.pack(side = BOTTOM)

lbl_rx_data_dc = LabelFrame(window, text = "Принятые данные")
lbl_rx_data_dc.place(x=15, y=320, width = 350, heigh = 240)

btn_reload_data = Button(lbl_rx_data_dc, text="Запросить", command = lambda: serial_rx_UIPQ('811605322100'))
btn_reload_data.place(x=250, y=180)

window.mainloop()
