import os
from shutil import copy, rmtree
from Tkinter import *
from PIL.ImageTk import PhotoImage
import PIL.Image
from time import sleep

#=======================================================================================================================

class Fullscreen_Window:

    path_list = []
    file_list = []

    c = 0
    left = 0

    end_toggled = False

    extensions = [".jpg" , ".gif", ".png", ".jpeg", ".tif", ".tiff", ".bmp", ".eps"]

    def __init__(self):
        self.root = Tk()
        self.root.geometry("800x500")
        self.root.title("Image Selector")
        self.frame = Frame(self.root, bg = "#151719")
        self.frame.pack(fill = BOTH, expand = 1)
        self.state = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)
        self.previous_image = None
        self.previous_path = None

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.root.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", False)
        return "break"

    def start_window(self):

        self.startframe = Frame(self.frame, bg = "#151719", pady = 30)
        self.startframe.place(relx=0.5, rely=0.4, anchor=CENTER)

        self.titolo = Label(self.startframe, bg = "#151719", fg = "#f3f3f3", text = "Filter System")
        self.titolo.configure(font=("Verdana", 35))
        self.titolo.pack(fill = X)

        self.info = Label(self.startframe, bg = "#151719", fg = "#f3f3f3", text = "Tasto k: Conserva Immagine           Tasto d:elimina immagine")
        self.info.configure(font=("Helvetica", 15))
        self.info.pack(fill = X)

        self.info2 = Label(self.startframe, bg = "#151719", fg = "#f3f3f3", text = "Tasto z: annulla operazione")
        self.info2.configure(font=("Helvetica", 15))
        self.info2.pack(fill = X)

        self.spazio = Label(self.startframe, height=5, bg = "#151719")
        self.spazio.pack()

        self.lbl3 = Label(self.startframe, text = "Percorso cartella da analizzare", bg = "#151719", fg = "#f3f3f3")
        self.lbl3.pack()
        self.txt3 = Entry(self.startframe, bg = "#851c1c", fg = "#f3f3f3")
        self.txt3.pack()

        self.lbl2 = Label(self.startframe, text = "Nome della cartella in cui salvare una copia delle immagini:", bg = "#151719", fg = "#f3f3f3")
        self.lbl2.pack()
        self.txt2 = Entry(self.startframe,  bg = "#851c1c", fg = "#f3f3f3")
        self.txt2.pack()

        self.lbl1 = Label(self.startframe, text = "Dove salvo questa cartella?", bg = "#151719", fg = "#f3f3f3")
        self.lbl1.pack()
        self.txt1 = Entry(self.startframe,  bg = "#851c1c", fg = "#f3f3f3")
        self.txt1.pack()

        self.btn3 = Button(self.startframe, text = "Start", height = 2, width = 20, bg = "#851c1c", fg = "#f3f3f3", relief = FLAT, cursor = "hand2")
        self.btn3.configure(font = ("Verdana", 12))
        self.btn3.pack(pady = 10, padx = 5)
        self.btn3.bind('<Button-1>',self.start)

    def start(self, event=None):

        self.rootdir = "C:/"

        self.dirname = self.txt2.get()

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
                #print name
                for ext in self.extensions:
                    if name.endswith(ext):
                        if path.endswith('\\'):
                            self.path_list.append(path)
                        else:
                            self.path_list.append(path + os.sep)
                        self.file_list.append(name)
                        self.left += 1
                    else:
                        pass

        percorso_creazione = os.path.join(os.environ["HOMEPATH"], "Desktop")

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

        print percorso_creazione
        os.chdir(percorso_creazione)

        if self.txt2.get():
            try:
                #print "x"
                os.mkdir(self.dirname)
                self.cartella = percorso_creazione + self.dirname + os.sep
            except:
                self.cartella = percorso_creazione + self.dirname + os.sep
        else:
            try:
                os.mkdir("provv")
                self.cartella = percorso_creazione + "provv" + os.sep
            except:
                self.cartella = percorso_creazione + "provv" + os.sep


        self.startframe.pack_forget()

        self.process_window()
        return "break"

    def process_window(self):

        self.process_frame = Frame(self.frame, bg="#151719")
        self.process_frame.pack(fill = BOTH)

        self.space = Label(self.process_frame, height = 3, bg = "#151719")
        self.space.pack()

        self.showImm()

        self.root.bind("<k>", self.keepImm)
        self.root.bind("<d>", self.delImm)
        self.root.bind("<z>", self.annulla)

    def showImm(self):

        self.ima = Image.open(self.path_list[self.c] + self.file_list[self.c])
        self.ima = self.ima.resize((600, 600), Image.ANTIALIAS)
        self.display_img = PhotoImage(self.ima)

        self.img1 = Label(self.process_frame, image = self.display_img, width = 600, height = 600, anchor = CENTER)
        self.img1.image = self.display_img
        self.img1.pack(anchor = CENTER)

        self.counter = Label(self.process_frame, text = "Mancano " + str(self.left - self.c) + " immagini", bg = "#151719", fg = "#f3f3f3")
        self.counter.configure(font = ("Verdana", 15))
        self.counter.pack(side = LEFT)

        self.root.update()

    def keepImm(self, event = None):

        self.previous_image = None
        self.previous_path = None

        os.chdir(self.path_list[self.c])
        copy(self.file_list[self.c], self.cartella)
        #print self.plist[c]
        #print self.flist[c]
        self.c += 1
        if len(self.file_list) > self.c:
            self.img1.pack_forget()
            self.counter.pack_forget()
            self.showImm()
            sleep(0.1)
        else:
            self.process_frame.pack_forget()
            self.root.unbind("<z>")
            self.end_window()

    def delImm(self, event = None):
        if self.previous_path != None:
            os.chdir(self.previous_path)
            os.remove(self.previous_image)
            self.previous_image = None
            self.previous_path = None

        self.previous_image = self.file_list[self.c]
        self.previous_path = self.path_list[self.c]
        self.c += 1

        if len(self.file_list) > self.c:
            self.img1.pack_forget()
            self.counter.pack_forget()
            self.showImm()
            sleep(0.1)
        else:
            self.process_frame.pack_forget()
            self.end_window()

    def annulla(self, event = None):
        if self.end_toggled:
            self.end_toggled = False
            self.end_frame.pack_forget()
            self.process_frame.pack(fill = BOTH)
            self.root.bind("<d>", self.delImm)
            self.root.bind("<k>", self.keepImm)
        else:
            pass
        if self.previous_path != None:
            self.previous_image = None
            self.previous_path = None
            self.c -= 1
            self.img1.pack_forget()
            self.counter.pack_forget()
            self.showImm()
            sleep(0.1)
        else:
            pass

    def end_window(self):
        self.root.unbind("k")
        self.root.unbind("d")

        self.end_toggled = True

        self.end_frame = Frame(self.frame, bg = "#151719")
        self.end_frame.pack()

        self.frtop = Frame(self.end_frame, bg = "#151719")
        self.frtop.pack(fill = X, anchor = N)

        self.frbot = Frame(self.end_frame, bg = "#151719")
        self.frbot.pack(anchor = S)

        self.lbl4 = Label(self.frtop, text = "Vuoi la cartella con le copie delle immagini? ", bg = "#151719", fg = "#f3f3f3")
        self.lbl4.configure(font=("Helvetica", 28))
        self.lbl4.pack()

        self.btn4 = Button(self.frbot, text = "Si", bg = "#151719", fg = "#f3f3f3", width = 10)
        self.btn4.pack(side = LEFT)
        self.btn4.bind("<Button-1>",self.close)


        self.btn5 = Button(self.frbot, text = "No", bg = "#151719", fg = "#f3f3f3", width = 10)
        self.btn5.pack(side = RIGHT)
        self.btn5.bind("<Button-1>",self.close)

    def close(self, event = None):
        os.chdir(self.cartella)
        os.chdir('..')
        rmtree(self.dirname)
        if self.previous_image != None:
            os.chdir(self.previous_path)
            os.remove(self.previous_image)
        exit()
#=======================================================================================================================
#        MAIN
#=======================================================================================================================

win1 = Fullscreen_Window()
win1.start_window()
win1.root.mainloop()
