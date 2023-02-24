import os
import socket
import threading
import inquirer


HOST = "127.0.0.1"
RECV_PORT = 8000
SEND_PORT = 8001

DATA_SIZE = 1024


class Peer:
    def __init__(self) -> None:
        self.__recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__recv_socket.bind((HOST, RECV_PORT))

        self.__send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__send_socket.bind((HOST, SEND_PORT))

        self.__is_running = False
        self.__peers = set()
        self.__files_uploaded = dict[str, str]

    def __exit(self) -> None:
        self.__is_running = False
        self.__send_socket.connect((HOST, RECV_PORT))
        self.__send_socket.sendall(b"")

    def __bounce_loop(self) -> None:
        while self.__is_running:
            self.__recv_socket.listen()
            conn, addr = self.__recv_socket.accept()
            if addr[0] != HOST:
                with conn:
                    print(f"Connected to {addr}")
                    data = conn.recv(DATA_SIZE)
                    print(data)
                    conn.sendall(data)

    def __input_loop(self) -> None:
        while self.__is_running:
            os.system("clear")
            action = inquirer.prompt([inquirer.List(
                "action",
                message="action",
                choices=["exit", "upload a file", "download a file"],
                carousel=True,
            )])["action"]

            if action == "exit":
                self.__exit()

    def run(self) -> None:
        self.__is_running = True

        threading.Thread(target=self.__bounce_loop).start()
        threading.Thread(target=self.__input_loop).start()
