from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import keyboard
import time
import pyautogui

class Controller():
    
  def __init__(self):
    self.devices = AudioUtilities.GetSpeakers()
    self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))

  def set_volumen(self,v):
    self.volume.SetMasterVolumeLevelScalar(v,None)

  def mute(self):
      current_volume = self.volume.GetMasterVolumeLevelScalar()
      new_volume = 0
      self.volume.SetMasterVolumeLevelScalar(new_volume, None)
  
  def subir_volumen(self):
      current_volume = self.volume.GetMasterVolumeLevelScalar()
      new_volume = current_volume+0.35  # 70% del volumen máximo
      self.volume.SetMasterVolumeLevelScalar(new_volume, None)
  
  def bajar_volumen(self):
      current_volume = self.volume.GetMasterVolumeLevelScalar()
      new_volume = current_volume-0.35# 70% del volumen máximo
      self.volume.SetMasterVolumeLevelScalar(new_volume, None)

  def pulsar_izquierda(self):
    keyboard.press("left")
    time.sleep(0.1)  # Puedes ajustar la duración de la pulsación si es necesario
    keyboard.release("left")

  def pulsar_tecla_espacio(self):
    keyboard.press("space")
    time.sleep(0.1)  # Puedes ajustar la duración de la pulsación si es necesario
    keyboard.release("space")

  def pulsar_derecha(self):
    keyboard.press("right")
    time.sleep(0.1)  # Puedes ajustar la duración de la pulsación si es necesario
    keyboard.release("right")
    
  def mover_cursor(self, x, y):
    print("X:\t"+str(x)+"\nY:\t"+str(y))
    pyautogui.moveTo(x, y, duration=0.1)  
