from flask import Flask, render_template, Response
import cv2
import os
import webbrowser

app = Flask(__name__)

def video_stream():
    # 웹캠 비디오 캡처 초기화
    cap = cv2.VideoCapture(0)

    # Haar Cascade 파일 경로
    cascade_path = 'haarcascade_frontalface_alt.xml'

    # Haar Cascade 분류기 초기화
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # TTS 설정
    tts_option = '-s 160 -p 80 -a 120 -v ko+f3'

    # TTS 실행 여부를 나타내는 플래그 변수
    tts_flag = True

    # YouTube 링크
    youtube_link = 'https://youtu.be/gIBz94KJZy8'

    # YouTube 링크를 열었는지를 나타내는 플래그 변수
    youtube_opened = False

    while True:
        # 프레임 읽기
        ret, frame = cap.read()

        # 얼굴 검출을 위해 그레이스케일로 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 얼굴 검출
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # 검출된 얼굴 주위에 사각형 그리기 및 TTS 실행
        if len(faces) > 0 and tts_flag:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # 얼굴이 검출된 사람 수를 TTS로 출력
            face_count = len(faces)
            speak_face_count(tts_option, face_count)

            # TTS 실행 후 플래그 변수를 False로 설정하여 다시 실행되지 않도록 함
            tts_flag = False

            # YouTube 링크를 열지 않은 경우에만 YouTube 링크 접속
            if not youtube_opened:
                open_youtube_link(youtube_link)
                youtube_opened = True
        youtube_opened = False
        # 얼굴이 검출되지 않았을 때 TTS 실행을 위해 플래그 변수를 True로 설정함
        if len(faces) == 0:
            tts_flag = True

        # 스트리밍을 위해 프레임 인코딩
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # 스트리밍 데이터 전송
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # 리소스 해제
    cap.release()

def speak_face_count(option, count):
    msg = '얼굴이 검출되었습니다.'.format(count)
    os.system("espeak {} '{}'".format(option, msg))
    os.system("youtube {} '{}'".format(option, msg))

def open_youtube_link(link):
    webbrowser.open(link)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
