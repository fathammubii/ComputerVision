import cv2 # Library untuk OpenCV
import numpy as np # Library NumPy
from tkinter import* # Library tkinter untuk GUI
from PIL import Image, ImageTk # Library TkInter untuk GUI
import tracemalloc # Modul python untuk menangkap block memori
import timeit # Modul Python untuk menyalakan timer

def main():
    gui() #Memanggil fungsi GUI
    cam_set('1080') #Memanggil fungsi setting ukuran frame dan memasukan parameter ukuran frame sebesar : 1080 px
    detection() #memanggil fungsi utama sistem deteksi
    #GUI
    waktuLabel = Label(frame_1, text = (f' Waktu Komputasi(s) : {elapsed_time}'), font=("arial",22),anchor="w").place(x=37, y=645, width=660)
    memoriLabel = Label(frame_1,text = (f' Memori(KiB) : {size/1024:.2f}'), font=("arial",22),anchor='w').place(x = 37, y = 707, width=660)
    resolusi_w, resolusi_h  = (round(cam.get(cv2.CAP_PROP_FRAME_WIDTH)),round(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    resolusiLabel = Label(frame_1,text = (f' Resolusi(px) : {resolusi_w}x{resolusi_h}'), font=("arial",22)).place(x = 720, y = 645, width=440)
    
    print(f"Resolusi : {resolusi_w, resolusi_h} px") #Cetak berapa resolusi
    print(f"Waktu komputasi(s) : {elapsed_time}") #Cetak waktu komputasi
    print(f"Memori(KiB) : {size/1024:.2f}\n\n") #Cetak penggunaan memori

    win.mainloop() # Loop untuk menjalankan program secara terus menerus hingga ditekan tombol silang 'x'

    del resolusi_h, resolusi_w, waktuLabel, memoriLabel, resolusiLabel #menghapus variabel
    
def cam_set(px): #Fungsi untuk set ukuran frame webcam
    match px :
        case '1080' :
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # Set ukuran webcam width : 1920 px
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # Set ukuran webcam height : 1080 px
        case '720' :
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        case '480': # VGA
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        case '240':# QVGA
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

def detection():
    global start_time, size, peak, elapsed_time # Deklarasi variabel global
    global ret, img, kernal, black_low, black_high, black_mask, contours, hierarchy, pic, contour, area
    global img1, iago, img2, iago2, blmaskRez, iago3
    
    tracemalloc.start() # Modul tracemalloc untuk menangkap blok memori di mulai
    start_time = timeit.default_timer() # Menyimpan nilai clock pada variabel start

    ret, img = cam.read() #ret : boolean untuk memeriksa apakah camera dapat terbaca, img : menyimpan nilai array citra yang dapat ditangkap oleh webcam
    
    black_low = np.array([30, 0, 0], np.uint8) # threshold bawah
    black_high = np.array([255, 30, 255], np.uint8) #threshold atas
    black_mask = cv2.inRange(img, black_low, black_high) # mask in range threshold atas dan bawah
    kernal = np.ones((5, 5), "uint8") # matriks 5x5 bernilai 1 untuk dilasi
    black_mask = cv2.dilate(black_mask, kernal) # dilasi black mask menggunakan matriks kernel 5x5

    contours, hierarchy = cv2.findContours(black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #mencari kontur gambar, cv2.find contur (black mask : source yang akan dicari konturnya), cv2.retr_tree (logic hirarki dalam menentukan kontur dalam dan luar (contohnya ada bounding box kecil didalam bounding box besar, nah itu dipilih maka yang besar aja sekalian, logic ini untuk menentukan hirarki nya))
    #chain approx simple : Untuk menyimpan nilai yang tercatat var kontur, simple hanya akan menerima nilai-nilai ujung dari kontur nya, misal kontur bernilai pd piksel 1-10, dari pada menyimpan nilai kontur : 1,2,3,..10 (Hanya menyimpan titik sudut dalam kontur). adalagi approx none, kalau ini menyimpan semua nilai, jadi makin berat tapi lebih detil
    #cv2.find countour ini akan menyimpan nilai kontur yang ada pada gambar biner pada proses sebelumnya (black mask)
   
    ## Logic create bonding box with countour area with color space masking
    
    elapsed_time = timeit.default_timer() - start_time #timer akhir : timer saat ini - timer awal
    size, peak = tracemalloc.get_traced_memory() # mencapture blok memori pada size (penggunaan memori saat ini), peak untuk alokasi sebelum program berjalan (scr keseluruhan kode)
    
    tracemalloc.stop() #(Capture/ modul python berhenti memonitor blok memori)

    img1 = cv2.resize(img,(790,527)) #Gui rezise ukuran image disesuaikan dengan ukuran frame pada gui
    img1 = img1[:,:,[2,1,0]] #Membalik array nilai BGR -> RGB
    iago = ImageTk.PhotoImage(Image.fromarray(img1)) #Menggunakan fungsi image TkInter untuk membaca hasil array img1 dan ditampilkan
    label1.configure(image=iago) # Memperbarui tampilan pada GUI label1 menjadi img1 (Citra hasil deteksi)
    label1.image = iago 

    _, img2 = cam.read()    
    img2 = cv2.resize(img2, (300, 200)) 
    img2 = img2[:,:,[2,1,0]]
    iago2 = ImageTk.PhotoImage(Image.fromarray(img2))
    label2.configure(image=iago2) # Memperbarui tampilan pada GUI label2 menjadi img2 (Citra konversi)
    label2.image = iago2

    blmaskRez = cv2.resize(black_mask,(300,200))
    iago3 = ImageTk.PhotoImage(Image.fromarray(blmaskRez))
    label3.configure(image=iago3) # Memperbarui tampilan pada GUI label3 menjadi blmaskRez (Citra Segementasi)
    label3.image = iago3

    win.after(10, detection) #Fungsi detection dipanggil secara berulang dengan interval 10 milidetik (estimasi program dijalankan per iterasi sebesar 10 mili (0.01 s))

def gui():
    global win, frame_1, label1, label2, label3
    global judul, judulruang, judulcam, judulmask
    
    win = Tk()
    frame_1 = Frame(win, width=1182, height=788, bg="#D9D9D9").place(x=0, y=0)
    label1 = Label(frame_1, width=790, height=527)
    label1.place(x=37, y=99)
    label2 = Label(frame_1, width=300, height=200)
    label2.place(x=856, y=158)
    label3 = Label(frame_1, width=300, height=200)
    label3.place(x=856, y=426)
    win.title("Deteksi Penyakit Busuk Daun Selada dengan Ruang Warna RGB")
    win.geometry("1182x788")
    win.resizable(False, False)
    judul = Label(frame_1,text = 'Deteksi Penyakit Busuk Daun Selada', font=("arial",28),bg='#929292').place(x= 37,y = 26, width=790)
    judulruang = Label(frame_1,text = 'Ruang Warna RGB', font=("arial",21),bg='#929292').place(x= 856,y = 26, width=300)
    judulcam = Label(frame_1,text = 'Konversi', font=("arial",25)).place(x= 856,y = 102, width=300)
    judulmask = Label(frame_1,text = 'Segmentasi', font=("arial",25)).place(x= 856,y = 367, width=300)
    

if __name__ == '__main__': #Program main script dijalankan
    cam = cv2.VideoCapture(1) #inisiasi variabel cam untuk capturing webcam yang akan digunakan untuk perekaman video dengan preferensi API

    main() #Fungsi main dipanggil

    tracemalloc.reset_peak() #reset hasil monitoring block memori
    del cam, win, frame_1, label1, label2, label3 # del variabel
    del judul, judulruang, judulcam, judulmask
    del start_time, size, peak, elapsed_time
    del ret, img, kernal, black_low, black_high, black_mask, contours, hierarchy, pic, contour, area
    del img1, iago, img2, iago2, blmaskRez, iago3