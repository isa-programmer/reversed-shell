#!/usr/bin/python3
import sys
import socket

with open('banner.txt', 'r', encoding='utf-8') as f:
    banner = f.read().replace('\\x1b','\x1b')


class Server:
    def __init__(self,ip: str, port: int,byte_size=1024) -> None:
        """
            Settings for server.py

            args:
                ip:
                    Your IP adress
                port:
                    Your port adress
                byte_size:
                    Maximum amount of bytes that sockets will take (default is 1024)
        
        """
        self.byte_size = byte_size
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip,port))
        self.server.listen(1)

    def AcceptClient(self) -> None:
        """
            Function to accept client. Retrieves client socket and client_info
        """
        self.client, self.client_info = self.server.accept()

    def SendCommand(self,command: str) -> str:
        """
            Sends the command to be executed to the client side
        """
        self.client.send(command.encode())
        return self.client.recv(self.byte_size).decode()

    def GetInput(self,input_value: str) -> str:
        """
            Receives data from the user's keyboard. If it is empty, it tries to receive data again.
        """
        command = input(input_value)
        if not command:
            return self.GetInput(input_value)
        return command   
    
    def Main(self) -> None:
        """
        This is where the program will start.
        
        1. Prints the banner to the screen
        2. Accepts the client
        3. In the while loop commands are constantly requested from the user and sent to the client side.
        
        4. If exit is written, the program exits and all socket connections will close
        """
        print(banner)
        self.AcceptClient()
        while True:
            command = self.GetInput(f"{self.client_info[0]}:~$")
            if command.lower() == "exit":
                print("Exiting...")
                self.SendCommand("exit")
                break
            output = self.SendCommand(command)
            print(f"\x1b[1m{output}\x1b[0m")
        self.client.close()
        self.server.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: ./{sys.argv[0]} <ip> <port> <byte-size (default is 1024)>")
        sys.exit()
    ip = sys.argv[1]
    port = int(sys.argv[2])
    byte_size = int(sys.argv[3]) if len(sys.argv) == 4 else 1024
    server = Server(ip,port,byte_size=byte_size)
    server.Main()
