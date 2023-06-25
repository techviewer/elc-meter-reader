from getAttributesTB import getDataTB

#def constMain():
WAIT2READ_TIME = 900   # 15 DAKİKADA (900s) BİR OKUMA ALINACAKTIR. BİR OKUMA 80sn

#def constSerialRead_3P():
PROB_NAME = 'KMK116'    #Kullanılan optik prob USB cihaz ismini giriniz
#kullanılan sayacın el sıkışma dönüş mesajını yazınız
WAKEUP_STR = '/MSY5<1>M600.2251'   
# Kullanılan sayaç modelini yazınız
DEVICE_TYPE = 'M600.2251' 
# standart IEC62056-21 Mod C Readout el sıkışma parametresi
WAKEUP_PARAM= b'\x2F\x3F\x21\x0D\x0A'     
# Mod C Readout (Tüm verileri alma) parametresi  
DATA_READOUT_PARAM = b'\x06\x30\x30\x30\x0D\x0A'  
#Bu çalışmada cihaz haberleşme ayarları değiştirilmemiş olup varsayılan 300 boud ile haberleşme yapılmıştır
DEV_BOUDRATE = 300
# istenilirse uygun parametre gönderilerek 9600 boud a geçilebilir
DEV_NEW_BOUDRATE = 9600 
# boud değirme aktif yapılacaksa True yapılmalıdır    
BOUD_SELECT = False 
#Sayaç verisi okuma için beklenecek maksimum sure. Bu değerden sonrası hata mesajı ile sonuçlanıp okuma işlemi bırakılır
TIME_OUT = 5
# Moc C de 300 boudrate için Readout okuma tamamlanmasının için beklenecek maksimum sure. Bu değerden sonrası hata mesajı ile sonuçlanıp okuma işlemi bırakılır
READOUT_FACTOR = 20

#ThingsBoard server hata dönüş mesaj ID'leri
#def constTBClient():
THINGSBOARD_OK = 200
THINGSBOARD_INVALID_DATA = 400
THINGSBOARD_INVALID_TOKEN = 401
THINGSBOARD_RESOURCE_NOT_FOUND = 404
HOST = "demo.thingsboard.io"
TOKEN = "ACSESS_TOKEN"  # ThingsBoard cihaz ulaşım kimliğini string ACSESS_TOKEN yazan yere kaydediniz
ATTR_1 = "SayacOkumaAyınGunu"

#def constSayacDB_1P():
#oluşturulacak veri tabanı dosyası ismi tanımlanır
DATABASE_NAME = r'electricMeter_1P.db'
#okunan anlık verilerin olası durumlar için inceleneceği metin dosyası isimi tanımlanır
TEXT_NAME = 'Elektrik Sayacı Anlık Veri.txt'
# 1 faz dört telli endüktif reaktif (kombi) sayaç
METER_ID = "SAYAC_SERİ_NO" 
#veri tabanında sayaç bilgileri tutulacak kullanıcı ismi tanımlanır
COSTUMER_NAME = r'Kullanıcı_Adı'
# sayaç en yüksek tüketim değerini ölçme zaman aralığı (dk)
DEMANT_TIME = 15


readDayReq = getDataTB(HOST,TOKEN,ATTR_1)
if readDayReq == None :
    READ_DAY = 15       #AYIH HANGİ GUNU SAYAC OKUMASI YAPILMAKTADIR (Varsayılan)
else:
    READ_DAY = readDayReq   # Kullanıcının belirlediği sunum katmanından okuma günü
        
DEMANT_TIME = 15
COSTUMER_NAME = r'Koray CAN'
INSTALLED_POWER_LESSThan_9kVA = True # kullanılmamaktadır. İkitanımlanmalı. değeri önemli değildir
PUNITIVE_IND_RATE_PER = 0.0
PUNITIVE_CAP_RATE_PER = 0.0

#Test dashboarddan yazılan verierin doğrulu test edilebilir
#print(READ_DAY)

#def constSendingDataTB_3P():
dataTable = {"d000" : "seriNo",
             "d080" : "demandmetreSuresi",
             "d091" : "sayacSaati",
             "d092" : "sayacTarihi",
             "d095" : "sayacHaftaninGunu",
             "d180" : "ToplamAktifTuketim",
             "d181" : "T1AktifTuketim",
             "d182" : "T2AktifTuketim",
             "d183" : "T3AktifTuketim",
             "d1801" : "TAktifAybasi",
             "d1811" : "T1AktifAybasi",
             "d1821" : "T2AktifAybasi",
             "d1831" : "T3AktifAybasi",
             "d1841" : "T4AktifAybasi",
             "d160" : "MaxAktifDemant",
             "d3170" : "L1Irms",
             "d3270" : "L1Vrms",
             "d9661" : "PilDurumu",
             "d9670" : "ustKapakAcilmaZamani",
             "d9671" : "klemensKapakAcilmaZamani"}


analizeDataTable = {1 : "anlikPT_kW",
                    2 : "anlikPT1_kW",
                    3 : "anlikPT2_kW",
                    4 : "anlikPT3_kW",             
                    5 : "anlikPToplam_kW",}

    
