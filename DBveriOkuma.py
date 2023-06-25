from ThingsboardClient import *
from sendingData2TB import dataTable
from main import METER_PHASE_TYPE

if METER_PHASE_TYPE == 1:
    from meterDB_1P import create_connection, get_labels
    from constants_1P import DATABASE_NAME,HOST,TOKEN,THINGSBOARD_OK,METER_ID,READ_DAY
    from meterDB_1P import getDatas
elif METER_PHASE_TYPE == 3:
    from meterDB_3P import create_connection, get_labels
    from constants_3P import DATABASE_NAME,HOST,TOKEN,THINGSBOARD_OK,METER_ID,READ_DAY
    from meterDB_3P import getDatas
    
from datetime import datetime,timedelta

def sendTB():
    database_connection = create_connection(DATABASE_NAME)
    cursor = database_connection.cursor()
    #labels = get_labels(database_connection, "data")

    #print(labels)
    #cursor.execute(f"SELECT * FROM data WHERE d000 = {METER_ID} ORDER BY d092 DESC, d091 DESC ") #verileri önce tarihe göre sonra zamana göre sıralama
    #cursor.execute("SELECT d880 FROM data")
    #rows = cursor.fetchall()
    #rows = cursor.fetchall()
    #print(rows)
    #cursor.execute(f"SELECT d092 FROM data WHERE d000 = {METER_ID} ORDER BY d092 DESC, d091 DESC ")
    #rowDate = cursor.fetchone()
    #print(type(rowDate[0]))
    #print(rowDate[0])
    #cursor.execute(f"SELECT d092 FROM data WHERE d000 = {METER_ID} ORDER BY d092 DESC, d091 DESC ")
    #print(type(rows[0][1]))
    #print(rows[1])
    #print((rows[0][6]-rows[1][6])*1000) #Waat olarak 15dk lik tüketim
    cursor.execute(f"SELECT * FROM data WHERE d000 = {METER_ID} AND d092 >= '2023-05-01' ORDER BY d092 DESC, d091 DESC ")
    # 15 gün öncesi bir önceki ay ise yıl-(ay-1)-(okuma günü) değilse yıl-ay-(okuma günü) / rowDate den tarihi işle ona göre sorgu yaz {} kullanarak
    rows = cursor.fetchall()
    print(rows)
    #----------------------------------------------
    """
    cursor.execute("SELECT * FROM data")
    td = datetime.now().date()
    fifteenDayEgo = td - timedelta(days = 15)
    for row in cursor.fetchall():
        date = datetime.strptime(row[3], "%Y-%m-%d").date() #tarih sutununun sıfır tabanlı indeksi
        if date >= fifteenDayEgo:
            print(row)
    """
    #---------------------------------------------
    today = datetime.now().date()
    day = today.day
    month = today.month
    year = today.year
    print(day)
    #print(type(day))
    #print(str(today))
    # sayaç okuma gönüne göre veri okuma tarihi hesaplanıyor
    if READ_DAY > day : # şu an, okuma gününden önce ise bir önceki aydan geriler çekilecektir
        #print(READ_DAY-day)
        #print("bir önceki aydan veri al")
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
        print(calcDate + ' önceki ay için hesaplanan tarih')
        cursor.execute(f"""SELECT * FROM data WHERE d000 = {METER_ID} AND d092 >= {calcDate} ORDER BY d092 ASC, d091 ASC """)
        rows = cursor.fetchone()
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
        print(calcDate + ' bu ay için hesaplanan tarih')
        cursor.execute(f"""SELECT * FROM data WHERE d000 = {METER_ID} AND d092 >= {calcDate} ORDER BY d092 ASC, d091 ASC """)
        rows = cursor.fetchone()
    else:
        print("Okuma günü hesaplanamdı!")
    
    # 15 gün öncesi bir önceki ay ise yıl-(ay-1)-(okuma günü) değilse yıl-ay-(okuma günü) / rowDate den tarihi işle ona göre sorgu yaz {} kullanarak
    
    print(rows)
    database_connection.close()


sendTB()
