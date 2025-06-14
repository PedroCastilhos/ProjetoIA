# tests/test_estado_desconhecido.py

import numpy as np
import cv2
from semaforo.main import verifica_estado_semaforo

def test_estado_desconhecido():
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    roi = [100, 100, 100, 100]
    estado = verifica_estado_semaforo(img, [roi])
    assert estado == "DESCONHECIDO"
    
