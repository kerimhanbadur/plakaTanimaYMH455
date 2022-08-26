import pytesseract
import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
import imutils
import easyocr
import io
import json
import requests
import re
from PIL import Image
import pandas as pd



"""
def cevir(adres):
    pytesseract.pytesseract.tesseract_cmd="C:\\Users\\Enforsec\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
    image=cv2.imread("KaydedilenPlakalar/Plaka" + str(adres)+".jpg")
    Plaka_str=pytesseract.image_to_string(image)
    res_txt=''
    for karakter in Plaka_str:
        if karakter.isalnum():
            res_txt+=karakter
    return res_txt


def cevirTest(adres):
    pytesseract.pytesseract.tesseract_cmd="C:\\Users\\Enforsec\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
    #image=cv2.imread(str(adres)+".jpg")
    Plaka_str=pytesseract.image_to_string(adres)
    res_txt=''
    for karakter in Plaka_str:
        if karakter.isalnum():
            res_txt+=karakter
    return res_txt"""








#image=cv2.imread("Plaka4.jpg")
#image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

"""
img = cv2.imread('Plaka4.jpg',0)

H,W = img.shape[:2] # Boyut bilgilerinden ilk 2 tanesini alır.
H,W= H*2 , W*2

img = cv2.resize(img , (W,H))

ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
thresh2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY,11,2)
thresh3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY,11,2)

plt.subplot(221), plt.imshow(img,'gray')
plt.title('Original Image')
plt.subplot(222), plt.imshow(thresh1, 'gray')
plt.title('THRESH_BINARY')
plt.subplot(223), plt.imshow(thresh2, 'gray')
plt.title('ADAPTIVE_THRESH_MEAN_C')
plt.subplot(224), plt.imshow(thresh3, 'gray')
plt.title('ADAPTIVE_THRESH_GAUSSIAN_C')

plt.show()




reader=easyocr.Reader(['en'], gpu=False)

result =reader.readtext(img)
print(result)

result =reader.readtext(thresh1)
print(result)

result =reader.readtext(thresh2)
print(result)

result =reader.readtext(thresh3)
print(result)



class Image:
    def __init__(self, image):
        self.image_name = image
        self.image = cv2.imread(image)
        self.height, self.width = (self.image.shape[0], self.image.shape[1])
        self.default_sizes = self.height, self.width

    def update_size(self):
        self.height, self.width = (self.image.shape[0], self.image.shape[1])

    def return_to_default(self):
        self.image = cv2.imread(self.image_name)
        self.height, self.width = self.default_sizes

    def resize(self, scale_percent):
        self.width = int(self.width * scale_percent / 100)
        self.height = int(self.height * scale_percent / 100)
        self.image = cv2.resize(self.image, (self.width, self.height))

    def show(self, title):
        cv2.imshow(title, self.image)
        cv2.waitKey(0)

    def convert_to_grayscale(self):
        for y in range(self.height):
            for x in range(self.width):
                b, g, r = self.image[y, x]
                s = sum((b, g, r)) // 3
                b, g, r = s, s, s
                self.image[y, x] = b, g, r
    def save(self, title):
        cv2.imwrite(title, self.image)
        
    def netlestir(self):
        for y in range(self.height):
            for x in range(self.width):
                try:
                    b, g, r = self.image[y, x]
                    if b <= 125 and g <= 125 and r <= 125:
                        self.image[y, x] = (0, 0, 0)
                except IndexError:
                    continue



img=Image("Plaka0.jpg")
img.show("sayfa")
img.convert_to_grayscale()
img.save("afterGray.jpg")
img.show("siyahbeyaz")
img.netlestir()
img.show("netlestirilmis")
img.save("afterNet.jpg")

print(cevirTest("afterGray"))
"""


"""
pytesseract.pytesseract.tesseract_cmd="C:\\Users\\Enforsec\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
roi=cv2.imread('KaydedilenPlakalar/Plaka11.jpg')
roi=cv2.resize(roi,None,fx=0.5,fy=0.5)
gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)

a_t=cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101,37)
config="--psm 7"
text=pytesseract.image_to_string(a_t, config=config)
print(text)

plt.title("Gri Format")
plt.imshow(gray , cmap="gray") # Plaka gösterir.
plt.show()

plt.title("Gri Format")
plt.imshow(a_t , cmap="gray") # Plaka gösterir.
plt.show()"""

"""
    
im1 = Image.open('beyaz.jpg')
im2 = Image.open('KaydedilenPlakalar/Plaka25.jpg')
im2=im2.resize((300,75))
back_im = im1.copy()
back_im.paste(im2, (100, 50))"""





"""
def cevirSon(adres):
    roi=cv2.imread('KaydedilenPlakalar/Plaka'+str(adres)+'.jpg')

    #H,W = roi.shape[:2] 
    #H,W= H*2 , W*2
    #roi = cv2.resize(roi , (W,H))

    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".jpg", roi, [1, 90])
    file_bytes = io.BytesIO(compressedimage)

    result = requests.post(url_api,
                  files = {"Plaka"+str(adres)+".jpg": file_bytes},
                  data = {"apikey": "K86965517388957",
                          "language": "tur"})

    result = result.content.decode()
    result = json.loads(result)

    parsed_results = result.get("ParsedResults")[0]
    text_detected = parsed_results.get("ParsedText")
    return text_detected

"""
def cevirSon(adres):
    liste=[]
    
    roi=cv2.imread('Resimler/KaydedilenPlakalar/Plaka'+str(adres)+'.jpg')
    """
    im1 = Image.open('beyaz.jpg')
    im2 = Image.open('KaydedilenPlakalar/Plaka'+str(adres)+'.jpg')
    im2=im2.resize((300,75))
    back_im = im1.copy()
    back_im.paste(im2, (100, 50))
    opencvImage = cv2.cvtColor(np.array(back_im), cv2.COLOR_RGB2BGR)
    ret, thresh = cv2.threshold(opencvImage, 120, 255, cv2.THRESH_TOZERO)"""
    
    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".jpg", roi, [1, 90])
    file_bytes = io.BytesIO(compressedimage)

    result = requests.post(url_api,
                  files = {"Resimler/Plaka"+str(adres)+".jpg": file_bytes},
                  data = {"apikey": "K86965517388957",
                          "language": "tur"})

    result = result.content.decode()
    result = json.loads(result)

    parsed_results = result.get("ParsedResults")[0]
    text_detected = parsed_results.get("ParsedText")
    liste.append(text_detected)
    
    


    #pytesseract.pytesseract.tesseract_cmd="C:\\Users\\Enforsec\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd="Tesseract-OCR/tesseract.exe"
    Plaka_str=pytesseract.image_to_string(roi)
    res_txt=''
    for karakter in Plaka_str:
        if karakter.isalnum():
            res_txt+=karakter
    
    liste.append(res_txt)
    
    
    reader=easyocr.Reader(['en'], gpu=False)
    resultt =reader.readtext(roi, detail=0)
    liste.append(resultt)
    


    for i in range(len(liste)):
        geçici=str(liste[i])
        a="'"
        geçici=geçici.replace('\r', '')
        geçici=geçici.replace('\n', '')
        geçici=geçici.replace('!', '')
        geçici=geçici.replace('.', '')
        geçici=geçici.replace('/', '')
        geçici=geçici.replace(a, '')
        geçici=geçici.replace('[', '')
        geçici=geçici.replace(']', '')
        geçici=geçici.replace('(', '')
        geçici=geçici.replace(')', '')
        geçici=geçici.replace(',', '')
        geçici=geçici.replace('*', '')
        geçici=geçici.replace('-', '')
        geçici=geçici.replace('_', '')
        liste[i]=geçici
    
    
    en_uzun = sorted(liste, key=lambda x: len(x), reverse=True)[0]
    for i in range(len(liste)):
        geçici=str(liste[i])
        sayı=0
        if(re.search(r'\b\d{2}.{0,1}[^\d\W]{0,1}.{0,1}\b\d{4,5}\b', geçici)):
            continue
        else:
            sayı=sayı+1
            
            
        if(re.search(r'\b\d{2}.{0,1}[^\d\W]{0,1}.{0,1}\b[^\d\W]{0,1}.{0,1}\b\d{3,4}\b', geçici)):
            continue
        else:
            sayı=sayı+1
            
            
        if(re.search(r'\b\d{2}.{0,1}[^\d\W]{0,1}.{0,1}\b[^\d\W]{0,1}.{0,1}\w{0,1}.{0,1}\b\d{2,3}\b', geçici)):
            continue
        else:
            sayı=sayı+1
            
            
        if sayı==3:
            liste[i]=""
        else:
            continue
            
    a=0
    for i in range(len(liste)):
        if liste[i]=="":
            a=a+1
            pass
        else:
            return str(liste[i])
    
    if a==3:
        return str(en_uzun)
    
"""
TEMPLATES = [
r'\b\d{2}.{0,1}[^\d\W]{0,1}.{0,1}\b\d{4,5}\b', #99 X 9999, 99 X 99999
r'\b\d{2}.{0,1}[^\d\W]{0,1}.{0,1}\b[^\d\W]{0,1}.{0,1}\b\d{3,4}\b', #99 XX 999, 99 XX 9999
r'\b\d{2}.{0,1}[^\d\W]{0,1}.{0,1}\b[^\d\W]{0,1}.{0,1}\w{0,1}.{0,1}\b\d{2,3}\b' #99 XXX 99, 99 XXX 999
]

bir=r'\b\d{2}.{0,1}[^\d\W]{0,1}.{0,1}\b\d{4,5}\b'
iki=r'\b\d{2}.{0,1}[^\d\W]{0,1}.{0,1}\b[^\d\W]{0,1}.{0,1}\b\d{3,4}\b'
uc=r'\b\d{2}.{0,1}[^\d\W]{0,1}.{0,1}\b[^\d\W]{0,1}.{0,1}\w{0,1}.{0,1}\b\d{2,3}\b'

plakaaa="B41BT996"

if(re.search(bir, plakaaa)):
    print(plakaaa)
else:
    print("Hatalı")
    
if(re.search(iki, plakaaa)):
    print(plakaaa)
else:
    print("Hatalı")

if(re.search(uc, plakaaa)):
    print(plakaaa)
else:
    print("Hatalı")
"""
    




"""
liste=[0,1,2,3,4,5,6]
print(liste)
del liste[5]
print(liste)"""
