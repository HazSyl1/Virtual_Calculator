from flask import Flask,render_template,Response, jsonify , request
import cv2 as cv 
from main import serve
import numpy as np
import base64
from flask_cors import CORS





app=Flask(__name__)
CORS(app)


# camera=cv.VideoCapture(2)
# camera.set(3,1280) #width
# camera.set(4,720) #height
history=[]




# def generate_frames():
#     while True:
       
#         success,frame=camera.read()
#         if not success:
#             break
#         else:
#             try:
#                 frame,finEq=serve(frame)
#             except:
#                 pass
#             if finEq!="":
#                 global history
#                 history.append(finEq)
#                 print(history)
#             ret,buffer=cv.imencode('.jpg',frame)
#             frame=buffer.tobytes()
#             yield(b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        

@app.route('/process_frame',methods=['POST'])
def process_frame():
    try:
        file=request.files['frame']
        
        file_byte=np.frombuffer(file.read(),np.uint8)
        frame=cv.imdecode(file_byte,cv.IMREAD_COLOR)
        frame,finEq=serve(frame)
        # print("GOT PROCESSED FILE")
        _,buffer=cv.imencode('.jpg',frame)
        processed_frame=base64.b64encode(buffer).decode('utf-8')
        if finEq!="":
            global history
            history.append(finEq)
            
            print(history)
        return jsonify(success=True, frame =processed_frame)
    except Exception as e:
        print(e)
        return jsonify(success=False,message=str(e)) 
        

@app.route('/get_history')
def update_history():
    global history
    print(history)
    return jsonify(success=True,history=history)

@app.route('/')
def index():
    # return "Starting"
    global history
    return render_template('index.html',history=history)

@app.route('/video')
def video_function():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__=="__main__":
    app.run(debug=True)