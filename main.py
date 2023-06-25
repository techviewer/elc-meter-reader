#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2023  <KCraspPi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#

#sayaç tipi değişkeni
METER_PHASE_TYPE = 3 # 1 ise 1 fazlı, 3 ise 3 fazlı sayaç aranır

#main başka bir yeden çağrıldığında (METER_PHASE_TYPE erişmek için) hiçbir modul tekrardan import edilmeyecektir
if METER_PHASE_TYPE == 1 and __name__ == '__main__':
    import time
    import datetime
    from sendingDataTB import sendingTB
    #import MeterSerialRead_1P
    import MeterSerialRead
    import meterDB_1P
    from constants_1P import WAIT2READ_TIME
if METER_PHASE_TYPE == 3 and __name__ == '__main__':
    import time
    import datetime
    from sendingDataTB import sendingTB
    #import MeterSerialRead_3P
    import MeterSerialRead
    import meterDB_3P
    from constants_3P import WAIT2READ_TIME
import threading
from tqdm.auto import tqdm




def main(args):
    
    currentTime: float = 0.0
    dottime: float = 60.0
    beginTime: float = 0.0
    timeCheck = True
    barCheck = True

    #time.sleep(10) # sistem tam açılış için bekleme zamanı
    
    while True:
        if timeCheck:
            dataCheck = ''
            beginTime = time.time()
            if METER_PHASE_TYPE == 1:
                dataCheck = MeterSerialRead.opticRead()
            elif METER_PHASE_TYPE == 3:
                dataCheck = MeterSerialRead.opticRead()
            else:
                print("Modul yükleme hatası!")
                break
            #print(type(dataCheck))
            #print(dataCheck)
            if dataCheck:
                if METER_PHASE_TYPE == 1:
                    meterDB_1P.writeDB()
                elif METER_PHASE_TYPE == 3:
                    meterDB_3P.writeDB()
                else:
                    print("Modul yükleme hatası!")
                    break            
                #DB veri çek
                #çekilen veriyi gönder
                sendingTB()
                now = datetime.datetime.now()
                print("")
                print (now.strftime("%Y-%m-%d %H:%M:%S"))
                readTime = time.time() - beginTime
                curMin = int(readTime / 60.0)
                curSec = int(readTime % 60.0)
                print("Bir sonraki sayaç okuması " + str(int(WAIT2READ_TIME/60.0) - curMin - 1) + "dk " + str(60 - curSec) + "sn sonra olacaktır.")
                timeCheck = False #time.sleep(840)
                barCheck = True
                #beginTime = time.time()
            else:
                print("Sayaç verisi alınamadı! Yeniden başlatılıyor")
        else:
            #time.sleep(10)
            if barCheck:
                readTime = time.time() - beginTime
                for i in tqdm(range(100),colour='#00ff00', desc= 'Zaman ilerleme çubuğu: '):
                    try:
                        time.sleep((float(WAIT2READ_TIME) - readTime) /100.0)
                    except ValueError: # mili/mikrosaniyelerde eksi değere düşerse hata dikkate alınmayacaktır.
                        pass
                print("")
                barCheck = False
            else:
                currentTime = time.time() - beginTime
                if currentTime >= WAIT2READ_TIME:
                    timeCheck = True
                time.sleep(0.2)
                #print(timeCheck, end = ' ' )

            
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
