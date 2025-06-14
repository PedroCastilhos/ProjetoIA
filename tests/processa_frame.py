import cv2
import numpy as np
from semaforo.main import processa_frame

def test_processa_frame_shape():
    dummy_img = np.zeros((480, 640, 3), dtype=np.uint8)
    dil, cinza, thresh = processa_frame(dummy_img)

    assert dil.shape == (480, 640)
    assert cinza.shape == (480, 640)
    assert thresh.shape == (480, 640)
