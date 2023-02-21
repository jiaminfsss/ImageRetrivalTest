from flask import Flask, render_template, request, send_from_directory, send_file, json, jsonify, make_response
import requests
from socket import *
import os
import time

sendPort = 9998
imageServerPort = 9999

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/searchResult/")
def searchResult():
    return render_template("searchResult.html")

@app.route("/getResult/<file_name>", methods=['GET'])
def getResult(file_name):
    directory = "/home/fusong/DataImage/searchBTResult/"
    
    while not os.path.exists(directory+file_name):
        time.sleep(1)
        #pass
    #try:
    response = make_response(
        send_from_directory(directory, file_name, as_attachment=True))
    print(response)
    return response

@app.route("/getImage/<file_name>", methods=['GET'])
def getImage(file_name):
    directory = "/home/fusong/DataImage/test3/"
    return send_file(directory+file_name, mimetype='image/gif')

@app.route("/searchByImage", methods=['POST'])
def searchByImage():
    img = request.files.get('searchImage')
    kNeighbor = request.form['kNeighbor']
    suffix = '.' + img.filename.split('.')[-1] # 获取文件后缀名
    basedir = '/home/fusong/DataImage/upload/'
    image_name = str(int(time.time()))+suffix
    image_path = basedir+image_name
    #保存图片至服务器指定文件夹
    img.save(image_path)
    sendMessage = ['1']
    sendMessage.append(image_name)
    sendMessage.append(kNeighbor)
    print("当前搜索的图片是："+image_name)
    sendSocket = socket(AF_INET,SOCK_STREAM)
    sendSocket.connect(('',imageServerPort))
    sendMessage_json = json.dumps(sendMessage)
    sendSocket.send(bytes(sendMessage_json.encode('utf-8')))
    portNum = sendSocket.recv(1024).decode("gbk")
    print("从服务器接收到的数据是："+portNum)
    sendSocket.close()
    return render_template('searchResult.html', 
                           filenameToSave=image_name, 
                           communicatePort=portNum
                           )

@app.route("/searchByText", methods=['POST'])
def searchByText():
    searchText = request.form['searchText']
    kNeighbor = request.form['kNeighbor']
    print("当前搜索的图片是："+searchText)
    sendSocket = socket(AF_INET,SOCK_STREAM)
    sendSocket.connect(('',imageServerPort))
    sendMessage = ['0']
    sendMessage.append(searchText)
    sendMessage.append(kNeighbor)
    sendMessage_json = json.dumps(sendMessage)
    sendSocket.send(bytes(sendMessage_json.encode('utf-8')))
    portNum = sendSocket.recv(1024).decode("gbk")
    print("从服务器接收到的数据是："+portNum)
    sendSocket.close()
    return render_template('searchResult.html', 
                           filenameToSave=searchText, 
                           communicatePort=portNum
                           )

if __name__ == "__main__":
    app.run()