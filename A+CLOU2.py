import time
import serial
import winreg


#Функция получения данных из реестра (если стоит программа)
def winreestr_pull():
    try:
        rsmon_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Incotex\\1Ph_pm\\')
        comport = winreg.QueryValueEx(rsmon_key, "ConnDev_COM")
    except Exception:
        comport = ("COM1", 1)            # при получении из реестра значения ключа получаем похожий кортеж
    return(comport[0])


class Loggable:
    def log(self, msg):
        print(str(time.ctime()) + ": " + str(msg))

class LoggableList(list, Loggable):
    def append(self,a):
        super(LoggableList,self).append(a)
        self.log(a)
a = LoggableList()


def serial_tx():
    try:
        ser = serial.Serial(winreestr_pull(), 9600, timeout = 1)
   
        
        parcel_send = '555555550002010057'
        parcel_full = bytes.fromhex(parcel_send)
        ser.write(parcel_full)
        serial_rx(ser, 0)                   
                    
        parcel_send = '555555550202010059'
        parcel_full = bytes.fromhex(parcel_send)
        ser.write(parcel_full)
        serial_rx(ser, 2)

        parcel_send = '55555555030201005A'
        parcel_full = bytes.fromhex(parcel_send)
        ser.write(parcel_full)
        serial_rx(ser, 3)

        parcel_send = '55555555040201005B'
        parcel_full = bytes.fromhex(parcel_send)
        ser.write(parcel_full)
        serial_rx(ser, 4)

        parcel_send = '55555555050201005C'
        parcel_full = bytes.fromhex(parcel_send)
        ser.write(parcel_full)
        serial_rx(ser, 5)

        parcel_send = '55555555060201005D'
        parcel_full = bytes.fromhex(parcel_send)
        ser.write(parcel_full)
        serial_rx(ser, 6)

        parcel_send = '55555555070201005E'
        parcel_full = bytes.fromhex(parcel_send)
        ser.write(parcel_full)
        serial_rx(ser, 7)

        parcel_send = '55555555080201005F'
        parcel_full = bytes.fromhex(parcel_send)
        ser.write(parcel_full)
        serial_rx(ser, 8)
            

        ser.close()
    except Exception:
        print("Не удалось открыть COM-порт")

def serial_rx(ser, number_pcb):
    try:
        display_data_rx = ser.read(16)
        parcel_hex = display_data_rx.hex()  #Переводим полученные данные в HEX-формат (убираем /x)
        parcel_hex = parcel_hex[18:]              #Удаляем отправленную посылку из принятых данных
        parcel_rx_up = parcel_hex.upper()
        a.append([winreestr_pull(), ' Ответ платы №', number_pcb, parcel_rx_up])
               
    except Exception:
        print("Нет принятых данных")
        

serial_tx()
time.sleep(1)
    












        
