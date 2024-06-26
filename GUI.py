from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk, filedialog
import json
import re
import GestureWizard
import sys

class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.insert("end", string)
        self.text_space.see("end")

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


        Button(self.root, text="Configurar Gestos", command=self.config).grid(row=0, column=0, padx=5, pady=5)
        Button(self.root, text="Configurar parametros", command=self.parametros).grid(row=1, column=0, padx=5, pady=5)
        Button(self.root, text="Mostrar/Ocultar Cámara", command=self.gw.toggle_mostrar).grid(row=2, column=0, padx=5, pady=5)
        



        self.btn_toggle = Button(self.root, text='Click Me!', image=self.pausa, command=self.toggle_run)
        self.btn_toggle.grid(row=5, column=0, padx=20, pady=20)


        text_widget = tk.Text(self.root, height=4)
        text_widget.grid(row=6,column=0)

        # Redirigir stdout al widget Text
        sys.stdout = StdoutRedirector(text_widget)

        self.root.mainloop()


    def toggle_run(self):
        self.gw.toggle()

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

        
        btn_borrar = ttk.Button(self.labelframe[self.linea], text='X', command = lambda idx = self.linea: self.borrar_accion_vacia(idx)).grid(column=8,row=0,padx=10,pady=10)      

        self.btn_anadir = ttk.Button(self.ventana_gestos,text="+", command=self.anadir)
        self.btn_anadir.grid(column=0, row =self.linea+2, padx =1,pady=1)

        self.btn_guardar = ttk.Button(self.ventana_gestos,text="Guardar", command=self.guardar)
        self.btn_guardar.grid(column=0, row =self.linea+3, padx =1,pady=1)

        
        self.linea+=1

    def aparicion_btn(self,cont):
        btn_seleccion=None
        try:            # En algun momento ha fallado, no se porque por lo que pongo un try
            if (self.accion[cont].get()=="OTRO"):
                btn_seleccion = ttk.Button(self.labelframe[cont], text="Seleccionar archivo", command=lambda:self.seleccionar_archivo(cont)) # Boton de seleccion de path de archivo
                btn_seleccion.grid(column=8, row=1, padx=10, pady=10)
            
        except:
            pass
            

    def parametros(self):
        
        try:    #En caso de que la nueva ventana este abierta, se cierra y reinicia la lista de labelFrames
            self.ventana_parametros.destroy()
        except:
            pass

        self.ventana_parametros = Toplevel(self.root)
        self.ventana_parametros.title("Ventana de configuracion de parametros")
        
        with open("config.json", 'r') as archivo:        # Cargar acciones registradas en JSON
                parametros = json.load(archivo)

        
        Label(self.ventana_parametros, text = "Umbral inicio").grid(column=0,row=0)
        self.umbral_inicio = Entry(self.ventana_parametros,width=20)
        self.umbral_inicio.grid(column=2,row=0)
        self.umbral_inicio.delete(0,tk.END)
        self.umbral_inicio.insert(0, str(parametros['humbral_inicio']))

        
        Label(self.ventana_parametros, text = "Umbral fin").grid(column=0,row=1)
        self.umbral_fin = Entry(self.ventana_parametros,width=20)
        self.umbral_fin.grid(column=2,row=1)
        self.umbral_fin.delete(0,tk.END)
        self.umbral_fin.insert(0, str(parametros['humbral_fin']))
        
        Label(self.ventana_parametros, text = "Confianza minima de deteccion").grid(column=0,row=2)
        self.min_detection_confidence = Entry(self.ventana_parametros,width=20)
        self.min_detection_confidence.grid(column=2,row=2)
        self.min_detection_confidence.delete(0,tk.END)
        self.min_detection_confidence.insert(0, str(parametros['min_detection_confidence']))        
        
        Label(self.ventana_parametros, text = "Confianza minima de trackeo").grid(column=0,row=3)
        self.min_tracking_confidence = Entry(self.ventana_parametros,width=20)
        self.min_tracking_confidence.grid(column=2,row=3)
        self.min_tracking_confidence.delete(0,tk.END)
        self.min_tracking_confidence.insert(0, str(parametros['min_tracking_confidence']))

        btn_guardar_param = ttk.Button(self.ventana_parametros,text="Guardar", command=self.guardar_param)

        btn_guardar_param.grid(column=1,row=4)        
    def guardar_param(self):
        
        new_data = dict()        # El JSON se dumpea desde diccionario
        try:
            new_data['humbral_inicio']=float(self.umbral_inicio.get())
            new_data['humbral_fin']=float(self.umbral_fin.get())
            new_data['min_detection_confidence']=float(self.min_detection_confidence.get())
            new_data['min_tracking_confidence']=float(self.min_tracking_confidence.get())
            
            with open('config.json', 'w') as archivo:
                json.dump(new_data, archivo)
        except Exception as e:
    
            messagebox.showinfo(message="Los valores tienen que ser numeros enteros", title="ADVERTENCIA")
            
            
        self.gw.load()            # Se recargan las acciones del programa de hand-tracking
        self.ventana_parametros.destroy()

        
    def config(self):

        
        try:    #En caso de que la nueva ventana este abierta, se cierra y reinicia la lista de labelFrames
            self.ventana_gestos.destroy()
        except:
            print("Cerrada pestaña abierta")

        self.ventana_gestos = Toplevel(self.root)

        self.ventana_gestos.title("Menu configuracion")
        
        self.mov_dict = {'U':0,'D':1,'L':2,'R':3,'X':4}        # Diccionario para paso de codigo a valor (Usado para seleccionar predeterminado)
        self.acc_dict = {"VOLUP":0,"VOLDOWN":1,"MUTE":2}       # Diccionario para traduccion en seleccion de accion
        
        with open("acciones.json", 'r') as archivo:        # Cargar acciones registradas en JSON
                self.data = json.load(archivo)
                
        self.mostrar_config()
        
    def mostrar_config(self):
  
      
        self.labelframe=[]

        self.scrollbar = tk.Scrollbar(self.ventana_gestos, orient=tk.VERTICAL)
        self.canvas = tk.Canvas(self.ventana_gestos,height=self.ventana_gestos.winfo_screenheight()*2/3, bd=0, highlightthickness=0,yscrollcommand=self.scrollbar.set)


        self.scrollbar.grid(column=1,row=0, sticky="nsew")
        self.canvas.grid(column=0,row=0,sticky="nsew")

        self.scrollbar.config(command=self.canvas.yview)    

        self.labels = ttk.Frame(self.canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.labels,anchor='nw')

        self.labels.bind('<Configure>', self.config_interior)
        self.canvas.bind('<Configure>', self.config_canvas)

        self.pos_dedos = [[None for _ in range(5)] for _ in range(len(self.data))]        # Arrays Nulos donde añadir posiciones, movimientos y acciones
        self.movimiento = [None for _ in range(len(self.data))]
        self.accion = [None for _ in range(len(self.data))]
                
        for i in range(0,len(self.data)):

            self.labelframe.append(ttk.LabelFrame(self.labels, text=f"Accion {i+1}"))
            self.labelframe[i].grid(row=i+1, column=0, padx=10, pady=10)

            pulgar=ttk.Label(self.labelframe[i], text="Dedo pulgar")
            pulgar.grid(column=0, row=0, padx=10, pady=10)

            self.pos_dedos[i][0]=ttk.Combobox(self.labelframe[i],state="readonly",values=["abierto","cerrado"])
            self.pos_dedos[i][0].current(list(self.data.keys())[i][0])
            self.pos_dedos[i][0].grid(column=0, row=1,padx=10,pady=10)


            indice=ttk.Label(self.labelframe[i], text="Dedo indice")
            indice.grid(column=1, row=0, padx=10, pady=10)

            self.pos_dedos[i][1]=ttk.Combobox(self.labelframe[i],state="readonly",values=["abierto","cerrado"])
            self.pos_dedos[i][1].current(list(self.data.keys())[i][1])
            self.pos_dedos[i][1].grid(column=1, row=1,padx=10,pady=10)


            corazon=ttk.Label(self.labelframe[i], text="Dedo corazon")
            corazon.grid(column=2, row=0, padx=10, pady=10)

            self.pos_dedos[i][2]=ttk.Combobox(self.labelframe[i],state="readonly",values=["abierto","cerrado"])
            self.pos_dedos[i][2].current(list(self.data.keys())[i][2])
            self.pos_dedos[i][2].grid(column=2, row=1,padx=10,pady=10)


            anular=ttk.Label(self.labelframe[i], text="Dedo anular")
            anular.grid(column=3, row=0, padx=10, pady=10)

            self.pos_dedos[i][3]=ttk.Combobox(self.labelframe[i],state="readonly",values=["abierto","cerrado"])
            self.pos_dedos[i][3].current(list(self.data.keys())[i][3])
            self.pos_dedos[i][3].grid(column=3, row=1,padx=10,pady=10)


            menique=ttk.Label(self.labelframe[i], text="Dedo meñique")
            menique.grid(column=4, row=0, padx=10, pady=10)

            self.pos_dedos[i][4]=ttk.Combobox(self.labelframe[i],state="readonly",values=["abierto","cerrado"])
            self.pos_dedos[i][4].current(list(self.data.keys())[i][4])
            self.pos_dedos[i][4].grid(column=4, row=1,padx=10,pady=10)



            mov_texto=ttk.Label(self.labelframe[i], text="Movimiento")
            mov_texto.grid(column=5, row=0, padx=20, pady=20)

            self.movimiento[i]=ttk.Combobox(self.labelframe[i],state="readonly",values=["Arriba","Abajo","Izquierda","Derecha","Cualquiera"])
            self.movimiento[i].current(self.mov_dict[list(self.data.keys())[i][5]])
            self.movimiento[i].grid(column=5, row=1,padx=10,pady=10)



            mov_texto=ttk.Label(self.labelframe[i], text="Accion")
            mov_texto.grid(column=7, row=0, padx=20, pady=20)

            self.accion[i]=ttk.Combobox(self.labelframe[i],state="readonly",values=["VOLUP","VOLDOWN","MUTE","OTRO"])
            self.accion[i].bind("<<ComboboxSelected>>", lambda event, arg1=i: self.aparicion_btn(arg1))  # Al seleccionar un valor se llama a la funcion de aparicion de boton de seleccion

            if list(self.data.values())[i] in self.acc_dict.keys():        # Si el valor de la accion i (del JSON) esta dentro del diccionario se pasa del valor seleccionado a su indice
                idx = self.acc_dict[list(self.data.values())[i]]
                
            else:                                                # Si el valor de la accion i no esta dentro del diccionario, es un path, se añade un nuevo valor seleccionable y se selecciona
                self.accion[i]['values'] = self.accion[i]['values'] + (f"{list(self.data.values())[i]}",)
                idx=len(self.accion[i]['values'])-1
                btn_seleccion = ttk.Button(self.labelframe[i], text="Seleccionar archivo", command=lambda idxsel = i:self.seleccionar_archivo(idxsel))
                btn_seleccion.grid(column=8,row=1,padx=10,pady=10)

            btn_borrar = ttk.Button(self.labelframe[i], text='X', command = lambda idx = i: self.borrar_accion(idx)).grid(column=8,row=0,padx=10,pady=10)            
            self.accion[i].current(idx)
            self.accion[i].grid(column=7, row=1,padx=10,pady=10)

        self.linea=len(self.labelframe)            # Añadir botones de guardar y +
      
        self.btn_anadir = ttk.Button(self.ventana_gestos,text="+", command=self.anadir)
        self.btn_anadir.grid(column=0, row =self.linea+1, padx =1,pady=1)

        self.btn_guardar = ttk.Button(self.ventana_gestos,text="Guardar", command=self.guardar)
        self.btn_guardar.grid(column=0, row =self.linea+2, padx =1,pady=1)

 #       self.ventana_gestos.protocol("WM_DELETE_WINDOW", self.mensajito())
        self.ventana_gestos.mainloop()


    def borrar_accion(self,idx):

        self.data.pop(list(self.data.keys())[idx])
       
        self.linea -=1
        

        self.btn_guardar.destroy()
        self.btn_anadir.destroy()

        self.mostrar_config()
        
    def borrar_accion_vacia(self,idx):

        self.labelframe[idx].destroy()
        self.linea-=1
        self.btn_anadir.grid(column=0, row =self.linea+2, padx =1,pady=1)
        self.btn_guardar.grid(column=0, row =self.linea+3, padx =1,pady=1)

        
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
        try:
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

                

                if re.match(r'\d{5}[UDLRX]$',code):        # Se comprueba que el codigo se haya compuesto de 5 digitos y una de las letras validas 
                   
                    try:                                   # Se usa un try porque la accion se puede haber guardado como seleccion del COMBOBOX o como valor en array
                            new_data[code]=self.accion[i].get()        

                    except:
                        if self.accion[i] is not None:
                            new_data[code]=self.accion[i]
        except:
            pass
        
        with open('acciones.json', 'w') as archivo:
            json.dump(new_data, archivo)
            
        self.gw.load()            # Se recargan las acciones del programa de hand-tracking
        self.ventana_gestos.destroy()

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
