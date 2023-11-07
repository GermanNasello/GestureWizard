from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


Class Controller():
  def __init__():
    self.devices = AudioUtilities.GetSpeakers()
    self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))

  def set_volumen(v):
    self.volume.SetMasterVolumeLevelScalar(v,None)

  def mute():
      current_volume = self.volume.GetMasterVolumeLevelScalar()
      new_volume = 0
      self.volume.SetMasterVolumeLevelScalar(new_volume, None)
  
  def subir_volumen():
      current_volume = self.volume.GetMasterVolumeLevelScalar()
      new_volume = current_volume+0.35  # 70% del volumen máximo
      self.volume.SetMasterVolumeLevelScalar(new_volume, None)
  
  def bajar_volumen():
      current_volume = self.volume.GetMasterVolumeLevelScalar()
      new_volume = current_volume-0.35# 70% del volumen máximo
      self.volume.SetMasterVolumeLevelScalar(new_volume, None)