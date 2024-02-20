from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


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
      try:
        current_volume = self.volume.GetMasterVolumeLevelScalar()
        new_volume = current_volume+0.35  # 70% del volumen máximo
        self.volume.SetMasterVolumeLevelScalar(new_volume, None)
      except:
        print("Esta al maximo")
  
  def bajar_volumen(self):
      try:
        current_volume = self.volume.GetMasterVolumeLevelScalar()
        new_volume = current_volume-0.35# 70% del volumen máximo
        self.volume.SetMasterVolumeLevelScalar(new_volume, None)
      except:
        print("Esta al minimo")
