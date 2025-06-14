
# 🚦 Monitoramento de Semáforos com Visão Computacional

## Integrante

- **Pedro Castilhos**

## 1. Introdução

Este projeto propõe o uso de **técnicas de visão computacional** para monitorar, por meio de um **vídeo gravado**, o estado de um **semáforo**, identificando se a luz está acesa na cor **vermelha, amarela ou verde**.

A detecção é baseada na coloração predominante de cada luz. O sistema determina, em tempo real durante a reprodução do vídeo, qual sinal está ativo e exibe essa informação sobre o vídeo. Este tipo de aplicação pode ser útil em sistemas de veículos autônomos, monitoramento de tráfego e projetos de cidades inteligentes.

## 2. Objetivo

Desenvolver um sistema que analise automaticamente um vídeo de um semáforo, detectando qual luz está acesa (**vermelha, amarela ou verde**). O sistema apresenta visualmente o status atual do semáforo sobre o vídeo, exibindo o texto correspondente.

## 3. Metodologia

### 3.1 Definição da Região do Semáforo

A área do semáforo é selecionada manualmente com o auxílio de uma interface gráfica, usando o script `roi.py`. A coordenada da região é salva automaticamente no arquivo `semaforo/roi.json` no formato `[x, y, largura, altura]`.

Essa abordagem garante flexibilidade e precisão para cada vídeo, evitando a necessidade de configurar manualmente no código.

### 3.2 Processamento do Quadro

Cada quadro do vídeo é processado pela função `processa_frame(img)`, que executa as seguintes etapas:

- **Conversão para escala de cinza**: prepara a imagem para binarização.
- **Limiar adaptativo (threshold)**: destaca regiões de interesse com contraste.
- **Filtro de mediana**: remove ruídos leves.
- **Dilatação**: reforça contornos para facilitar visualizações auxiliares.

### 3.3 Detecção da Luz Acesa

A função `verifica_estado_semaforo(img, semaforo)` realiza:

- Leitura da ROI salva no `roi.json`.
- Conversão da imagem ROI para o espaço de cor HSV.
- Criação de máscaras para tons de **vermelho** (dois intervalos HSV), **amarelo** e **verde**.
- Contagem de pixels em cada máscara para determinar qual luz está acesa.
- Retorno do status: `"VERMELHO"`, `"AMARELO"` ou `"VERDE"` (ou `"DESCONHECIDO"` se a ROI estiver vazia ou inválida).

### 3.4 Exibição do Status

A função `exibe_status(img, status)` exibe o texto correspondente ao status atual no canto superior esquerdo do vídeo:

- **“VERMELHO”**, em vermelho.
- **“AMARELO”**, em amarelo.
- **“VERDE”**, em verde.

## 4. Execução do Sistema

O sistema é executado por meio do script `main.py`. Ele realiza:

- Leitura do vídeo com `cv2.VideoCapture`.
- Carregamento da ROI via JSON.
- Processamento de cada quadro.
- Identificação da luz acesa.
- Exibição do resultado visual em tempo real.

## 5. Requisitos

- Python 3
- Bibliotecas:
  - OpenCV (`opencv-python`)
  - NumPy

### Instalação recomendada:

```bash
pip install opencv-python numpy
```

### Execução do projeto:

```bash
python semaforo/roi.py      # Para selecionar a região do semáforo
python semaforo/main.py     # Para iniciar a detecção
```

A execução pode ser encerrada a qualquer momento com a tecla `q`.

## 6. Considerações Finais

Este projeto demonstra como é possível utilizar técnicas simples de visão computacional para resolver problemas práticos relacionados ao monitoramento de tráfego urbano. A detecção de estados de semáforos pode ser aplicada em veículos autônomos, sistemas inteligentes de transporte e projetos de cidades inteligentes.

> Por conta do serviço, de outros trabalhos da faculdade como o PD1 não consegui me dedicar o quanto queria nesse trabalho. Algumas execuções não saíram como eu gostaria, e o resultado final ficou longe do que sei que poderia ter feito. 
> Agradeço pela compreensão :/
