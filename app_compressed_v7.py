import os
from shutil import copy, rmtree
from Tkinter import *
from PIL.ImageTk import PhotoImage
import PIL.Image
import sys
#=======================================================================================================================
class Fullscreen_Window:
	path_list = [];file_list = [];c = 0;left = 0;end_toggled = False;extensions = [".jpg" , ".gif", ".png", ".jpeg", ".tif", ".tiff", ".bmp", ".eps"];prevdel = False;in_progress = False;del_vector = []
#-----------------------------------------------------------------------------------------------------------------------
#		Error Catching Method
	def catchErr(self, error):
		try:
			try:os.chdir(os.environ["HOME"])
			except:os.chdir(os.environ["HOMEPATH"])
			with open("error.txt","w+") as file:file.write(error)
			sys.exit()
		except:print error;sys.exit()
#-----------------------------------------------------------------------------------------------------------------------
#       Inizializzazione
	def __init__(self):
		try:
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
			self.root.protocol("WM_DELETE_WINDOW", self.closeEvent)
		except Exception as err:self.catchErr(err)
#-----------------------------------------------------------------------------------------------------------------------
#       Funzione per mettere la finestra a schermo intero
	def toggle_fullscreen(self, event=None):
		try:self.state = not self.state;self.root.attributes("-fullscreen", self.state);return "break"
		except Exception as err:self.catchErr(err)

	def end_fullscreen(self, event=None):
		try:self.state = False;self.root.attributes("-fullscreen", False);return "break"
		except Exception as err:self.catchErr(err)
#-----------------------------------------------------------------------------------------------------------------------
#       Inizializzazione schermata iniziale
	def start_window(self):
		try:
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
			self.txt3 = Entry(self.startframe, bg = "#173f5f", fg = "#f3f3f3")
			self.txt3.pack()
			self.lbl2 = Label(self.startframe, text = "Nome della cartella in cui salvare una copia delle immagini:", bg = "#151719", fg = "#f3f3f3")
			self.lbl2.pack()
			self.txt2 = Entry(self.startframe,  bg = "#173f5f", fg = "#f3f3f3")
			self.txt2.pack()
			self.lbl1 = Label(self.startframe, text = "Dove salvo questa cartella?", bg = "#151719", fg = "#f3f3f3")
			self.lbl1.pack()
			self.txt1 = Entry(self.startframe,  bg = "#173f5f", fg = "#f3f3f3")
			self.txt1.pack()
			self.btn3 = Button(self.startframe, text = "Start", height = 2, width = 20, bg = "#173f5f", fg = "#f3f3f3", relief = FLAT, cursor = "hand2")
			self.btn3.configure(font = ("Verdana", 12))
			self.btn3.pack(pady = 10, padx = 5)
			self.btn3.bind('<Button-1>',self.start)
		except Exception as err:self.catchErr(err)
#-----------------------------------------------------------------------------------------------------------------------
#       Analisi e ricerca immagini, creazione cartella di salvataggio provvisorio
	def start(self, event=None):
		try:
			try:
				self.rootdir = "C:/"
				os.chdir(self.rootdir)
				if self.txt3.get():
					if self.txt3.get().startswith("C:/") or self.txt3.get().startswith("C:\\") or self.txt3.get().startswith("c:\\") or self.txt3.get().startswith("c:/"):
						if self.txt3.get().endswith("/") or  self.txt3.get().endswith("\\"):self.rootdir = self.txt3.get()
						else:self.rootdir = self.txt3.get() + os.sep
					else:pass
				else:pass
			except:
				self.rootdir = "/"
				if self.txt3.get():
					if self.txt3.get().startswith("/") or self.txt3.get().startswith("\\") or self.txt3.get().startswith("\\") or self.txt3.get().startswith("/"):
					   if self.txt3.get().endswith("/") or  self.txt3.get().endswith("\\"):self.rootdir = self.txt3.get()
					   else:self.rootdir = self.txt3.get() + os.sep
					else:pass
				else:pass
			for path, dirname, filelist in os.walk(self.rootdir):
				for name in filelist:
					for ext in self.extensions:
						if name.endswith(ext):
							if path.endswith('\\'):self.path_list.append(path)
							else:self.path_list.append(path + os.sep)
							self.file_list.append([name,False])
							self.left += 1
						else:pass
			try:
				percorso_creazione = os.path.join(os.environ["HOMEPATH"], "Desktop")
				if self.txt1.get():
					if self.txt1.get().startswith("C:/") or self.txt1.get().startswith("C:\\") or self.txt1.get().startswith("c:\\") or self.txt1.get().startswith("c:/"):
						if self.txt1.get().endswith("/") or  self.txt1.get().endswith("\\"):percorso_creazione = self.txt1.get()
						else:percorso_creazione = self.txt1.get() + os.sep
					else:pass
				else:pass
			except:
				percorso_creazione = os.path.join(os.environ["HOME"], "Desktop")
				if self.txt1.get():
					if self.txt1.get().startswith("/") or self.txt1.get().startswith("\\") or self.txt1.get().startswith("\\") or self.txt1.get().startswith("/"):
						if self.txt1.get().endswith("/") or  self.txt1.get().endswith("\\"):percorso_creazione = self.txt1.get()
						else:percorso_creazione = self.txt1.get() + os.sep
					else:pass
				else:pass
			os.chdir(percorso_creazione)
			if self.txt2.get():
				self.dirname = self.txt2.get()
				try:os.mkdir(self.dirname);self.cartella = percorso_creazione + os.sep + self.dirname + os.sep
				except:self.cartella = percorso_creazione + os.sep + self.dirname + os.sep
			else:
				self.dirname = "provv"
				try:os.mkdir("provv");self.cartella = percorso_creazione + os.sep + "provv" + os.sep
				except:self.cartella = percorso_creazione + os.sep + "provv" + os.sep
			self.startframe.place_forget()
			try:os.chdir(os.environ["HOMEPATH"])
			except:os.chdir(os.environ["HOME"])
			try:
				with open("sorter_progress.txt") as file: self.c = int(file.read())
				with open("sorter_progress_files.txt") as file:del_list = file.readlines()
				i = 0
				for name in del_list:
					if name.endswith("\n"):del_list[i] = name[:-1]
					i += 1
				i = 0
				with open("sorter_progress_paths.txt") as file: path_del_list = file.readlines()
				for name in path_del_list:
					if name.endswith("\n"): path_del_list[i] = name[:-1]
					i += 1
				with open("sorter_progress.txt","w+") as file:file.write(str(self.c))
				del i
				try:
					for i in range(self.c):
						self.del_vector.append((del_list[i], path_del_list[i]))
				except:pass
			except:
				with open("sorter_progress.txt","w+") as file:file.write(str(self.c))
			try:
				for file in self.file_list:
					for deleted in self.del_vector:
						if file[0] == deleted[0]:file[1] = True
			except:pass
			self.process_window()
			return "break"
		except Exception as err:self.catchErr(err)
#-----------------------------------------------------------------------------------------------------------------------
#       Inizializzazione schermata di lavoro
	def process_window(self):
		try:
			self.process_frame = Frame(self.frame, bg="#151719")
			self.process_frame.pack(fill = BOTH, expand = 1)
			self.space = Label(self.process_frame, height = 40, bg = "#151719")
			self.space.pack(fill = BOTH)
			self.showImm()
			self.root.bind("<k>", self.keepImm)
			self.root.bind("<d>", self.delImm)
			self.root.bind("<z>", self.annulla)
			self.root.bind("<Configure>", self.resize)
		except Exception as err:self.catchErr(err)
#-----------------------------------------------------------------------------------------------------------------------
#		Metodo di ridimensionamento degli oggetti nella finestra
	def resize(self, event):
		try:self.root.unbind("<Configure>");self.showImm()
		except Exception as err:self.catchErr(err)
#-----------------------------------------------------------------------------------------------------------------------
#       Metodo per mostrare un'immagine
	def showImm(self):
		try:
			hprop = self.root.winfo_height() / 740.0
			wprop = self.root.winfo_width() / 1366.0
			if self.root.winfo_height() > self.root.winfo_width(): prop = wprop
			else: prop = hprop
			if self.file_list[self.c][1]==True:color = "#b80f0a"
			else:color = "#0b6623"
			try:self.img1.pack_forget();self.counter.pack_forget();self.extButton.pack_forget();self.show_is_deleted.pack_forget()
			except:pass
			self.show_is_deleted = Canvas(self.space, bg = "#151719", height = int(40.0 * prop), width = int(40.0 * prop), bd=0, highlightthickness=0, relief='ridge')
			self.show_is_deleted.create_oval(0, 0, int (40.0 * prop), int (40.0 * prop), fill=color)
			self.show_is_deleted.pack(anchor = CENTER, pady = int(20.0 * prop))
			self.ima = PIL.Image.open(self.path_list[self.c] + self.file_list[self.c][0])
			width, height = self.ima.size
			if width < 2*height:width = int(((500/float(height))*float(width))*prop);height = int(500.0 * prop)
			else:height = int(((1000/float(width))*float(height))*prop);width = int(1000.0 * prop)
			self.ima = self.ima.resize((width, height), PIL.Image.ANTIALIAS)
			self.display_img = PhotoImage(self.ima)
			self.img1 = Label(self.process_frame, image = self.display_img, width = int(1000.0 * prop), height = (500.0 * prop), anchor = CENTER, bg = "#151719")
			self.img1.image = self.display_img
			self.img1.pack(anchor = CENTER, pady = int(20.0 * prop))
			self.counter = Label(self.process_frame, text = "Immgine " + str(self.c+1) + " su " + str(self.left), bg = "#151719", fg = "#f3f3f3")
			self.counter.configure(font = ("Verdana", int(15.0 * prop)))
			self.counter.pack(side = LEFT)
			self.extButton = Button(self.process_frame, bg = "#173f5f", fg = "#f3f3f3", text = "Salva ed esci", height = int(2.0 * prop), width = int(20.0 * prop), relief = FLAT, cursor = "hand2")
			self.extButton.pack(side = RIGHT, pady = int(10.0 * prop), padx = int(10.0*prop))
			self.extButton.configure(font = ("Verdana", int(15.0 * prop)))
			self.extButton.bind('<Button-1>',self.closeEvent)
			self.root.update()
			self.root.bind("<Configure>", self.resize)
		except Exception as err:self.catchErr(err)
#-----------------------------------------------------------------------------------------------------------------------
#       Metodo per salvare l'immagine corrente
	def keepImm(self, event = None):
		try:
			self.prevdel = False
			self.file_list[self.c][1]=False
			os.chdir(self.path_list[self.c])
			copy(self.file_list[self.c][0], self.cartella)
			self.c += 1
			try:os.chdir(os.environ["HOMEPATH"])
			except:os.chdir(os.environ["HOME"])
			with open("sorter_progress.txt","w+") as file:file.write(str(self.c))
			if len(self.file_list) > self.c:self.showImm()
			else:self.process_frame.pack_forget();self.end_window()
		except Exception as err:self.catchErr(err)

#-----------------------------------------------------------------------------------------------------------------------
#       Metodo per eliminare l'immagine corrente
	def delImm(self, event = None):
		try:
			self.prevdel = True
			self.file_list[self.c][1] = True
			self.del_vector.append((self.file_list[self.c][0],self.path_list[self.c]))
			self.c += 1
			try:os.chdir(os.environ["HOMEPATH"])
			except:os.chdir(os.environ["HOME"])
			with open("sorter_progress.txt","w+") as file:file.write(str(self.c))
			if len(self.file_list) > self.c:	self.showImm()
			else:self.process_frame.pack_forget();self.end_window()
		except Exception as err:self.catchErr(err)
#-----------------------------------------------------------------------------------------------------------------------
#       Metodo per tornare indietro di un'immagine nel caso di erronea eliminazione da parte dell'utente
	def annulla(self, event = None):
		try:
			if self.c > 0:
				if self.end_toggled:
					self.end_toggled = False
					self.end_frame.pack_forget()
					self.process_frame.pack(fill = BOTH)
					self.root.bind("<d>", self.delImm)
					self.root.bind("<k>", self.keepImm)
					self.root.bind("<Configure>", self.resize)
				else:pass
				if self.file_list[self.c-1][1] == True:del self.del_vector[-1]
				self.c -= 1
				try:os.chdir(os.environ["HOMEPATH"])
				except:os.chdir(os.environ["HOME"])
				with open("sorter_progress.txt","w+") as file:file.write(str(self.c))
				self.showImm()
		except Exception as err:self.catchErr(err)
#-----------------------------------------------------------------------------------------------------------------------
#       Inizializzazione schermata finale
	def end_window(self):
		try:
			self.root.unbind("k")
			self.root.unbind("d")
			self.root.unbind("<Configure>")
			self.end_toggled = True
			self.end_frame = Frame(self.frame, bg = "#151719")
			self.end_frame.pack()
			self.frtop = Frame(self.end_frame, bg = "#151719")
			self.frtop.pack(fill = X, anchor = N)
			self.frbot = Frame(self.end_frame, bg = "#151719")
			self.frbot.pack(anchor = S)
			self.lbl4 = Label(self.frtop, text = "Vuoi conservare la cartella con le copie delle immagini? ", bg = "#151719", fg = "#f3f3f3")
			self.lbl4.configure(font=("Helvetica", 24))
			self.lbl4.pack(pady = 50)
			self.btn4 = Button(self.frbot,  bg = "#173f5f", fg = "#f3f3f3", text = "Si", height = 2, width = 20, relief = FLAT, cursor = "hand2")
			self.btn4.configure(font=("Helvetica", 20))
			self.btn4.pack(side = LEFT, padx = 20)
			self.btn4.bind("<Button-1>",self.salva)
			self.btn5 = Button(self.frbot, bg = "#173f5f", fg = "#f3f3f3", text = "No", height = 2, width = 20, relief = FLAT, cursor = "hand2")
			self.btn5.configure(font=("Helvetica", 20))
			self.btn5.pack(side = RIGHT, padx = 20)
			self.btn5.bind("<Button-1>",self.close)
		except Exception as err:self.catchErr(err)
#-----------------------------------------------------------------------------------------------------------------------
#       Eliminazione della cartella provvisoria per il backup delle immagini e chiusura del programma
	def close(self, event = None):
		try:
			try:
				for i in range(len(self.del_vector)):os.chdir(self.del_vector[i][1]);os.remove(self.del_vector[i][0])
			except:pass
			try:os.chdir(self.cartella);os.chdir('..');rmtree(self.dirname)
			except:pass
			try:
				try:os.chdir(os.environ["HOMEPATH"])
				except:os.chdir(os.environ["HOME"])
				os.remove("sorter_progress.txt")
				try:os.remove("sorter_progress_files.txt");os.remove("sorter_progress_paths.txt")
				except:pass
			except:pass
			sys.exit()
		except Exception as err:self.catchErr(err)
#-----------------------------------------------------------------------------------------------------------------------
#       Conserva la cartella provvisoria per il backup delle immagini e chiusura del programma
	def salva(self, event = None):
		try:
			for i in range(len(self.del_vector)):os.chdir(self.del_vector[i][1]);os.remove(self.del_vector[i][0])
			try:os.chdir(os.environ["HOMEPATH"])
			except:os.chdir(os.environ["HOME"])
			os.remove("sorter_progress.txt")
			try:os.remove("sorter_progress_files.txt");os.remove("sorter_progress_paths.txt")
			except:pass
			sys.exit()
		except Exception as err:self.catchErr(err)
#-----------------------------------------------------------------------------------------------------------------------
#       Cosa fare nel caso di chiusura inaspettata della finestra
	def closeEvent(self, event=None):
		try:
			if event == None:
				try:os.chdir(self.cartella);os.chdir('..');rmtree(self.dirname)
				except:
					try:
						try:os.chdir(os.environ["HOMEPATH"])
						except:os.chdir(os.environ["HOME"])
						rmtree("provv")
					except:pass
				try:
					try:os.chdir(os.environ["HOMEPATH"])
					except:os.chdir(os.environ["HOME"])
					os.remove("sorter_progress.txt")
					try:os.remove("sorter_progress_files.txt");os.remove("sorter_progress_paths.txt")
					except:pass
				except:pass
			else:
				with open("sorter_progress_files.txt","w+") as file:
					for name in self.del_vector:file.write(name[0]+"\n")
				with open("sorter_progress_paths.txt","w+") as file:
					for name in self.del_vector:file.write(name[1]+"\n")
			sys.exit()
		except Exception as err:self.catchErr(err)
#=======================================================================================================================
#        MAIN
#=======================================================================================================================
win1 = Fullscreen_Window()
win1.start_window()
win1.root.mainloop()