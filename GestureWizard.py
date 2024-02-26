import cv2
import mediapipe as mp
import Controller
import HandProcesor
import json

class GestureWizard():

    def toggle(self):
        self.running = not self.running
        print(f"El programa esta en funcionamiento: {self.running}")

    def load(self):
        print("Cargando config")
        with open("config.json", "r") as archivo_json:
            config = json.load(archivo_json)
        self.humbral_inicio=config["humbral_inicio"]
        self.humbral_fin=config["humbral_fin"]
        self.min_detection_confidence = config["min_detection_confidence"]
        self.min_tracking_confidence = config["min_tracking_confidence"]

        with open("acciones.json","r") as archivo_json:
            self.catalogo_gestos=json.load(archivo_json)

        for key in list(self.catalogo_gestos.keys()):
            if key[5] == 'X':
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
                print(f"Se ejecuta el os.system({path})")
                
        
        self.funcionando = None

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
            cv2.imshow("GestureWizard", image)
            cv2.waitKey(2)
