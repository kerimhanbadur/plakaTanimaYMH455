import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from Plaka_Tespit import plakaKonumBul
import shutil
from tkinter import messagebox


"""
veri = os.listdir("Plakalar") # Plakalar klasöründeki arabaların ADRESLERİNİ okur.


PlakaResmi = veri[1]

resim = cv2.imread("Plakalar/"+PlakaResmi) # imread fonksiyonu belirtilen adresteki plakanın BGR değerlerini okuyucak.
resim = cv2.resize(resim, (500,500))

plaka = plakaKonumBul(resim)
x , y , w , h = plaka
if(w>h): # fonksiyonda bazen w ve h yerleri karışabiliyo bunu bir ifle kontrol ediyoruz.
    PlakaBGR = resim[y:y+h , x:x+w].copy()
else:
    PlakaBGR = resim[y:y+w , x:x+h].copy()
    
plt.imshow(PlakaBGR) # Plaka gösterir.
plt.show()

#plakanın görüntüsündeki pixelleri 2 katına çıkartıyoruz çünkü yapmazsak plakadaki sayıların bulunmasında yanılgıya düşebiliriz.
H,W = PlakaBGR.shape[:2] # Boyut bilgilerinden ilk 2 tanesini alır.
H,W= H*2 , W*2

PlakaBGR = cv2.resize(PlakaBGR , (W,H))

plt.imshow(PlakaBGR) # Plaka gösterir.
plt.show()

#Plaka resmini Griye çeviriyoruz.
GriPlaka = cv2.cvtColor(PlakaBGR , cv2.COLOR_BGR2GRAY)

plt.title("Gri Format")
plt.imshow(GriPlaka , cmap="gray") # Plaka gösterir.
plt.show()

#GriPlaka =cv2.adaptiveThreshold(işlemeGiricek resim , eşiğin üstünde kalanlar kac px olsun , hangi tür eşikleme kullanıcaksın , Nasıl eşikleme yapılacak , filtre karesinin kaç boyutlu olcağı , komşu sayısı)
EşiklenmişPlaka =cv2.adaptiveThreshold(GriPlaka , 255 , cv2.ADAPTIVE_THRESH_MEAN_C , cv2.THRESH_BINARY_INV , 11 , 2) #(1.1) Ayrıştırmanın ilk adımı eşiklemedir. adaptiveThreshold gelişmiş eşiklemedir.

plt.title("Eşiklenmiş Format")
plt.imshow(EşiklenmişPlaka , cmap="gray") # Plaka gösterir.
plt.show()


#Gürültüleri yokettik yani resimdeki pürüzleri sildik.
kernel = np.ones((3,3), np.uint8)
EşiklenmişPlaka = cv2.morphologyEx(EşiklenmişPlaka , cv2.MORPH_OPEN , kernel , iterations =1)

plt.title("Gürültü Yok Edilmiş Format")
plt.imshow(EşiklenmişPlaka , cmap="gray") # Plaka gösterir.
plt.show()


counter = cv2.findContours(EşiklenmişPlaka, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #2. kısım hiyerarşiyi nasıl işleme alcağımızdır. son kısımda pixel pixel butun counterlermi gelsin yoksa x y w h değerlerimi gelsin bunu seçiyoruz. CHAIN_APPROX_SIMPLE ile konum konum döner.
counter = counter[0] #counterler 2 değişken döndürür. 1.counterin konumununu döndürür[counter[0]]. 2. hiyerarşik yapıyı döndürür(counter[1]).

#sorted(key=cv2.contourArea = alanlarına göre küçükten büyüğe sırala , ters çevir büyükten küçüğe olsun.)[:15]=ilk 15 değerin alınması için.
counter = sorted(counter , key=cv2.contourArea, reverse=True)[:15] #istediğimiz counterler yani plakadaki karakterlerin olduğu counterler en büyük 10 yada 20 nin içindedir bu yüzden sıralıyoruz.


for i,c in enumerate(counter):
    rect=cv2.minAreaRect(c) # en küçük dikdörtgeni bana döndür demek. x , y ,Merkezin x y si ve rotuate açısı bulunur.
    (x,y) , (w,h) , r = rect
    kontrol1 =  max([w,h]) < W/4 # w in w/4 olması şartı
    kontrol2 = w*h > 200         # alanın 200 olma şartı
    
    if(kontrol1 and kontrol2):
        box = cv2.boxPoints(rect) #dikdörtgenin 4 noktasını bize verir.
        box = np.int64(box) # kordinat buçuklu olabilir tam sayıya çeviriyoruz.
        
        minx = np.min(box[:,0]) # 0 x eksenini ifade eder x  i gezer ve en küçüğünü bulur.
        miny = np.min(box[:,1]) # 1 y eksenini ifade eder y  yi gezer ve en küçüğünü bulur.
        maxx = np.max(box[:,0]) # 0 x eksenini ifade eder x  i gezer ve en büyüğü bulur.
        maxy = np.max(box[:,1]) # 1 y eksenini ifade eder y  yi gezer ve en büyüğü bulur.
        
        Fazlapx = 2 # karakteri tam yakalar 2 px geriden yakalamasını istiyoruz.
        
        minx = max(0 , minx - Fazlapx) # kesme işlemini eksi ile yapamayız.
        miny = max(0 , miny - Fazlapx)
        maxx = min(W , maxx + Fazlapx) # w demek resimdeki en yüksek px değeri demek var olmayanı kesemiyceğimiz için böyle dedik.
        maxy = min(H , maxy + Fazlapx)
        
        kesme = PlakaBGR[miny:maxy , minx:maxx].copy()
        
        try:
            cv2.imwrite(f"YakalananKarakterler/{PlakaResmi}_{i}.jpg",kesme) #klasöre ekleme
        except:
            pass
        
        yaz = PlakaBGR.copy()
        cv2.drawContours(yaz, [box], 0, (0,255,0) , 1)
        
        plt.imshow(yaz)
        plt.show()
"""

def plakaKarakterleri():
    try:
        countPlk=0
        count_kacPlk = os.listdir("Resimler/KaydedilenPlakalar")
        if len(count_kacPlk) == 0:
            countPlk=0
        else:
            countPlk=len(count_kacPlk)
        
        PlakaBGR = cv2.imread("Resimler/KaydedilenPlakalar/Plaka"+str(countPlk+1)+".jpg")
        #resim = cv2.imread("KaydedilenPlakalar/Plaka"+str(countPlk)+".jpg") # imread fonksiyonu belirtilen adresteki plakanın BGR değerlerini okuyucak.
        #PlakaBGR = cv2.resize(PlakaBGR, (500,500))
        
        
        
        #plakanın görüntüsündeki pixelleri 2 katına çıkartıyoruz çünkü yapmazsak plakadaki sayıların bulunmasında yanılgıya düşebiliriz.
        H,W = PlakaBGR.shape[:2] # Boyut bilgilerinden ilk 2 tanesini alır.
        H,W= H*2 , W*2

        PlakaBGR = cv2.resize(PlakaBGR , (W,H))

        #Plaka resmini Griye çeviriyoruz.
        GriPlaka = cv2.cvtColor(PlakaBGR , cv2.COLOR_BGR2GRAY)


        #GriPlaka =cv2.adaptiveThreshold(işlemeGiricek resim , eşiğin üstünde kalanlar kac px olsun , hangi tür eşikleme kullanıcaksın , Nasıl eşikleme yapılacak , filtre karesinin kaç boyutlu olcağı , komşu sayısı)
        EşiklenmişPlaka =cv2.adaptiveThreshold(GriPlaka , 255 , cv2.ADAPTIVE_THRESH_MEAN_C , cv2.THRESH_BINARY_INV , 11 , 2) #(1.1) Ayrıştırmanın ilk adımı eşiklemedir. adaptiveThreshold gelişmiş eşiklemedir.



        #Gürültüleri yokettik yani resimdeki pürüzleri sildik.
        kernel = np.ones((3,3), np.uint8)
        EşiklenmişPlaka = cv2.morphologyEx(EşiklenmişPlaka , cv2.MORPH_OPEN , kernel , iterations =1)


        counter = cv2.findContours(EşiklenmişPlaka, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #2. kısım hiyerarşiyi nasıl işleme alcağımızdır. son kısımda pixel pixel butun counterlermi gelsin yoksa x y w h değerlerimi gelsin bunu seçiyoruz. CHAIN_APPROX_SIMPLE ile konum konum döner.
        counter = counter[0] #counterler 2 değişken döndürür. 1.counterin konumununu döndürür[counter[0]]. 2. hiyerarşik yapıyı döndürür(counter[1]).

        #sorted(key=cv2.contourArea = alanlarına göre küçükten büyüğe sırala , ters çevir büyükten küçüğe olsun.)[:15]=ilk 15 değerin alınması için.
        counter = sorted(counter , key=cv2.contourArea, reverse=True)[:15] #istediğimiz counterler yani plakadaki karakterlerin olduğu counterler en büyük 10 yada 20 nin içindedir bu yüzden sıralıyoruz.
        
        os.mkdir("Resimler/YakalananKarakterler/Plaka"+str(countPlk+1))


        for i,c in enumerate(counter):
            rect=cv2.minAreaRect(c) # en küçük dikdörtgeni bana döndür demek. x , y ,Merkezin x y si ve rotuate açısı bulunur.
            (x,y) , (w,h) , r = rect
            kontrol1 =  max([w,h]) < W/4 # w in w/4 olması şartı
            kontrol2 = w*h > 200         # alanın 200 olma şartı
            
            if(kontrol1 and kontrol2):
                box = cv2.boxPoints(rect) #dikdörtgenin 4 noktasını bize verir.
                box = np.int64(box) # kordinat buçuklu olabilir tam sayıya çeviriyoruz.
                
                minx = np.min(box[:,0]) # 0 x eksenini ifade eder x  i gezer ve en küçüğünü bulur.
                miny = np.min(box[:,1]) # 1 y eksenini ifade eder y  yi gezer ve en küçüğünü bulur.
                maxx = np.max(box[:,0]) # 0 x eksenini ifade eder x  i gezer ve en büyüğü bulur.
                maxy = np.max(box[:,1]) # 1 y eksenini ifade eder y  yi gezer ve en büyüğü bulur.
                
                Fazlapx = 2 # karakteri tam yakalar 2 px geriden yakalamasını istiyoruz.
                
                minx = max(0 , minx - Fazlapx) # kesme işlemini eksi ile yapamayız.
                miny = max(0 , miny - Fazlapx)
                maxx = min(W , maxx + Fazlapx) # w demek resimdeki en yüksek px değeri demek var olmayanı kesemiyceğimiz için böyle dedik.
                maxy = min(H , maxy + Fazlapx)
                
                kesme = PlakaBGR[miny:maxy , minx:maxx].copy()
                
                try:
                    cv2.imwrite("Resimler/YakalananKarakterler/Plaka"+str(countPlk+1)+"/PlakaResmi_"+str(i)+".jpg",kesme) #klasöre ekleme
                except:
                    pass
                
                yaz = PlakaBGR.copy()
                cv2.drawContours(yaz, [box], 0, (0,255,0) , 1)
        adres="Resimler\YakalananKarakterler\Plaka"+str(countPlk+1)
        count_plkA = os.listdir("Resimler/YakalananKarakterler/Plaka"+str(countPlk+1))
        if len(count_plkA) <=5:
            PlakaBGR = cv2.imread("Resimler/KaydedilenPlakalar/Plaka"+str(countPlk+1)+".jpg")
            PlakaBGR = PlakaBGR[16:65, 21:210]
            shutil.rmtree(adres)
            
            countPlk=0
            count_kacPlk = os.listdir("Resimler/KaydedilenPlakalar")
            if len(count_kacPlk) == 0:
                countPlk=0
            else:
                countPlk=len(count_kacPlk)
            
            
            #resim = cv2.imread("KaydedilenPlakalar/Plaka"+str(countPlk)+".jpg") # imread fonksiyonu belirtilen adresteki plakanın BGR değerlerini okuyucak.
            #PlakaBGR = cv2.resize(PlakaBGR, (500,500))
            
            
            
            #plakanın görüntüsündeki pixelleri 2 katına çıkartıyoruz çünkü yapmazsak plakadaki sayıların bulunmasında yanılgıya düşebiliriz.
            H,W = PlakaBGR.shape[:2] # Boyut bilgilerinden ilk 2 tanesini alır.
            H,W= H*2 , W*2

            PlakaBGR = cv2.resize(PlakaBGR , (W,H))

            #Plaka resmini Griye çeviriyoruz.
            GriPlaka = cv2.cvtColor(PlakaBGR , cv2.COLOR_BGR2GRAY)


            #GriPlaka =cv2.adaptiveThreshold(işlemeGiricek resim , eşiğin üstünde kalanlar kac px olsun , hangi tür eşikleme kullanıcaksın , Nasıl eşikleme yapılacak , filtre karesinin kaç boyutlu olcağı , komşu sayısı)
            EşiklenmişPlaka =cv2.adaptiveThreshold(GriPlaka , 255 , cv2.ADAPTIVE_THRESH_MEAN_C , cv2.THRESH_BINARY_INV , 11 , 2) #(1.1) Ayrıştırmanın ilk adımı eşiklemedir. adaptiveThreshold gelişmiş eşiklemedir.



            #Gürültüleri yokettik yani resimdeki pürüzleri sildik.
            kernel = np.ones((3,3), np.uint8)
            EşiklenmişPlaka = cv2.morphologyEx(EşiklenmişPlaka , cv2.MORPH_OPEN , kernel , iterations =1)


            counter = cv2.findContours(EşiklenmişPlaka, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #2. kısım hiyerarşiyi nasıl işleme alcağımızdır. son kısımda pixel pixel butun counterlermi gelsin yoksa x y w h değerlerimi gelsin bunu seçiyoruz. CHAIN_APPROX_SIMPLE ile konum konum döner.
            counter = counter[0] #counterler 2 değişken döndürür. 1.counterin konumununu döndürür[counter[0]]. 2. hiyerarşik yapıyı döndürür(counter[1]).

            #sorted(key=cv2.contourArea = alanlarına göre küçükten büyüğe sırala , ters çevir büyükten küçüğe olsun.)[:15]=ilk 15 değerin alınması için.
            counter = sorted(counter , key=cv2.contourArea, reverse=True)[:15] #istediğimiz counterler yani plakadaki karakterlerin olduğu counterler en büyük 10 yada 20 nin içindedir bu yüzden sıralıyoruz.
            
            os.mkdir("Resimler/YakalananKarakterler/Plaka"+str(countPlk+1))


            for i,c in enumerate(counter):
                rect=cv2.minAreaRect(c) # en küçük dikdörtgeni bana döndür demek. x , y ,Merkezin x y si ve rotuate açısı bulunur.
                (x,y) , (w,h) , r = rect
                kontrol1 =  max([w,h]) < W/4 # w in w/4 olması şartı
                kontrol2 = w*h > 200         # alanın 200 olma şartı
                
                if(kontrol1 and kontrol2):
                    box = cv2.boxPoints(rect) #dikdörtgenin 4 noktasını bize verir.
                    box = np.int64(box) # kordinat buçuklu olabilir tam sayıya çeviriyoruz.
                    
                    minx = np.min(box[:,0]) # 0 x eksenini ifade eder x  i gezer ve en küçüğünü bulur.
                    miny = np.min(box[:,1]) # 1 y eksenini ifade eder y  yi gezer ve en küçüğünü bulur.
                    maxx = np.max(box[:,0]) # 0 x eksenini ifade eder x  i gezer ve en büyüğü bulur.
                    maxy = np.max(box[:,1]) # 1 y eksenini ifade eder y  yi gezer ve en büyüğü bulur.
                    
                    Fazlapx = 2 # karakteri tam yakalar 2 px geriden yakalamasını istiyoruz.
                    
                    minx = max(0 , minx - Fazlapx) # kesme işlemini eksi ile yapamayız.
                    miny = max(0 , miny - Fazlapx)
                    maxx = min(W , maxx + Fazlapx) # w demek resimdeki en yüksek px değeri demek var olmayanı kesemiyceğimiz için böyle dedik.
                    maxy = min(H , maxy + Fazlapx)
                    
                    kesme = PlakaBGR[miny:maxy , minx:maxx].copy()
                    
                    try:
                        cv2.imwrite("Resimler/YakalananKarakterler/Plaka"+str(countPlk+1)+"/PlakaResmi_"+str(i)+".jpg",kesme) #klasöre ekleme
                    except:
                        pass
                    
                    yaz = PlakaBGR.copy()
                    cv2.drawContours(yaz, [box], 0, (0,255,0) , 1)
            count_plkA = os.listdir("Resimler/KaydedilenPlakalar")
            os.startfile(adres)
        else:
            os.startfile(adres)
    except Exception as e:
        print(e)
        messagebox.showerror("Hata",e)
            