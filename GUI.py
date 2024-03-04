from tkinter import *
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
        print(f"Linea {self.linea}")
    
        self.btn_anadir.destroy()
        self.btn_guardar.destroy()

        self.pos_dedos.append([None,None,None,None,None])
        print(f"pos {len(self.pos_dedos)}")
        self.movimiento.append(None)
        self.accion.append(None)

        self.labelframe.append(ttk.LabelFrame(self.newWindow, text=f"Accion {self.linea + 1}"))
        self.labelframe[self.linea].grid(row=self.linea+ 2, column=0, padx=10, pady=10)

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
        self.accion[self.linea].bind("<<ComboboxSelected>>", lambda event, arg1=self.linea: self.aparicion_btn(arg1))

        self.accion[self.linea].grid(column=7, row=1, padx=10, pady=10)


        self.btn_anadir = ttk.Button(self.newWindow,text="+", command=self.anadir)
        self.btn_anadir.grid(column=0, row =self.linea+3, padx =1,pady=1)

        self.btn_guardar = ttk.Button(self.newWindow,text="Guardar", command=self.guardar)
        self.btn_guardar.grid(column=2, row =self.linea+1, padx =1,pady=1)

        self.linea+=1

    def aparicion_btn(self,cont):
        btn_seleccion=None
        try:
            if (self.accion[cont].get()=="OTRO"):
                btn_seleccion = ttk.Button(self.labelframe[cont], text="Seleccionar archivo", command=lambda:self.seleccionar_archivo(cont))
                btn_seleccion.grid(column=8, row=1, padx=10, pady=10)
            else:
                print("DESTRUIR\n")
                btn_seleccion.destroy()
        except:
            print("error")

    def delete(self,i):
        print(self.linea)
        print(i)
        try:

            self.linea-=1
            print(self.linea)
            self.data.pop(list(self.data.keys())[i])
            self.pos_dedos.pop(i)
            self.movimiento.pop(i)
            self.accion.pop(i)

            self.labelframe[i].destroy()
            
        except Exception as error:
            print("Error borrando: ",error)
    
    def config(self):

        try:
            self.newWindow.destroy()
            self.labelframe=[]
        except:
            print("Cerrada pestaña abierta")


        # Toplevel object which will
        # be treated as a new window

        self.newWindow = Toplevel(self.root)

        # sets the title of the
        # Toplevel widget

        self.newWindow.title("New Window")

        # sets the geometry of toplevel


        # A Label widget to show in toplevel
        Label(self.newWindow,text ="This is a new window").grid(row=0, column=0, padx=4, pady=4)
        print("Esto abre el menu de configuracion")

        self.mostrar()
    
    def mostrar(self):

        mov_dict = {'U':0,'D':1,'L':2,'R':3,'X':4}
        acc_dict = {"VOLUP":0,"VOLDOWN":1,"MUTE":2}

        for i in range(len(self.labelframe)):
            self.labelframe[i].destroy()

        
        with open("acciones.json", 'r') as archivo:
                self.data = json.load(archivo)

        print(f"Len data : {len(self.data)}")

        self.pos_dedos = [[None for _ in range(5)] for _ in range(len(self.data))]
        self.movimiento = [None for _ in range(len(self.data))]
        self.accion = [None for _ in range(len(self.data))]

        btn_borrar = [None for _ in range(len(self.data))]

        
        for i in range(0,len(self.data)):



            
            self.labelframe.append(ttk.LabelFrame(self.newWindow, text=f"self.accion {i+1}"))
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



            mov_texto=ttk.Label(self.labelframe[i], text="self.movimiento")
            mov_texto.grid(column=5, row=0, padx=20, pady=20)

            self.movimiento[i]=ttk.Combobox(self.labelframe[i],state="readonly",values=["Arriba","Abajo","Izquierda","Derecha","Cualquiera"])
            self.movimiento[i].current(mov_dict[list(self.data.keys())[i][5]])
            self.movimiento[i].grid(column=5, row=1,padx=10,pady=10)



            mov_texto=ttk.Label(self.labelframe[i], text="self.accion")
            mov_texto.grid(column=7, row=0, padx=20, pady=20)

            self.accion[i]=ttk.Combobox(self.labelframe[i],state="readonly",values=["VOLUP","VOLDOWN","MUTE"])

            if list(self.data.values())[i] in acc_dict.keys():
                idx = acc_dict[list(self.data.values())[i]]
            else:
                self.accion[i]['values'] = self.accion[i]['values'] + (f"{list(self.data.values())[i]}",)
                idx=len(self.accion[i]['values'])-1
                btn_seleccion = ttk.Button(self.labelframe[i], text="Seleccionar archivo", command=lambda:self.seleccionar_archivo(i))
                btn_seleccion.grid(column=8,row=1,padx=10,pady=10)

            self.accion[i].current(idx)
            self.accion[i].grid(column=7, row=1,padx=10,pady=10)
            
            btn_borrar[i] = ttk.Button(self.labelframe[i],text="x", command=lambda idx = i:self.delete(idx))
            btn_borrar[i].grid(column=8, row =0, padx =1,pady=1)

        self.linea=len(self.labelframe)

        self.btn_anadir = ttk.Button(self.newWindow,text="+", command=self.anadir)
        self.btn_anadir.grid(column=0, row =self.linea+1, padx =1,pady=1)

        self.btn_guardar = ttk.Button(self.newWindow,text="Guardar", command=self.guardar)
        self.btn_guardar.grid(column=0, row =self.linea+2, padx =1,pady=1)

 #       self.newWindow.protocol("WM_DELETE_WINDOW", self.mensajito())
        self.newWindow.mainloop()

    def seleccionar_archivo(self,i):
        ruta_archivo = filedialog.askopenfilename()
        if ruta_archivo is not None:
            print(ruta_archivo)
            self.accion[i]=ruta_archivo

        for i in self.accion:
            try:
                print(i.get())
            except:
                print(i)

    def guardar(self):

        new_data = dict()
        for i in range(len(self.pos_dedos)):
            code =""
            
            for j in range(len(self.pos_dedos[i])):
                print(f"I J {i} {j}")
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

            if re.match(r'\d{5}[UDLRX]$',code):
                print("Este lo guardo\n")
                try:
                        new_data[code]=self.accion[i].get()

                except:
                    if self.accion[i] is not None:
                        new_data[code]=self.accion[i]

        with open('acciones.json', 'w') as archivo:
            json.dump(new_data, archivo)
        self.gw.load()
        self.newWindow.destroy()

