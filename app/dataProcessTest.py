from socket import *
import os      
import torch
import clip       
from PIL import Image
import json

#socket通信设置
imageProcess_server = socket(AF_INET,SOCK_STREAM)
address = ('',9999)
imageProcess_server.bind(address)

imagePath = '/home/fusong/DataImage/test2/'


#载入模型
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)


#遍历图片
def getImage(imagePath):
    files_list = os.listdir(path = imagePath)
    return files_list

while (1):
    print("等待通讯……………………")
    imageProcess_server.listen()

    client_socket, clientAddr = imageProcess_server.accept()
    searchText = client_socket.recv(1024).decode("gbk")
    print("接收的数据："+searchText+" Client addrs is: "+str(clientAddr))

    send_data = client_socket.send(str(clientAddr[1]).encode("gbk"))
    client_socket.close()
    
    
    #模型处理图片和文字
    text = clip.tokenize([searchText, "a diagram", "a car", "a rabbit"]).to(device)
    text_features = model.encode_text(text)
    imageList = getImage(imagePath)#得到图片库中的图片List
    
    with open("/home/fusong/DataImage/searchBTResult/"
              +searchText+str(clientAddr[1])+".json", 'a') as f:
        f.write("[")
        count = 0
        for i in imageList:
            image = preprocess(Image.open(imagePath+i)).unsqueeze(0).to(device)
            with torch.no_grad():
                image_features = model.encode_image(image)
                logits_per_image, logits_per_text = model(image, text)
                probs = logits_per_image.softmax(dim=-1).cpu().numpy()
                if (probs[0][0]>0.8):
                    print("Label of image "+i+" probs:", probs[0][0])
                    if(count == 1):
                        f.write(", \""+i+"\"")
                    else:
                        f.write(" \""+i+"\"")
                        count = 1
        f.write(" ]")
        f.close()
    

