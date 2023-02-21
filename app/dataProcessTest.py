from socket import *
import os      
import torch
import clip       
from PIL import Image
import json
import faiss
import pymysql

#socket通信设置
imageProcess_server = socket(AF_INET,SOCK_STREAM)
address = ('',9999)
imageProcess_server.bind(address)

imagePath = '/home/fusong/DataImage/test2/'
imagePathUpload = '/home/fusong/DataImage/upload/'
#载入模型
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

#连接数据库
db = pymysql.connect(host = '127.0.0.1',
                     user = 'fsjm',
                     password = '123456',
                     database = 'Image_id_name')
#创建数据库游标对象cursor
cursor = db.cursor()

#载入之前训练好的Faiss索引
index = faiss.read_index('/home/fusong/DataImage/index_test3')

while (1):
    print("等待通讯……………………")
    imageProcess_server.listen()

    client_socket, clientAddr = imageProcess_server.accept()
    receiveMessage_json = client_socket.recv(1024)
    receiveMessage = json.loads(receiveMessage_json)
    #searchMode为0时表示文字搜图，为1时为以图搜图
    searchMode = receiveMessage[0]
    if searchMode=='0':
        filenameToSave = receiveMessage[1]
        print("接收的数据："+filenameToSave+" Client addrs is: "+str(clientAddr))

        send_data = client_socket.send(str(clientAddr[1]).encode("gbk"))
        client_socket.close()
        
        #模型处理图片和文字
        text = clip.tokenize([filenameToSave]).to(device)
        text_features = model.encode_text(text)
        text_features_np = text_features.cpu().detach().numpy().astype('float32')
        #归一化以用于计算余弦相似度
        faiss.normalize_L2(text_features_np)
        
        #检索k近邻
        k = int(receiveMessage[2])
        dis, image_id = index.search(text_features_np,k)
        #将搜索结果存储，以便于前端展示
        imageResultList=[]
        for i in image_id[0]:
            sql = 'SELECT * FROM Image_id_name_test3 WHERE image_id="'+str(i)+'";'
            cursor.execute(sql)
            imageResultList.append(cursor.fetchone()[1])
            #print(cursor.fetchone())
        #将结果转换成json格式
        imageResultList_json = json.dumps(imageResultList,ensure_ascii=False)
            
        #将搜索结果保存在文件中
        with open("/home/fusong/DataImage/searchBTResult/"
                +filenameToSave+str(clientAddr[1])+".json", 'w') as f:
            f.write(imageResultList_json)
    elif searchMode=='1':
        filenameToSave = receiveMessage[1]
        print("接收的数据："+filenameToSave+" Client addrs is: "+str(clientAddr))

        send_data = client_socket.send(str(clientAddr[1]).encode("gbk"))
        client_socket.close()
        #处理接收到的图片
        image = preprocess(Image.open(imagePathUpload+filenameToSave)).unsqueeze(0).to(device)
        #模型提取该图片的特征向量
        image_features = model.encode_image(image)
        image_features_np = image_features.cpu().detach().numpy().astype('float32')
        #归一化以用于计算余弦相似度
        faiss.normalize_L2(image_features_np)
        #检索k近邻
        k = int(receiveMessage[2])
        dis, image_id = index.search(image_features_np,k)
        #将搜索结果存储，以便于前端展示
        imageResultList=[]
        for i in image_id[0]:
            sql = 'SELECT * FROM Image_id_name_test3 WHERE image_id="'+str(i)+'";'
            cursor.execute(sql)
            imageResultList.append(cursor.fetchone()[1])
            #print(cursor.fetchone())
        #将结果转换成json格式
        imageResultList_json = json.dumps(imageResultList,ensure_ascii=False)
        with open("/home/fusong/DataImage/searchBTResult/"
                +filenameToSave+str(clientAddr[1])+".json", 'w') as f:
            f.write(imageResultList_json)
        
        
                        
        
    

