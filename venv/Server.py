import socket
from Client import NTPPacket, DHCPPacket
import struct

serverPort = 67
clientPort = 68

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('', serverPort))
    dest = ('255.255.255.255', clientPort)
    answer = DHCPPacket()

    while 1:
        try:
            print("Wait DHCP discovery.")
            data, address = s.recvfrom(1024)
            print("Receive DHCP discovery.")
            print(answer.unpack(data).to_display())

            #print("Send DHCP offer.")
            data = DHCPPacket(0x350102)
            s.sendto(data.pack(), dest)

            while 1:
                try:
                    print("Wait DHCP request.")
                    data, address = s.recvfrom(1024)
                    print("Receive DHCP request.")

                    print("Send DHCP ack.\n")
                    data = DHCPPacket(0x350105)
                    s.sendto(data.pack(), dest)
                    break
                except:
                    raise

        except:
            raise