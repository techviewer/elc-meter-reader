import sqlite3
from sqlite3 import Error
from main import METER_PHASE_TYPE
from datetime import datetime
from getAttributesTB import getDataTB

if METER_PHASE_TYPE == 1:
    from constants_1P import DATABASE_NAME,TEXT_NAME,METER_ID,READ_DAY,DEMANT_TIME,COSTUMER_NAME,analizeDataTable,PUNITIVE_IND_RATE_PER,PUNITIVE_CAP_RATE_PER,HOST,TOKEN,ATTR_1
    from meterDB_1P import create_connection
elif METER_PHASE_TYPE == 3:
    from meterDB_3P import create_connection
    from constants_3P import DATABASE_NAME,TEXT_NAME,METER_ID,READ_DAY,DEMANT_TIME,COSTUMER_NAME,analizeDataTable,PUNITIVE_IND_RATE_PER,PUNITIVE_CAP_RATE_PER,HOST,TOKEN,ATTR_1


def readDayDataQuery ():
    today = datetime.now().date()
    day = today.day
    month = today.month
    year = today.year
    db = create_connection(DATABASE_NAME)
    cursor = db.cursor()
    readDayTB = getDataTB(HOST,TOKEN,ATTR_1)
    if READ_DAY > day : # şu an, okuma gününden önce ise bir önceki aydan geriler çekilecektir
        month -= 1
        if month <= 0:
            month = 12
            year -= 1
        sDay = str(READ_DAY)
        sMonth = str(month)
        sYear = str(year)
        if READ_DAY < 10 :
            sDay = '0' + sDay
        if month < 10 :
            sMonth = '0' + sMonth
        calcDate = '\'' + sYear + '-' + sMonth + '-' + sDay + '\''      #okuma günü hesaplanıyor o tarihteki ilk veri çekilecektir. yüzde hesabında ceza durumu için kullanılacak veri
        print('Önceki ay için hesaplanan tarih: ' + calcDate)
        cursor.execute(f"""SELECT * FROM data WHERE d000 = {METER_ID} AND d092 >= {calcDate} ORDER BY d092 ASC, d091 ASC """)
        return cursor.fetchone()
    elif READ_DAY <= day : # şu an, okuma gününden sonra ise bir şu anki aydan geriler çekilecektir
        #print(READ_DAY-day)
        #print("bu aydan veri al")
        sDay = str(READ_DAY)
        sMonth = str(month)
        sYear = str(year)
        if READ_DAY < 10 :
            sDay = '0' + sDay
        if month < 10 :
            sMonth = '0' + sMonth
        calcDate = '\'' + sYear + '-' + sMonth + '-' + sDay + '\''      #okuma günü hesaplanıyor o tarihteki ilk veri çekilecektir. yüzde hesabında ceza durumu için kullanılacak veri
        print('Bu ay için hesaplanan tarih: ' + calcDate)
        cursor.execute(f"""SELECT * FROM data WHERE d000 = {METER_ID} AND d092 >= {calcDate} ORDER BY d092 ASC, d091 ASC """)
        rows = cursor.fetchone()
        db.close()
        return rows
    else:
        print("Okuma günü hesaplanamdı!")
        db.close()
        return []


def analizeData():
    try:
        ilkEndeksPT = 0.0
        ilkEndeksPT1T = 0.0
        ilkEndeksPT2T = 0.0
        ilkEndeksPT3T = 0.0
        ilkEndeksEndQT = 0.0
        ilkEndeksKapQT = 0.0
        sonEndeksPT = 0.0
        sonEndeksPT1T = 0.0
        sonEndeksPT2T = 0.0
        sonEndeksPT3T = 0.0
        sonEndeksEndQT = 0.0
        sonEndeksKapQT = 0.0        
        anlikPT = 0.0
        anlikEndQT = 0.0
        anlikKapQT = 0.0
        endQTYuzdePT = 0.0
        kapQTYuzdePT = 0.0
        cezaDurumu = False
        analiedData = {}
        
        if METER_PHASE_TYPE == 1:
            database_connection = create_connection(DATABASE_NAME)
            cursor = database_connection.cursor()
            cursor.execute(f"SELECT * FROM data WHERE d000 = {METER_ID} ORDER BY d092 DESC, d091 DESC ") #verileri önce tarihe göre sonra zamana göre sıralama
            rows = cursor.fetchmany(2)
            #print(rows)
            #print("")
            sonEndeksPT = round(rows[0][5],3)
            for i in range(1,(len(analizeDataTable)+1)):
                #print(analizeDataTable[i])
                if i == 1:  #anlikAktifT_kW
                    analiedData[analizeDataTable[i]] = round((rows[0][5]-rows[1][5]),3) #kW olarak 15dk lik tüketim
                elif i == 2:    #anlikAktifT1_kW
                    analiedData[analizeDataTable[i]] = round((rows[0][6]-rows[1][6]),3)
                elif i == 3:    #anlikAktifT2_kW
                    analiedData[analizeDataTable[i]] = round((rows[0][7]-rows[1][7]),3)
                elif i == 4:    #anlikAktifT3_kW
                    analiedData[analizeDataTable[i]] = round((rows[0][8]-rows[1][8]),3)
                elif i == 5:    #anlikPToplam_kW
                    dataRows = readDayDataQuery()
                    #print(dataRows)
                    ilkEndeksPT = round(dataRows[5],3)
                    anlikPT = sonEndeksPT - ilkEndeksPT
                    if anlikPT < 0:
                        print("Hatalı aktif güç tüketim bilgisi hesabı!")
                        break
                    analiedData[analizeDataTable[i]] = round(anlikPT,3)
                else:
                    break 
                    
        elif METER_PHASE_TYPE == 3:
            database_connection = create_connection(DATABASE_NAME)
            cursor = database_connection.cursor()
            cursor.execute(f"SELECT * FROM data WHERE d000 = {METER_ID} ORDER BY d092 DESC, d091 DESC ") #verileri önce tarihe göre sonra zamana göre sıralama
            rows = cursor.fetchmany(2)
            #rows = cursor.fetchone()       # fetchone metodu kullanılacaksa rows[5] --> sonEndeksPT
            #print(rows)
            #print("")
            #print(rows[0][6])
            #print(rows[1][6])
            sonEndeksPT = round(rows[0][5],3)
            sonEndeksPT1T = round(rows[0][6],3)
            sonEndeksPT2T = round(rows[0][7],3)
            sonEndeksPT3T = round(rows[0][8],3)
            sonEndeksEndQT = round(rows[0][14],3)
            sonEndeksKapQT = round(rows[0][16],3)            
            
            for i in range(1,(len(analizeDataTable)+1)):
                #print(analizeDataTable[i])
                if i == 1:  #anlikAktifT_kW
                    analiedData[analizeDataTable[i]] = round((rows[0][5]-rows[1][5]),3) #kW olarak 15dk lik tüketim
                elif i == 2:    #anlikAktifT1_kW
                    analiedData[analizeDataTable[i]] = round((rows[0][6]-rows[1][6]),3)
                elif i == 3:    #anlikAktifT2_kW
                    analiedData[analizeDataTable[i]] = round((rows[0][7]-rows[1][7]),3)
                elif i == 4:    #anlikAktifT3_kW
                    analiedData[analizeDataTable[i]] = round((rows[0][8]-rows[1][8]),3)
                elif i == 5:    #anlikEndReaktifT_kVAr
                    analiedData[analizeDataTable[i]] = round((rows[0][14]-rows[1][14]),3)
                elif i == 6:    #anlikKapReaktifT_kVAr
                    analiedData[analizeDataTable[i]] = round((rows[0][16]-rows[1][16]),3)
                elif i == 7:    #anlikPToplam_kW
                    dataRows = readDayDataQuery()
                    #print(dataRows)
                    ilkEndeksPT = round(dataRows[5],3)
                    ilkEndeksPT1T = round(dataRows[6],3)
                    ilkEndeksPT2T = round(dataRows[7],3)
                    ilkEndeksPT3T = round(dataRows[8],3)
                    ilkEndeksEndQT = round(dataRows[14],3)
                    ilkEndeksKapQT = round(dataRows[16],3)

                    anlikPT = sonEndeksPT - ilkEndeksPT
                    if anlikPT < 0:
                        print("Hatalı aktif güç tüketim bilgisi hesabı!")
                        break
                    analiedData[analizeDataTable[i]] = round(anlikPT,3)
                elif i == 8:    #anlikPT1Toplam_kW
                    anlikPT1Toplam_kW = sonEndeksPT1T - ilkEndeksPT1T
                    analiedData[analizeDataTable[i]] = round(anlikPT1Toplam_kW,3)
                elif i == 9:    #anlikPT2Toplam_kW
                    anlikPT2Toplam_kW = sonEndeksPT2T - ilkEndeksPT2T
                    analiedData[analizeDataTable[i]] = round(anlikPT2Toplam_kW,3)
                elif i == 10:    #anlikPT3Toplam_kW
                    anlikPT3Toplam_kW = sonEndeksPT3T - ilkEndeksPT3T
                    analiedData[analizeDataTable[i]] = round(anlikPT3Toplam_kW,3)
                elif i == 11:    #anlikEndQToplam_kVAr
                    anlikEndQT = sonEndeksEndQT - ilkEndeksEndQT
                    analiedData[analizeDataTable[i]] = round(anlikEndQT,3)
                elif i == 12:    #anlikKapQToplam_kVAr
                    anlikKapQT = sonEndeksKapQT - ilkEndeksKapQT
                    analiedData[analizeDataTable[i]] = round(anlikKapQT,3)
                elif i == 13:    #yuzdeEndReaktif
                    endQTYuzdePT =  (anlikEndQT * 100) / anlikPT 
                    analiedData[analizeDataTable[i]] = round(endQTYuzdePT,2)
                    #print(rows)
                elif i == 14:    #yuzdeKapReaktif
                    kapQTYuzdePT =  (anlikKapQT * 100) / anlikPT 
                    analiedData[analizeDataTable[i]] = round(kapQTYuzdePT,2)
                elif i == 15:    #cezaDurumu
                    if (endQTYuzdePT > PUNITIVE_IND_RATE_PER) or (kapQTYuzdePT > PUNITIVE_CAP_RATE_PER ) :
                        analiedData[analizeDataTable[i]] = True
                    else:
                        analiedData[analizeDataTable[i]] = False
                elif i == 16:    #endCezaDurumu
                    if endQTYuzdePT > PUNITIVE_IND_RATE_PER :
                        analiedData[analizeDataTable[i]] = True
                    else:
                        analiedData[analizeDataTable[i]] = False
                elif i == 17:    #kapCezaDurumu
                    if kapQTYuzdePT > PUNITIVE_CAP_RATE_PER :
                        analiedData[analizeDataTable[i]] = True
                    else:
                        analiedData[analizeDataTable[i]] = False
                else:
                    break
            #test module
            #print(analiedData)
            #print(analizeDataTable)
        else:
            print("Cihaz faz tipi bilgisi alınamadı!") 
    except sqlite3.Error as error:
        print("Hata! ", error)
        return False
    database_connection.close()
    return analiedData

#Test Module
#analizeData()
