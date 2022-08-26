import os # Diske bağlanılıcak ve plakaların URL'leri alınacak.
import matplotlib.pyplot as plt # Verileri görselleştirme ve grafik oluşturmada yarıyor.
import cv2 # Bilgisayar görüşü kütüphanesidir.
from Plaka_Tespit import plakaKonumBul

"""
veri = os.listdir("Plakalar") # Plakalar klasöründeki arabaların ADRESLERİNİ okur.
yenisi= veri.sort
for resim_adresi in veri:
    resim = cv2.imread("Plakalar/"+resim_adresi) # imread fonksiyonu belirtilen adresteki plakanın BGR değerlerini okuyucak.
    
    resim = cv2.resize(resim, (500,500))
    plaka=plakaKonumBul(resim) # x , y , w , h değerleri gelir.
    x,y,w,h = plaka
    if(w>h): # fonksiyonda bazen w ve h yerleri karışabiliyo bunu bir ifle kontrol ediyoruz.
        PlakaBGR = resim[y:y+h , x:x+w].copy()
    else:
        PlakaBGR = resim[y:y+w , x:x+h].copy()
    resim = cv2.cvtColor(PlakaBGR, cv2.COLOR_BGR2RGB) # Resimleri RGB değerine dönüştürdük.
    plt.imshow(resim) # Resimi ekranda göstermek içindir.
    plt.show()
"""

def PlakaResimBul(resim):
    resim = cv2.resize(resim, (500,500))
    plaka=plakaKonumBul(resim)
    x,y,w,h = plaka
    if(w>h):
        PlakaBGR = resim[y:y+h , x:x+w].copy()
    else:
        PlakaBGR = resim[y:y+w , x:x+h].copy()
    sonResim = cv2.cvtColor(PlakaBGR, cv2.COLOR_BGR2RGB)
    
    count=0
    count_kac = os.listdir("Resimler/KaydedilenPlakalar")
    if len(count_kac) == 0:
        count=0
    else:
        count=len(count_kac)
    
    cv2.imwrite("Resimler/KaydedilenPlakalar/Plaka"+str(count+2)+".jpg", sonResim)
    