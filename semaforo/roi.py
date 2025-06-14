import cv2
import numpy as np
import json
import os

def selecionar_rois(imagem):
    rois = []
    while True:
        img = imagem.copy()
        cv2.namedWindow('Selecionar Região do Semáforo', cv2.WINDOW_NORMAL)
        cv2.imshow('Selecionar Região do Semáforo', img)
        roi = cv2.selectROI('Selecionar Região do Semáforo', img, fromCenter=False, showCrosshair=True)
        if roi == (0, 0, 0, 0):
            break
        rois.append(roi)
        cv2.destroyWindow('Selecionar Região do Semáforo')
        print("Pressione 'q' para sair ou qualquer outra tecla para selecionar outra região.")
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    return rois

def capturar_quadro_do_video(caminho_video, numero_quadro):
    cap = cv2.VideoCapture(caminho_video)
    cap.set(cv2.CAP_PROP_POS_FRAMES, numero_quadro)
    ret, quadro = cap.read()
    cap.release()
    return quadro


caminho_video = 'semaforo/semaforo.mp4'
numero_quadro = 30 


quadro = capturar_quadro_do_video(caminho_video, numero_quadro)


if quadro is None:
    print("Erro: não foi possível capturar o quadro do vídeo.")
    exit(1)

rois = selecionar_rois(quadro)

if rois:
    x, y, largura, altura = rois[0]
    roi_data = {"semaforo": [x, y, largura, altura]}
    with open("semaforo/roi.json", "w") as f:
        json.dump(roi_data, f)
    print(f"✅ ROI salva em semaforo/roi.json: {roi_data}")
else:
    print("⚠️ Nenhuma ROI foi selecionada.")

