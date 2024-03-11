import cv2
import numpy as np
from tkinter import*
from PIL import Image, ImageTk
import tracemalloc
import timeit

def main():
    gui()
    cam_set('1080')
    detection()
    
    waktuLabel = Label(frame_1, text = (f' Waktu Komputasi(s) : {elapsed_time}'), font=("arial",22),anchor="w").place(x=37, y=645, width=660)
    memoriLabel = Label(frame_1,text = (f' Memori(KiB) : {size/1024:.2f}'), font=("arial",22),anchor='w').place(x = 37, y = 707, width=660)
    resolusi_w, resolusi_h  = (round(cam.get(cv2.CAP_PROP_FRAME_WIDTH)),round(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    resolusiLabel = Label(frame_1,text = (f' Resolusi(px) : {resolusi_w}x{resolusi_h}'), font=("arial",22)).place(x = 720, y = 645, width=440)
    
    print(f"Resolusi : {resolusi_w, resolusi_h}")
    print(f"waktu komputasi : {elapsed_time}")
    print(f"Memori(KiB) : {size/1024:.2f}\n\n")

    win.mainloop()

    del resolusi_h, resolusi_w, waktuLabel, memoriLabel, resolusiLabel
    
def cam_set(px):
    match px :
        case '1080' :
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
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
    global start_time, size, peak, elapsed_time
    global ret, img, kernal, black_low, black_high, black_mask, contours, hierarchy, pic, contour, area
    global img1, iago, img2, iago2, blmaskRez, iago3, ycc
    
    tracemalloc.start()
    start_time = timeit.default_timer()

    ret, img = cam.read()
    
    ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

    black_low = np.array([0, 136, 122], np.uint8)
    black_high = np.array([98, 255, 255], np.uint8)
    black_mask = cv2.inRange(ycc, black_low, black_high)
    kernal = np.ones((5, 5), "uint8")
    black_mask = cv2.dilate(black_mask, kernal)

    ## Logic create bonding box with countour area with color space masking
    
    elapsed_time = timeit.default_timer() - start_time
    size, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    img1 = cv2.resize(img,(790,527))
    img1 = img1[:,:,[2,1,0]]
    iago = ImageTk.PhotoImage(Image.fromarray(img1))
    label1.configure(image=iago)
    label1.image = iago

    _, img2 = cam.read()    
    img2 = cv2.resize(img2, (300, 200)) 
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2YCR_CB)
    iago2 = ImageTk.PhotoImage(Image.fromarray(img2))
    label2.configure(image=iago2)
    label2.image = iago2

    blmaskRez = cv2.resize(black_mask,(300,200))
    iago3 = ImageTk.PhotoImage(Image.fromarray(blmaskRez))
    label3.configure(image=iago3)
    label3.image = iago3

    win.after(10, detection)

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
    win.title("Deteksi Penyakit Busuk Daun Selada dengan Ruang Warna YCbCr")
    win.geometry("1182x788")
    win.resizable(False, False)
    judul = Label(frame_1,text = 'Deteksi Penyakit Busuk Daun Selada', font=("arial",28),bg='#929292').place(x= 37,y = 26, width=790)
    judulruang = Label(frame_1,text = 'Ruang Warna YCbCr', font=("arial",21),bg='#929292').place(x= 856,y = 26, width=300)
    judulcam = Label(frame_1,text = 'Konversi', font=("arial",25)).place(x= 856,y = 102, width=300)
    judulmask = Label(frame_1,text = 'Segmentasi', font=("arial",25)).place(x= 856,y = 367, width=300)
    

if __name__ == '__main__':
    cam = cv2.VideoCapture(1)

    main()

    del cam, win, frame_1, label1, label2, label3
    del judul, judulruang, judulcam, judulmask
    del start_time, size, peak, elapsed_time
    del ret, img, kernal, black_low, black_high, black_mask, contours, hierarchy, pic, contour, area
    del img1, iago, img2, iago2, blmaskRez, iago3, ycc