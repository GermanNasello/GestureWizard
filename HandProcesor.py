Class Hand():

########################################
  def distance(v1,v2,p1,p2):
    return math.sqrt(math.pow(v1.landmark[p1].x - v2.landmark[p2].x, 2) + math.pow(v1.landmark[p1].y - v2.landmark[p2].y, 2))

########################################
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
########################################

  def mostrarPuntos(resultmanos, mp_drawing, image):
    for hand_landmarks in resultsmanos.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mphands.HAND_CONNECTIONS
            )
  return image
