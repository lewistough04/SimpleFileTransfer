import socket
import sys
import commonFunc as com_f

cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    portNumber = int(sys.argv[2])
    cli_sock.connect((sys.argv[1],portNumber))
except socket.gaierror:
    print(f"invalid address address {sys.argv[1]}")
    sys.exit(1)
except ValueError:
    print("Port number must be an integer.")
    sys.exit(1)
except Exception as e:
    print(f"Connection error: {e}")
    sys.exit(1)

real_com = True
message = ''
if sys.argv[3]=='put':
    filename = sys.argv[4]
    message=f'put {filename}'
elif sys.argv[3]=='get':
    filename = sys.argv[4]
    message = f'get {filename}'
elif sys.argv[3]=='list':
    message = 'list'

elif sys.argv[3]=='EXIT':
    message = 'EXIT'
else:
    print('invalid command')
    real_com = False
    
if real_com:
    cli_sock.sendall(message.encode('utf-8'))
    if message.startswith('get'):
        com_f.recover_file(cli_sock, filename)
    elif message.startswith('put'):
        com_f.send_file(cli_sock, filename)
    elif message.startswith('list'):
        response = cli_sock.recv(1024).decode('utf-8')
        print(response)
cli_sock.close()