import os # Resimlerin adreslerinin alınması için.
import cv2 # Görüntü işleme kütüphanesidir.
import matplotlib.pyplot as plt # Resimleri görselleştirme ve incelemek için gereklidir.
import numpy as np # Liste işlemlerini kolay yapmamızı sağlar.

"""

RsmAdres = os.listdir("Plakalar") # Plakalar klasöründeki arabaların ADRESLERİNİ okur.

resim = cv2.imread("Plakalar/" + RsmAdres[2]) #RsmAdres deki sıfırıncı resmi çağırdık.
resim = cv2.resize(resim,(500,500)) #Seçilen resmi 500x500 olarak yeniden boyutlandırdık.

plt.imshow(cv2.cvtColor(resim,cv2.COLOR_BGR2RGB)) # Resimleri RGB değerine dönüştürdük.
plt.show()

#Resmi 2 formatta inceliycez biri BGR diğeri ise GRİ format.
resim_bgr = resim
resim_gri = cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)

# Gri resmimizi ekranda gösterme
plt.imshow(resim_gri , cmap="gray")
plt.show()

# Kenar tespiti yapabilmek için  medyan bulanıklaştırma işlemi gerçekleştirilicek. 
#(Plakanın siyah kenarlarını belirginleştirme)

mb_resim = cv2.medianBlur(resim_gri , 5) # Buradaki 5 plakanın siyah çizgisinin pixelinden dolayı verildi 5x5 bulanıklaştırma işlemi yapıcaz.
mb_resim = cv2.medianBlur(mb_resim , 5) # plaka iyice belli olsun diye işlemi 2 kere yapıyoruz.


plt.imshow(mb_resim , cmap="gray") # Blurlama resmimizi ekranda gösterme
plt.show()

medyan = np.median(mb_resim) # Yoğunluk merkezi hesaplamak için resmin medyanını hesaplıyoruz.

# Yoğunluk merkezimizin 2/3 alt yoğunluk merkezi, 3/4 ise üst yoğunluk merkezimizdir.

alt = 0.67*medyan
üst = 1.33*medyan

# Yukarıdaki yoğunluk merkezlerini kullanarak kenarlık tespiti yapmamız gerek.

kenar = cv2.Canny(mb_resim , alt , üst) #cv2.Canny() = john f Canny algoritmasıdır. alt ve üste göre plakanın kenarlarını çıkartır.

plt.imshow(kenar , cmap="gray") # Kenarları çıkartılmış resim.
plt.show()


#Plaka Tespit Algoritması
# kenar tespitinden sonra plakanın daha anlaşılır olması için genişletme işlemi yapmamız gereklidir.
Gkenar = cv2.dilate(kenar , np.ones((3,3) , np.uint8) , iterations = 1) #np.ones()= genişletme için bir filtre 3x3 matris içi onesden dolayı 1 olucak , iterations ise tekrar sayısıdır.

plt.imshow(Gkenar , cmap="gray") #kenar tespiti resim.
plt.show()


#counter bulma işlemi yapıcaz aynı pixel değerine sahip değerleri bulma işlemi yani.

counter = cv2.findContours(Gkenar , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE) #cv2.RETR_TREE = hiyerarşik yapıda olsun demek yani plaka ebeveyin içindeki sayılar çocuk olucak şekilde. cv2.CHAIN_APPROX_SIMPLE ise bütün pixellerin konumlarını almak yerine dikdörtgenimsi olarak tam plakanın köşelerini aldık.
counter = counter[0] #counterin merkezlerine ihtiyacımız var.  
#Bu işlemden sonra resimde plakada dahil birçok dikdörtgen olabilir counter değişkeninin içnide bu yüzden sıralama yapıyoruz.           
counter = sorted(counter , key=cv2.contourArea , reverse=True) #key=cv2.contourArea mevcut counterlerin alanına göre sıralama yapmamızı sağlar.

H , W = 500 , 500 # yükseklik ve genişlik değerlerimiz 500 en üstte resimleri 500x500 ayarlamıştık.
Plaka = None #plakanın konumu.

#for döngüsü counterlerin içindeki dikdörtgenleri dolaşıcak ve 
for i in counter:
    #BİR algoritmanın 1. kuralı dikdörtgenleri belirlemek.
    rect = cv2.minAreaRect(i) # x y w h ve r değerlerini döndürür counterin içindeki dikdörtgenlerin.
    (x , y) , (w , h) , r = rect # x ve y dikdörtgenin merkez kordinatlarıdır.w ve h genişlik ve yükseklik değerleri gönderir. r ise rotate yani dönme açısıdır.
    
    #İKİ algoritmanın 2. kuralı oran h ve w arası minimum oranın 2 olması kuralı.
    if(w > h and w > h*2) or (h > w and h > w*2):
        köşeler = cv2.boxPoints(rect) # plakanın 4 köşesinin kordinatlarının bulunduğu bir liste döndürür.
        köşeler = np.int64(köşeler)
        
        minx = np.min(köşeler[:,0]) #yukarıdaki boxPoints kodunda 4 tane (x,y) dönücek buradaki kodla 4 ündede x değerlerini alıyoruz.
        miny = np.min(köşeler[:,1]) #yukarıdaki boxPoints kodunda 4 tane (x,y) dönücek buradaki kodla 4 ündede y değerlerini alıyoruz.
        maxx = np.max(köşeler[:,0])
        maxy = np.max(köşeler[:,1])
        
        tahminiPlaka = resim_gri[miny:maxy , minx:maxx].copy() #Tahmini plakadan miny den maxy ve minx den maxx e kestik.
        tahminiPlakaMedyan = np.median(tahminiPlaka)
        
        #ÜÇ renk değer ortalaması yani medyanı 85 ve 200 arası olmalı.
        kontrol1 = tahminiPlakaMedyan > 85 and tahminiPlakaMedyan < 200
        #DÖRT boyut sınırlaması
        kontrol2 = h < 50 and w < 150
        
        kontrol3 = w < 50 and h < 150
        
        plt.figure()
        kontrol=False # plakanın tespit edilip edilmemesini gösterir.
        if(kontrol1 and (kontrol2 or kontrol3)):# kontrol 1 kesin doğru olmalı kontrol 2 veya kontrol 3 arasından birinin doğru olması yeterlidir.
            #plaka
            cv2.drawContours(resim, [köşeler] , 0 , (0 , 255 , 0) , 2) # resmi belirtilen köşelere göre çizdirir.
            Plaka = [int(i) for i in [minx , miny , w , h]]
            
            plt.title("Plaka tespit edildi.")
            kontrol = True # plaka tespit edildi.
        else:
            #plaka değil.
            cv2.drawContours(resim, [köşeler] , 0 , (0 , 0 , 255) , 2)
            plt.title("Plaka tespit edilemedi.")
        
        plt.imshow(cv2.cvtColor(resim , cv2.COLOR_BGR2RGB))
        plt.show()
        
        if(kontrol):
            break
"""

#yukarıdaki kodu metotlaştırıyoruz.
def plakaKonumBul(resim):
    #Resmi 2 formatta inceliycez biri BGR diğeri ise GRİ format.
    resim_bgr = resim
    resim_gri = cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)
    
    # Kenar tespiti yapabilmek için  medyan bulanıklaştırma işlemi gerçekleştirilicek. 
    #(Plakanın siyah kenarlarını belirginleştirme)

    mb_resim = cv2.medianBlur(resim_gri , 5) # Buradaki 5 plakanın siyah çizgisinin pixelinden dolayı verildi 5x5 bulanıklaştırma işlemi yapıcaz.
    mb_resim = cv2.medianBlur(mb_resim , 5) # plaka iyice belli olsun diye işlemi 2 kere yapıyoruz.

    medyan = np.median(mb_resim) # Yoğunluk merkezi hesaplamak için resmin medyanını hesaplıyoruz.

    # Yoğunluk merkezimizin 2/3 alt yoğunluk merkezi, 3/4 ise üst yoğunluk merkezimizdir.

    alt = 0.67*medyan
    üst = 1.33*medyan

    # Yukarıdaki yoğunluk merkezlerini kullanarak kenarlık tespiti yapmamız gerek.

    kenar = cv2.Canny(mb_resim , alt , üst) #cv2.Canny() = john f Canny algoritmasıdır. alt ve üste göre plakanın kenarlarını çıkartır.


    #Plaka Tespit Algoritması
    # kenar tespitinden sonra plakanın daha anlaşılır olması için genişletme işlemi yapmamız gereklidir.
    Gkenar = cv2.dilate(kenar , np.ones((3,3) , np.uint8) , iterations = 1) #np.ones()= genişletme için bir filtre 3x3 matris içi onesden dolayı 1 olucak , iterations ise tekrar sayısıdır.


    #counter bulma işlemi yapıcaz aynı pixel değerine sahip değerleri bulma işlemi yani.

    counter = cv2.findContours(Gkenar , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE) #cv2.RETR_TREE = hiyerarşik yapıda olsun demek yani plaka ebeveyin içindeki sayılar çocuk olucak şekilde. cv2.CHAIN_APPROX_SIMPLE ise bütün pixellerin konumlarını almak yerine dikdörtgenimsi olarak tam plakanın köşelerini aldık.
    counter = counter[0] #counterin merkezlerine ihtiyacımız var.  
    #Bu işlemden sonra resimde plakada dahil birçok dikdörtgen olabilir counter değişkeninin içnide bu yüzden sıralama yapıyoruz.           
    counter = sorted(counter , key=cv2.contourArea , reverse=True) #key=cv2.contourArea mevcut counterlerin alanına göre sıralama yapmamızı sağlar.

    H , W = 500 , 500 # yükseklik ve genişlik değerlerimiz 500 en üstte resimleri 500x500 ayarlamıştık.
    Plaka = None #plakanın konumu.

    #for döngüsü counterlerin içindeki dikdörtgenleri dolaşıcak ve 
    for i in counter:
        #BİR algoritmanın 1. kuralı dikdörtgenleri belirlemek.
        rect = cv2.minAreaRect(i) # x y w h ve r değerlerini döndürür counterin içindeki dikdörtgenlerin.
        (x , y) , (w , h) , r = rect # x ve y dikdörtgenin merkez kordinatlarıdır.w ve h genişlik ve yükseklik değerleri gönderir. r ise rotate yani dönme açısıdır.
        
        #İKİ algoritmanın 2. kuralı oran h ve w arası minimum oranın 2 olması kuralı.
        if(w > h and w > h*2) or (h > w and h > w*2):
            köşeler = cv2.boxPoints(rect) # plakanın 4 köşesinin kordinatlarının bulunduğu bir liste döndürür.
            köşeler = np.int64(köşeler)
            
            minx = np.min(köşeler[:,0]) #yukarıdaki boxPoints kodunda 4 tane (x,y) dönücek buradaki kodla 4 ündede x değerlerini alıyoruz.
            miny = np.min(köşeler[:,1]) #yukarıdaki boxPoints kodunda 4 tane (x,y) dönücek buradaki kodla 4 ündede y değerlerini alıyoruz.
            maxx = np.max(köşeler[:,0])
            maxy = np.max(köşeler[:,1])
            
            tahminiPlaka = resim_gri[miny:maxy , minx:maxx].copy() #Tahmini plakadan miny den maxy ve minx den maxx e kestik.
            tahminiPlakaMedyan = np.median(tahminiPlaka)
            
            #ÜÇ renk değer ortalaması yani medyanı 85 ve 200 arası olmalı.
            kontrol1 = tahminiPlakaMedyan > 85 and tahminiPlakaMedyan < 200
            #DÖRT boyut sınırlaması
            kontrol2 = h < 50 and w < 150
            
            kontrol3 = w < 50 and h < 150
            
            kontrol=False # plakanın tespit edilip edilmemesini gösterir.
            if(kontrol1 and (kontrol2 or kontrol3)):# kontrol 1 kesin doğru olmalı kontrol 2 veya kontrol 3 arasından birinin doğru olması yeterlidir.
                #plaka
                cv2.drawContours(resim, [köşeler] , 0 , (0 , 255 , 0) , 2) # resmi belirtilen köşelere göre çizdirir.
                Plaka = [int(i) for i in [minx , miny , w , h]]
                
                kontrol = True # plaka tespit edildi.
            else:
                #plaka değil.
                cv2.drawContours(resim, [köşeler] , 0 , (0 , 0 , 255) , 2)
            
            if(kontrol):
                return Plaka
    return []
