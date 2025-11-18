import winsound

# ===== SONIDOS BÁSICOS =====

def sonido_tiempo_tick():
    winsound.Beep(1200, 60)

def sonido_correcta():
    winsound.Beep(1000, 100)
    winsound.Beep(1300, 100)
    winsound.Beep(1600, 150)

def sonido_incorrecta():
    winsound.Beep(300, 250)
    winsound.Beep(220, 300)
    
def sonido_bonus():
    winsound.Beep(1500, 120)
    winsound.Beep(1800, 150)
