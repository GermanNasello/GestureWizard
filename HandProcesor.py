import math

class Hand():
  def __init__(self):
    self.posiciones=[]
    self.movimiento=[0,0]
########################################
  def distance(self,v1,v2,p1,p2):
    return math.sqrt(math.pow(v1.landmark[p1].x - v2.landmark[p2].x, 2) + math.pow(v1.landmark[p1].y - v2.landmark[p2].y, 2))

########################################
  def comprobar_mano(self,m):
      res=""
  
      if self.distance(m, m, 4, 17) < self.distance(m, m, 2, 4):
          res+='1'
      else:
          res+='0'
  
      if self.distance(m, m, 0, 8) < self.distance(m, m, 0, 6):
          res+= '1'
      else:
          res+= '0'
  
      if self.distance(m, m, 0, 12) < self.distance(m, m, 0, 9):
          res+= '1'
      else:
          res+= '0'
  
      if self.distance(m, m, 0, 16) < self.distance(m, m, 0, 13):
          res+= '1'
      else:
          res+= '0'
  
      if self.distance(m, m, 0, 20) < self.distance(m, m, 0, 17):
          res+= '1'
      else:
          res+= '0'
  
      return res
########################################

  def mostrarPuntos(self, resultsmanos, mp_drawing, image, mphands):
    for hand_landmarks in resultsmanos:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mphands.HAND_CONNECTIONS
            )
    return image

########################################

  def guardarPosicion(self, mano, p):
    self.posiciones.append([mano.landmark[p].x, mano.landmark[p].y])


########################################

  def procesarMovimiento(self):
    self.movimientos=[0,0]
    for i in range(1, len(self.posiciones)):
      self.movimiento[0]+= self.posiciones[i][0]-self.posiciones[i-1][0]
      self.movimiento[1]+= self.posiciones[i][1]-self.posiciones[i-1][1]
    self.posiciones=[]
    if abs(self.movimiento[0]) > abs(self.movimiento[1]):
      if(self.movimiento[0]>0):
        return "R"
      else:
        return "L"
    else:
      if (self.movimiento[1]>0):
        return "U"
      else:
        return "D"
     
