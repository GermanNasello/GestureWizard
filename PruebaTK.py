from tkinter import *
from tkinter import ttk
import json
def toggle_run():
    print("Esto va a cambiar si el programa corre o no")
def config():
    labelframe = []

    mov_dict = {'U':0,'D':1,'L':2,'R':3,'X':4}
    acc_dict = {"VOLUP":0,"VOLDOWN":1,"MUTE":2}
    # Toplevel object which will 
    # be treated as a new window
    global newWindow
    newWindow = Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("New Window")
 
    # sets the geometry of toplevel
    newWindow.geometry("200x200")
 
    # A Label widget to show in toplevel
    Label(newWindow,text ="This is a new window").grid(row=0, column=0, padx=4, pady=4)
    print("Esto abre el menu de configuracion")



    with open("acciones.json", 'r') as archivo:
            data = json.load(archivo)

    pos_dedos = [[None for _ in range(5)] for _ in range(len(data))]
    movimiento = [None for _ in range(len(data))]
    accion = [None for _ in range(len(data))]
    
    for i in range(0,len(data)):
        
        labelframe.append(ttk.LabelFrame(newWindow, text=f"Accion {i+1}"))     
        labelframe[i].grid(row=i+1, column=0, padx=10, pady=10)        
        
        pulgar=ttk.Label(labelframe[i], text="Dedo pulgar")
        pulgar.grid(column=0, row=0, padx=10, pady=10)

        pos_dedos[i][0]=ttk.Combobox(labelframe[i],state="readonly",values=["abierto","cerrado"])
        pos_dedos[i][0].current(list(data.keys())[i][0])
        pos_dedos[i][0].grid(column=0, row=1,padx=10,pady=10)

        
        indice=ttk.Label(labelframe[i], text="Dedo indice")
        indice.grid(column=1, row=0, padx=10, pady=10)
        
        pos_dedos[i][1]=ttk.Combobox(labelframe[i],state="readonly",values=["abierto","cerrado"])
        pos_dedos[i][1].current(list(data.keys())[i][1])
        pos_dedos[i][1].grid(column=1, row=1,padx=10,pady=10)       

        
        corazon=ttk.Label(labelframe[i], text="Dedo corazon")
        corazon.grid(column=2, row=0, padx=10, pady=10)

        pos_dedos[i][2]=ttk.Combobox(labelframe[i],state="readonly",values=["abierto","cerrado"])
        pos_dedos[i][2].current(list(data.keys())[i][2])
        pos_dedos[i][2].grid(column=2, row=1,padx=10,pady=10)
        
        
        anular=ttk.Label(labelframe[i], text="Dedo anular")
        anular.grid(column=3, row=0, padx=10, pady=10)
        
        pos_dedos[i][3]=ttk.Combobox(labelframe[i],state="readonly",values=["abierto","cerrado"])
        pos_dedos[i][3].current(list(data.keys())[i][3])
        pos_dedos[i][3].grid(column=3, row=1,padx=10,pady=10)       
        
        
        menique=ttk.Label(labelframe[i], text="Dedo meñique")
        menique.grid(column=4, row=0, padx=10, pady=10)
        
        pos_dedos[i][4]=ttk.Combobox(labelframe[i],state="readonly",values=["abierto","cerrado"])
        pos_dedos[i][4].current(list(data.keys())[i][4])
        pos_dedos[i][4].grid(column=4, row=1,padx=10,pady=10)


        
        mov_texto=ttk.Label(labelframe[i], text="Movimiento")
        mov_texto.grid(column=5, row=0, padx=20, pady=20)

        movimiento[i]=ttk.Combobox(labelframe[i],state="readonly",values=["Arriba","Abajo","Izquierda","Derecha","Cualquiera"])
        movimiento[i].current(mov_dict[list(data.keys())[i][5]])
        movimiento[i].grid(column=5, row=1,padx=10,pady=10)


        
        mov_texto=ttk.Label(labelframe[i], text="Accion")
        mov_texto.grid(column=7, row=0, padx=20, pady=20)

        accion[i]=ttk.Combobox(labelframe[i],state="readonly",values=["VOLUP","VOLDOWN","MUTE"])

        if list(data.values())[i] in acc_dict.keys():
            print(list(data.values())[i])
            idx = acc_dict[list(data.values())[i]]
        else:
            accion[i]['values'] = accion[i]['values'] + (f"{list(data.values())[i]}",)
            idx=len(accion[i]['values'])-1
        accion[i].current(idx)
        accion[i].grid(column=7, row=1,padx=10,pady=10)       
        

        

    newWindow.protocol("WM_DELETE_WINDOW", mensajito)
    newWindow.mainloop()
    

    
def mensajito():
    global newWindow
    print("Me cerré")
    newWindow.destroy()
    
root = Tk()

photo = PhotoImage(file="pausa.png")

Button(root, text='Click Me!', image=photo, command=toggle_run).grid(row=0, column=0, padx=20, pady=20)
Button(root, text="configuracion", command=config).grid(row=0, column=1, padx=20, pady=20)

root.mainloop()
