import requests
import json


def getDataTB(hostId,entityId,attributeKey):
        # param hostId: HOST
        # param entityId: TOKEN istek yapılacak cihaz erişim şifresi (accses token)
        # param attributeKey: tanımlı cihazın paylaştığı veri anaktar isimi
    try:        
        # ThingsBoard sunucu URL'si
        url = f"http://{hostId}/api/v1/{entityId}/attributes"

        #GET isteği
        response = requests.get(url)

        # GET yanıt kontrolü
        if response.status_code == 200:
            # JSON yanıt verisi
            data = json.loads(response.text)
            #print(data)
            if not data.get('shared') == None:            
                if not data['shared'].get(attributeKey) == None :
                    return data['shared'][attributeKey]
                else:
                    print("GET sorugusunda cihaza ait paylaşılan veri bulunmamıştır!")
                    return None
            else:
                print("Bu cihazdda paylaşılan veri yok! Cihaz kimliğini veya paylaşılan öznitelikleri kontrol edin.")
                return None
        else:
            print("İstek başarısız. Hata kosdu:", response.status_code)
            return None

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

#Test
#print(getDataTB("demo.thingsboard.io","hbP8tKDH5BZDnZmx7N18","SayacOkumaAyınGunu"))
