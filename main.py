import GestureWizard
import GUI
import threading
import time
import sys


gw = GestureWizard.GestureWizard()

def grafica():
    gui = GUI.GUI(gw)
def run():
    while True:
        gw.run()


# Crea un objeto de hilo
hilo = threading.Thread(target=grafica)

hilo2 = threading.Thread(target=run)

# Inicia el hilo
hilo.start()
hilo2.start()

hilo.join()

sys.exit()
