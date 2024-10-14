import os

def send_list(cli_sock):    #uses utf-8 as will be transmitting strings
    dir_list = os.listdir('.')
    dir = ",".join(dir_list)
    cli_sock.sendall(f"recieved message- listing directory--{dir}".encode('utf-8'))

def recover_file(cli_sock, filename):
    with open(filename, 'wb') as new_f:
        while True:
            data = cli_sock.recv(1024)
            if not data:                #no more data recieved
                break
            new_f.write(data)
    print(f"File {filename} has been recovered")


def send_file(cli_sock, filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                cli_sock.sendall(data)
        print(f"File {filename} has been sent")
    else:
        print(f"File {filename} does not exist")
        cli_sock.sendall(f"File {filename} does not exist".encode('utf-8'))