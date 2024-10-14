import socket
import sys
import os
import commonFunc as com_f


print("[STARTING] Server is starting")
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
portNumber = int(sys.argv[1])
server_sock.bind(('0.0.0.0', portNumber))

server_sock.listen(10)

#print server message and IP address  and port number
print("{} server running".format(portNumber))
running = True
while running:
    try:
        cli_sock,  cli_address = server_sock.accept()
        print(f"[NEW CONNECTION] {cli_address} connected")
        request = cli_sock.recv(1024).decode('utf-8')
        request_msg = request.split(" ")
        command = request_msg[0]        

        #if server is closed
        if command == "EXIT":
            cli_sock.sendall("server has shutdown.".encode('utf-8'))
            running = False

        #if command is put
        elif command == "put":
            if len(request_msg) < 2:
                print("Filename missing.")
                cli_sock.sendall("Filename missing.".encode('utf-8'))
            else:
                print("Receiving file")
                filename = request_msg[1]
                com_f.recover_file(cli_sock, filename)

        #if command is get
        elif command == "get":
            if len(request_msg) < 2:
                cli_sock.sendall("Filename missing.".encode('utf-8'))
            else:
                filename = request_msg[1]
                com_f.send_file(cli_sock, filename)

        #if command is list
        elif command == "list":
            print("List command received")
            com_f.send_list(cli_sock)

        else:
            print("Invalid command")
            cli_sock.sendall("Invalid command".encode('utf-8'))
        cli_sock.close()
    except Exception as e:
        print(f"Error: {e}")
        cli_sock.close()
        running = False

server_sock.close()