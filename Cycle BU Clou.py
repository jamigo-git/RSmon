import time
import serial

class Loggable:
    def log(self, msg):
        print(str(time.ctime()) + ": " + str(msg))

class LoggableList(list, Loggable):
    def append(self,a):
        super(LoggableList,self).append(a)
        self.log(a)
a = LoggableList()


def serial_tx(parcel):
    try:
        ser = serial.Serial('COM1', 9600, timeout = 1)
   
        if parcel == 1:
            ser.setDTR(False)
            ser.setRTS(True)
            parcel_send = '8116052033'
            parcel_full = bytes.fromhex(parcel_send)
            ser.write(parcel_full)
            serial_rx(ser, 1)                   
            ser.close()
        elif parcel == 2:
            ser.setDTR(True)
            ser.setRTS(False) 
            parcel_send = '812000065670'
            parcel_full = bytes.fromhex(parcel_send)
            ser.write(parcel_full)
            serial_rx(ser, 2)
            ser.close()
    except Exception:
        print("Не удалось открыть COM-порт")

def serial_rx(ser, parcel):
    try:
        display_data_rx = ser.read(23)[4:13]
        #print("Принятые данные ", display_data_rx)
        if display_data_rx == b'':
            if parcel == 1:
                a.append('Нет ответа от эталонного счетчика')
            else:
                a.append('Нет ответа от БЛОКА УПРАВЛЕНИЯ')
        else:
           if parcel == 1:
               a.append('Ответ от эталонного счетчика -ОК') 
           else:
               a.append('Ответ от блока управления -ОК')
    except Exception:
        print("Нет принятых данных")
        
while True:
    serial_tx(1)
    time.sleep(1)
    serial_tx(2)
    time.sleep(1)












        
