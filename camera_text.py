import cv2
import numpy as np
import mediapipe as mp

def detectar_mao_aberta(hand_landmarks):
    if not hand_landmarks:
        return False
    
    # Pega as coordenadas dos dedos
    dedos = []
    for dedo in [8, 12, 16, 20]:  # Pontas dos dedos (exceto polegar)
        dedos.append(hand_landmarks.landmark[dedo].y)
    
    # Pega a coordenada da base da mão
    base = hand_landmarks.landmark[0].y
    
    # Verifica se todos os dedos estão estendidos (y menor que a base)
    return all(dedo < base for dedo in dedos)

def main():
    # Inicializa a câmera
    cap = cv2.VideoCapture(0)
    
    # Verifica se a câmera foi aberta corretamente
    if not cap.isOpened():
        print("Erro ao abrir a câmera!")
        return
    
    # Inicializa o MediaPipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    mp_draw = mp.solutions.drawing_utils
    
    # Variável para controlar a exibição do texto
    mostrar_texto = False
    
    print("Mostre sua mão aberta para alternar o texto 'vamo embora'")
    print("Pressione 'k' para sair")
    
    while True:
        # Captura frame por frame
        ret, frame = cap.read()
        
        # Se não conseguir capturar o frame, sai do loop
        if not ret:
            print("Erro ao capturar frame!")
            break
        
        # Converte a imagem para RGB para o MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Processa a imagem
        results = hands.process(frame_rgb)
        
        # Verifica se detectou mãos
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Desenha os pontos da mão
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Verifica se a mão está aberta
                if detectar_mao_aberta(hand_landmarks):
                    mostrar_texto = not mostrar_texto
        
        # Se mostrar_texto for True, adiciona o texto
        if mostrar_texto:
            # Configurações do texto
            fonte = cv2.FONT_HERSHEY_SIMPLEX
            texto = "vamo embora"
            posicao = (50, 50)
            escala = 1
            cor_vermelho = (0, 0, 255)  # Vermelho
            cor_preto = (0, 0, 0)  # Preto
            espessura_borda = 4
            espessura_texto = 2
            
            # Adiciona a borda preta do texto
            cv2.putText(frame, texto, posicao, fonte, escala, cor_preto, espessura_borda)
            
            # Adiciona o texto vermelho por cima
            cv2.putText(frame, texto, posicao, fonte, escala, cor_vermelho, espessura_texto)
        
        # Mostra o frame
        cv2.imshow('Camera com Detecção de Mão', frame)
        
        # Verifica as teclas pressionadas
        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord('k'):
            break
    
    # Libera a câmera e fecha todas as janelas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 