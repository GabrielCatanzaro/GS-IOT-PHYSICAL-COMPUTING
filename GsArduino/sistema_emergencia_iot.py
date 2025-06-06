"""
SISTEMA DE EMERGENCIA IoT - PHYSICAL COMPUTING
Projeto: GS Arduino - Detecao de Emergencias
Desenvolvido para situacoes de falta de energia
Tecnologia: MediaPipe + OpenCV + Python
"""

import cv2
import mediapipe as mp
import numpy as np
import time
import os

# Suprimir warnings
import warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class SistemaEmergenciaIoT:
    def __init__(self):
        print("Iniciando Sistema de Emergencia IoT...")
        
        # Inicializar MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.mp_draw = mp.solutions.drawing_utils
        
        # Estados do sistema
        self.status_atual = "MONITORANDO"
        self.confianca = 0.0
        self.ultima_deteccao = time.time()
        
        # Cores dos alertas (BGR)
        self.cores_status = {
            "SOCORRO": (0, 0, 255),           # Vermelho
            "ESTOU_BEM": (0, 255, 0),         # Verde
            "PRECISO_AJUDA": (0, 255, 255),   # Amarelo
            "PARE": (0, 165, 255),            # Laranja
            "PESSOA_CAIDA": (255, 0, 255),    # Magenta
            "MONITORANDO": (100, 100, 100)    # Cinza
        }
        
        # Mensagens simplificadas
        self.mensagens = {
            "SOCORRO": "EMERGENCIA CRITICA",
            "ESTOU_BEM": "PESSOA SEGURA",
            "PRECISO_AJUDA": "PRECISA ASSISTENCIA",
            "PARE": "COMANDO PARE",
            "PESSOA_CAIDA": "POSSIVEL QUEDA",
            "MONITORANDO": "SISTEMA ATIVO"
        }
        
        # Historico para estabilidade
        self.historico_gestos = []
        self.contador_frames = 0
        
        print("Sistema inicializado com sucesso!")

    def classificar_gesto_mao(self, landmarks):
        """Classifica gestos das maos"""
        if not landmarks:
            return "NONE", 0.0
        
        # Pontos dos dedos
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        index_tip = landmarks[8]
        index_pip = landmarks[6]
        middle_tip = landmarks[12]
        middle_pip = landmarks[10]
        ring_tip = landmarks[16]
        ring_pip = landmarks[14]
        pinky_tip = landmarks[20]
        pinky_pip = landmarks[18]
        
        # Verificar dedos estendidos
        fingers = []
        
        # Polegar
        if thumb_tip.x > thumb_ip.x:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Outros dedos
        tips = [index_tip, middle_tip, ring_tip, pinky_tip]
        pips = [index_pip, middle_pip, ring_pip, pinky_pip]
        
        for tip, pip in zip(tips, pips):
            if tip.y < pip.y:
                fingers.append(1)
            else:
                fingers.append(0)
        
        # Classificacao de gestos
        if fingers == [0, 1, 1, 1, 1]:  # 4 dedos
            return "SOCORRO", 0.95
        elif fingers == [1, 1, 0, 0, 0]:  # OK
            return "ESTOU_BEM", 0.90
        elif fingers == [0, 1, 1, 0, 0]:  # 2 dedos
            return "PRECISO_AJUDA", 0.85
        elif fingers == [1, 1, 1, 1, 1]:  # Mao aberta
            return "PARE", 0.88
        else:
            return "INDEFINIDO", 0.3

    def analisar_postura(self, landmarks, formato_frame):
        """Analisa postura corporal"""
        if not landmarks:
            return "POSE_NAO_DETECTADA", 0.0
        
        h, w = formato_frame[:2]
        
        # Pontos importantes
        nose = landmarks[0]
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]
        left_hip = landmarks[23]
        right_hip = landmarks[24]
        
        # Converter coordenadas
        nose_y = nose.y * h
        shoulder_y = ((left_shoulder.y + right_shoulder.y) / 2) * h
        hip_y = ((left_hip.y + right_hip.y) / 2) * h
        
        # Detectar pessoa caida
        if abs(nose_y - hip_y) < h * 0.25:
            return "PESSOA_CAIDA", 0.92
        
        return "POSTURA_NORMAL", 0.80

    def desenhar_hud_limpa(self, frame):
        """HUD moderna e limpa"""
        h, w = frame.shape[:2]
        
        # Painel superior minimalista
        cv2.rectangle(frame, (0, 0), (w, 70), (20, 20, 20), -1)
        
        # Titulo
        cv2.putText(frame, "SISTEMA IoT EMERGENCIA", (20, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
        # Status com cor
        cor = self.cores_status.get(self.status_atual, (255, 255, 255))
        cv2.putText(frame, self.status_atual, (20, 55),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, cor, 2)
        
        # Info lateral direita
        cv2.putText(frame, f"{self.confianca:.0%}", (w - 80, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, time.strftime("%H:%M:%S"), (w - 100, 55),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Alerta principal (apenas para emergencias)
        if self.status_atual != "MONITORANDO":
            # Fundo do alerta
            alpha = 0.7
            if self.status_atual in ["SOCORRO", "PESSOA_CAIDA"]:
                alpha = 0.5 + 0.3 * abs(np.sin(time.time() * 4))  # Piscar
            
            overlay = np.zeros((60, w, 3), dtype=np.uint8)
            overlay[:] = cor
            
            y_start = h - 60
            frame[y_start:h] = cv2.addWeighted(
                frame[y_start:h], 1-alpha, overlay, alpha, 0)
            
            # Mensagem centralizada
            message = self.mensagens[self.status_atual]
            text_size = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
            text_x = (w - text_size[0]) // 2
            
            cv2.putText(frame, message, (text_x, h - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
        # Instrucoes minimas (canto)
        if self.status_atual == "MONITORANDO":
            instrucoes = [
                "4 dedos = SOCORRO",
                "OK = ESTOU BEM", 
                "2 dedos = AJUDA",
                "Mao aberta = PARE"
            ]
            
            for i, instr in enumerate(instrucoes):
                cv2.putText(frame, instr, (w - 200, 90 + i * 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180, 180, 180), 1)
        
        return frame

    def estabilizar_deteccao(self, gesto, confianca):
        """Estabiliza deteccao"""
        self.historico_gestos.append((gesto, confianca))
        
        if len(self.historico_gestos) > 5:
            self.historico_gestos.pop(0)
        
        if len(self.historico_gestos) >= 3:
            gestos_recentes = [g[0] for g in self.historico_gestos[-3:]]
            confiancas = [g[1] for g in self.historico_gestos[-3:]]
            
            mais_comum = max(set(gestos_recentes), key=gestos_recentes.count)
            if gestos_recentes.count(mais_comum) >= 2 and max(confiancas) > 0.7:
                return mais_comum, max(confiancas)
        
        return self.status_atual, self.confianca

    def executar_sistema(self):
        """Loop principal"""
        print("Iniciando camera...")
        print("Instrucoes:")
        print("  4 dedos = SOCORRO")
        print("  OK = ESTOU BEM")
        print("  2 dedos = AJUDA")
        print("  Mao aberta = PARE")
        print("  q = sair | r = reset | s = screenshot | v = gravar")
        
        # Inicializar camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("ERRO: Camera nao encontrada!")
            return
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        gravando = False
        video_writer = None
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    continue
                
                self.contador_frames += 1
                frame = cv2.flip(frame, 1)
                
                # Processar com MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                hand_results = self.hands.process(rgb_frame)
                pose_results = self.pose.process(rgb_frame)
                
                # Reset se sem deteccao
                if (not hand_results.multi_hand_landmarks and 
                    not pose_results.pose_landmarks and
                    time.time() - self.ultima_deteccao > 3):
                    self.status_atual = "MONITORANDO"
                    self.confianca = 0.0
                
                # Processar maos
                gesto_detectado = "MONITORANDO"
                confianca_gesto = 0.0
                
                if hand_results.multi_hand_landmarks:
                    for hand_landmarks in hand_results.multi_hand_landmarks:
                        # Desenhar landmarks
                        self.mp_draw.draw_landmarks(
                            frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                            self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2),
                            self.mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
                        )
                        
                        gesto, conf = self.classificar_gesto_mao(hand_landmarks.landmark)
                        if conf > confianca_gesto:
                            gesto_detectado = gesto
                            confianca_gesto = conf
                
                # Processar pose
                if pose_results.pose_landmarks:
                    # Desenhar skeleton
                    self.mp_draw.draw_landmarks(
                        frame, pose_results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                        self.mp_draw.DrawingSpec(color=(245, 117, 66), thickness=2),
                        self.mp_draw.DrawingSpec(color=(245, 66, 230), thickness=2)
                    )
                    
                    pose_status, pose_conf = self.analisar_postura(
                        pose_results.pose_landmarks.landmark, frame.shape)
                    
                    if pose_status == "PESSOA_CAIDA" and pose_conf > 0.8:
                        gesto_detectado = "PESSOA_CAIDA"
                        confianca_gesto = pose_conf
                
                # Atualizar estado
                if confianca_gesto > 0.7:
                    status, conf = self.estabilizar_deteccao(gesto_detectado, confianca_gesto)
                    self.status_atual = status
                    self.confianca = conf
                    self.ultima_deteccao = time.time()
                
                # Desenhar HUD
                frame = self.desenhar_hud_limpa(frame)
                
                # Indicador gravacao
                if gravando:
                    cv2.circle(frame, (30, 30), 8, (0, 0, 255), -1)
                
                # Mostrar frame
                cv2.imshow('Sistema IoT Emergencia - GS Arduino', frame)
                
                # Gravar se ativo
                if gravando and video_writer:
                    video_writer.write(frame)
                
                # Controles
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    self.status_atual = "MONITORANDO"
                    self.confianca = 0.0
                    self.historico_gestos.clear()
                    print("Sistema resetado")
                elif key == ord('s'):
                    filename = f"screenshot_{int(time.time())}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"Screenshot salvo: {filename}")
                elif key == ord('v'):
                    if not gravando:
                        video_name = f"video_emergencia_{int(time.time())}.avi"
                        fourcc = cv2.VideoWriter_fourcc(*'XVID')
                        video_writer = cv2.VideoWriter(video_name, fourcc, 20.0, 
                                                     (frame.shape[1], frame.shape[0]))
                        gravando = True
                        print(f"Gravacao iniciada: {video_name}")
                    else:
                        gravando = False
                        if video_writer:
                            video_writer.release()
                        print("Gravacao finalizada")
        
        except Exception as e:
            print(f"Erro: {e}")
        
        finally:
            if gravando and video_writer:
                video_writer.release()
            cap.release()
            cv2.destroyAllWindows()
            print("Sistema finalizado!")

def main():
    print("=" * 50)
    print("SISTEMA DE EMERGENCIA IoT")
    print("Projeto: GS Arduino")
    print("Physical Computing Challenge")
    print("=" * 50)
    
    try:
        import mediapipe as mp
        print(f"MediaPipe: {mp.__version__}")
        print(f"OpenCV: {cv2.__version__}")
        
        sistema = SistemaEmergenciaIoT()
        sistema.executar_sistema()
        
    except ImportError as e:
        print("ERRO: Dependencias nao instaladas!")
        print("Solucao: pip install mediapipe opencv-python")
    
    input("Pressione Enter para finalizar...")

if __name__ == "__main__":
    main()