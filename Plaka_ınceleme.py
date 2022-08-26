import os # Diske bağlanılıcak ve plakaların URL'leri alınacak.
import matplotlib.pyplot as plt # Verileri görselleştirme ve grafik oluşturmada yarıyor.
import cv2 # Bilgisayar görüşü kütüphanesidir.

veri = os.listdir("Resimler/Plakalar") # Plakalar klasöründeki arabaların ADRESLERİNİ okur.

for resim_adresi in veri:
    resim = cv2.imread("Resimler/Plakalar/"+resim_adresi) # imread fonksiyonu belirtilen adresteki plakanın BGR değerlerini okuyucak.
    resim = cv2.cvtColor(resim, cv2.COLOR_BGR2RGB) # Resimleri RGB değerine dönüştürdük.
    resim = cv2.resize(resim, (500,500))
    plt.imshow(resim) # Resimi ekranda göstermek içindir.
    plt.show()
    