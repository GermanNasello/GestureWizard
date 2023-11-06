import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

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

def distance(v1,v2,p1,p2):
    return math.sqrt(math.pow(v1.landmark[p1].x - v2.landmark[p2].x, 2) + math.pow(v1.landmark[p1].y - v2.landmark[p2].y, 2))
def mute():
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = 0
    volume.SetMasterVolumeLevelScalar(new_volume, None)

def subir_volumen():
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = current_volume+0.35  # 70% del volumen máximo
    volume.SetMasterVolumeLevelScalar(new_volume, None)

def bajar_volumen():
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = current_volume-0.35# 70% del volumen máximo
    volume.SetMasterVolumeLevelScalar(new_volume, None)

def comprobar_mano(m):
    res=""

    if distance(m, m, 4, 17) < distance(m, m, 2, 4):
        res+='1'
    else:
        res+='0'

    if distance(m, m, 0, 8) < distance(m, m, 0, 6):
        res+= '1'
    else:
        res+= '0'

    if distance(m, m, 0, 12) < distance(m, m, 0, 9):
        res+= '1'
    else:
        res+= '0'

    if distance(m, m, 0, 16) < distance(m, m, 0, 13):
        res+= '1'
    else:
        res+= '0'

    if distance(m, m, 0, 20) < distance(m, m, 0, 17):
        res+= '1'
    else:
        res+= '0'

    return res


contador=dict()
funcionando=None
humbral_inicio=2
humbral_fin=2

return_counter=humbral_fin
posiciones=[]
while True:
    data, image = cap.read()
    image = cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB)
    resultsmanos = manos.process(image)
    resultspose = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if resultsmanos.multi_hand_landmarks:
        for hand_landmarks in resultsmanos.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mphands.HAND_CONNECTIONS
            )
        alto, ancho , c = image.shape
        #print(image.shape)
        i=0

        for hand_landmarks in resultsmanos.multi_hand_landmarks:
            for j in range(21):
                px = hand_landmarks.landmark[j].x * ancho
                py = hand_landmarks.landmark[j].y * alto
                #print(int(hand_landmarks.landmark[0].x*100))
                #image = cv2.putText(image,str(j),(int(px),int(py)), cv2.FONT_HERSHEY_SIMPLEX, 0.2,
                      #(0, 0, 255), 1, cv2.LINE_AA)
            i+=1


        if funcionando!=None :
            master=None
            for mano in resultsmanos.multi_hand_landmarks:
                if comprobar_mano(mano)==funcionando:
                    master = mano
                    break
            if(master==None):
                return_counter-=1
                if return_counter<=0:
                    if funcionando == "00110":
                        mute()
                        funcionando = None
                        posiciones=[]
                    else:
                        funcionando = None
                        print("Fin de trackeo, procesar movimiento")
                        movimiento=[0,0]
                        for i in range(1,len(posiciones)):
                            movimiento[0] += posiciones[i][0]-posiciones[i-1][0]
                            movimiento[1] += posiciones[i][1]-posiciones[i-1][1]
                        print(movimiento)
                        posiciones=[]
                        if movimiento[0]<0:
                            print("bajar el volumen")
                            try:
                                bajar_volumen()
                            except:
                                print("Esta al minimo")
                        else:
                            print("subir el volumen")
                            try:
                                subir_volumen()
                            except:
                                print("Esta al maximo")

                    
            else:
                print("Guardando posicion")
                posiciones.append([master.landmark[0].x,master.landmark[0].y])
                return_counter=humbral_fin
        if funcionando==None:
            for mano in resultsmanos.multi_hand_landmarks:
                pos = comprobar_mano(mano)
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


    cv2.imshow("PRUEBA3", image)
    cv2.waitKey(2)

