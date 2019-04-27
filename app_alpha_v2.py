import sys
import os
from shutil import copy
from Tkinter import *
from ImageTk import PhotoImage
import Image
import keyboard
from time import sleep

#=======================================================================================================================

class Fullscreen_Window:

    def __init__(self):
        self.root = Tk()
        self.root.state('zoomed')  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.
        self.frame = Frame(self.root, bg = "#205374")
        self.frame.pack(fill=BOTH, expand=1)
        self.state = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.root.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", False)
        return "break"

#=======================================================================================================================
class Start_window(Fullscreen_Window):

    extensions = [".jpg" , ".gif", ".png", ".jpeg", ".tif", ".tiff", ".bmp", ".eps"]

    file_list = []
    path_list = []



    def __init__(self):
        Fullscreen_Window.__init__(self)

        self.lbl3 = Label(self.frame, text = "Percorso della cartella da analizzare", bg = "#205374", fg = "#D3F5CE")
        self.lbl3.pack()
        self.txt3 = Entry(self.frame, bg = "#27A09E", fg = "white")
        self.txt3.pack()

        self.lbl1 = Label(self.frame, text = "Inserire perscorso cartella in cui mettere le immagini", bg = "#205374", fg = "#D3F5CE")
        self.lbl1.pack()
        self.txt1 = Entry(self.frame,  bg = "#27A09E", fg = "white")
        self.txt1.pack()

        self.lbl2 = Label(self.frame, text = "Nome Cartella:", bg = "#205374", fg = "#D3F5CE")
        self.lbl2.pack()
        self.txt2 = Entry(self.frame,  bg = "#27A09E", fg = "white")
        self.txt2.pack()

        self.btn3 = Button(self.frame, text = "Start", height = 5, width = 50, bg = "#27A09E", fg = "white", relief = FLAT, cursor = "hand2")
        self.btn3.pack(pady = 10, padx = 5)
        self.btn3.bind('<Button-1>',self.start)




    def start(self, event=None):

        self.rootdir = "C:/"

        if self.txt3.get():
            if self.txt3.get().startswith("C:/") or self.txt3.get().startswith("C:\\") or self.txt3.get().startswith("c:\\") or self.txt3.get().startswith("c:/"):
                if self.txt3.get().endswith("/") or  self.txt3.get().endswith("\\"):
                    self.rootdir = self.txt3.get()
                else:
                    self.rootdir = self.txt3.get() + os.sep
            else:
                pass
        else:
            pass

        print ("processing")
        for path, dirname, filelist in os.walk(self.rootdir):
            for name in filelist:

                for ext in self.extensions:
                    if name.endswith(ext):
                        if path.endswith('\\'):
                            self.path_list.append(path)
                        else:
                            self.path_list.append(path + os.sep)
                        self.file_list.append(name)
                    else:
                        pass

        percorso_creazione = "C:\\"

        if self.txt1.get():
            #print "a"
            if self.txt1.get().startswith("C:/") or self.txt1.get().startswith("C:\\") or self.txt1.get().startswith("c:\\") or self.txt1.get().startswith("c:/"):
                if self.txt1.get().endswith("/") or  self.txt1.get().endswith("\\"):
                    percorso_creazione = self.txt1.get()
                else:
                    percorso_creazione = self.txt1.get() + os.sep
            else:
                pass
        else:
            pass

        #print percorso_creazione
        os.chdir(percorso_creazione)

        if self.txt2.get():
            try:
                #print "x"
                os.mkdir(self.txt2.get())
                self.cartella = percorso_creazione + self.txt2.get() + os.sep
            except:
                self.cartella = percorso_creazione + self.txt2.get() + os.sep
        else:
            try:
                os.mkdir("provv")
                self.cartella = percorso_creazione + "provv" + os.sep
            except:
                self.cartella = percorso_creazione + "provv" + os.sep

        self.root.destroy()
        return "break"

    def getRootdir(self):
        return self.rootdir

    def getFileList(self):
        return self.file_list

    def getPathList(self):
        return self.path_list

    def getCopyDir(self):
        return self.cartella
#=======================================================================================================================

class Process_window(Fullscreen_Window):

    previous_path = None
    previous_image = None

    plist = []
    flist = []

    def __init__(self, copydir, files, paths, c = 0):
        Fullscreen_Window.__init__(self)

        self.plist = paths
        self.flist = files
        self.dir = copydir

        self.ima = Image.open(paths[c] + files[c])
        self.ima = self.ima.resize((600, 600), Image.ANTIALIAS)
        self.display_img = PhotoImage(self.ima)

        self.img1 = Label(self.frame, image = self.display_img, width = 600, height = 600, anchor = CENTER)
        self.img1.image = self.display_img
        self.img1.pack(anchor = CENTER)

        self.root.bind("<k>", self.keepImm)
        self.root.bind("<d>", self.delImm)
        self.root.bind("<z>", self.annulla)

    def nextImm(self, c, event=None):
        self.img1.pack_forget()
        self.ima = Image.open(self.plist[c] + self.flist[c])
        self.ima = self.ima.resize((600, 600), Image.ANTIALIAS)
        self.display_img = PhotoImage(self.ima)

        self.img1 = Label(self.frame, image = self.display_img, width = 600, height = 600, anchor = CENTER)
        self.img1.image = self.display_img
        self.img1.pack(anchor = CENTER)

        self.root.update()


    def keepImm(self, event = None):
        #print "works"
        global c
        if self.previous_path != None:
            self.previous_image = None
            self.previous_path = None
        os.chdir(self.plist[c])
        copy(self.flist[c],self.dir)
        #print self.plist[c]
        #print self.flist[c]
        c += 1
        if len(self.flist) > c:
            self.nextImm(c)
            sleep(0.1)
        else:
            self.root.withdraw()

    def delImm(self, event = None):

        global c

        if self.previous_path != None:
            os.chdir(self.previous_path)
            os.remove(self.previous_image)
            previous_image = None
            previous_path = None

        self.previous_image = self.flist[c]
        self.previous_path = self.plist[c]
        c += 1

        if len(self.flist) > c:
            self.nextImm(c)
            sleep(0.1)
        else:
            self.root.withdraw()

    def annulla(self, event = None):
        global c
        if self.previous_path != None:
            self.previous_image = None
            self.previous_path = None
            c -= 1
            self.nextImm(c)
            sleep(0.1)

#=======================================================================================================================
class Close_window(Fullscreen_Window):

    def __init__(self, copydir, files, paths, prev_win):
        Fullscreen_Window.__init__(self)

        self.prev_win = prev_win

        self.copydir = copydir
        self.files = files
        self.paths = paths

        self.frtop = Frame(self.frame, bg = "#205374")
        self.frtop.pack(fill = X, anchor = N)

        self.frbot = Frame(self.frame, bg = "#205374")
        self.frbot.pack(anchor = S)

        self.lbl4 = Label(self.frtop, text = "Vuoi confermare l'eliminazione della cartella originale? ", bg = "#205374", fg = "#D3F5CE")
        self.lbl4.configure(font=("Helvetica", 28))
        self.lbl4.pack()

        self.btn4 = Button(self.frbot, text = "Si", bg = "#205374", fg = "#D3F5CE", width = 10)
        self.btn4.pack(side = LEFT)
        self.btn4.bind("<Button-1>",quit)


        self.btn5 = Button(self.frbot, text = "No", bg = "#205374", fg = "#D3F5CE", width = 10)
        self.btn5.pack(side = RIGHT)
        self.btn5.bind("<Button-1>",quit)

        self.root.bind("<z>", self.back)

    def back(self, event = None):
        global c
        c -= 1
        self.root.withdraw()
        self.prev_win.root.deiconify()
        self.root.deiconify()

#=======================================================================================================================
#           MAIN
#=======================================================================================================================

if __name__ == '__main__':

    previous_key = 'k'
    c = 0

    inizio = Start_window()
    inizio.root.mainloop()

    mid = Process_window(inizio.getCopyDir(), inizio.getFileList(), inizio.getPathList())
    mid.root.mainloop()

    fin = Close_window(inizio.getCopyDir(), inizio.getFileList(), inizio.getPathList(), mid)
    fin.root.mainloop()
