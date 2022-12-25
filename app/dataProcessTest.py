from socket import *
import os             


imageProcess_server = socket(AF_INET,SOCK_STREAM)
address = ('',9999)
imageProcess_server.bind(address)


while (1):
    print("等待通讯……………………")
    imageProcess_server.listen()

    client_socket, clientAddr = imageProcess_server.accept()
    searchText = client_socket.recv(1024)
    print("接收的数据：", searchText.decode("gbk"))

    send_data = client_socket.send("我接受到的数据为：".encode("gbk")+searchText)
    client_socket.close()



