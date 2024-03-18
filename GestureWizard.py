import cv2
import mediapipe as mp
import Controller
import HandProcesor
import json
import os
import subprocess


class GestureWizard():

    def toggle(self):
        self.running = not self.running
        print(f"El programa esta en funcionamiento: {self.running}")


    
    def load(self):
        print("Cargando config")
        with open("config.json", "r") as archivo_json:
            config = json.load(archivo_json)
            
        self.humbral_inicio=config["humbral_inicio"]    # Los JSON son diccionarios    
        self.humbral_fin=config["humbral_fin"]
        self.min_detection_confidence = config["min_detection_confidence"]
        self.min_tracking_confidence = config["min_tracking_confidence"]

        with open("acciones.json","r") as archivo_json:
            self.catalogo_gestos=json.load(archivo_json)

        for key in list(self.catalogo_gestos.keys()):
            if key[5] == 'X':        # En caso de que el gesto se quiera hacer hacia cualquier movimiento, se añade a las acciones conocidas en todas las direcciones (Para aligerar la decision en la funcion fin)
                self.catalogo_gestos[key[:5] + 'L'] = self.catalogo_gestos[key]
                self.catalogo_gestos[key[:5] + 'U'] = self.catalogo_gestos[key]
                self.catalogo_gestos[key[:5] + 'R'] = self.catalogo_gestos[key]
                self.catalogo_gestos[key[:5] + 'D'] = self.catalogo_gestos[key]


       
    def __init__(self):
        print("CARGANDO LA MAGIA")
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mphands = mp.solutions.hands
        self.mppose = mp.solutions.pose
        self.catalogo_gestos = []

        self.load()

        self.cap = cv2.VideoCapture(0)
        self.manos = self.mphands.Hands(min_detection_confidence=self.min_detection_confidence, min_tracking_confidence=self.min_tracking_confidence)
        self.pose = self.mppose.Pose()

        self.controller = Controller.Controller()
        self.hp = HandProcesor.Hand()

        self.contador = dict()
        self.funcionando = None
        self.master=None

        self.return_counter = self.humbral_fin

        self.running=True

    """
    Ejecucion principal del programa, captura una imagen, detecta manos, comprueba posicion de las manos,
    
    Si esta seleccionada una posicion de mano: 
            - Se busca la mano con la posicion seleccionada.
            - Si la encuentra guarda la posicion de la mano y sale de los bucles
            - Si no la encuentra decrementa el contador de retorno. Si este es 0 llama a la funcion fin

    Si no esta seleccionada ninguna posicion de mano;
            - Por cada mano se comprueba la posicion de los dedos
            - Se comprueba si una de las posiciones esta dentro de las posiciones de la lista de acciones
            - Se crea/aumenta el contador para esa posicion en concreto
            - Si el valor de esa posicion esta dentro del humbral de inicio se selecciona una posicion de la mano, se borra el contador y se sale de los bucles
    
    Si no se ha detectado ninguna mano se decrementan los contadores de cada posicion y el contador de retorno
    """
    def run(self):
        if self.running:

            data, image = self.cap.read()
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            resultsmanos = self.manos.process(image)
            resultspose = self.pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if resultsmanos.multi_hand_landmarks:

                image = self.hp.mostrarPuntos(resultsmanos.multi_hand_landmarks, self.mp_drawing, image, self.mphands)

                if self.funcionando != None:
                    self.master = None
                    for mano in resultsmanos.multi_hand_landmarks:
                        if self.hp.comprobar_mano(mano) == self.funcionando:
                            self.master = mano
                            break
                    if (self.master == None):
                        self.return_counter-=1
                        if (self.return_counter <= 0):
                            self.fin()

                    else:
                        print("Guardando posicion")
                        self.hp.guardarPosicion(self.master, 0)
                        self.return_counter = self.humbral_fin

                if self.funcionando == None:
                    for mano in resultsmanos.multi_hand_landmarks:
                        pos = self.hp.comprobar_mano(mano)
                        for posiciones_esperadas in self.catalogo_gestos.keys():
                            if pos == posiciones_esperadas[:5]:
                                try:
                                    self.contador[pos] += 1
                                    if (self.contador[pos]) >= self.humbral_inicio:
                                        self.funcionando = pos
                                        self.contador.clear()
                                        print("la funcion actual es " + pos)
                                        break
                                except KeyError:
                                    self.contador[pos] = 1

            else:
                self.return_counter-=1
                for key in self.contador.keys():
                    self.contador[key]-=1
                if (self.return_counter <= 0 and self.funcionando != None):
                    print("Fin por fuera de foco")
                    self.fin()
            #cv2.imshow("GestureWizard", image)
            cv2.waitKey(2)

    def fin(self):
        print("Fin de trackeo, procesar movimiento")
        movimiento = self.hp.procesarMovimiento()
        gesto_completo=self.funcionando+movimiento

        print(f"Gesto completo: {gesto_completo}")
        
        if gesto_completo in self.catalogo_gestos.keys():
            if self.catalogo_gestos[gesto_completo] == "VOLUP":
                self.controller.subir_volumen()
            elif self.catalogo_gestos[gesto_completo] == "VOLDOWN":
                self.controller.bajar_volumen()
            elif self.catalogo_gestos[gesto_completo] == "MUTE":
                self.controller.mute()
            else:
                path = self.catalogo_gestos[gesto_completo]
                #path = path.replace(" ","\ ")
                print(f"Se ejecuta el os.system({path})")
         
                #os.system("start "+path)
                subprocess.Popen(["start","",path],shell=True)
        
        self.funcionando = None
