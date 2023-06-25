from ThingsboardClient import *
#from sendingData2TB import dataTable
from main import METER_PHASE_TYPE
from dataAnalysis import analizeData

if METER_PHASE_TYPE == 1:
    from meterDB_1P import create_connection, get_labels
    from constants_1P import DATABASE_NAME,HOST,TOKEN,THINGSBOARD_OK,analizeDataTable,dataTable
    from meterDB_1P import getDatas
elif METER_PHASE_TYPE == 3:
    from meterDB_3P import create_connection, get_labels
    from constants_3P import DATABASE_NAME,HOST,TOKEN,THINGSBOARD_OK,analizeDataTable,dataTable
    from meterDB_3P import getDatas
    


client = ThingsboardClient(HOST)

def sendingTB():
    try:
        database_connection = create_connection(DATABASE_NAME)
        cursor = database_connection.cursor()
        labels = get_labels(database_connection, "data")
        cursor.execute("SELECT * FROM data")
        rows = cursor.fetchall()
        #print(type(rows))  #veri tabanında çekilen en son sayaç verisi gönderiliyor
        status = client.send_telemetry(
            TOKEN,
            {
                dataTable[labels[label_index]]: rows[-1][label_index]
                for label_index in range(len(labels))
            },
        )
        #veri tabanında çekilen analiz edilen sayaç verileri gönderiliyor
        analizeRes = analizeData()
        status = client.send_telemetry(
            TOKEN,
            {
                analizeDataTable[i] : analizeRes[analizeDataTable[i]]
                for i in range(1,(len(analizeDataTable)+1))
            },
        )
        database_connection.close()
        for i in range(1,(len(analizeDataTable)+1)):
            print(analizeDataTable[i] + " = " + str(analizeRes[analizeDataTable[i]]) ) 

        if status != THINGSBOARD_OK:
            print("hingsBoard server hatası oluştu!")
            return False
        else:
            return True    

    except requests.exceptions.RequestException as err:
        print ("TB sorugu hatası!: ",err)
        return -1
    except requests.exceptions.HTTPError as errh:
        print ("Http Hatası: ",errh)
        return -1
    except requests.exceptions.ConnectionError as errc:
        print ("Bağlantı hatası: ",errc)
        return -1
    except requests.exceptions.Timeout as errt:
        print ("Timeout Hatası: ",errt)
        return -1

    
"""
def sendTB():
    print("Veri başarıyla gönderildi.")
    analizeRes = analizeData()

    #print("")
    #for i in range(1,(len(analizeDataTable)+1)):
        #print(analizeDataTable[i] + " = " + str(analizeRes[analizeDataTable[i]]) )  

    status = client.send_telemetry(
        TOKEN,
        {
            analizeDataTable[i] : analizeRes[analizeDataTable[i]]
            for i in range(1,(len(analizeDataTable)+1))
        },
    )
    if status != THINGSBOARD_OK:
        print("Bir hata oluştu!")
    else:
        return True
"""
#sendTB()
#sendingTB(10)
