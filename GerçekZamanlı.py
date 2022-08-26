from tkinter import *
from tkinter import ttk
import tkinter as tk
import PIL as p
import PIL.ImageTk as ptk
import PIL.Image as pı
import cv2
import pytesseract
import numpy as np
import os
import matplotlib.pyplot as plt
from tkinter import filedialog
import pyodbc
from tkinter import messagebox
import datetime
import time



def Kamera_Ac_Gercek():
    try:
        os.startfile("Resimler\KaydedilenPlakalarGercek")
    except:
        os.startfile("Resimler/KaydedilenPlakalarGercek")
    print("1")
    global x
    x=1
    PlakaData = cv2.CascadeClassifier("PlakaModel.xml") #Plaka bulmak için önceden eğitilmiş bir model.
    Kamera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    MinAlan=500
    global kontrol
    kontrol=False
    global count
    dongu=True
    deneme=0
    
    while dongu:
        try:
            count_kac = os.listdir("Resimler/KaydedilenPlakalarGercek")
        except:
            count_kac = os.listdir("Resimler\KaydedilenPlakalarGercek")  
        if len(count_kac) == 0:
            count=0
        else:
            count=len(count_kac)
        deneme=deneme+1
        resimROİ=""
        başarılı , resim = Kamera.read()
        ResimGri = cv2.cvtColor(resim , cv2.COLOR_BGR2BGRA)
        PlakaNo= PlakaData.detectMultiScale(ResimGri , 1.1 , 4)
        if deneme== 50:
            deneme=0
        for(x , y , w , h) in PlakaNo:
            alan = w*h
            if alan > MinAlan:
                cv2.rectangle(resim, (x,y), (x+w , y+h), (255,0,0),2)  #Plakayı dikdörtgene alıyoruz.
                cv2.putText(resim, "PLAKA", (x,y-5), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255),2) # Tespit edilen plakanın üstüne yazı koyuyoruz.
                resimROİ = resim[y:y+h,x:x+w].copy()   # ilgi bölgemizi tanımlıyoruz.
                #cv2.imshow("ROİ",resimROİ)      # ilgi bölgemizi gösteriyoruz.
        cv2.imshow("SONUC", resim)
        if deneme >35:
            if str(resimROİ) != "":
                try:
                    cv2.imwrite("Resimler/KaydedilenPlakalarGercek/Plaka"+str(count+2)+".jpg", resimROİ)
                except:
                    cv2.imwrite("Resimler\KaydedilenPlakalarGercek\Plaka"+str(count+2)+".jpg", resimROİ) 
                deneme=0
        if cv2.waitKey(1) & 0xFF == ord('q'):
            Kamera.release()
            cv2.destroyAllWindows()
            break
