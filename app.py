from flask import Flask,render_template,Response
import cv2 as cv 
from main import serve

app=Flask(__name__)
camera=cv.VideoCapture(2)
camera.set(3,1280) #width
camera.set(4,720) #height
history=[]

def generate_frames():
    while True:
       
        success,frame=camera.read()
        if not success:
            break
        else:
            try:
                frame,finEq=serve(frame)
            except:
                pass
            if finEq!="":
                global history
                history.append(finEq)
                print(history)
            ret,buffer=cv.imencode('.jpg',frame)
            frame=buffer.tobytes()
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        

@app.route('/')
def index():
    # return "Starting"
    return render_template('index.html')

@app.route('/video')
def video_function():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__=="__main__":
    app.run(debug=True)