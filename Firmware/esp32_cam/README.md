# _Projeto - ESP32-CAM_

![Firmware version](https://img.shields.io/badge/Firmware_version-1.0.0-blue)

---

## Sumário

- [Histórico de Versão](#histórico-de-versão)
- [Resumo](#resumo)
- [Objetivo](#objetivo)
- [Links para estudos](#links-para-estudos)
- [Pinos do projeto eletrônico](#pinos-do-projeto-eletrônico)
- [Bibliotecas](#bibliotecas)
- [Informações](#informações)

## Histórico de versão

| Versão | Data       | Autor         | Descrição          |
|--------|------------|---------------|--------------------|
| 1.0.0  | 19/03/2026 | Adenilton R   | Inicio do projeto  |

---

## Resumo

Este projeto implementa um firmware embarcado utilizando o ESP32-CAM com ESP-IDF v5.4, responsável pela captura de imagens e transmissão em tempo real através de um servidor HTTP com stream MJPEG.

O sistema realiza:

- Inicialização da câmera (sensor OV2640)
- Conexão Wi-Fi configurável via menuconfig
- Configuração opcional de IP fixo
- Execução de servidor HTTP embarcado
- Transmissão contínua de frames via rede

O firmware foi desenvolvido com FreeRTOS, garantindo execução eficiente e controle de tarefas.

## Objetivo

- Implementar um firmware para transformar o ESP32-CAM em uma câmera IP
- Permitir configuração flexível via menuconfig
- Disponibilizar stream de vídeo via HTTP
- Criar base reutilizável para aplicações embarcadas com visão

## Links para estudos

[**Documentação ESP-IDF**](https://docs.espressif.com/projects/esp-idf/en/v5.4.0/esp32s3/index.html)

[**Servidor Web de Transmissão ao Vivo ESP32-CAM ESP-IDF**](https://esp32tutorials.com/esp32-cam-esp-idf-live-streaming-web-server/)

[**FreeRTOS**](https://www.freertos.org/)

## Pinos do projeto eletrônico

| **Pino** | **Conexão** | **Tipo** | **Descrição** |
|----------|-------------|----------|---------------|
| GPIO16   | TX (UART)   | UART     | Transmissão   |
| GPIO15   | RX (UART)   | UART     | Recepção      |

## Bibliotecas

## Estrutura do Projeto

```
main/
├── main.c# Inicialização do sistema e servidor HTTP
├── connect_wifi.c# Gerenciamento da conexão Wi-Fi
├── connect_wifi.h
├── camera_pins.h# Definição dos pinos da câmera
├── Kconfig.projbuild# Configurações via menuconfig
```

## Configuração via Menuconfig

O projeto utiliza o sistema nativo do ESP-IDF para configuração.

## Acessar menuconfig

```
idf.py menuconfig
```

## Parâmetros configuráveis

### Wi-Fi

- SSID da rede
- Senha
- Número máximo de tentativas

### Rede

- Ativar IP fixo
- Endereço IP
- Gateway
- Máscara de rede

### Hardware

- Seleção do modelo da placa (ESP32-CAM)

## Funcionamento do Firmware

O fluxo de execução do sistema segue a seguinte sequência:

### Inicialização

1. Inicializa memória NVS
2. Inicializa stack de rede (TCP/IP)
3. Conecta ao Wi-Fi
4. Configura IP (fixo ou DHCP)
5. Inicializa câmera
6. Inicia servidor HTTP

### Captura de imagem

- A câmera captura frames no formato **JPEG**
- Os dados são armazenados em buffer na PSRAM
- Frames são enviados continuamente

### Streaming MJPEG

- Servidor HTTP responde na rota `/`
- Envia stream multipart (`multipart/x-mixed-replace`)
- Navegador exibe como vídeo em tempo real

## Inicialização esperada (log)

```
Wi-Fi conectado!
IP obtido: 192.168.X.X
Câmera inicializada com sucesso
Servidor HTTP iniciado
```

## Acesso ao Stream

Após iniciar o firmware:

```
http://IP_DO_ESP32
```

Exemplo:

```
http://192.168.15.30
```

## Observações Técnicas

- Uso de **PSRAM é obrigatório** para melhor desempenho
- Resolução recomendada: VGA ou inferior para estabilidade
- Wi-Fi ativo pode impactar FPS
- Logs do tipo `wifi:<ba-add>` são normais
- Erros de porta COM são do ambiente de desenvolvimento

## Possíveis Melhorias Futuras

- Endpoint para captura de imagem (`/capture`)
- Controle de qualidade/resolução via HTTP
- Autenticação de acesso
- Buffer duplo para aumento de FPS
- Integração com backend

## Informações

| Info        | Modelo           |
|-------------|------------------|
| uC          | ESP32            |
| Placa       | ESP32-CAM        |
| Arquitetura | Xtensa / RISC    |
| IDE         | IDF v5.4.0       |