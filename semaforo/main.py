import cv2
import numpy as np
import json
import os

def carregar_roi_json(caminho_json):
    if not os.path.exists(caminho_json):
        print(f"❌ Arquivo de ROI não encontrado: {caminho_json}")
        return [[0, 0, 0, 0]]
    with open(caminho_json, "r") as f:
        dados = json.load(f)
        return [dados["semaforo"]]

SEMAFORO = carregar_roi_json("semaforo/roi.json")

DELAY = 10


def processa_frame(img):
    
    img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_threshold = cv2.adaptiveThreshold(
        img_cinza, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 25, 16
    )
    img_blur = cv2.medianBlur(img_threshold, 5)
    kernel = np.ones((3, 3), np.int8)
    img_dil = cv2.dilate(img_blur, kernel)
    return [img_dil, img_cinza, img_threshold]


def verifica_estado_semaforo(img, semaforo):
    
    x, y, w, h = semaforo[0]
    roi = img[y:y + h, x:x + w]

    # Verifica se a ROI capturada é válida
    if roi.size == 0:
        print("⚠️ ROI vazia ou fora da imagem. Verifique a coordenada.")
        return 'DESCONHECIDO'

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Máscaras de cor para vermelho, amarelo e verde
    vermelho_baixo1 = np.array([0, 100, 100])
    vermelho_alto1 = np.array([10, 255, 255])
    vermelho_baixo2 = np.array([160, 100, 100])
    vermelho_alto2 = np.array([179, 255, 255])

    amarelo_baixo = np.array([20, 100, 100])
    amarelo_alto = np.array([30, 255, 255])

    verde_baixo = np.array([40, 50, 50])
    verde_alto = np.array([90, 255, 255])

    mask_vermelho1 = cv2.inRange(hsv, vermelho_baixo1, vermelho_alto1)
    mask_vermelho2 = cv2.inRange(hsv, vermelho_baixo2, vermelho_alto2)
    mask_vermelho = cv2.bitwise_or(mask_vermelho1, mask_vermelho2)

    mask_amarelo = cv2.inRange(hsv, amarelo_baixo, amarelo_alto)
    mask_verde = cv2.inRange(hsv, verde_baixo, verde_alto)

    # Conta os pixels de cada máscara
    total_vermelho = cv2.countNonZero(mask_vermelho)
    total_amarelo = cv2.countNonZero(mask_amarelo)
    total_verde = cv2.countNonZero(mask_verde)

    # Determina qual cor está com mais intensidade
    max_cor = max(total_vermelho, total_amarelo, total_verde)

    if max_cor == total_vermelho:
        estado = 'VERMELHO'
    elif max_cor == total_amarelo:
        estado = 'AMARELO'
    elif max_cor == total_verde:
        estado = 'VERDE'
    else:
        estado = 'DESCONHECIDO'

    return estado
    

def exibe_status(img, estado):
    """
    Exibe no canto superior esquerdo o status atual do semáforo.
    """
    cv2.rectangle(img, (90, 0), (500, 60), (0, 0, 0), -1)

    if estado == 'VERMELHO':
        cor = (0, 0, 255)
    elif estado == 'AMARELO':
        cor = (0, 255, 255)
    elif estado == 'VERDE':
        cor = (0, 255, 0)
    else:
        cor = (255, 255, 255)

    cv2.putText(
        img, estado, (100, 45),
        cv2.FONT_HERSHEY_DUPLEX, 1.5, cor, 4
    )


def main():
    video_path = 'semaforo/semaforo.mp4'
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print(f"Erro ao abrir o vídeo: {video_path}")
        return

    while True:
        check, img = video.read()
        if not check:
            break

        img_dil, img_cinza, img_threshold = processa_frame(img)

        estado = verifica_estado_semaforo(img, SEMAFORO)
        exibe_status(img, estado)

        # Exibe os resultados
        cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Video', 910, 510)
        cv2.imshow('Video', img)

        cv2.namedWindow('Cinza', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Cinza', 480, 270)
        cv2.imshow('Cinza', img_cinza)

        cv2.namedWindow('Threshold', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Threshold', 480, 270)
        cv2.imshow('Threshold', img_threshold)

        cv2.namedWindow('Dilatada', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Dilatada', 480, 270)
        cv2.imshow('Dilatada', img_dil)

        if cv2.waitKey(DELAY) == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

