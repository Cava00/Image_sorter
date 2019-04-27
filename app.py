import sys
import os
from shutil import copy
from Tkinter import *
from ImageTk import PhotoImage
import Image
import keyboard
from time import sleep

#================================================================================================================================================================

previous_image = None
previous_path = None

previous_key = 'z'

path_list = []
file_list = []

extensions = [".jpg" , ".gif", ".png", ".jpeg", ".tif", ".tiff", ".bmp", ".eps"]
c=0

#=====================================================================================================================================================================
def keep(f, path, dir):
    global previous_path
    global previous_image
    if previous_path != None:
        previous_image = None
        previous_path = None
    os.chdir(path)
    copy(f,dir)

#=====================================================================================================================================================================
def delete(f, path):
    global previous_path
    global previous_image

    if previous_path != None:
        os.chdir(previous_path)
        os.remove(previous_image)
        previous_image = None
        previous_path = None

    previous_image = f
    previous_path = path

#====================================================================================================================================================================

def start(event):
    global c
    global previous_key
    global previous_path
    global previous_image
    crea()

    rootdir = "C:/"

    if txt3.get():
        if txt3.get().startswith("C:/") or txt3.get().startswith("C:\\") or txt3.get().startswith("c:\\") or txt3.get().startswith("c:/"):
            if txt3.get().endswith("/") or  txt3.get().endswith("\\"):
                rootdir = txt3.get()
            else:
                rootdir = txt3.get() + os.sep
        else:
            pass
    else:
        pass

    txt1.pack_forget()
    txt2.pack_forget()
    txt3.pack_forget()
    lbl1.pack_forget()
    lbl2.pack_forget()
    lbl3.pack_forget()
    btn3.pack_forget()


    print ("processing")
    for path, dirname, filelist in os.walk(rootdir):
        for name in filelist:

            for ext in extensions:
                if name.endswith(ext):
                    if path.endswith('\\'):
                        path_list.append(path)
                    else:
                        path_list.append(path + os.sep)
                    file_list.append(name)
                else:
                    pass
    nextimm()
    getkey()
#=======================================================================================================================================================================
def getkey():
    global c
    global previous_key
    global previous_path
    global previous_image
    while TRUE:
        root.update()
        if keyboard.is_pressed('k'):
            previous_key = 'k'
            keep(file_list[c], path_list[c], cartella)
            c+=1
            if len(file_list) > c:
                nextimm()
                sleep(0.1)
            else:
                break
        else:
            pass
        if keyboard.is_pressed('d'):
            previous_key = 'd'
            delete(file_list[c], path_list[c])
            c+=1
            if len(file_list) > c:
                nextimm()
                sleep(0.1)
            else:
                break
        else:
            pass
        if keyboard.is_pressed('z') and previous_path != None and previous_key != 'z':
            #print previous_path
            #print previous_image
            #print c
            previous_key = 'z'
            previous_image = None
            previous_path = None
            c-=1
            nextimm()
            sleep(0.1)
        else:
            pass
    sch_finale()
#=============================================================================================================================================
def nextimm():

    global c
    global img1

    img1.pack_forget()

    #print path_list[c] + file_list[c]


    ima = Image.open(path_list[c] + file_list[c])
    ima = ima.resize((600, 600), Image.ANTIALIAS)
    display_img = PhotoImage(ima)

    img1 = Label(mainframe, image = display_img, width = 600, height = 600, anchor = CENTER)
    img1.image = display_img
    img1.pack(anchor = CENTER)

#=============================================================================================================================================
def crea():
    global cartella

    percorso_creazione = "C:\\"

    if txt1.get():
        if txt1.get().startswith("C:/") or txt1.get().startswith("C:\\") or txt1.get().startswith("c:\\") or txt1.get().startswith("c:/"):
            if txt1.get().endswith("/") or  txt1.get().endswith("\\"):
                percorso_creazione = txt1.get()
            else:
                percorso_creazione = txt1.get() + os.sep
        else:
            pass
    else:
        pass


    os.chdir(percorso_creazione)

    if txt2.get():
        try:
            os.mkdir(txt2.get())
            cartella = percorso_creazione + txt2.get() + os.sep
        except:
            cartella = percorso_creazione + txt2.get() + os.sep
    else:
        try:
            os.mkdir("provv")
            cartella = percorso_creazione + "provv" + os.sep
        except:
            cartella = percorso_creazione + "provv" + os.sep

#=======================================================================================================================================================================
def sch_finale():

    global c

    global previous_key
    global previous_path
    global previous_image

    global img1

    img1.pack_forget()

    #print path_list[c] + file_list[c]
    frtop = Frame(mainframe, bg = "#205374")
    frtop.pack(fill = X, anchor = N)

    frbot = Frame(mainframe, bg = "#205374")
    frbot.pack(anchor = S)

    lbl4 = Label(frtop, text = "Vuoi confermare l'eliminazione della cartella originale? ", bg = "#205374", fg = "#D3F5CE")
    lbl4.configure(font=("Helvetica", 28))
    lbl4.pack()

    btn4 = Button(frbot, text = "Si", bg = "#205374", fg = "#D3F5CE", width = 10)
    btn4.pack(side = LEFT)
    btn4.bind("<Button-1>",quit)


    btn5 = Button(frbot, text = "No", bg = "#205374", fg = "#D3F5CE", width = 10)
    btn5.pack(side = RIGHT)
    btn5.bind("<Button-1>",quit)

#=======================================================================================================================================================================

cartella = "C:/provv"

root = Tk()
root.title("Image selector")
root.state('zoomed')

mainframe = Frame(root, bg = "#205374")
mainframe.pack(fill=BOTH, expand=1)

lbl3 = Label(mainframe, text = "Percorso della cartella da analizzare", bg = "#205374", fg = "#D3F5CE")
lbl3.pack()
txt3 = Entry(mainframe, bg = "#27A09E", fg = "white")
txt3.pack()

lbl1 = Label(mainframe, text = "Inserire perscorso cartella in cui mettere le immagini", bg = "#205374", fg = "#D3F5CE")
lbl1.pack()
txt1 = Entry(mainframe,  bg = "#27A09E", fg = "white")
txt1.pack()

lbl2 = Label(mainframe, text = "Nome Cartella:", bg = "#205374", fg = "#D3F5CE")
lbl2.pack()
txt2 = Entry(mainframe,  bg = "#27A09E", fg = "white")
txt2.pack()

btn3 = Button(mainframe, text = "Start", height = 5, width = 50, bg = "#27A09E", fg = "white", relief = FLAT, cursor = "hand2")
btn3.pack(pady = 10, padx = 5)
btn3.bind('<Button-1>',start)

img1 = Label(mainframe)

root.mainloop()
