import socket
import numpy as np
import cv2

# 서버의 IP 주소를 입력받는다.
server_ip = input('접속할 서버의 IP 또는 도메인을 입력해주세요.\n(기본값: 127.0.0.1) >>> ')
if not server_ip:
    server_ip = '127.0.0.1'
server_port = 50000

# 통신용 소켓을 생성한다.
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # 서버에 연결한다.
    client_sock.connect((server_ip, server_port))
except ConnectionRefusedError as e:
    print(e)
    exit(1)

# 서버에 연결했음을 알린다.
print('[Client] 서버 연결: {}:{}'.format(server_ip, server_port))

while cv2.waitKey(16) != 27:
    try:
        client_sock.send(b'1')

        length = int(client_sock.recv(16, socket.MSG_WAITALL))
        data = client_sock.recv(length, socket.MSG_WAITALL)
        data = np.frombuffer(data, dtype='uint8')

        frame = cv2.imdecode(data, 1)
        cv2.imshow('Remote', frame)
    except ConnectionResetError as e:
        print(e)
        break

client_sock.close()
print('[Client] 프로그램을 종료합니다.')
