import cv2
import mediapipe as mp
import Controller
import HandProcesor
import pyautogui


screen_width, screen_height = pyautogui.size()
print(pyautogui.size())
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands
mppose = mp.solutions.pose
cap = cv2.VideoCapture(0)
manos = mphands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
pose = mppose.Pose()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

controller = Controller.Controller()
hp = HandProcesor.Hand()

contador=dict()
funcionando=None
humbral_inicio=1
humbral_fin=2


line_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
circle_radius = int(.007 * 460)
point_spec = mp_drawing.DrawingSpec(color=(220, 100, 0), thickness=-1, circle_radius=circle_radius)

return_counter=humbral_fin


def fin():
    global funcionando
    print(len(hp.posiciones))
    print("Fin de trackeo, procesar movimiento")
    movimiento = hp.procesarMovimiento()
    if funcionando=="00110":
        controller.pulsar_derecha()
        print("Pulsar derecha")
    elif funcionando=="10001":
        controller.pulsar_izquierda()
        print("Pulsar izquierda")

    funcionando = None


while True:
    ret,image = cap.read()
    image = cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB)
    resultsmanos = manos.process(image)
    resultspose = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    alto, ancho,_ = image.shape
    if resultsmanos.multi_hand_landmarks:

        if resultspose.pose_landmarks:
                mp_drawing.draw_landmarks(
                        image,
                        landmark_list=resultspose.pose_landmarks,
                        connections=mppose.POSE_CONNECTIONS,
                        landmark_drawing_spec=point_spec,
                        connection_drawing_spec=line_spec
                    )
        
        image = hp.mostrarPuntos(resultsmanos.multi_hand_landmarks, mp_drawing, image, mphands)
        
        if funcionando!=None :
            master=None
            for mano in resultsmanos.multi_hand_landmarks:
                if hp.comprobar_mano(mano)==funcionando:
                    master = mano
                    break
            if(master==None):
                
                if ((return_counter:=return_counter-1)<=0):
                    fin()
                    
            else:
                if funcionando == "00011":
                    px = int(master.landmark[12].x*10)
                    py = int(master.landmark[12].y*10)
                    controller.mover_cursor(px*screen_width/10,py*screen_height/10)
                print("Guardando posicion")
                hp.guardarPosicion(master, 0)
                return_counter=humbral_fin
                
        if funcionando==None:
            for mano in resultsmanos.multi_hand_landmarks:
                pos = hp.comprobar_mano(mano)
                if pos in ["00110","10001","00011"]:
                    try:
                        contador[pos]+=1
                        if(contador[pos])>=humbral_inicio:
                            funcionando=pos
                            contador.clear()
                            print("la funcion actual es "+pos)
                            break
                    except KeyError:
                        contador[pos]=1

    else:
        if ((return_counter:=return_counter-1)<=0 and funcionando!=None):
            print("Fin por fuera de foco")
            fin()
  
    #cv2.imshow("GestureWizard", image)
    cv2.waitKey(1)

