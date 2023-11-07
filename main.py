import cv2
import mediapipe as mp
import Controller
import HandProcesor

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands
mppose = mp.solutions.pose
cap = cv2.VideoCapture(0)
manos = mphands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
pose = mppose.Pose()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

controller = Controller()
hp = HandProcesor()

contador=dict()
funcionando=None
humbral_inicio=2
humbral_fin=2

return_counter=humbral_fin

while True:
    data, image = cap.read()
    image = cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB)
    resultsmanos = manos.process(image)
    resultspose = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if resultsmanos.multi_hand_landmarks:
        
        image = hp.mostrarPuntos()
        
        if funcionando!=None :
            master=None
            for mano in resultsmanos.multi_hand_landmarks:
                if hp.comprobar_mano(mano)==funcionando:
                    master = mano
                    break
            if(master==None):
                
                if ((return_counter:=return_counter-1)<=0):
                    if funcionando == "00110":
                        controller.mute()
                        funcionando = None
                        hp.posiciones=[]
                    else:
                        funcionando = None
                        print("Fin de trackeo, procesar movimiento")
                        movimiento = hp.procesarMovimiento()
                        print(movimiento)

                        if(movimiento=="derecha"):
                            try:
                                controller.subir_volumen()
                            else:
                                controller.set_volumen(1)
                                print("Está al maximo")

                        elif(movimiento=="izquierda"):
                            try:
                                controller.bajar_volumen()
                            else:
                                controller.set_volumen(0)
                                print("Está al minimo")
                        else:
                            print(movimiento)
                    
            else:
                print("Guardando posicion")
                hp.guardarPosicion(master, 0)
                return_counter=humbral_fin
                
        if funcionando==None:
            for mano in resultsmanos.multi_hand_landmarks:
                pos = hp.comprobar_mano(mano)
                if pos in ["00110","01110"]:
                    try:
                        contador[pos]+=1
                        if(contador[pos])>=humbral_inicio:
                            funcionando=pos
                            contador.clear()
                            print("la funcion actual es "+pos)
                            break
                    except KeyError:
                        contador[pos]=1


    cv2.imshow("GestureWizard", image)
    cv2.waitKey(2)

