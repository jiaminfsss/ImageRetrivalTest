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
    '''
    except Exception as e:
        return jsonify({"code": "异常", "message": "{}".format(e)})
    '''

@app.route("/getImage/<file_name>", methods=['GET'])
def getImage(file_name):
    directory = "/home/fusong/DataImage/test2/"
    return send_file(directory+file_name, mimetype='image/gif')

@app.route("/searchByImage", methods=['POST'])
def searchByImage():
    img = request.files.get('searchImage')
    suffix = '.' + img.filename.split('.')[-1] # 获取文件后缀名
    basedir = '/home/fusong/DataImage/upload/'
    image_name = str(int(time.time()))+suffix
    image_path = basedir+image_name
    img.save(image_path)

@app.route("/searchByText", methods=['POST'])
def searchByText():
    searchText = request.form['searchText']
    print("当前搜索的图片是："+searchText)
    sendSocket = socket(AF_INET,SOCK_STREAM)
    sendSocket.connect(('',imageServerPort))
    sendSocket.send(searchText.encode("gbk"))
    portNum = sendSocket.recv(1024).decode("gbk")
    print("从服务器接收到的数据是："+portNum)
    sendSocket.close()
    return render_template('searchResult.html', 
                           searchText=searchText, 
                           communicatePort=portNum
                           )

if __name__ == "__main__":
    app.run()