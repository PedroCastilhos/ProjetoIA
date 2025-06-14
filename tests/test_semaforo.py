import cv2
import numpy as np
from semaforo.main import verifica_estado_semaforo

def test_verifica_estado_com_roi_vazia():   
    img = np.zeros((480, 640, 3), dtype=np.uint8)    
    semaforo = [[1000, 1000, 100, 100]]
    estado = verifica_estado_semaforo(img, semaforo)
    assert estado == "DESCONHECIDO"

