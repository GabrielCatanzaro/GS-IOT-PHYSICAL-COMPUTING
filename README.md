# GS-IOT-PHYSICAL-COMPUTING

# 🚨 Sistema IoT de Emergência - Physical Computing

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red.svg)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen.svg)

## 📖 Sobre o Projeto

O **Sistema IoT de Emergência** é uma solução inovadora desenvolvida para o **Physical Computing Challenge** que utiliza **visão computacional** e **inteligência artificial** para detectar situações de emergência através de gestos e posturas corporais.

### 🎯 Problema Identificado

Durante **falhas de energia**, pessoas podem ficar em situações de risco sem conseguir se comunicar adequadamente com serviços de emergência. Sistemas tradicionais de comunicação falham, mas dispositivos com bateria (laptops, tablets, smartphones) ainda podem funcionar por horas.

### 💡 Nossa Solução

Um sistema que funciona **apenas com uma câmera** e detecta automaticamente:
- 🖐️ **Gestos de emergência** (socorro, ajuda, pare)
- 🤸 **Posturas corporais** (quedas, posições anômalas)
- ✅ **Sinais de segurança** (pessoa está bem)

---

## 🚀 Tecnologias Utilizadas

| Tecnologia | Versão | Função |
|------------|--------|--------|
| **Python** | 3.11+ | Linguagem principal |
| **MediaPipe** | 0.10.9 | Detecção de landmarks corporais |
| **OpenCV** | 4.x | Processamento de imagem |
| **NumPy** | Latest | Operações matemáticas |
| **Anaconda** | Latest | Gerenciamento de ambiente |

---

## 📥 Instalação e Configuração

### Pré-requisitos
- **Python 3.11** (recomendado via Anaconda)
- **Webcam** funcional
- **Sistema Operacional:** Windows 10/11, macOS, Linux

### 1️⃣ Instalar Anaconda
```bash
# Baixe e instale o Anaconda
# https://www.anaconda.com/download
```

### 2️⃣ Criar Ambiente Virtual
```bash
# Criar ambiente com Python 3.11
conda create -n mediapipe_project python=3.11 -y

# Ativar ambiente
conda activate mediapipe_project
```

### 3️⃣ Instalar Dependências
```bash
# Instalar bibliotecas necessárias
pip install mediapipe==0.10.9 opencv-python numpy matplotlib
```

### 4️⃣ Verificar Instalação
```bash
# Testar se tudo está funcionando
python -c "import mediapipe as mp; import cv2; print('✅ Instalação OK!')"
```

---

## ▶️ Como Executar

### Método 1: Executar Diretamente
```bash
# Navegar para pasta do projeto
cd /caminho/para/o/projeto

# Ativar ambiente
conda activate mediapipe_project

# Executar sistema
python sistema_emergencia_iot.py
```

### Método 2: Clone do Repositório
```bash
# Clonar repositório
git clone https://github.com/seu-usuario/sistema-iot-emergencia.git
cd sistema-iot-emergencia

# Configurar ambiente
conda env create -f environment.yml
conda activate mediapipe_project

# Executar
python sistema_emergencia_iot.py
```

---

## 🎮 Como Usar

### Gestos de Emergência Detectados

| Gesto | Detecção | Status | Cor |
|-------|----------|--------|-----|
| 🖐️ **4 Dedos** (sem polegar) | Socorro | `EMERGENCIA CRITICA` | 🔴 Vermelho |
| 👌 **OK** (polegar + indicador) | Segurança | `PESSOA SEGURA` | 🟢 Verde |
| ✌️ **2 Dedos** (paz/vitória) | Assistência | `PRECISA ASSISTENCIA` | 🟡 Amarelo |
| 🖐️ **Mão Aberta** (todos dedos) | Parada | `COMANDO PARE` | 🟠 Laranja |
| 🤸 **Pessoa Deitada** | Queda | `POSSIVEL QUEDA` | 🟣 Magenta |

### Controles do Sistema

| Tecla | Função |
|-------|--------|
| **Q** | Sair do sistema |
| **R** | Reset/Reiniciar detecção |
| **S** | Tirar screenshot |
| **V** | Iniciar/Parar gravação |

---

## 🎯 Funcionalidades

### ✅ Principais Recursos
- **Detecção em tempo real** de gestos e posturas
- **Interface limpa e responsiva** 
- **Sistema de estabilização** (evita falsos positivos)
- **Alertas visuais coloridos** para diferentes emergências
- **Gravação automática** de situações de emergência
- **Screenshots** para documentação
- **Timestamp** e monitoramento contínuo

### 🧠 Algoritmos Utilizados
- **Hand Landmark Detection** (MediaPipe)
- **Pose Estimation** (MediaPipe) 
- **Background Subtraction** para movimento
- **Algoritmo de estabilização** com histórico
- **Classificação por múltiplos fatores**

---

---

## 🏥 Aplicações Práticas

### 🎯 Cenários de Uso
- **Hospitais** durante falhas de energia
- **Residências** com idosos ou pessoas com mobilidade reduzida
- **Centros de comando** em situações de emergência
- **Escolas** durante evacuações
- **Escritórios** em situações de risco
- **Casas inteligentes** com sistema de monitoramento

### 💼 Benefícios
- ✅ **Sem hardware adicional** (apenas câmera)
- ✅ **Baixo consumo** de energia
- ✅ **Funcionamento offline**
- ✅ **Interface intuitiva**
- ✅ **Detecção precisa** e estável
- ✅ **Gravação automática** de evidências

---

## 🔧 Configuração Avançada

### Ajustar Sensibilidade
```python
# No arquivo sistema_emergencia_iot.py
# Linha ~30-35: Configurações do MediaPipe

self.hands = self.mp_hands.Hands(
    min_detection_confidence=0.7,  # Diminuir para mais sensível
    min_tracking_confidence=0.5    # Aumentar para mais estável
)
```

### Personalizar Gestos
```python
# Adicionar novos gestos na função classificar_gesto_mao()
# Exemplo: gesto de punho fechado
elif sum(fingers) == 0:  # Todos dedos fechados
    return "EMERGENCIA_MAXIMA", 0.95
```

---

## 🐛 Resolução de Problemas

### ❌ Problemas Comuns

**1. Câmera não abre:**
```bash
# Testar câmera
python -c "import cv2; cap = cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'ERRO')"
```

**2. MediaPipe não importa:**
```bash
# Reinstalar MediaPipe
pip uninstall mediapipe -y
pip install mediapipe==0.10.9
```

**3. Gestos não detectados:**
- Verificar iluminação adequada
- Manter mãos visíveis na câmera
- Fazer gestos de forma clara e pausada

**4. Performance lenta:**
- Fechar outros programas que usam câmera
- Reduzir resolução da câmera
- Verificar se está no ambiente correto



### 🔮 Próximas Versões
- [ ] **v2.0:** Detecção de múltiplas pessoas
- [ ] **v2.1:** Integração com sistemas IoT
- [ ] **v2.2:** App mobile companion
- [ ] **v2.3:** Dashboard web em tempo real
- [ ] **v2.4:** Inteligência artificial aprimorada
- [ ] **v2.5:** Integração com services de emergência

### 🎯 Melhorias Planejadas
- Efeitos sonoros para identificação mais adequada
- mais métodos de identificação e comandos
