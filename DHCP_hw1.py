import socket, argparse
import struct
from uuid import getnode as get_mac
from random import randint
import ipaddress

MAX_BYTES = 65535


def getMacInBytes():
    mac = str(hex(get_mac()))
    mac = mac[2:]
    while len(mac) < 12:
        mac = '0' + mac
    macb = b''
    for i in range(0, 12, 2):
        m = int(mac[i:i + 2], 16)
        macb += struct.pack('!B', m)
    return macb


class DHCPDiscover:
    def __init__(self):
        self.transactionID = b''
        for i in range(4):
            t = randint(0, 255)
            self.transactionID += struct.pack('!B', t)

    def buildPacket(self):
        # https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol#DHCP_discovery
        macb = getMacInBytes()

        packet = b''
        packet += b'\x01\x01\x06\x00'  # OP ,HTYPE ,HLEN ,HOPS
        packet += self.transactionID
        packet += b'\x00\x00'  # SECS
        packet += b'\x80\x00'  # FLAGS
        packet += b'\x00\x00\x00\x00'  # CIADDR
        packet += b'\x00\x00\x00\x00'  # YIADDR
        packet += b'\x00\x00\x00\x00'  # SIADDR
        packet += b'\x00\x00\x00\x00'  # GIADDR
        packet += macb
        packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        packet += b'\x00' * 192
        packet += b'\x63\x82\x53\x63'  # MAGIC COOKIE
        packet += b'\x35\x01\x01'  # Option: (t=53,l=1) DHCP Message Type = DHCP Discover
        packet += b'\x3d\x06\x00\x26\x9e\x04\x1e\x9b'  # Option: (t=61,l=6) Client identifier
        packet += b'\x3d\x06' + macb
        packet += b'\x37\x03\x03\x01\x06'  # Option: (t=55,l=3) Parameter Request List
        packet += b'\xff'

        return packet


class DHCPOffer:
    def __init__(self, data):
        self.data = data
        self.transactionID = data[4:8]

    def buildPacket(self, data, address):
        # https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol#DHCP_discovery

        macb = getMacInBytes()

        packet = b''
        packet += b'\x01\x01\x06\x00'  # OP ,HTYPE ,HLEN ,HOPS
        packet += self.transactionID
        packet += b'\x00\x00'  # SECS
        packet += b'\x80\x00'  # FLAGS
        packet += b'\x00\x00\x00\x00'  # CIADDR
        packet += ipaddress.v4_int_to_packed(
            int(ipaddress.IPv4Address(address)))  # YIADDR
        packet += ipaddress.v4_int_to_packed(
            int(ipaddress.IPv4Address(socket.inet_aton(socket.gethostbyname(socket.gethostname())))))  # SIADDR
        packet += b'\x00\x00\x00\x00'  # GIADDR
        #   acket += b'\x44\x8a\x5b\xec\xbf\x92'
        packet += macb
        packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        packet += b'\x00' * 192
        packet += b'\x63\x82\x53\x63'  # MAGIC COOKIE
        packet += b'\x35\x01\x02'  # Option: (t=53,l=2) DHCP Message Type = DHCP Offer
        packet += b'\x3d\x06\x00\x26\x9e\x04\x1e\x9b'  # Option: (t=61,l=6) Client identifier
        packet += b'\x3d\x06' + macb
        packet += b'\x37\x03\x03\x01\x06'  # Option: (t=55,l=3) Parameter Request List
        packet += b'\xff'  # End Option\

        return packet


class DHCPRequest:
    def __init__(self, data):
        self.data = data
        self.transactionID = data[4:8]

    def buildPacket(self, data, address):
        # https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol#DHCP_discovery
        macb = getMacInBytes()

        packet = b''
        packet += b'\x01\x01\x06\x00'  # OP ,HTYPE ,HLEN ,HOPS
        packet += self.transactionID
        packet += b'\x00\x00'  # SECS
        packet += b'\x80\x00'  # FLAGS
        packet += b'\x00\x00\x00\x00'  # CIADDR
        packet += ipaddress.v4_int_to_packed(
            int(ipaddress.IPv4Address(address)))  # YIADDR
        packet += ipaddress.v4_int_to_packed(
            int(ipaddress.IPv4Address(socket.inet_aton(socket.gethostbyname(socket.gethostname())))))  # SIADDR
        packet += b'\x00\x00\x00\x00'  # GIADDR
        #   acket += b'\x44\x8a\x5b\xec\xbf\x92'
        packet += macb
        packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        packet += b'\x00' * 192
        packet += b'\x63\x82\x53\x63'  # MAGIC COOKIE
        packet += b'\x35\x01\x03'  # Option: (t=53,l=2) DHCP Message Type = DHCP Offer
        packet += b'\x3d\x06\x00\x26\x9e\x04\x1e\x9b'  # Option: (t=61,l=6) Client identifier
        packet += b'\x3d\x06' + macb
        packet += b'\x37\x03\x03\x01\x06'  # Option: (t=55,l=3) Parameter Request List
        packet += b'\xff'  # End Option\

        return packet


class DHCPAck:
    def __init__(self, data):
        self.data = data
        self.transactionID = data[4:8]

    def buildPacket(self, data, address):
        # https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol#DHCP_discovery
        macb = getMacInBytes()

        packet = b''
        packet += b'\x01\x01\x06\x00'  # OP ,HTYPE ,HLEN ,HOPS
        packet += self.transactionID
        packet += b'\x00\x00'  # SECS
        packet += b'\x80\x00'  # FLAGS
        packet += b'\x00\x00\x00\x00'  # CIADDR
        packet += ipaddress.v4_int_to_packed(
            int(ipaddress.IPv4Address(address)))  # YIADDR
        packet += ipaddress.v4_int_to_packed(
            int(ipaddress.IPv4Address(socket.inet_aton(socket.gethostbyname(socket.gethostname())))))  # SIADDR
        packet += b'\x00\x00\x00\x00'  # GIADDR
        #   acket += b'\x44\x8a\x5b\xec\xbf\x92'
        packet += macb
        packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        packet += b'\x00' * 192
        packet += b'\x63\x82\x53\x63'  # MAGIC COOKIE
        packet += b'\x35\x01\x05'  # Option: (t=53,l=5) DHCP Message Type = DHCP Ack
        packet += b'\x3d\x06\x00\x26\x9e\x04\x1e\x9b'  # Option: (t=61,l=6) Client identifier
        packet += b'\x3d\x06' + macb
        packet += b'\x37\x03\x03\x01\x06'  # Option: (t=55,l=3) Parameter Request List
        packet += b'\xff'  # End Option\

        return packet


def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 67))

    print('Listening at {}'.format(sock.getsockname()))
    while True:

        data, address = sock.recvfrom(MAX_BYTES)

        if data[242] == 1:
            print('GET DISCOVERY')
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(DHCPOffer(data).buildPacket(data, address[0]), ('<broadcast>', address[1]))

        if data[242] == 3:
            print('GET REQUEST')
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(DHCPAck(data).buildPacket(data, address[0]), ('<broadcast>', address[1]))


            # text = data.decode('ascii')
            # print('the client at says {!r}'.format(data))
            # data = text.encode('ascii')
            # sock.sendto(data, address)


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    try:
        sock.bind(('', 68))
    except Exception as e:
        print('[System]Port 68 is use.')
        sock.close()
        exit()
    # socket.gethostbyname(sock.getsockname())


    sock.sendto(DHCPDiscover().buildPacket(), ('<broadcast>', 67))

    print('DHCP Discover sent waiting for reply...\n')

    # receiving DHCPOffer packet
    sock.settimeout(3)
    try:
        data, address = sock.recvfrom(MAX_BYTES)
        if data[242] == 2:
            print('GET OFFER')
            sock.sendto(DHCPRequest(data).buildPacket(data, address[0]), ('<broadcast>', 67))

        data, address = sock.recvfrom(MAX_BYTES)
        if data[242] == 5:
            print('GET ACK')
            print('Finish all the transmit')


    except socket.timeout as e:
        print('[System] server is occur error')


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    args = parser.parse_args()
    function = choices[args.role]
    function()
