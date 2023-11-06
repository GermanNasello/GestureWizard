Class Controller():
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
