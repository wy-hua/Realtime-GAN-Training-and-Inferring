from flask import Flask
# from flask import jsonify
# from flask_cors import  CORS
# from flask import  request
import  time
from  flask_socketio import  SocketIO
from src.training import Train
app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins='*')
myTrain=Train(socketio)
myTrain.Listen()
if __name__ == '__main__':
    socketio.run(app,debug=True,host='0.0.0.0',port=5000)  
