import socket

server_ip = '127.0.0.1'
server_port = 50000

# 통신용 소켓을 생성한다.
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결한다.
client_sock.connect((server_ip, server_port))

# 서버에 연결했음을 알린다.
print('[TCP 클라이언트] 서버 연결: {}:{}'.format(server_ip, server_port))

while True:
    # 송신할 데이터를 입력한다.
    buffer = input('Send: ')
    if not buffer:
        break

    # 데이터를 송신한다.
    retval = client_sock.send(buffer.encode('utf-8'))

    # 데이터를 수신한다.
    buffer = client_sock.recv(1024)

    # 수신한 데이터를 출력한다.
    print('Recv: {}'.format(buffer.decode('utf-8'), end='\n\n'))

# 통신용 소켓을 닫는다.
client_sock.close()

print('프로그램을 종료합니다.')
exit(0)
