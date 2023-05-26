from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

def video_stream():
    # 웹캠 비디오 캡처 초기화
    cap = cv2.VideoCapture(0)

    # Haar Cascade 파일 경로
    cascade_path = 'haarcascade_frontalface_alt.xml'

    # Haar Cascade 분류기 초기화
    face_cascade = cv2.CascadeClassifier(cascade_path)

    while True:
        # 프레임 읽기
        ret, frame = cap.read()

        # 얼굴 검출을 위해 그레이스케일로 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 얼굴 검출
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # 검출된 얼굴 주위에 사각형 그리기
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # 스트리밍을 위해 프레임 인코딩
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # 스트리밍 데이터 전송
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # 리소스 해제
    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
