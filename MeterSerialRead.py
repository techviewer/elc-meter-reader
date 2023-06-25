import serial
import time
import subprocess
from main import METER_PHASE_TYPE

if METER_PHASE_TYPE == 1:
    from constants_1P import PROB_NAME,TEXT_NAME,WAKEUP_STR,DEVICE_TYPE,WAKEUP_PARAM,DATA_READOUT_PARAM,DEV_BOUDRATE,DEV_NEW_BOUDRATE,BOUD_SELECT,TIME_OUT,READOUT_FACTOR
elif METER_PHASE_TYPE == 3:
    from constants_3P import PROB_NAME,TEXT_NAME,WAKEUP_STR,DEVICE_TYPE,WAKEUP_PARAM,DATA_READOUT_PARAM,DEV_BOUDRATE,DEV_NEW_BOUDRATE,BOUD_SELECT,TIME_OUT,READOUT_FACTOR


deviceFind = False


def boudSlect():
    global DEV_BOUDRATE
    if BOUD_SELECT:
        DEV_BOUDRATE = DEV_NEW_BOUDRATE
        return DEV_BOUDRATE
    else:
        return DEV_BOUDRATE


def findDevice():
    devOut = []
    dev = subprocess.Popen(['python', '-m', 'serial.tools.list_ports', '-v'],stdout=subprocess.PIPE)
    devFind =False
    for line in dev.stdout:
        devOut.append(line.decode('UTF-8'))
    for i in range(len(devOut)):
        devInfo = str(devOut[i])
        for x in devInfo.split():
            if x == PROB_NAME:
                print("Optik sensör bulundu!")
                devFind = True
                break
        if devFind:
            devIndis = i
            print(devOut[i][4:-26])  # seri portta bulunan sensör kimliği
            break
    devFind = False
    devIndis = None
    print("Cihaz port bilgisi: " + str(devOut[i-1][:12]))
    return str(devOut[i-1][:12])    


#port tara hangi port olduğunu bul
def PortDefine():
    global port
    port = serial.Serial ( port = findDevice(), baudrate = boudSlect(),
                           parity = serial.PARITY_EVEN,
                           stopbits = serial.STOPBITS_ONE,
                           bytesize = serial.SEVENBITS,
                           writeTimeout = 0,
                           timeout = 0.05,
                           rtscts = False,
                           dsrdtr = False,
                           xonxoff = False,
                           )
    #print(port)



def charList2String(array2str = ['S','a','y',' ','H','I']):
    toStr = ""
    for i in array2str:
        toStr += i
    return toStr


def devDataReadout(startByte = b'\x02'):
    currentTime: float = 0.0
    bufData = bytes
    dataList = [] 
    dataPackage = ''
    try:
        beginTime = time.time() 
        while startByte != bufData:
            bufData = port.read(1)
            currentTime = time.time() - beginTime
            if currentTime >= TIME_OUT*2:
                #print(":(")
                return -1
        #dataList.append(bufData.decode('utf-8'))
        while b'\x03' != bufData:
            bufData = port.read(1)
            dataList.append(bufData.decode('utf-8'))
            currentTime = time.time() - beginTime
            if currentTime >= TIME_OUT*READOUT_FACTOR:
                #print(":)")
                return -1
        dataPackage = charList2String(dataList)
    except (IndexError):            #test edilip değiştirileceks
        pass
    return dataPackage
    
def readDeviceData(startByte = b'\x02', endByte = b'\r\n' ):
    dataList = []    #[b'']
    dataPackage = ''
    currentTime: float = 0.0
    bufData = b''
    global deviceFind
    """
    param: startByte STX (hex 02) (metin başlangıcı)
    param: stopByte LN (hex 0D) (satır iletimi), CR (hex 0A) (satır başı)
    """
        
    beginTime = time.time()        
    while True:
        try:
            while b'/' != bufData:
                bufData = port.read(1)
                #print(bufData)
                currentTime = time.time() - beginTime            
                if '/' == bufData.decode('utf-8'):
                    dataList.append(bufData.decode('utf-8'))
                    while b'\n' != bufData:                        
                        bufData = port.read(1)
                        #print(dataList)
                        dataList.append(bufData.decode('utf-8'))
                        currentTime = time.time() - beginTime
                        if currentTime >= TIME_OUT:
                            print("Timeout: Bitiş karakteri alınmadı")
                            return -1                    
                    dataPackage = charList2String(dataList)
                    print(dataPackage)
                    if dataPackage.find(DEVICE_TYPE) != -1:
                        print("Tip: " + dataPackage[8:(len(DEVICE_TYPE)+8)] + " elektrik sayacı ile haberleşildi.")
                        dataPackage = dataPackage[0:(len(DEVICE_TYPE)+8)]
                        deviceFind = True
                        break                        
                if currentTime >= TIME_OUT*2:
                    print("Timeout: Başlangıç karakteri alınmadı")
                    return -1
                if deviceFind:
                    break              
            currentTime = time.time() - beginTime 
            if currentTime >= TIME_OUT:
                break
        except (IndexError):
            pass
    return dataPackage


def opticRead():
    currentTime: float = 0.0
    zamanBaslangic = time.time()
    dataReadout = ''
    global deviceFind
    
    try: 
        beginTime = time.time() 
        PortDefine()
        print("Bağlantı portu: " + port.portstr)
        port.write(WAKEUP_PARAM) 
        #time.sleep(0.2)
        readWakeupData = readDeviceData()

        if readWakeupData == -1:
            print("Cihaz uyandırma mesajı yazılamadı")
        else:
            print("Sayaçtan gelen Veri: " + readWakeupData)
            currentTime = time.time() - beginTime
            print("Bağlantı işlem zamanı: ",end='')
            print(round(currentTime,3),end='')
            print("s")
          
        if deviceFind:
            currentTime = time.time()
            port.write(DATA_READOUT_PARAM)
            dataReadout = devDataReadout()
            if dataReadout == -1:
                print("Cihaz enerji verisi okuma zaman aşımı")
            else:
                print(dataReadout)
            deviceFind = False
            currentTime = time.time() - beginTime
            print("Elektrik sayacından veri okuma zamanı: ",end='')
            print(round(currentTime,3),end='')
            print("s")
            file  = open(TEXT_NAME,"w") # en son okunan verinin dosya olarak açılıp okunmasını sağlayacak text dosyası oluşturuluyor
            if type(dataReadout) == str:
                # tarif formatını SQLite date formatına dönüştürme YYYY-MM-DD
                # "0.9.2" Sayaç tarihi YY-MM-DD
                dataReadout= dataReadout[:(dataReadout.find("0.9.2")+6)] + "20" + dataReadout[(dataReadout.find("0.9.2")+6):]
                file.write(dataReadout)
                file.close()
            else:
                print("Hatalı veri okundu! Sensörü kontrol edin!")
                print("")
                file.close()
                return ''
            print("Sayaç veri okuma tamamlandı.")
            return dataReadout
        elif readWakeupData == -1:
            return ''
        else:
            print(WAKEUP_STR + " tip sayaç enerji verisi alınamamıştır!")
            return ''
    except FileNotFoundError:
        print("Seri port kontrol edilmeli.")
    except (OSError, FileNotFoundError):
        print("Cihaz Bulunamadı")
        pass

#opticRead()
