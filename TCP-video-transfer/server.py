import queue
import socket
import threading
import cv2
import numpy


def save_frames(buffer: queue.Queue):
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while cv2.waitKey(16) != 27:
        ret, frame = capture.read()

        if not ret:
            print('Error: capture.read()')
            return

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
        ret, img_encode = cv2.imencode('.jpg', frame, encode_param)

        if not ret:
            print('Error: cv2.imencode()')
            return

        buffer.put(numpy.array(img_encode).tostring())
        if buffer.qsize() == 63:
            buffer.get()
        cv2.imshow('Local', frame)


def send_frames(client_sock: socket.socket, addr: tuple, buffer: queue.Queue):
    print('\n[Server] 클라이언트 접속: {}:{}'.format(addr[0], addr[1]))

    while True:
        try:
            data = client_sock.recv(1, socket.MSG_WAITALL)

            if not data:
                print('[Server] 클라이언트 종료: {}:{}'.format(addr[0], addr[1]))
                break

            data = buffer.get()
            client_sock.send(str(len(data)).ljust(16).encode())
            client_sock.send(data)

        except ConnectionResetError:
            print('[Server] 클라이언트 종료: {}:{}'.format(addr[0], addr[1]))
            break
    client_sock.close()


server_port = 50000
buffer = queue.Queue()

# 서버 대기용 소켓을 생성한다.
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Local IP 주소와 Local Port 번호를 설정한다.
server_sock.bind(('', server_port))

# 서버 대기용 소켓을 LISTENING 상태로 변경한다.
server_sock.listen()

thread1 = threading.Thread(target=save_frames, args=(buffer,))
thread1.start()

while True:
    # 클라이언트의 접속을 기다린다.
    client_sock, addr = server_sock.accept()

    thread2 = threading.Thread(target=send_frames, args=(client_sock, addr, buffer))
    thread2.start()

server_sock.close()
