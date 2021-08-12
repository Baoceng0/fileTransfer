#!/usr/bin/env python3

import socket
import sys
import json
import tqdm
import os
import configparser
import logging


# Create a separator
SEPARATE = "<SEPARATE>"

# Configuration
parser = configparser.ConfigParser()
parser.read(sys.argv[1])
HOST = parser.get('info','HOST')
PORT = int(parser.get('info','PORT'))

logging.basicConfig(level=logging.DEBUG,
  format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
  datefmt='%a, %d %b %Y %H:%M:%S',
  filename='clientlog.log',
  filemode='w')
  
# Create Buffer for file
BufferSize = 4096

# Socket created
#s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#print('Connecting with Server')
#s.connect((HOST, PORT))
#print(f'Connected!{HOST}{PORT}')

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('\nConnecting with Server')
    logging.info('Connecting with Server')
    s.connect((HOST, PORT))
    print(f'Connecting!{HOST}{PORT}\n')
    logging.info('Connecting!')
    # print(s.recv(1024).decode())
    command = input("Enter your command: ")
    #s.sendall(command.encode('utf-8'))
    if(command == 'HELP' or command == 'help'):
        s.sendall(command.encode('utf-8'))
        print(s.recv(1024).decode('utf-8'))
        logging.info('Command HELP')
    elif(command == "LIST" or command == "ls"):
        logging.info('Command LIST')
        s.sendall(command.encode('utf-8'))
        arr = s.recv(4096).decode('utf-8')
        #list1 = arr.split(" ")
        print(arr)
    elif(command == "STOP" or command == "stop" or command == "exit" or command == "quit"):
        logging.info('Command QUIT')
        s.sendall(command.encode('utf-8'))
        print(s.recv(1024).decode('utf-8'))
        break
    elif(command == "SEND" or command == "send"):
        logging.info('Command SEND')
        try:
            filename = input("Please type in the file name: ");
            file_size = os.path.getsize(filename)
            print("FILE SIZE")
            print(file_size)
            s.sendall(command.encode('utf-8'))
            # send file name then
            s.send(f"{filename}{SEPARATE}{file_size}".encode('utf-8'))
            # tracking
            progress = tqdm.tqdm(range(file_size),f"Sending {filename}",unit="B",unit_divisor=1024)
            with open(filename,"rb") as file:
                bytes_read = file.read(BufferSize);
                while (len(bytes_read)>0):    
                    s.sendall(bytes_read)
                    progress.update(len(bytes_read))
                    #time.sleep(1)
                    bytes_read = file.read(BufferSize);
            progress.close()
        except Exception:
            print("This file is not exist!")
        #print(s.recv(1024).decode('utf-8'))
    elif (command == "DELETE" or command == "delete"):
        logging.info('Command DELETE')
        s.sendall(command.encode('utf-8'))
        filename = input("Please type in the file name: ");
        s.sendall(filename.encode('utf-8'))
        print(s.recv(1024).decode('utf-8'))
    else:
        logging.info('Invalid command')
        s.sendall(command.encode('utf-8'))
        print("Invalid command! Available Command: \n\t <SEND | send> \n\t <STOP | stop | quit | exit> \n\t <HELP | help> \n\t <DELETE | delete> \n\t <LIST | ls>")
    s.close()

#s.close()