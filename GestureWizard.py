import cv2
import mediapipe as mp
import Controller
import HandProcesor
import json

class GestureWizard():

    def load(self):
        with open("config.json", "r") as archivo_json:
            config = json.load(archivo_json)
        self.humbral_inicio=config["humbral_inicio"]
        self.humbral_fin=config["humbral_fin"]
        self.min_detection_confidence = config["min_detection_confidence"]
        self.min_tracking_confidence = config["min_tracking_confidence"]

    def __init__(self):
        print("CARGANDO LA MAGIA")
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mphands = mp.solutions.hands
        self.mppose = mp.solutions.pose

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



    def fin(self):
        print("\n\nFINFINFIN\n\n")
        if self.funcionando == "00110":
            self.controller.mute()
            self.funcionando = None
            self.hp.posiciones = []
        else:
            self.funcionando = None
            print("Fin de trackeo, procesar movimiento")
            movimiento = self.hp.procesarMovimiento()
            if (movimiento == "derecha"):
                try:
                    self.controller.subir_volumen()
                except:
                    self.controller.set_volumen(1)
                    print("Está al maximo")
            elif (movimiento == "izquierda"):
                try:
                    self.controller.bajar_volumen()
                except:
                    self.controller.set_volumen(0)
                    print("Está al minimo")
            else:
                print(movimiento)

    def run(self):
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
                    if pos in ["00110", "01110"]:
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
