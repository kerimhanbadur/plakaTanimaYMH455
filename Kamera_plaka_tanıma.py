import cv2

"""
PlakaData = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml") #Plaka bulmak için önceden eğitilmiş bir model.
Kamera = cv2.VideoCapture(0)
MinAlan=500
count = 0
dongu=True
while dongu:
    başarılı , resim = Kamera.read()
    ResimGri = cv2.cvtColor(resim , cv2.COLOR_BGR2BGRA)
    PlakaNo= PlakaData.detectMultiScale(ResimGri , 1.1 , 4)
    
    for(x , y , w , h) in PlakaNo:
        alan = w*h
        if alan > MinAlan:
            cv2.rectangle(resim, (x,y), (x+w , y+h), (255,0,0),2)  #Plakayı dikdörtgene alıyoruz.
            cv2.putText(resim, "PLAKA", (x,y-5), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255),2) # Tespit edilen plakanın üstüne yazı koyuyoruz.
            resimROİ = resim[y:y+h,x:x+w]   # ilgi bölgemizi tanımlıyoruz.
            cv2.imshow("ROİ",resimROİ)      # ilgi bölgemizi gösteriyoruz.
    
    cv2.imshow("SONUC", resim)
    if cv2.waitKey(1) & 0xFF == ord('s'): # s ye basarsak algılanan plaka kaydedilir.
        cv2.imwrite("KaydedilenPlakalar/Plaka"+str(count)+".jpg", resimROİ)
        cv2.rectangle(resim, (0,200), (640,300), (255,0,0),cv2.FILLED)  
        cv2.putText(resim, "KAYDEDILDI", (15,265), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,255),2) #kaydettikten sonra ekranda KAYDEDİLDİ görülücektir.
        cv2.imshow("SONUC", resim)
        cv2.waitKey(500)
        count = count + 1
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        Kamera.release()
        cv2.destroyAllWindows()
        
     """   

def Kamera_Ac():
    PlakaData = cv2.CascadeClassifier("PlakaModel.xml") #Plaka bulmak için önceden eğitilmiş bir model.
    Kamera = cv2.VideoCapture(0)
    MinAlan=500
    global kontrol
    kontrol=False
    global count
    count=0
    dongu=True
    while dongu:
        başarılı , resim = Kamera.read()
        ResimGri = cv2.cvtColor(resim , cv2.COLOR_BGR2BGRA)
        PlakaNo= PlakaData.detectMultiScale(ResimGri , 1.1 , 4)
        
        for(x , y , w , h) in PlakaNo:
            alan = w*h
            if alan > MinAlan:
                cv2.rectangle(resim, (x,y), (x+w , y+h), (255,0,0),2)  #Plakayı dikdörtgene alıyoruz.
                cv2.putText(resim, "PLAKA", (x,y-5), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255),2) # Tespit edilen plakanın üstüne yazı koyuyoruz.
                resimROİ = resim[y:y+h,x:x+w]   # ilgi bölgemizi tanımlıyoruz.
                cv2.imshow("ROİ",resimROİ)      # ilgi bölgemizi gösteriyoruz.
        
        cv2.imshow("SONUC", resim)
        if cv2.waitKey(1) & 0xFF == ord('s'): # s ye basarsak algılanan plaka kaydedilir.
            cv2.imwrite("Resimler/KaydedilenPlakalar/Plaka"+str(count)+".jpg", resimROİ)
            cv2.rectangle(resim, (0,200), (640,300), (255,0,0),cv2.FILLED)  
            cv2.putText(resim, "KAYDEDILDI", (15,265), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,255),2) #kaydettikten sonra ekranda KAYDEDİLDİ görülücektir.
            cv2.imshow("SONUC", resim)
            cv2.waitKey(500)
            count = count + 1
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            Kamera.release()
            cv2.destroyAllWindows()

def Kamera_Plaka_adres():
    return "Resimler/KaydedilenPlakalar/Plaka" + str(count) + ".jpg"
 