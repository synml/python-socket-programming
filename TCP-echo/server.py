import socket

server_port = 50000

# 서버 대기용 소켓을 생성한다.
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Local IP 주소와 Local Port 번호를 설정한다.
server_sock.bind(('', server_port))

# 서버 대기용 소켓을 LISTENING 상태로 변경한다.
server_sock.listen()

while True:
    # 클라이언트의 접속을 기다린다.
    client_sock, addr = server_sock.accept()

    # 클라이언트가 접속하면 정보를 출력한다.
    print(f'\n[TCP 서버] 클라이언트 접속: {addr[0]}:{addr[1]}')

    while True:
        # 데이터를 수신한다.
        try:
            buffer = client_sock.recv(1024)
            buffer = buffer.decode('utf-8')
        except ConnectionResetError as e:
            print(e)
            break

        # 빈 문자열을 수신하면 서버를 종료한다.
        if buffer == '':
            break

        # 수신한 데이터를 출력한다.
        print(f'[TCP/{addr[0]}:{addr[1]}] {buffer}')

        # 수신한 데이터를 그대로 송신한다.
        buffer = buffer.encode('utf-8')
        retval = client_sock.send(buffer)

    # 통신용 소켓을 닫는다.
    client_sock.close()

    # 클라이언트의 종료를 알린다.
    print('[TCP 서버] 클라이언트 종료: {}:{}'.format(addr[0], addr[1]))

# 서버 대기용 소켓을 닫는다.
server_sock.close()
