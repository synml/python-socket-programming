import socket

server_ip = '127.0.0.1'
server_port = 50000

# 클라이언트 소켓을 생성한다.
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결한다.
client_sock.connect((server_ip, server_port))

# 서버에 연결했음을 알린다.
print(f'[TCP 클라이언트] 서버 연결: {server_ip}:{server_port}')

while True:
    # 송신할 데이터를 입력한다. 그냥 엔터를 누르면 연결 끊기
    buffer = input('Send: ')
    if buffer == '':
        print('서버와 연결 끊기')
        break

    # 데이터를 송신한다.
    buffer = buffer.encode('utf-8')
    retval = client_sock.send(buffer)

    # 데이터를 수신한다.
    buffer = client_sock.recv(1024)
    buffer = buffer.decode('utf-8')

    # 수신한 데이터를 출력한다.
    print(f'Recv: {buffer}')

# 클라이언트 소켓을 닫는다.
client_sock.close()
