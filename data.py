import tkinter.messagebox
from functools import partial
import tkinter as tk
from functions import *
from tkinter import filedialog 
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import ttk

class Application(tk.Tk):

    def __init__(self):
        
        tk.Tk.__init__(self)
        self.geometry("1024x720")
        self.create_widget()
        self.v=tk.IntVar()
        self.mainFunc()
        


    def create_widget(self):

        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)


        self.menu1 = tk.Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Fichier",menu=self.menu1)


        """Titre"""
        self.champ_titre=tk.Label(self,text="Data Visualisation",padx="10",pady="10")
        self.champ_titre.config(font=("Courier", 44))
        self.champ_titre.pack(side="top")
        
        self.main=tk.Frame(self)
        self.main.pack()


    def browseFiles(self): 
        global filename
        filename = filedialog.askopenfilename(initialdir = "/", 
                                            title = "Select a File", 
                                            filetypes = (("CSV files", 
                                                            "*.csv*"), 
                                                        ("all files", 
                                                            "*.*"))) 
        self.openedFileLabel.configure(text=filename.split("/")[-1])
        self.runImportFrame()


    def mainFunc(self):    
        
        for widget in self.main.winfo_children():
            widget.forget()

        tk.Button(self.main,text="Selectionner un fichier",command=self.browseFiles,padx=10).grid(row=0,column=0)
        self.openedFileLabel=tk.Label(self.main,padx=10)
        self.openedFileLabel.grid(row=0,column=1)

    def runImportFrame(self):
        tk.Label(self.main,text="Choisissez un séparateur :",padx=10,pady=10).grid(row=1,column=0)
        self.sepVar=tk.StringVar()
        self.separatorEntry=tk.Entry(self.main,textvariable=self.sepVar)
        self.separatorEntry.grid(row=1,column=1)

        tk.Button(self.main,text="Lancer l'importation",padx=10,command=self.runImport).grid(row=1,column=3)
        
        

    def runImport(self):
        try:
            sep=self.sepVar.get()
            sep=str(sep)
            self.dataFrame=getDataSet(filename,sep)
            self.displayOperationWindow()
            
        except:
            msg="Veuillez saisir un separateur valide"
            tkinter.messagebox.showinfo( "Erreur", msg)

    def displayDataFrame(self):

        self.newWindow = tk.Toplevel(self) 
        self.newWindow.title("New Window") 
        self.newWindow.geometry("1024x620") 
        pd.set_option('display.max_rows', None)
        self.text = tk.Text(self.newWindow)
        self.text.insert(tk.END, str(self.dataFrame))
        self.text.pack(fill = "both",expand = True)

    def displayColumnList(self):

        self.newWindow = tk.Toplevel(self) 
        self.newWindow.title("New Window") 
        self.newWindow.geometry("1024x620") 
        pd.set_option('display.max_rows', None)
        self.text = tk.Text(self.newWindow)
        self.text.insert(tk.END, str(self.dataFrame.columns))
        self.text.pack(fill = "both",expand = True)

    def encodeColumns(self):

        self.newWindow = tk.Toplevel(self) 
        self.newWindow.title("New Window") 
        self.newWindow.geometry("1024x620") 
        tk.Label(self.newWindow,text="Choisissez les colonnes a encoder").pack()
        self.listbox=tk.Listbox(self.newWindow,selectmode="multiple")
        for i in range(len(self.dataFrame.columns.values)):
            self.listbox.insert(i+1,self.dataFrame.columns.values[i])

        self.listbox.pack()
        tk.Button(self.newWindow,text="Lancer l'encodage",command=self.runEncoding).pack()

    def runEncoding(self):
        try:
            self.dataFrame=encodeColumns(self.dataFrame,[self.listbox.get(i) for i in self.listbox.curselection()])
            self.newWindow.destroy()
            self.displayDataFrame()
        except:
            msg="Veuillez saisir des colonnes valide"
            tkinter.messagebox.showinfo( "Erreur", msg)
      
    def scaleColumns(self):

        self.newWindow = tk.Toplevel(self) 
        self.newWindow.title("New Window") 
        self.newWindow.geometry("1024x620") 
        tk.Label(self.newWindow,text="Choisissez les colonnes a scaler").pack()
        self.listbox=tk.Listbox(self.newWindow,selectmode="multiple")
        for i in range(len(self.dataFrame.columns.values)):
            self.listbox.insert(i+1,self.dataFrame.columns.values[i])

        self.listbox.pack()
        tk.Button(self.newWindow,text="Lancer le scaling",command=self.runScaling).pack()

    def runScaling(self):
        try:
            self.dataFrame=scaleFeatures(self.dataFrame,[self.listbox.get(i) for i in self.listbox.curselection()])
            self.newWindow.destroy()
            self.displayDataFrame()
        except:
            msg="Veuillez saisir des colonnes valide"
            tkinter.messagebox.showinfo( "Erreur", msg)

    def runNanSearch(self):
        try:
            self.dataFrame=transformNan(self.dataFrame)
            
            self.displayDataFrame()
        except:
            msg="Veuillez saisir des colonnes valide"
            tkinter.messagebox.showinfo( "Erreur", msg)

    def plotFrame(self):
        self.newWindow = tk.Toplevel(self) 
        self.newWindow.title("New Window") 
        self.newWindow.geometry("1024x620") 
        tk.Label(self.newWindow,text="Choisissez X").grid(row=0,column=0)
        tk.Label(self.newWindow,text="Choisissez Y").grid(row=0,column=1)
        self.listboxX=ttk.Combobox(self.newWindow,value=self.dataFrame.columns.values)
        self.listboxY=ttk.Combobox(self.newWindow,value=self.dataFrame.columns.values)

      
        self.listboxX.grid(row=1,column=0)
        self.listboxY.grid(row=1,column=1)
        tk.Button(self.newWindow,text="Lancer le tracé de graphique",command=self.runPloting).grid(row=2,column=1)

    def runPloting(self):
        try:
            x=self.listboxX.get().replace("'","")
            y=self.listboxY.get().replace("'","")
            plt.plot(self.dataFrame[x],self.dataFrame[y],"ro")
        
            plt.show()
        
            
        except:
            msg="Veuillez saisir des colonnes valide"
            tkinter.messagebox.showinfo( "Erreur", msg)


    def displayOperationWindow(self):
        self.operationFrame=tk.Frame(self)
        self.operationFrame.pack()
        tk.Button(self.operationFrame,text="Afficher le dataframe",padx=10,command=self.displayDataFrame).grid(row=0,column=0)
        tk.Button(self.operationFrame,text="Afficher la liste des colonnes",padx=10,command=self.displayColumnList).grid(row=0,column=1)
        tk.Button(self.operationFrame,text="Encoder les colonnes",padx=10,command=self.encodeColumns).grid(row=0,column=2)
        tk.Button(self.operationFrame,text="Supprimer les valeurs manquantes",padx=10,command=self.runNanSearch).grid(row=0,column=3)
        tk.Button(self.operationFrame,text="Scale Features",padx=10,command=self.scaleColumns).grid(row=0,column=4)
        tk.Button(self.operationFrame,text="Graphiques",padx=10,command=self.plotFrame).grid(row=1,column=0)
        


app=Application()
app.mainloop()
        

