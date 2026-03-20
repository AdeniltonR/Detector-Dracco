'''
 * NOME: Adenilton Ribeiro
 * DATA: 20/03/2026
 * PROJETO: Flask com Orange Pi Zero 3
 * VERSAO: 01
 * DESCRICAO: - feat: Criar página para exibir stream da ESP32-CAM.
'''

from flask import Flask, render_template, Response
import cv2

# URL da ESP32-CAM
CAMERA_URL = "http://192.168.15.30"

def create_app():
    app = Flask(__name__)

    # Inicializa captura (uma única vez)
    video_capture = cv2.VideoCapture(CAMERA_URL, cv2.CAP_FFMPEG)

    def generate_frames():
        while True:
            success, frame = video_capture.read()

            if not success:
                print("❌ Erro ao capturar frame da câmera")
                continue

            # Codifica JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            # Stream MJPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/video_feed')
    def video_feed():
        return Response(generate_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    return app