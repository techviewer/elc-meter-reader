from getAttributesTB import getDataTB

#def constMain():
WAIT2READ_TIME = 15*60   # 15 DAKİKADA (900s) BİR OKUMA ALINACAKTIR. BİR OKUMA 80sn


#def constSerialRead_3P():
PROB_NAME = 'KMK116'    #Kullanılan optik prob USB cihaz ismini giriniz
#kullanılan sayacın el sıkışma dönüş mesajını yazınız
WAKEUP_STR =  '/MSY5<1>C520.KMY.2251'   
# Kullanılan sayaç modelini yazınız
DEVICE_TYPE = 'C520.KMY.2251'  
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
ATTR_2 = "KuruluPDurumuLT50kW"

#def constSayacDB_3P():
#oluşturulacak veri tabanı dosyası ismi tanımlanır
DATABASE_NAME = r'electricMeter_3P.db'
#okunan anlık verilerin olası durumlar için inceleneceği metin dosyası isimi tanımlanır
TEXT_NAME = 'Elektirik Sayacı Anlık Veri.txt'
# 3 faz dört telli endüktif reaktif (kombi) sayaç
METER_ID = "SAYAC_SERİ_NO" 
#veri tabanında sayaç bilgileri tutulacak kullanıcı ismi tanımlanır
COSTUMER_NAME = r'Kullanıcı_Adı'
# sayaç en yüksek tüketim değerini ölçme zaman aralığı (dk)
DEMANT_TIME = 15

readDayReq = getDataTB(HOST,TOKEN,ATTR_1)
if readDayReq == None :
    READ_DAY = 15       #AYIH HANGİ GUNU SAYAC OKUMASI YAPILMAKTADIR. (VARSAYILAN)
else:
    READ_DAY = readDayReq   # Kullanıcının belirlediği sunum katmanından okuma günü

installedPState = getDataTB(HOST,TOKEN,ATTR_2)
if installedPState == None :
    INSTALLED_POWER_LESSThan_50kVA = True # varsayılan kurulu güç 50kW dan küçük
else:
    INSTALLED_POWER_LESSThan_50kVA = installedPState # Kullanıcı kurululu gücünün 50kW  dan büyk veya küçük olduğunu belirliyor
    
if INSTALLED_POWER_LESSThan_50kVA:
    PUNITIVE_IND_RATE_PER = 33.0
    PUNITIVE_CAP_RATE_PER = 20.0
else:
    PUNITIVE_IND_RATE_PER = 20.0
    PUNITIVE_CAP_RATE_PER = 15.0
    
#Test dashboarddan yazılan verierin doğrulu test edilebilir
#print(READ_DAY)
#print(INSTALLED_POWER_LESSThan_50kVA)

#def constSendingDataTB_3P():
dataTable = {"d000" : "seriNo",                 # rows[][0]
             "d080" : "demandmetreSuresi",      # rows[][1]
             "d091" : "sayacSaati",             # rows[][2]
             "d092" : "sayacTarihi",            # rows[][3]
             "d095" : "sayacHaftaninGunu",      # rows[][4]
             "d180" : "ToplamAktifTuketim",     # rows[][5]
             "d181" : "T1AktifTuketim",         # rows[][6]
             "d182" : "T2AktifTuketim",         # rows[][7]
             "d183" : "T3AktifTuketim",         # rows[][8]
             "d1801" : "TAktifAybasi",          # rows[][9]
             "d1811" : "T1AktifAybasi",         # rows[][10]
             "d1821" : "T2AktifAybasi",         # rows[][11]
             "d1831" : "T3AktifAybasi",         # rows[][12]
             "d1841" : "T3AktifAybasi",         # rows[][13]
             "d580" : "toplamEndReaktifTuk",    # rows[][14]
             "d5801" : "endReaktifTukGecenAy",  # rows[][15]
             "d880" : "kapReaktifTukT",         # rows[][16]
             "d8801" : "kapReaktifTukTGecenAy", # rows[][17]
             "d160" : "MaxAktifDemant",         # rows[][18]
             "d3170" : "L1Irms",                # rows[][19]
             "d5170" : "L2Irms",                # rows[][20]
             "d7170" : "L3Irms",                # rows[][21]
             "d3270" : "L1Vrms",                # rows[][22]
             "d5270" : "L2Vrms",                # rows[][23]
             "d7270" : "L3Vrms",                # rows[][24]
             "d9661" : "PilDurumu",             # rows[][25]
             "d9670" : "ustKapakAcilmaZamani",  # rows[][26]
             "d9671" : "klemensKapakAcilmaZamani"}  # rows[][27]

analizeDataTable = {1 : "anlikPT_kW",
                    2 : "anlikPT1_kW",
                    3 : "anlikPT2_kW",
                    4 : "anlikPT3_kW",
                    5 : "anlikEndQ_kVAr",
                    6 : "anlikKapQ_kVAr",
                    7 : "anlikPToplam_kW",
                    8 : "anlikPT1Toplam_kW",
                    9 : "anlikPT2Toplam_kW",
                    10: "anlikPT3Toplam_kW",
                    11: "anlikEndQToplam_kVAr",
                    12: "anlikKapQToplam_kVAr",
                    13: "yuzdeEndReaktif",
                    14: "yuzdeKapReaktif",
                    15: "cezaDurumu",
                    16: "endCezaDurumu",
                    17: "kapCezaDurumu" }

    
