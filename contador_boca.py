import cv2
import numpy as np
import mediapipe as mp
import time

def calcular_distancia(ponto1, ponto2):
    return np.sqrt((ponto1.x - ponto2.x)**2 + (ponto1.y - ponto2.y)**2)

def formatar_tempo(segundos):
    minutos = int(segundos // 60)
    segundos = int(segundos % 60)
    return f"{minutos:02d}:{segundos:02d}"

def main():
    # Inicializa a câmera
    cap = cv2.VideoCapture(0)
    print("Câmera inicializada")
    print("Inicializando câmera...")
    
    # Verifica se a câmera foi aberta corretamente
    if not cap.isOpened():
        print("Erro ao abrir a câmera!")
        return
    
    # Inicializa o MediaPipe
    mp_face_mesh = mp.solutions.face_mesh
    mp_hands = mp.solutions.hands
    
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    
    # Variáveis para controle
    contador = 0
    mão_na_boca = False
    distancia_anterior = float('inf')
    tempo_inicial = time.time()
    
    print("O programa vai contar quantas vezes você leva a mão à boca")
    print("Pressione 'k' para sair")
    
    while True:
        # Captura frame por frame
        ret, frame = cap.read()
        
        # Se não conseguir capturar o frame, sai do loop
        if not ret:
            print("Erro ao capturar frame!")
            break
        
        # Calcula o tempo decorrido
        tempo_atual = time.time()
        tempo_decorrido = tempo_atual - tempo_inicial
        tempo_formatado = formatar_tempo(tempo_decorrido)
        
        # Converte a imagem para RGB para o MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Processa a imagem para detecção de rosto
        face_results = face_mesh.process(frame_rgb)
        
        # Processa a imagem para detecção de mãos
        hands_results = hands.process(frame_rgb)
        
        # Pega a posição da boca
        boca_x = boca_y = None
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                # Pega o ponto da boca (índice 13)
                boca = face_landmarks.landmark[13]
                boca_x = int(boca.x * frame.shape[1])
                boca_y = int(boca.y * frame.shape[0])
        
        # Verifica se detectou mãos
        if hands_results.multi_hand_landmarks and boca_x is not None:
            for hand_landmarks in hands_results.multi_hand_landmarks:
                # Pega o ponto do dedo médio (índice 12)
                dedo_medio = hand_landmarks.landmark[12]
                dedo_x = int(dedo_medio.x * frame.shape[1])
                dedo_y = int(dedo_medio.y * frame.shape[0])
                
                # Calcula a distância entre o dedo e a boca
                distancia = np.sqrt((dedo_x - boca_x)**2 + (dedo_y - boca_y)**2)
                
                # Verifica se a mão está próxima da boca
                if distancia < 50:  # Ajuste este valor conforme necessário
                    if not mão_na_boca and distancia < distancia_anterior:
                        contador += 1
                        mão_na_boca = True
                else:
                    mão_na_boca = False
                
                distancia_anterior = distancia
        
        # Mostra o contador e o tempo na tela
        fonte = cv2.FONT_HERSHEY_SIMPLEX
        texto_contador = f"Contador: {contador}"
        texto_tempo = f"Tempo: {tempo_formatado}"
        
        # Posição e estilo do contador
        posicao_contador = (50, 50)
        posicao_tempo = (50, 100)
        escala = 1
        cor = (0, 255, 0)  # Verde
        espessura = 2
        
        cv2.putText(frame, texto_contador, posicao_contador, fonte, escala, cor, espessura)
        cv2.putText(frame, texto_tempo, posicao_tempo, fonte, escala, cor, espessura)
        
        # Mostra o frame
        cv2.imshow('Contador de Mão na Boca', frame)
        
        # Verifica as teclas pressionadas
        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord('k'):
            break
    
    # Libera a câmera e fecha todas as janelas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 