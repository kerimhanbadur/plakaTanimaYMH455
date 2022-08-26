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
from Plaka_Yazıya_Çevir import cevirSon
from tkinter import filedialog
from KarakterTanıma import PlakaResimBul
from Plaka_ayrıştırma import plakaKarakterleri
from GerçekZamanlı import Kamera_Ac_Gercek
import pyodbc
from tkinter import messagebox
import datetime


"""
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
"""


global x
x=0
arayüz = Tk()
arayüz.title("Plaka Tanıma Sistemi")
arayüz.iconbitmap(r'Resimler/icon.ico')
width= arayüz.winfo_screenwidth()
height= arayüz.winfo_screenheight()
#setting tkinter window size
arayüz.geometry("%dx%d" % (width, height))
arayüz.state('zoomed') 

canvas = Canvas(arayüz , height=600, width=1400, bg='#EBDDE2') #boyutları verilir.
canvas.pack()

frame_başlık= Frame(arayüz , bg='#FA1805',highlightthickness=2, highlightbackground="black")
frame_başlık.place(relx=0.01, rely=0.08, relwidth=0.98, relheight=0.1)

frame_kamera= Frame(arayüz , bg='#3BB9FF',highlightthickness=2, highlightbackground="black")
frame_kamera.place(relx=0.01, rely=0.19, relwidth=0.24, relheight=0.78)

frame_foto= Frame(arayüz , bg='#3BB9FF',highlightthickness=2, highlightbackground="black")
frame_foto.place(relx=0.26, rely=0.19, relwidth=0.27, relheight=0.78)

frame_vt= Frame(arayüz , bg='#3BB9FF',highlightthickness=2, highlightbackground="black")
frame_vt.place(relx=0.54, rely=0.19, relwidth=0.45, relheight=0.78)

vt_ad_lbl = Label(frame_vt, bg='#3BB9FF', text="Ad Soyad: ", font="Verdana 10 bold")
vt_ad_lbl.place(relx=0.02, rely=0.02)


    
r=IntVar()
r.set("1")
global kac
kac=1
def radionn(deger):
    global kac
    if deger == 1:
        kac=1
    elif deger == 2:
        kac=2

Radiobutton1=Radiobutton(frame_vt, text='Ad', value=1,variable=r ,bg='#3BB9FF', font="Verdana 8 bold", command=lambda: radionn(r.get()))
Radiobutton1.place(relx=0.69, rely=0.15, relwidth=0.10, relheight=0.03)
Radiobutton2=Radiobutton(frame_vt, text='Plaka', value=2,variable=r, bg='#3BB9FF', font="Verdana 8 bold", command=lambda: radionn(r.get()))
Radiobutton2.place(relx=0.77, rely=0.15, relwidth=0.10, relheight=0.03)

global vt_ad
vt_ad=StringVar()
global vt_ad_txt
vt_ad_txt=Entry(frame_vt, width=20, textvariable=vt_ad)
vt_ad_txt.place(relx=0.16, rely=0.02)

vt_tel_lbl = Label(frame_vt, bg='#3BB9FF', text="Telefon: ", font="Verdana 10 bold")
vt_tel_lbl.place(relx=0.02, rely=0.08)

global vt_tel
vt_tel=StringVar()
global vt_tel_txt
vt_tel_txt=Entry(frame_vt, width=20, textvariable=vt_tel)
vt_tel_txt.place(relx=0.16, rely=0.08)

vt_plk_lbl = Label(frame_vt, bg='#3BB9FF', text="Plaka: ", font="Verdana 10 bold")
vt_plk_lbl.place(relx=0.02, rely=0.14)

global vt_plk
vt_plk=StringVar()
global vt_plk_txt
vt_plk_txt=Entry(frame_vt, width=20, textvariable=vt_plk)
vt_plk_txt.place(relx=0.16, rely=0.14)

vt_giris_lbl = Label(frame_vt, bg='#3BB9FF', text="Giriş Zamanı: ", font="Verdana 10 bold")
vt_giris_lbl.place(relx=0.40, rely=0.02)

global vt_girisDeger
vt_girisDeger=StringVar()
global vt_girisDeger_lbl
vt_girisDeger_lbl = Label(frame_vt, bg='#3BB9FF', textvariable=vt_girisDeger, font="Verdana 10 bold")
vt_girisDeger_lbl.place(relx=0.56, rely=0.02)

global vt_no
vt_no=IntVar()
global vt_no_lbl
vt_no_lbl = Label(frame_vt, bg='#3BB9FF', textvariable=vt_no, font="Verdana 8 bold")
vt_no_lbl.place(relx=0.94, rely=0.02)

vt_cıkıs_lbl = Label(frame_vt, bg='#3BB9FF', text="Çıkış Zamanı: ", font="Verdana 10 bold")
vt_cıkıs_lbl.place(relx=0.40, rely=0.08)

global vt_cıkısDeger
vt_cıkısDeger=StringVar()
global vt_cıkısDeger_lbl
vt_cıkısDeger_lbl = Label(frame_vt, bg='#3BB9FF', textvariable=vt_cıkısDeger, font="Verdana 10 bold")
vt_cıkısDeger_lbl.place(relx=0.56, rely=0.08)



def Hakkımda():
    messagebox.showinfo("PROJE HAKKINDA","Plaka Tanıma Projesi, Fırat Üniversitesi Teknoloji Fakültesi Yazılım Mühendisliği Bölümü YMH455 Ders Kodlu Bitirme Projesi Dersi Kapsamında Doç. Dr. ÖZAL YILDIRIM Danışmanlığında 180541033 Öğrenci Numaralı Kerimhan Badur Tarafından Geliştirilmiştir...")
def Kullanım():
    messagebox.showinfo("PROJE KULLANIM","Kamera Kısmı\n\nKamera Aç: Görüntü açılır ve plakayı ekrana tutup s tuşuna basarak plakayı tanıtın.\nÇıkmak için ise q tuşuna basılı tutunuz.\nNOT: Yeni bir karakter tanıtmadan önce Sıfırla butonuna basınız. \nGerçek Zamanlı: Açılan kamerada plaka gösterin ve açılan klasörde plakanın kaydedildiğini görücelsiniz.\nÇıkmak için ise q tuşuna basılı tutunuz.\nKarakter Göster: Plaka tanımlama adımından sonra basılarak plakadaki Gler çıkartılır ve çıkarttığı dosya konumu açılır.\nSıfırla: Ekrandaki plaka ve plaka resmi sıfırlanır ve yeni işlem için hazırlanılır.\n\nResim Kısmı\n\nResim Seç: Butona basıp çıkan ekranda plakası okunacak resim seçilir ve devam denir ve gerekli işlemler yapıldıktan sonra program ekrana plakayı basar.\nKarakter Göster: Plaka tanımlama adımından sonra basılarak plakadaki karakterler çıkartılır ve çıkarttığı dosya konumu açılır.\nSıfırla: Ekrandaki plaka ve plaka resmi sıfırlanır ve yeni işlem için hazırlanılır.\n\nKayıtlar Kısmı\n\nTablodan eklenen alan seçilir ve gerekli bilgileri program yukardaki kutucuklara çıkartır. Burdan sonra kalan boş kutucukları doldurup Güncelle butonuna basarak plakaya ait bilgiler eklenir.\nÇıkış: İçerideki aracın çıkış yaptığınıbelirtir.\nGiren Araçlar: İçerideki araçların listesini verir.\nÇıkan Araçlar: Çıkış yapan araçların listesini verir.\nKayıt Çıkart: Tablodan kaydı direk siler.\nAra: burda Ad alanı seçilik kutucuğa ad bilgisi girilirse ada göre arama yapar eğer Plaka seçilip arama yapılırsa plaka bilgisine göre bir arama gerçekleşecektir.\n Yenile:yenile sembolüne tıklanırsa tablo yenilenicektir.\nÜcret: Bu kısımda default olarak saatlik 10 TL belirlenmiştir. Buraya saatlik ücret girilerek değiştir denirse saatlik yeni ücret belirlenebilir. \n0-1 Saat ücretsiz tiki seçilirse parklarda 1 saate kadar ücretsiz park yapılabilecektir.")
photoHakkımda = PhotoImage(file = "Resimler/hakkımda.png")
btn_reset_vt= Button(arayüz, image=photoHakkımda,compound=LEFT, command=Hakkımda)
btn_reset_vt.place(relx=0.92, rely=0.01, relwidth=0.03, relheight=0.06)

photoKullanım = PhotoImage(file = "Resimler/kullanım.png")
btn_reset_vt= Button(arayüz, image=photoKullanım,compound=LEFT, command=Kullanım)
btn_reset_vt.place(relx=0.96, rely=0.01, relwidth=0.03, relheight=0.06)


baslık_kamera_lbl = Label(frame_başlık, bg='#FA1805', text="Kamera", font="Verdana 12 bold")
baslık_kamera_lbl.place(relx=0.01, rely=0.15, relwidth=0.27, relheight=0.8)

baslık_resim_lbl = Label(frame_başlık, bg='#FA1805', text="Resim", font="Verdana 12 bold")
baslık_resim_lbl.place(relx=0.30, rely=0.15, relwidth=0.27, relheight=0.8)

baslık_vt_lbl = Label(frame_başlık, bg='#FA1805', text="Kayıtlar", font="Verdana 12 bold")
baslık_vt_lbl.place(relx=0.67, rely=0.15, relwidth=0.27, relheight=0.8)






# =============================================================================
# ------
# =============================================================================

#database Select işlemi





vt_tablo= Frame(frame_vt , bg='#3BB9FF', relief=RIDGE,highlightthickness=2, highlightbackground="black")
vt_tablo.place(relx=0.01, rely=0.24, relwidth=0.97, relheight=0.6)

scroll_x= Scrollbar(vt_tablo, orient=HORIZONTAL)
scroll_y= Scrollbar(vt_tablo, orient=VERTICAL)

design=ttk.Style()
design.theme_use("clam")

global veri_listesi
veri_listesi=ttk.Treeview(vt_tablo, height=12, column=("No","AdSoyad","Telefon","Plaka","GirişZamanı","ÇıkışZamanı","Ücret"),xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)

veri_listesi.configure(yscrollcommand=scroll_x.set)
scroll_x.configure(command=veri_listesi.xview)

veri_listesi.configure(yscrollcommand=scroll_y.set)
scroll_y.configure(command=veri_listesi.yview)

veri_listesi.heading("No", text="No")
veri_listesi.heading("AdSoyad", text="Ad Soyad")
veri_listesi.heading("Telefon", text="Telefon")
veri_listesi.heading("Plaka", text="Plaka")
veri_listesi.heading("GirişZamanı", text="Giriş Zamanı")
veri_listesi.heading("ÇıkışZamanı", text="Çıkış Zamanı")
veri_listesi.heading("Ücret", text="Ücret")

veri_listesi['show']='headings'

veri_listesi.column("No", width=4, anchor=tk.CENTER)
veri_listesi.column("AdSoyad", width=50, anchor=tk.CENTER)
veri_listesi.column("Telefon", width=50, anchor=tk.CENTER)
veri_listesi.column("Plaka", width=40, anchor=tk.CENTER)
veri_listesi.column("GirişZamanı", width=55, anchor=tk.CENTER)
veri_listesi.column("ÇıkışZamanı", width=55, anchor=tk.CENTER)
veri_listesi.column("Ücret", width=29, anchor=tk.CENTER)
veri_listesi.pack(fill=BOTH, expand=1)

def datalist(veri_l):
    try:
        con=pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=DB\PlakaDB.accdb;')
        cur=con.cursor()
        
        cur.execute("SELECT * FROM Plaka")
        
        rows = cur.fetchall()
        
        if len(rows) !=0:
            veri_l.delete(*veri_l.get_children())
            for row in rows:
                veri_l.insert('',END, values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
            con.commit()
        con.close()
            
    except pyodbc.Error as e:
        messagebox.showerror("Bağlantı Hatası","Bağlantı Hatası oluştu.")

def vt_select(ev):
    cursor_row = veri_listesi.focus()
    contents= veri_listesi.item(cursor_row)
    row=contents['values']
    vt_no.set(row[0])
    vt_ad.set(row[1])
    vt_tel.set(row[2])
    vt_plk.set(row[3])
    vt_girisDeger.set(row[4])
    vt_cıkısDeger.set(row[5])


def zaman():
    şuan=datetime.datetime.now()
    gün=şuan.day
    ay=şuan.month
    yıl=şuan.year
    saat=şuan.hour
    dakika=şuan.minute
    if saat <=9:
        saat="0"+str(saat)
    if dakika <=9:
        dakika="0"+str(dakika)
    return str(gün) +"-"+ str(ay) +"-"+ str(yıl) +"  "+ str(saat) +":"+str(dakika)


global fiyatKac
fiyatKac=IntVar()
fiyatKac.set(10)

global var1
var1 =IntVar()
var1.set(0)
                
def kacDakıkaVeTL(tarih, tariha):
    global fiyatKac
    global var1
    dakFiyat=int(fiyatKac.get())/60
    boşluk=0
    sub=0
    atama=1
    gün=""
    ay=""
    yıl=""
    saat=""
    dakika=""
    for i in range(len(tarih)):
        if tarih[i]==" ":
            if boşluk==0:
                yıl=int(tarih[sub:(i)])
                atama=atama+1
                sub=i
                boşluk=boşluk+1
                #sub=sub+1
            continue
        if tarih[i]=="-" or tarih[i]==":":
            if atama ==1:
                gün=int(tarih[sub:(i)])
                atama=atama+1
                sub=i
            elif atama==2:
                ay=int(tarih[sub:(i)])
                atama=atama+1
                sub=i
            elif atama ==4:
                saat=int(tarih[sub:(i)])
                atama=atama+1
                sub=i
                dakika=int(tarih[(sub+1):len(tarih)])
            sub=sub+1
    tarih1=datetime.datetime(yıl, ay, gün,saat,dakika)
    boşluka=0
    suba=0
    atamaa=1
    güna=""
    aya=""
    yıla=""
    saata=""
    dakikaa=""
    for i in range(len(tariha)):
        if tariha[i]==" ":
            if boşluka==0:
                yıla=int(tariha[suba:(i)])
                atamaa=atamaa+1
                suba=i
                boşluka=boşluka+1
                #sub=sub+1
            continue
        if tariha[i]=="-" or tariha[i]==":":
            if atamaa ==1:
                güna=int(tariha[suba:(i)])
                atamaa=atamaa+1
                suba=i
            elif atamaa==2:
                aya=int(tariha[suba:(i)])
                atamaa=atamaa+1
                suba=i
            elif atamaa ==4:
                saata=int(tariha[suba:(i)])
                atamaa=atamaa+1
                suba=i
                dakikaa=int(tariha[(suba+1):len(tariha)])
            suba=suba+1
    tarih2=datetime.datetime(yıla, aya, güna,saata,dakikaa)
    tarihFark=tarih1-tarih2
    saatSon=saat-saata
    dakikaSon=dakika-dakikaa
    sonuç=str(int(((tarihFark.total_seconds()/60)*(dakFiyat)))) +" TL"
    if int(var1.get())==1:
        if int(tarihFark.total_seconds()/60) <= 59:
            return "Ücretsiz"
    return sonuç  
    
    


#Güncelleme Fonksiyonu
def Güncelle():
    try:
        con=pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=DB\PlakaDB.accdb;')
        cur=con.cursor()
        
        cur.execute("UPDATE Plaka SET [AdSoyad]=?, [Telefon]=?, [Plaka]=? WHERE [No]=?",(vt_ad_txt.get(),vt_tel_txt.get(), vt_plk.get(), vt_no.get()))
        con.commit()
        messagebox.showinfo("Kayıt Güncelleme","Güncelleme Başarılı")
        con.close()
        datalist(veri_listesi)
    except pyodbc.Error as e:
        messagebox.showerror("Error Update","Güncelleme Hatası")


def Çıkış():
    try:
        cık=str(zaman())
        gir=str(vt_girisDeger.get())
        TL=kacDakıkaVeTL(cık,gir)
        con=pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=DB\PlakaDB.accdb;')
        cur=con.cursor()
        
        cur.execute("UPDATE Plaka SET [ÇıkışZamanı]=? , [Ücret]=? WHERE [No]=?",(cık,TL, vt_no.get()))
        con.commit()
        mesaj="Çıkış başarıyla Yapıldı. Ücret= "+TL
        messagebox.showinfo("Çıkış",mesaj)
        con.close()
        datalist(veri_listesi)
    except pyodbc.Error as e:
        messagebox.showerror("Çıkış Hatası","Çıkış sırasında hata oluştu.")

def Sil():
    try:
        soru =messagebox.askyesno('Kayıt silme','Silmek istediğinize emin misiniz?')
        if soru==1:
            con=pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=DB\PlakaDB.accdb;')
            cur=con.cursor()
            cur.execute("DELETE FROM Plaka WHERE [No]=?",(vt_no.get()))
            con.commit()
            Select_item= veri_listesi.selection()[0]
            veri_listesi.delete(Select_item)
            con.close()
            datalist(veri_listesi)
            messagebox.showinfo("Silme işlemi","Silme işlemi başarılı.")
        else:
            messagebox.showinfo("Silme işlemi","Silme işlemi iptal edildi.")
        
    except pyodbc.Error as e:
        messagebox.showerror("Kayıt silme hatası","Silme sırasında hata meydana geldi.")

btn_sil_vt= Button(frame_vt, bg='#B09898', text="Kayıt Çıkart", command=Sil)
btn_sil_vt.place(relx=0.83, rely=0.87, relwidth=0.15, relheight=0.10)



def Ara():
    try:
        con=pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=DB\PlakaDB.accdb;')
        cur=con.cursor()
        hangisi=kac
        if hangisi ==1:
            cur.execute("SELECT * FROM Plaka WHERE AdSoyad LIKE '%"+(vt_plk_txt.get())+"%'")
        elif hangisi==2:
            cur.execute("SELECT * FROM Plaka WHERE Plaka LIKE '%"+(vt_plk_txt.get())+"%'")
        rows = cur.fetchall()
        
        if len(rows) !=0:
            veri_listesi.delete(*veri_listesi.get_children())
            for row in rows:
                veri_listesi.insert('',END, values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
            con.commit()
        else:
            messagebox.showerror("Uyarı","Lütfen doğru plakayı giriniz..")
        con.close()
            
    except pyodbc.Error as e:
        print(str(e))
        messagebox.showerror("Uyarı","Lütfen doğru plakayı giriniz.")
        
        
def İçerdekiler():
    try:
        datalist(veri_listesi)
        con=pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=DB\PlakaDB.accdb;')
        cur=con.cursor()
        
        cur.execute("SELECT * FROM Plaka WHERE ÇıkışZamanı = 'Çıkmadı'")
        
        rows = cur.fetchall()
        
        if len(rows) !=0:
            veri_listesi.delete(*veri_listesi.get_children())
            for row in rows:
                veri_listesi.insert('',END, values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
            con.commit()
        else:
            messagebox.showerror("Uyarı","İçeride araba yok.")
        con.close()
            
    except pyodbc.Error as e:
        messagebox.showerror("Uyarı","İçeride araba yok.")


def Dışardakiler():
    try:
        datalist(veri_listesi)
        con=pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=DB\PlakaDB.accdb;')
        cur=con.cursor()
        
        cur.execute("SELECT * FROM Plaka WHERE ÇıkışZamanı <> 'Çıkmadı'")
        
        rows = cur.fetchall()
        
        if len(rows) !=0:
            veri_listesi.delete(*veri_listesi.get_children())
            for row in rows:
                veri_listesi.insert('',END, values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
            con.commit()
        else:
            messagebox.showerror("Uyarı","İçeride araba yok.")
        con.close()
            
    except pyodbc.Error as e:
        messagebox.showerror("Uyarı","İçeride araba yok.")
 

def Sırala():
    try:
        datalist(veri_listesi)
        con=pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=DB\PlakaDB.accdb;')
        cur=con.cursor()
        
        cur.execute("SELECT * FROM Plaka ORDER BY No")
        rows = cur.fetchall()
        
        if len(rows) !=0:
            veri_listesi.delete(*veri_listesi.get_children())
            for row in rows:
                veri_listesi.insert('',END, values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
            con.commit()
        else:
            messagebox.showerror("Uyarı","Veri yok.")
        con.close()
            
    except pyodbc.Error as e:
        messagebox.showerror("Uyarı","Veri yok.")
        
            
            
        
   


btn_cıkıs_vt= Button(frame_vt, bg='#B09898', text="Giren Araçlar", command=İçerdekiler)
btn_cıkıs_vt.place(relx=0.41, rely=0.87, relwidth=0.15, relheight=0.10)

btn_cıkıs_vt= Button(frame_vt, bg='#B09898', text="Çıkan Araçlar", command=Dışardakiler)
btn_cıkıs_vt.place(relx=0.62, rely=0.87, relwidth=0.15, relheight=0.10)


def DegFitafM():
    try:
        global fiyatKac
        Mesaj="Fiyat değişikliği başarılı \n\n Saatlik Fiyat="+str(fiyatKac.get())+" TL"
        messagebox.showinfo("Başarılı",Mesaj)
    except:
        messagebox.showerror("Uyarı","Lütfen doğru fiyat giriniz.")
        vt_fiyat_txt.delete(0,END)
        


vt_fiyat_lbl = Label(frame_vt, bg='#3BB9FF', text="Fiyat: ", font="Verdana 10 bold")
vt_fiyat_lbl.place(relx=0.38, rely=0.19)

vt_fiyat_txt=Entry(frame_vt, width=15, textvariable=fiyatKac)
vt_fiyat_txt.place(relx=0.46, rely=0.19)

vt_fiyat_lbl = Label(frame_vt, bg='#3BB9FF', text="TL", font="Verdana 10 bold")
vt_fiyat_lbl.place(relx=0.60, rely=0.19)

vt_fiyat_btn= Button(frame_vt, bg='#B09898', text="Değiş",command=DegFitafM)
vt_fiyat_btn.place(relx=0.65, rely=0.19, relwidth=0.06, relheight=0.04)



def fon():
    global var1
    if var1.get() == 1:
        messagebox.showinfo("Başarılı","0 - 1 Saat ücretsizdir.")
    else:
        messagebox.showinfo("Başarılı","0 - 1 Saat ücretlidir.")

c1 = tk.Checkbutton(frame_vt,bg='#3BB9FF', text='0-1 Ücretsiz',font="Verdana 8 bold",variable=var1, onvalue=1, offvalue=0,command=fon)
c1.place(relx=0.73, rely=0.19, relwidth=0.16, relheight=0.04)




vt_plk_lbl = Label(frame_vt, bg='#3BB9FF', text="Ara: ", font="Verdana 10 bold")
vt_plk_lbl.place(relx=0.40, rely=0.14)

vt_plk_txt=Entry(frame_vt, width=17)
vt_plk_txt.place(relx=0.46, rely=0.14)

btn_ara_vt= Button(frame_vt, bg='#B09898', text="Ara", command=Ara)
btn_ara_vt.place(relx=0.65, rely=0.14, relwidth=0.05, relheight=0.04)


def R():
    datalist(veri_listesi)

photo = PhotoImage(file = "Resimler/Restart.png")
btn_reset_vt= Button(frame_vt, image=photo,compound=LEFT, command=R)
btn_reset_vt.place(relx=0.93, rely=0.18, relwidth=0.05, relheight=0.05)


photoSırala = PhotoImage(file = "Resimler/Sırala.png")
btn_reset_vt= Button(frame_vt, image=photoSırala,compound=LEFT, command=R)
btn_reset_vt.place(relx=0.01, rely=0.19, relwidth=0.04, relheight=0.04) 



btn_cıkıs_vt= Button(frame_vt, bg='#B09898', text="Güncelle", command=Güncelle)
btn_cıkıs_vt.place(relx=0.22, rely=0.87, relwidth=0.15, relheight=0.10)
    
btn_cıkıs_vt= Button(frame_vt, bg='#B09898', text="Çıkış", command=Çıkış)
btn_cıkıs_vt.place(relx=0.01, rely=0.87, relwidth=0.15, relheight=0.10)

veri_listesi.bind('<ButtonRelease-1>',vt_select)






#dataların treeviewde görünmesi,
datalist(veri_listesi)












def vt_kayıt_ekle(plaka):
    try:
        con=pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=DB\PlakaDB.accdb;')
        cur=con.cursor()
        
        cur.execute("INSERT INTO Plaka([AdSoyad],[Telefon],[Plaka],[GirişZamanı],[ÇıkışZamanı]) VALUES ('" "','" "','"+str(plaka)+"','"+str(zaman())+"','Çıkmadı')")
        con.commit()
        con.close()
        messagebox.showinfo("Başarılı","Veri tabanına plakanız eklenmiştir.")
        datalist(veri_listesi)
            
    except pyodbc.Error as e:
        messagebox.showerror("Error connect","Ekleme Hatası")












global araba_rsm

"""

canvas_kamera= Canvas(frame_kamera,width=500, height=100)

kamera_plk=PhotoImage(file='bosplk.png')
r_kamera_plk=kamera_plk.subsample(4,4)

def_plaka= canvas_kamera.create_image(50, 30, image=r_kamera_plk, anchor=CENTER)

canvas_kamera.place(relx=0.20, rely=0.44, relwidth=0.53, relheight=0.16)"""
imageKamera = pı.open("Resimler/bosplk.png")
imageKamera = imageKamera.resize((174,74), pı.ANTIALIAS)
picKamera = ptk.PhotoImage(imageKamera)
    
canvas_kamera= Canvas(frame_kamera,width=500, height=100,highlightthickness=2, highlightbackground="black", bg='#3BB9FF')
canvas_kamera.place(relx=0.20, rely=0.44, relwidth=0.46, relheight=0.12)
def_plaka=canvas_kamera.create_image(0,0, image=picKamera, anchor="nw")
canvas_kamera.place(relx=0.20, rely=0.44, relwidth=0.51, relheight=0.12)
canvas_kamera.image=picKamera

def karakterGosterme():
        global x
        if x>=1:
            plakaKarakterleri()
            x=0
        elif x==0:
            messagebox.showerror("Hata","Lütfen plaka tanıtın.")





btn_karakter_göster_kamera= Button(frame_kamera, bg='#B09898', text="Karakter Göster", command=karakterGosterme)
btn_karakter_göster_kamera.place(relx=0.52, rely=0.87, relwidth=0.45, relheight=0.10)



def Kamera_Ac():
    global x
    x=1
    Resim_plaka_text.delete(0,END)
    PlakaData = cv2.CascadeClassifier("PlakaModel.xml") #Plaka bulmak için önceden eğitilmiş bir model.
    Kamera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    MinAlan=500
    global kontrol
    kontrol=False
    global count
    count_kac = os.listdir("Resimler/KaydedilenPlakalar")
    if len(count_kac) == 0:
        count=0
    else:
        count=len(count_kac)
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
            #resimROİ=resimROİ[10:90, 10:90]
            cv2.imwrite("Resimler/KaydedilenPlakalar/Plaka"+str(count+2)+".jpg", resimROİ)
            cv2.rectangle(resim, (0,200), (640,300), (255,0,0),cv2.FILLED)  
            cv2.putText(resim, "KAYDEDILDI", (15,265), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,255),2) #kaydettikten sonra ekranda KAYDEDİLDİ görülücektir.
            cv2.imshow("SONUC", resim)
            cv2.waitKey(1000)
            
            
            img = pı.open("Resimler/KaydedilenPlakalar/Plaka"+str(count+2)+".jpg")
            img_r= img.resize((178, 70), pı.ANTIALIAS)
            img = ptk.PhotoImage(img_r)
            canvas_kamera.imgref = img
            canvas_kamera.itemconfig(def_plaka, image = img)
            plaka=cevirSon(count+2)
            Kamera_plaka_text.insert(0,plaka)
            vt_kayıt_ekle(plaka)
            #count = count + 1
            dongu=False
            Kamera.release()
            cv2.destroyAllWindows()
            
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            Kamera.release()
            cv2.destroyAllWindows()
            break


btn_kamera_ac= Button(frame_kamera, bg='#B09898', text="Kamera Aç", command=Kamera_Ac,  font="Verdana 14 bold")
btn_kamera_ac.place(relx=0.03, rely=0.05, relwidth=0.45, relheight=0.2)

btn_kamera_ac_Gercek= Button(frame_kamera, bg='#B09898', text="Gerçek Zamanlı",command=Kamera_Ac_Gercek,  font="Verdana 12 bold")
btn_kamera_ac_Gercek.place(relx=0.52, rely=0.05, relwidth=0.45, relheight=0.2)


Kamera_plaka_string = Label(frame_kamera, bg='#3BB9FF', text="Plaka: ", font="Verdana 10 bold")
Kamera_plaka_string.place(relx=0.29, rely=0.78)

Kamera_plaka_text=Entry(frame_kamera, width=20)#,state='disabled'
Kamera_plaka_text.place(relx=0.44, rely=0.78)


def sfr_kamera():
    global x
    x=0
    Kamera_plaka_text.delete(0,END)
    
    imageKamera = pı.open("Resimler/bosplk.png")
    imageKamera = imageKamera.resize((174,74), pı.ANTIALIAS)
    picKamera = ptk.PhotoImage(imageKamera)
    
    canvas_kamera.imgref = picKamera
    canvas_kamera.itemconfig(def_plaka, image = picKamera)
    


btn_sıfırla_kamera= Button(frame_kamera, bg='#B09898', text="Sıfırla", command=sfr_kamera)
btn_sıfırla_kamera.place(relx=0.03, rely=0.87, relwidth=0.45, relheight=0.10)





#--------------------------------------------------------------------------------------)
"""
canvas_resim= Canvas(frame_foto,width=500, height=100)

resim_plk=PhotoImage(file='bosplk.png')
r_resim_plk=resim_plk.subsample(4,4)

def_plaka2= canvas_resim.create_image(103, 30, image=r_resim_plk, anchor=CENTER)

canvas_resim.place(relx=0.45, rely=0.44, relwidth=0.47, relheight=0.16)"""


imageResim = pı.open("Resimler/bosplk.png")
imageResim = imageResim.resize((174,74), pı.ANTIALIAS)
picResim = ptk.PhotoImage(imageResim)
    
canvas_resim= Canvas(frame_foto,width=500, height=100,highlightthickness=2, highlightbackground="black", bg='#3BB9FF')
canvas_resim.place(relx=0.45, rely=0.44, relwidth=0.46, relheight=0.12)
def_plaka2=canvas_resim.create_image(0,0, image=picResim, anchor="nw")
canvas_resim.place(relx=0.45, rely=0.44, relwidth=0.46, relheight=0.12)
canvas_resim.image=picResim


"""
canvas_araba= Canvas(frame_foto,width=500, height=500)
resim_bos_arb=PhotoImage(file='arb.png')
r_resim_bos_arb=resim_bos_arb.subsample(1,1)

def_bosArb= canvas_araba.create_image(85, 85, image=r_resim_bos_arb, anchor=CENTER)
canvas_araba.place(relx=0.02, rely=0.30, relwidth=0.40, relheight=0.40)"""

imageAraba = pı.open("Resimler/arb.png")
imageAraba = imageAraba.resize((150,185), pı.ANTIALIAS)
picAraba = ptk.PhotoImage(imageAraba)
    
canvas_araba= Canvas(frame_foto,width=150, height=185,highlightthickness=2, highlightbackground="black", bg='#3BB9FF')
canvas_araba.place(relx=0.02, rely=0.35, relwidth=0.40, relheight=0.29)
def_bosArb= canvas_araba.create_image(0,0, image=picAraba, anchor="nw")
canvas_araba.place(relx=0.02, rely=0.35, relwidth=0.40, relheight=0.29)
canvas_araba.image=picAraba



def resimSecPlk():
    global x
    x=1
    Resim_plaka_text.delete(0,END)
    ResimYolu=filedialog.askopenfilename(initialdir="Resimler/Plakalar")
    img = pı.open(ResimYolu)
    img_r= img.resize((150,185), pı.ANTIALIAS)
    img = ptk.PhotoImage(img_r)
    canvas_araba.imgref = img
    canvas_araba.itemconfig(def_bosArb, image = img)
    
    count=0
    count_kac = os.listdir("Resimler/Plakalar")
    if len(count_kac) == 0:
        count=0
    else:
        count=len(count_kac)
    
    cv2Araba=cv2.imread(ResimYolu)
    cv2.imwrite("Resimler\\Plakalar\\"+str(count+2)+".jpg", cv2Araba)
    
    resim = cv2.imread("Resimler\\Plakalar\\"+str(count+2)+".jpg")
    PlakaResimBul(resim)
    
    
    
    countPlk=0
    count_kacPlk = os.listdir("Resimler/KaydedilenPlakalar")
    if len(count_kacPlk) == 0:
        countPlk=0
    else:
        countPlk=len(count_kacPlk)
    
    img2 = pı.open("Resimler/KaydedilenPlakalar/Plaka"+str(countPlk+1)+".jpg")
    img_r2= img2.resize((178, 70), pı.ANTIALIAS)
    img2 = ptk.PhotoImage(img_r2)
    canvas_resim.imgref = img2
    canvas_resim.itemconfig(def_plaka2, image = img2)
    
    plaka=cevirSon(countPlk+1)
    Resim_plaka_text.insert(0,plaka)
    vt_kayıt_ekle(plaka)


def sfr_resim():
    global x
    x=0
    Resim_plaka_text.delete(0,END)
    
    imageResim = pı.open("Resimler/bosplk.png")
    imageResim = imageResim.resize((174,74), pı.ANTIALIAS)
    picResim = ptk.PhotoImage(imageResim)
    canvas_resim.imgref = picResim
    canvas_resim.itemconfig(def_plaka2, image = picResim)
#araba_lbl2.place(relx=0.35, rely=0.27, relwidth=0.30, relheight=0.30)
    
    imageAraba = pı.open("Resimler/arb.png")
    imageAraba = imageAraba.resize((150,185), pı.ANTIALIAS)
    picAraba = ptk.PhotoImage(imageAraba)
    
    canvas_araba.imgref = picAraba
    canvas_araba.itemconfig(def_bosArb, image = picAraba)






btn_resim_sec= Button(frame_foto, bg='#B09898', text="Resim Seç", command=resimSecPlk, font="Verdana 14 bold")
btn_resim_sec.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.2)



#araba_rsm2=Image.open("bosplk.png")
#araba_resize2= araba_rsm2.resize((400, 400), Image.ANTIALIAS)
#yeni_araba_rsm2 = ImageTk.PhotoImage(araba_resize)

#araba_lbl2= Label(frame_foto, image=yeni_araba_rsm2)

#plk_rsm=Image.open("bosplk.png")
#plk_rsm_resz= plk_rsm.resize((400, 400), Image.ANTIALIAS)
#plk_rsm_yeni = ImageTk.PhotoImage(plk_rsm_resz)

#araba_lbl= Label(frame_foto, image=plk_rsm_yeni)
#araba_lbl.place(relx=0.25, rely=0.60, relwidth=0.5, relheight=0.15)

Resim_plaka_string = Label(frame_foto, bg='#3BB9FF', text="Plaka: ", font="Verdana 10 bold")
Resim_plaka_string.place(relx=0.29, rely=0.78)

Resim_plaka_text=Entry(frame_foto, width=20)#,state='disabled'
Resim_plaka_text.place(relx=0.44, rely=0.78)


btn_sıfırla_resim= Button(frame_foto, bg='#B09898', text="Sıfırla", command=sfr_resim)
btn_sıfırla_resim.place(relx=0.03, rely=0.87, relwidth=0.45, relheight=0.10)




btn_karakter_göster_resim= Button(frame_foto, bg='#B09898', text="Karakter Göster", command=karakterGosterme)
btn_karakter_göster_resim.place(relx=0.52, rely=0.87, relwidth=0.45, relheight=0.10)


arayüz.mainloop() #sürekli açık kalması sağlanır.



#--------------------------------------------------------------------------------------




