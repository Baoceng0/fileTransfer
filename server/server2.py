# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import configparser
import socket
import sys
import logging
import tqdm
import os
import datetime

SEPARATE = "<SEPARATE>"
# Configuration
logging.basicConfig(level=logging.DEBUG,
  format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
  datefmt='%a, %d %b %Y %H:%M:%S',
  filename='serverlog.log',
  filemode='w')

parser = configparser.ConfigParser()
parser.read(sys.argv[1])
HOST = parser.get('info','HOST')
PORT = int(parser.get('info','PORT'))

# Create Buffer for file
BufferSize = 4096

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST, PORT))
print("Listening {datetime.datetime.now()} {HOST} {PORT}")
logging.info('Server listening')
print(f"Listening {datetime.datetime.now()} {HOST} {PORT}")
# s.listen(5)
# conn, addr = s.accept()
# Request command
# conn.sendall("Enter your command: ".encode())
while True:
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.bind((HOST, PORT))
    #print(f"Listening {datetime.datetime.now()} {HOST} {PORT}")
    s.listen(5)
    conn, addr = s.accept()
    command = conn.recv(1024).decode('utf-8')
    if(command == 'HELP' or command == 'help'):
        print("Sending helps to client!")
        logging.info('Sending helps to client!')
        conn.send("Helps: \n\t <SEND | send> \n\t\t Sending a file from client to server \n\t <LIST | ls> \n\t\t return a list of files from server\n\t <STOP | stop | quit | exit> \n\t\t end both client & server \n\t <HELP | help>\n\t\t documentation\n\t <DELETE | delete>\n\t\t delete file in server".encode('utf-8'))
    elif(command == "STOP" or command == "stop" or command == "exit" or command == "quit"):
        logging.info('Server exit')
        conn.send("Server is closed".encode('utf-8'))
        break;
    elif(command =="SEND" or command =="send"):
        logging.info('Command SEND')
        recv = conn.recv(BufferSize).decode('utf-8')
        filename,file_size = recv.split(SEPARATE)
        filename = os.path.basename(filename)
        file_size = int(file_size)
        progress = tqdm.tqdm(range(file_size),f"receiving {filename}",unit="B",unit_divisor=1024,unit_scale=True)

        with open(filename,"wb") as f:
            bytes_read = conn.recv(BufferSize)
            while (len(bytes_read)>0):
                f.write(bytes_read)
                progress.update(len(bytes_read))
                bytes_read = conn.recv(BufferSize)
        progress.close()
    elif(command =="DELETE" or command =="delete"):
        logging.info('Command DELETE')
        filename = conn.recv(1024).decode('utf-8')
        pwd = os.getcwd()
        pwd += '\\'
        pwd += filename
        if (os.path.isfile(pwd)):
            os.remove(pwd)
            conn.send("Delete the file!".encode('utf-8'))
        else:
            conn.send("Fail!, as file doesn't exist.".encode('utf-8'))

    elif(command == "LIST" or command == "list" or command == "ls"):
        logging.info('Command LIST')
        arr = os.listdir()
        b = [str(j) for j in arr]
        list = " ".join(b)
        list = str(list)
        #arr = str(arr)
        conn.send(list.encode('utf-8'))
    else:
        logging.info('Invalid command!')
        print("Invalid command!\nAvailable Command: \n\t <SEND | send> \n\t <STOP | stop | quit | exit> \n\t <HELP | help> \n\t <DELETE | delete>")
    conn.close()
    #s.close()

# conn.close()
s.close()

