from flask import Flask,render_template,request
import requests
from socket import *

sendPort = 9998
imageServerPort = 9999

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/searchByText",methods=['POST'])
def searchByText():
    searchText = request.form['searchText']
    print("当前搜索的图片是："+searchText)
    sendSocket = socket(AF_INET,SOCK_STREAM)
    sendSocket.connect(('',imageServerPort))
    sendSocket.send(searchText.encode("gbk"))
    from_imageServer_msg = sendSocket.recv(1024)
    print("从服务器接收到的数据是："+from_imageServer_msg.decode("gbk"))
    sendSocket.close()
    return render_template('index.html')

if __name__ == "__main__":
    app.run()