"""
 * NOME: Adenilton Ribeiro
 * DATA: 20/03/2026
 * PROJETO: CAM Control for ESP32-CAM
 * VERSAO: 1.0.0
 * DESCRICAO: - 
"""
import cv2

# URL da ESP32-CAM
url = "http://192.168.15.30"

cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Erro ao capturar frame")
        break

    cv2.imshow("ESP32-CAM", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC para sair
        break

cap.release()
cv2.destroyAllWindows()