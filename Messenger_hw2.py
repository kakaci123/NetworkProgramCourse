import socket, argparse
from getpass import getpass
import threading

MAX_BYTES = 65535


def server(port):
    MemberList = {'john': {'password': '123456', 'login': None, 'note': []},
                  'mary': {'password': '654321', 'login': None, 'note': []}}
    LoginLog = {}

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 67))

    def friend(command, address):
        def list(self):
            rlt = ''
            for index in sorted(MemberList):
                if MemberList[index]['login'] is not None:
                    loginstatus = 'online'
                else:
                    loginstatus = 'offline'
                rlt = rlt + index + '\t' + loginstatus + '\n'
            return rlt[:len(rlt) - 1]

        def add(name):
            if MemberList.get(name) is not None:
                return '{} is existed!'.format(name)
            MemberList.update({name: {'password': '24613', 'login': None, 'note': []}})

            return '{} is added into the friend list'.format(name)

        def rm(name):
            if MemberList.get(name) is None:
                return '{} is not existed!'.format(name)
            del MemberList[name]
            return '{} removed from the friend list'.format(name)

        friendFunc = {'list': list, 'add': add, 'rm': rm}
        function = friendFunc[command.split('@')[0]]
        try:
            para = command.split('@')[1]
        except:
            para = 'nopara'
        print(para)
        return function(para)

    def login(para, address):
        username = para.split('@')[0]
        password = para.split('@')[1]
        CHECKTEMP = MemberList.get(username)

        if CHECKTEMP is not None and CHECKTEMP['password'] == password and CHECKTEMP['login'] is None:
            CHECKTEMP['login'] = address
            LoginLog.update({address: username})
            if len(CHECKTEMP['note']) != 0:
                print(len(CHECKTEMP['note']))
                rlt = ''
                for index in CHECKTEMP['note']:
                    rlt = rlt + 'Message from ' + index[0] + ':' + index[1].replace(index[0] + '>', '') + '\n'

                del CHECKTEMP['note']
                return rlt
            return '1'
        return '0'

    def logout(username, address):
        CHECKTEMP = MemberList.get(username)
        if CHECKTEMP is not None:
            CHECKTEMP['login'] = None
            del LoginLog[address]
            return 'Thank you for your using, {} !'.format(username)

    def send(command, address):
        userFrom = LoginLog[address]
        toWho = command.split('@')[0]
        message = userFrom + '>' + command.split('@')[1]
        CHECKTEMP = MemberList.get(toWho)
        if CHECKTEMP is not None:
            receiverAddress = CHECKTEMP['login']
            if receiverAddress is None:
                print('take a note')
                CHECKTEMP['note'].append([userFrom, message])
            else:
                sock.sendto(message.encode('ascii'), receiverAddress)
        else:
            return '[System] cannot find the people!'
        return ''

    def sendfile(command, address):
        userFrom = LoginLog[address]
        toWho = command.split('@')[0]
        filepath=command.split('@')[1]
        CHECKTEMP = MemberList.get(toWho)
        if CHECKTEMP is not None:
            receiverAddress = CHECKTEMP['login']
            if receiverAddress is None:
                return '[System]The user is not online'
            else:
                sock.sendto('{} wants to send file to you (Y/N)'.format(userFrom).encode('ascii'), receiverAddress)
                data, address1 = sock.recvfrom(MAX_BYTES)
                CHECKSTAN = data.decode('ascii')
                if CHECKSTAN == 'y_y@y':
                    sock.sendto('0x123456789'.encode('ascii'),receiverAddress)
                    f=open(filepath,'rb')
                    l=f.read(1024)
                    while(l):
                        sock.sendto(l,receiverAddress)
                        l=f.read(1024)
                    f.close()
                    sock.sendto('end of file transmitted'.encode('ascii'), address)
                else:
                    sock.sendto('denied from {}'.format(toWho).encode('ascii'), address)

        else:
            return '[System] cannot find the people!'
        return ''

    MyFunc = {'login': login, 'logout': logout, 'friend': friend, 'send': send, 'sendfile': sendfile}
    print('Server is Listening at {}'.format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        data = data.decode('ascii')
        print(data)
        try:
            para = data.split('_')[1]
        except:
            para = '-1'
        try:
            rlt = MyFunc[data.split('_')[0]](para, address)
            print(rlt)
            rlt = rlt.encode('ascii')
            sock.sendto(rlt, address)
        except:
            rlt = '[System]Please Check the function is usable.'.encode('ascii')
            sock.sendto(rlt, address)


def client(port):
    def sendThreadFunc():
        print('=== Please insert command ===')
        while True:
            UserInput = input().lower()
            Command = UserInput.split(' ')[0]
            Temp = UserInput.replace(Command + ' ', '').split(' ')[0]
            Para = UserInput.replace(Temp + ' ', '').replace(Command + ' ', '')
            Command = Command + '_' + Temp + '@' + Para
            if 'logout' in Command:
                Command = 'logout_' + username
                sock.sendto(Command.encode('ascii'),
                            ('127.0.0.1', 67))
                data, address = sock.recvfrom(MAX_BYTES)
                print(data.decode('ascii'))
                exit()
            sock.sendto(Command.encode('ascii'),
                        ('127.0.0.1', 67))

    def recvThreadFunc():
        while True:
            try:
                otherword,address = sock.recvfrom(MAX_BYTES)
                otherword=otherword.decode('ascii')
                if '0x123456789' ==otherword:
                    print('receive file')
                    f = open('file_recv.txt', 'wb')  # open in binary
                        # recibimos y escribimos en el fichero
                    l = sock.recv(MAX_BYTES)
                    f.write(l)
                    f.close()
                    print('end receive')
                elif otherword:
                    print(otherword)
                else:
                    pass
            except ConnectionAbortedError:
                print('Server closed this connection!')

            except ConnectionResetError:
                print('Server is closed!')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind(('127.0.0.1', port))

    except Exception as e:
        print('[System]The port is use.')
        sock.close()
        exit()

    print('Client is running at {}'.format(sock.getsockname()))
    username = input('login:').strip()
    password = getpass().strip()
    data = 'login_' + username + "@" + password
    sock.sendto(data.encode('ascii'),
                ('127.0.0.1', 67))

    data, address = sock.recvfrom(MAX_BYTES)
    rlt = data.decode('ascii')
    if rlt != '0':
        print('Hello ! ' + username)
        if rlt != '1':
            print(rlt)
        th1 = threading.Thread(target=sendThreadFunc)
        th2 = threading.Thread(target=recvThreadFunc)
        threads = [th1, th2]
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
    else:
        print('[System]Please make sure both your account and password are correct!')


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)
