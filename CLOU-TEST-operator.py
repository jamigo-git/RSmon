import tkinter.ttk as ttk
from tkinter import *  
from tkinter.ttk import Combobox, Button, Radiobutton, Label, Entry, Spinbox
import serial
import time
import winreg

version_reply = '81161720434C333131563220342E3233'
speeds = ['1200','2400', '4800', '9600', '19200', '38400', '57600', '115200']

#Функция записи данных в реестр (последняя отправленная посылка, выбранный COM-порт)
def winreestr_push(comport):
    software_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software')
    winreg.CreateKey(software_key, 'dev3000')
    rsmon_key = winreg.OpenKey(software_key, 'dev3000', 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(rsmon_key, "last_com" , None, winreg.REG_SZ, comport)
    winreg.CloseKey(rsmon_key)

#Функция получения данных из реестра (последняя отправленная посылка, выбранный COM-порт)
def winreestr_pull():
    try:
        rsmon_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\dev3000')
        comport = winreg.QueryValueEx(rsmon_key, "last_com")
    except Exception:
        comport = ("COM1", 1)            # при получении из реестра значения ключа получаем похожий кортеж
    return (comport)

#Функция получения данных из реестра (если стоит программа)
def winreestr_pull_company():
    try:
        rsmon_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\company\\3Ph_pm\\device_v4.23')
        comport = winreg.QueryValueEx(rsmon_key, "device_COM")
    except Exception:
        comport = ("COM1", 1)            # при получении из реестра значения ключа получаем похожий кортеж
    combo.set(comport[0])

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

#Функция отправляет посылку устройству
def serial_tx(parcel):
    try:
        ser = serial.Serial(combo.get(), 9600, timeout = 1)
        
        if parcel == 1:
            ser.setDTR(False)
            ser.setRTS(True)
            parcel_send = '8116052033'
            parcel_full = bytes.fromhex(parcel_send)
            ser.write(parcel_full)
            serial_rx(ser)                   
            ser.close()
            
        elif parcel == 2:
            ser.setDTR(True)
            ser.setRTS(False) 
            parcel_send = '812000065670'
            parcel_full = bytes.fromhex(parcel_send)
            ser.write(parcel_full)
            serial_rx(ser)
            ser.close()
                        
        elif parcel == 3:
            parcel_send = '8110200749FF818110200846FF00818110200847FF00808110200849FF8E8110200863FF00A4812000263500103FFFFFFFFFFFFF00405000000000000000000000000000320000006400005A'
            parcel_full = bytes.fromhex(parcel_send)
            ser.write(parcel_full)
            
            
    except Exception:
        lbl_error_com = Label(lbl_rx_data_dc, text = "Не удалось открыть COM-порт\nПовторите попытку снова\n                \n                              \n                                      ", foreground = 'red')
        lbl_error_com.place(x=5, y=5)

def serial_rx(ser):
    try:
        display_data_rx1 = ser.read(23)
        
        display_data_rx = display_data_rx1[4:13]
        if display_data_rx == b'':
            lbl_parcel_rx = Label(lbl_rx_data_dc, text = "                                 \n                            \n                               ")
            lbl_parcel_rx.place(x=5, y=5)
            lbl_parcel_rx = Label(lbl_rx_data_dc, text = 'Нет данных!!!\n попробуйте перезагрузить блок управления', foreground = 'red') 
            lbl_parcel_rx.place(x=5, y=5)
        else:
            lbl_parcel_rx = Label(lbl_rx_data_dc, text = "                                 \n                             \n                                  ")
            lbl_parcel_rx.place(x=5, y=5)
            lbl_parcel_rx = Label(lbl_rx_data_dc, text = display_data_rx, foreground = 'green') 
            lbl_parcel_rx.place(x=5, y=5)
            lbl_parcel_rx = Label(lbl_rx_data_dc, text = "                                 ")
            lbl_parcel_rx.place(x=5, y=20)
            lbl_parcel_rx = Label(lbl_rx_data_dc, text = 'Версия ПО                                                            \n                                       ', foreground = 'green') 
            lbl_parcel_rx.place(x=5, y=20)
    except Exception:
        lbl_error_com = Label(lbl_rx_data_dc, text = "Нет принятых данных\nПроверьте соединение\nи настройка COM-порта\n                ", foreground = 'red')
        lbl_error_com.place(x=5, y=5)        
               
        
     
#Main program
    
window = Tk()
window.title("Test-Operator")  
window.geometry('300x300')

btn_opros = Button(window, text="Из реестра", command = winreestr_pull_company)
btn_opros.place(x=190, y=35)

reestr = winreestr_pull()       # присваиваем переменной кортеж значений (0-последняя посылка из реестра (кортеж), 1-последний выбраный COM-порт (кортеж))
lbl0 = Label(window, text = "Выберите COM-порт:").place(x=15, y=15)
combo = Combobox(window, values = serial_ports())
combo.place(x=15, y=35)
#combo.bind('<<ComboboxSelected>>', com_port_state) #вызываем функцию отображения состояния порта
combo.set(reestr[0])   # устанавливае при запуске программы значение COM-порта из реестра

btn_send = Button(window, text="Эталонный счетчик", width = 20, command = lambda: serial_tx(1))
btn_send.place(x=15, y=70)

btn_send = Button(window, text="Блок управления", width = 20, command = lambda: serial_tx(2))
btn_send.place(x=15, y=100)

btn_stop = Button(window, text="Остановить установку", width = 20, command = lambda: serial_tx(3))
btn_stop.place(x=15, y=150)

lbl_rx_data_dc = LabelFrame(window, text = "Принятые данные")
lbl_rx_data_dc.place(x=15, y=190, width = 250, heigh = 100)

window.mainloop()


