from socket import *
from time import ctime
import json

print("-----------------------------时间戳TCP服务器------------------")

HOST = '127.0.0.1' #主机号为空白，表示使用任何可以使用的地址
PORT = 3368
BUFSIZ = 1024
ADDR = (HOST, PORT)
MAGIC_STRING = "HTTP"

tcpSerSock = socket(AF_INET, SOCK_STREAM) #创建TCP服务器套接字
tcpSerSock.bind(ADDR)                     #套接字与地址绑定
tcpSerSock.listen(5)                      #监听连接，同时连接请求的最大数目

while True:
    print('等待客户端的连接')
    tcpCliSock, addr =tcpSerSock.accept()  #收取客户端连接请求
    print('取得连接：', addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ)     #连续接受指定字节的数据，接收到的是字节数组
        if not data:                       #如果数据空白，退出接受
            break
        weather = []
        with open("forecast.json", "r") as file_obj:
            weather = json.load(file_obj)

        for k in range(1, len(weather)):
            if(weather[k]['date'] == data.decode('utf-8')):
                ans = weather[k]
                break;
        pd = 'Am I right?'
        tcpCliSock.send(bytes('[%s]\n[%s]\n[%s]\n' %(ans,pd,ctime()), 'utf-8'))

        print(data)

    tcpCliSock.close()
tcpSerSock.close()


