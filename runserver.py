import socket, subprocess
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
host = socket.gethostbyname(socket.gethostname())
port = '8000'
print('running server on {}:{}'.format(host, port))
subprocess.run('python3 {}/manage.py runserver {}:{}'.format(dir_path, host, port).split())
