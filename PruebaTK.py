from tkinter import *

def toggle_run():
    print("Esto va a cambiar si el programa corre o no")
def config():
    print("Esto abre el menu de configuracion")



root = Tk()

photo = PhotoImage(file="pausa.png")
Button(root, text='Click Me!', image=photo,command=toggle_run).pack(side=LEFT)
Button(root, text="configuracion",command=config).pack(side=LEFT)

root.mainloop()