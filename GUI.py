from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog
import json
import re
import GestureWizard


class GUI():

    def __init__(self,gw):
        self.linea =0
        self.labelframe = []
        self.gw=gw
        self.pos_dedos = [[]]
        self.movimiento = []
        self.accion = []
        
        
        self.root = Tk()


        self.pausa = PhotoImage(file="pausa.png")
        self.play = PhotoImage(file="play.png")

        self.btn_toggle = Button(self.root, text='Click Me!', image=self.pausa, command=self.toggle_run)
        self.btn_toggle.grid(row=0, column=0, padx=20, pady=20)
        Button(self.root, text="configuracion", command=self.config).grid(row=0, column=1, padx=20, pady=20)

        self.root.mainloop()


    def toggle_run(self):
        self.gw.toggle()
        print("Esto va a cambiar si el programa corre o no")

        current_image = self.btn_toggle['image']

        # Dependiendo de la imagen actual, cambiar a la otra imagen
        if current_image == str(self.play):
            self.btn_toggle.config(image=self.pausa)
        else:
            self.btn_toggle.config(image=self.play)


    def anadir(self):
        self.linea=len(self.labelframe)
        self.btn_anadir.destroy()
        self.btn_guardar.destroy()   

        self.pos_dedos.append([None,None,None,None,None])
        self.movimiento.append(None)
        self.accion.append(None)

        self.labelframe.append(ttk.LabelFrame(self.labels, text=f"Accion {self.linea + 1}"))
        self.labelframe[self.linea].grid(row=self.linea+ 1, column=0, padx=10, pady=10)

        pulgar = ttk.Label(self.labelframe[self.linea], text="Dedo pulgar")
        pulgar.grid(column=0, row=0, padx=10, pady=10)

        self.pos_dedos[self.linea][0] = ttk.Combobox(self.labelframe[self.linea], state="readonly", values=["abierto", "cerrado"])
        self.pos_dedos[self.linea][0].current(0)
        self.pos_dedos[self.linea][0].grid(column=0, row=1, padx=10, pady=10)

        indice = ttk.Label(self.labelframe[self.linea], text="Dedo indice")
        indice.grid(column=1, row=0, padx=10, pady=10)

        self.pos_dedos[self.linea][1] = ttk.Combobox(self.labelframe[self.linea], state="readonly", values=["abierto", "cerrado"])
        self.pos_dedos[self.linea][1].current(0)
        self.pos_dedos[self.linea][1].grid(column=1, row=1, padx=10, pady=10)

        corazon = ttk.Label(self.labelframe[self.linea], text="Dedo corazon")
        corazon.grid(column=2, row=0, padx=10, pady=10)

        self.pos_dedos[self.linea][2] = ttk.Combobox(self.labelframe[self.linea], state="readonly", values=["abierto", "cerrado"])
        self.pos_dedos[self.linea][2].current(0)
        self.pos_dedos[self.linea][2].grid(column=2, row=1, padx=10, pady=10)

        anular = ttk.Label(self.labelframe[self.linea], text="Dedo anular")
        anular.grid(column=3, row=0, padx=10, pady=10)

        self.pos_dedos[self.linea][3] = ttk.Combobox(self.labelframe[self.linea], state="readonly", values=["abierto", "cerrado"])
        self.pos_dedos[self.linea][3].current(0)
        self.pos_dedos[self.linea][3].grid(column=3, row=1, padx=10, pady=10)

        menique = ttk.Label(self.labelframe[self.linea], text="Dedo meñique")
        menique.grid(column=4, row=0, padx=10, pady=10)

        self.pos_dedos[self.linea][4] = ttk.Combobox(self.labelframe[self.linea], state="readonly", values=["abierto", "cerrado"])
        self.pos_dedos[self.linea][4].current(0)
        self.pos_dedos[self.linea][4].grid(column=4, row=1, padx=10, pady=10)

        mov_texto = ttk.Label(self.labelframe[self.linea], text="self.movimiento")
        mov_texto.grid(column=5, row=0, padx=20, pady=20)

        self.movimiento[self.linea] = ttk.Combobox(self.labelframe[self.linea], state="readonly",
                                     values=["Arriba", "Abajo", "Izquierda", "Derecha", "Cualquiera"])
        self.movimiento[self.linea].grid(column=5, row=1, padx=10, pady=10)

        mov_texto = ttk.Label(self.labelframe[self.linea], text="self.accion")
        mov_texto.grid(column=7, row=0, padx=20, pady=20)

        self.accion[self.linea] = ttk.Combobox(self.labelframe[self.linea], state="readonly", values=["VOLUP", "VOLDOWN", "MUTE","OTRO"])
        self.accion[self.linea].bind("<<ComboboxSelected>>", lambda event, arg1=self.linea: self.aparicion_btn(arg1))  # Al seleccionar un valor se llama a la funcion de aparicion de boton de seleccion

        self.accion[self.linea].grid(column=7, row=1, padx=10, pady=10)


        self.btn_anadir = ttk.Button(self.newWindow,text="+", command=self.anadir)
        self.btn_anadir.grid(column=0, row =self.linea+2, padx =1,pady=1)

        self.btn_guardar = ttk.Button(self.newWindow,text="Guardar", command=self.guardar)
        self.btn_guardar.grid(column=2, row =self.linea+1, padx =1,pady=1)

    def aparicion_btn(self,cont):
        btn_seleccion=None
        try:            # En algun momento ha fallado, no se porque por lo que pongo un try
            if (self.accion[cont].get()=="OTRO"):
                btn_seleccion = ttk.Button(self.labelframe[cont], text="Seleccionar archivo", command=lambda:self.seleccionar_archivo(cont)) # Boton de seleccion de path de archivo
                btn_seleccion.grid(column=8, row=1, padx=10, pady=10)
            else:
                print("DESTRUIR\n")
        except:
            print("error")

    def config(self):

        try:    #En caso de que la nueva ventana este abierta, se cierra y reinicia la lista de labelFrames
            self.newWindow.destroy()
            self.labelframe=[]
        except:
            print("Cerrada pestaña abierta")


        mov_dict = {'U':0,'D':1,'L':2,'R':3,'X':4}        # Diccionario para paso de codigo a valor (Usado para seleccionar predeterminado)
        acc_dict = {"VOLUP":0,"VOLDOWN":1,"MUTE":2}       # Diccionario para traduccion en seleccion de accion 
     

        self.newWindow = Toplevel(self.root)

        self.newWindow.title("Menu configuracion")
      

        self.scrollbar = tk.Scrollbar(self.newWindow, orient=tk.VERTICAL)
        self.canvas = tk.Canvas(self.newWindow,height=self.newWindow.winfo_screenheight()*2/3, bd=0, highlightthickness=0,yscrollcommand=self.scrollbar.set)


        self.scrollbar.grid(column=1,row=0, sticky="nsew")
        self.canvas.grid(column=0,row=0,sticky="nsew")

        self.scrollbar.config(command=self.canvas.yview)    

        self.labels = ttk.Frame(self.canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.labels,anchor='nw')

        self.labels.bind('<Configure>', self.config_interior)
        self.canvas.bind('<Configure>', self.config_canvas)

        with open("acciones.json", 'r') as archivo:        # Cargar acciones registradas en JSON
                data = json.load(archivo)

        self.pos_dedos = [[None for _ in range(5)] for _ in range(len(data))]        # Arrays Nulos donde añadir posiciones, movimientos y acciones
        self.movimiento = [None for _ in range(len(data))]
        self.accion = [None for _ in range(len(data))]

        for i in range(0,len(data)):

            self.labelframe.append(ttk.LabelFrame(self.labels, text=f"Accion {i+1}"))
            self.labelframe[i].grid(row=i+1, column=0, padx=10, pady=10)

            pulgar=ttk.Label(self.labelframe[i], text="Dedo pulgar")
            pulgar.grid(column=0, row=0, padx=10, pady=10)

            self.pos_dedos[i][0]=ttk.Combobox(self.labelframe[i],state="readonly",values=["abierto","cerrado"])
            self.pos_dedos[i][0].current(list(data.keys())[i][0])
            self.pos_dedos[i][0].grid(column=0, row=1,padx=10,pady=10)


            indice=ttk.Label(self.labelframe[i], text="Dedo indice")
            indice.grid(column=1, row=0, padx=10, pady=10)

            self.pos_dedos[i][1]=ttk.Combobox(self.labelframe[i],state="readonly",values=["abierto","cerrado"])
            self.pos_dedos[i][1].current(list(data.keys())[i][1])
            self.pos_dedos[i][1].grid(column=1, row=1,padx=10,pady=10)


            corazon=ttk.Label(self.labelframe[i], text="Dedo corazon")
            corazon.grid(column=2, row=0, padx=10, pady=10)

            self.pos_dedos[i][2]=ttk.Combobox(self.labelframe[i],state="readonly",values=["abierto","cerrado"])
            self.pos_dedos[i][2].current(list(data.keys())[i][2])
            self.pos_dedos[i][2].grid(column=2, row=1,padx=10,pady=10)


            anular=ttk.Label(self.labelframe[i], text="Dedo anular")
            anular.grid(column=3, row=0, padx=10, pady=10)

            self.pos_dedos[i][3]=ttk.Combobox(self.labelframe[i],state="readonly",values=["abierto","cerrado"])
            self.pos_dedos[i][3].current(list(data.keys())[i][3])
            self.pos_dedos[i][3].grid(column=3, row=1,padx=10,pady=10)


            menique=ttk.Label(self.labelframe[i], text="Dedo meñique")
            menique.grid(column=4, row=0, padx=10, pady=10)

            self.pos_dedos[i][4]=ttk.Combobox(self.labelframe[i],state="readonly",values=["abierto","cerrado"])
            self.pos_dedos[i][4].current(list(data.keys())[i][4])
            self.pos_dedos[i][4].grid(column=4, row=1,padx=10,pady=10)



            mov_texto=ttk.Label(self.labelframe[i], text="self.movimiento")
            mov_texto.grid(column=5, row=0, padx=20, pady=20)

            self.movimiento[i]=ttk.Combobox(self.labelframe[i],state="readonly",values=["Arriba","Abajo","Izquierda","Derecha","Cualquiera"])
            self.movimiento[i].current(mov_dict[list(data.keys())[i][5]])
            self.movimiento[i].grid(column=5, row=1,padx=10,pady=10)



            mov_texto=ttk.Label(self.labelframe[i], text="self.accion")
            mov_texto.grid(column=7, row=0, padx=20, pady=20)

            self.accion[i]=ttk.Combobox(self.labelframe[i],state="readonly",values=["VOLUP","VOLDOWN","MUTE","OTRO"])
            self.accion[i].bind("<<ComboboxSelected>>", lambda event, arg1=i: self.aparicion_btn(arg1))  # Al seleccionar un valor se llama a la funcion de aparicion de boton de seleccion

            if list(data.values())[i] in acc_dict.keys():        # Si el valor de la accion i (del JSON) esta dentro del diccionario se pasa del valor seleccionado a su indice
                idx = acc_dict[list(data.values())[i]]
                
            else:                                                # Si el valor de la accion i no esta dentro del diccionario, es un path, se añade un nuevo valor seleccionable y se selecciona
                self.accion[i]['values'] = self.accion[i]['values'] + (f"{list(data.values())[i]}",)
                idx=len(self.accion[i]['values'])-1
                btn_seleccion = ttk.Button(self.labelframe[i], text="Seleccionar archivo", command=lambda idxsel = i:self.seleccionar_archivo(idxsel))
                btn_seleccion.grid(column=8,row=1,padx=10,pady=10)

            self.accion[i].current(idx)
            self.accion[i].grid(column=7, row=1,padx=10,pady=10)

        self.linea=len(self.labelframe)            # Añadir botones de guardar y +

        self.btn_anadir = ttk.Button(self.newWindow,text="+", command=self.anadir)
        self.btn_anadir.grid(column=0, row =self.linea+1, padx =1,pady=1)

        self.btn_guardar = ttk.Button(self.newWindow,text="Guardar", command=self.guardar)
        self.btn_guardar.grid(column=2, row =self.linea+1, padx =1,pady=1)

 #       self.newWindow.protocol("WM_DELETE_WINDOW", self.mensajito())
        self.newWindow.mainloop()


    def seleccionar_archivo(self,i):
        ruta_archivo = filedialog.askopenfilename()
        if ruta_archivo is not None:
            print(f"Ruta_archivo de elemento {i}: {ruta_archivo}")
            #self.accion[i]=ruta_archivo
            self.accion[i]['values'] = self.accion[i]['values'] + (f"{ruta_archivo}",)
            idx=len(self.accion[i]['values'])-1
            self.accion[i].current(idx)
            self.accion[i].grid(column=7, row=1,padx=10,pady=10)



    def guardar(self):
        
        new_data = dict()        # El JSON se dumpea desde diccionario
        for i in range(len(self.pos_dedos)):                # Se recorren los arrays |||| SE PUEDE CAMBIAR EL LEN(...) POR SELF.LINEA
            code =""
            for j in range(len(self.pos_dedos[i])):         # Una vuelta por cada dedo
                if(self.pos_dedos[i][j].get()=='abierto'):
                    code+='0'
                else:
                    code+='1'

            if (self.movimiento[i].get() == 'Arriba'):
                code+='U'
            elif (self.movimiento[i].get() == 'Abajo'):
                code+='D'
            elif (self.movimiento[i].get() == 'Izquierda'):
                code+='L'
            elif (self.movimiento[i].get() == 'Derecha'):
                code+='R'
            elif (self.movimiento[i].get() == 'Cualquiera'):
                code+='X'

            print(code)

            if re.match(r'\d{5}[UDLRX]$',code):        # Se comprueba que el codigo se haya compuesto de 5 digitos y una de las letras validas 
                print("Este lo guardo\n")
                try:                                   # Se usa un try porque la accion se puede haber guardado como seleccion del COMBOBOX o como valor en array
                        new_data[code]=self.accion[i].get()        

                except:
                    if self.accion[i] is not None:
                        new_data[code]=self.accion[i]

        with open('acciones.json', 'w') as archivo:
            json.dump(new_data, archivo)
            
        self.gw.load()            # Se recargan las acciones del programa de hand-tracking
        self.newWindow.destroy()

    def config_interior(self, event):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.labels.winfo_reqwidth(), self.labels.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.labels.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width=self.labels.winfo_reqwidth())

    def config_canvas(self,event):
        if self.labels.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())