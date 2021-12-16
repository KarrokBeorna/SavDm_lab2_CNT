import datetime
import time
import socket
import struct

class DHCPPacket:
    _FORMAT = "!B B B B I H H 18I"

    def __init__(self, type=0x350102):
        self.op = 2                         # 1 byte
        self.htype = 1                      # 1 byte
        self.hlen = 6                       # 1 byte
        self.hops = 0                       # 1 byte
        self.xid = 0x3903F326               # 4 bytes
        self.secs = 0                       # 2 bytes
        self.flags = 0                      # 2 bytes
        self.ciaddr = 0                     # 4 bytes
        self.yiaddr = 0xC0A80164            # 4 bytes   192.168.1.100
        self.siaddr = 0xC0A80101            # 4 bytes   192.168.1.1
        self.giaddr = 0                     # 4 bytes
        self.chaddr1 = 0x0000001D
        self.chaddr2 = 0x6057ED80
        self.chaddr3 = 0
        self.chaddr4 = 0                    # 16 bytes
        self.magiccookie = 0x63825363       # 4 bytes
        self.options1 = type                # 4 bytes | DHCP OFFER (value = 2) | DHCP ACK (value = 5)
        self.options2_1 = 0x0104
        self.options2_2 = 0xFFFFFF00        # 8 bytes | 255.255.255.0 subnet mask
        self.options3_1 = 0x0304
        self.options3_2 = 0xC0A80101        # 8 bytes | 192.168.1.1 router
        self.options4_1 = 0x3304
        self.options4_2 = 0x00015180        # 8 bytes | 86400s(1 day) IP address lease time
        self.options5_1 = 0x3604
        self.options5_2 = 0xC0A80101        # 8 bytes | DHCP server

    def pack(self):
        return struct.pack(DHCPPacket._FORMAT,
                           self.op,
                           self.htype,
                           self.hlen,
                           self.hops,
                           self.xid,
                           self.secs,
                           self.flags,
                           self.ciaddr,
                           self.yiaddr,
                           self.siaddr,
                           self.giaddr,
                           self.chaddr1, self.chaddr2, self.chaddr3, self.chaddr4,
                           self.magiccookie,
                           self.options1,
                           self.options2_1, self.options2_2,
                           self.options3_1, self.options3_2,
                           self.options4_1, self.options4_2,
                           self.options5_1, self.options5_2,)

    def unpack(self, data: bytes):
        unpacked_data = struct.unpack(DHCPPacket._FORMAT, data)

        self.op = unpacked_data[0]
        self.htype = unpacked_data[1]
        self.hlen = unpacked_data[2]
        self.hops = unpacked_data[3]
        self.xid = unpacked_data[4]
        self.secs = unpacked_data[5]
        self.flags = unpacked_data[6]
        self.ciaddr = unpacked_data[7]
        self.yiaddr = unpacked_data[8]
        self.siaddr = unpacked_data[9]
        self.giaddr = unpacked_data[10]
        self.chaddr = (unpacked_data[11] << 96) + (unpacked_data[12] << 64) + (unpacked_data[13] << 32) + unpacked_data[14]
        self.magiccookie = unpacked_data[15]
        self.options1 = unpacked_data[16]
        self.options2 = (unpacked_data[17] << 32) + unpacked_data[18]
        self.options3 = (unpacked_data[19] << 32) + unpacked_data[20]
        self.options4 = (unpacked_data[21] << 32) + unpacked_data[22]
        self.options5 = (unpacked_data[23] << 32) + unpacked_data[24]

        return self

    def to_display(self):
        return "Op: {0.op}\n" \
               "Htype: {0.htype}\n" \
               "Hlen: {0.hlen}\n" \
               "Hops: {0.hops}\n" \
               "Xid: {0.xid:#X}\n" \
               "Secs: {0.secs}\n" \
               "Flags: {0.flags}\n" \
               "Ciaddr: {0.ciaddr:#X}\n" \
               "Yiaddr: {0.yiaddr:#X}\n" \
               "Siaddr: {0.siaddr:#X}\n" \
               "Giaddr: {0.giaddr:#X}\n" \
               "Magic cookie: {0.magiccookie:#X}\n" \
               "Options 1: {0.options1:#X}\n" \
               "Options 2: {0.options2:#X}\n" \
               "Options 3: {0.options3:#X}\n" \
               "Options 4: {0.options4:#X}\n" \
               "Options 5: {0.options5:#X}" \
            .format(self)

class NTPPacket:
    # сетевой порядок байт, размер типов стандартный
    # int(1b) int(1b) int(1b) int(1b) 11*int(4b)
    _FORMAT = "!B B B B 11I"

    def __init__(self, version_number=4, mode=3, transmit=0):
        # Necessary of enter leap second (2 bits)
        self.leap_indicator = 0
        # Version of protocol (3 bits)
        self.version_number = version_number
        # Mode of sender (3 bits)
        self.mode = mode
        # The level of "layering" reading time (1 byte)
        self.stratum = 0
        # Interval between requests (1 byte)
        self.pool = 0
        # Precision (log2) (1 byte)
        self.precision = 0
        # Interval for the clock reach NTP server (4 bytes)
        self.root_delay = 0
        # Scatter the clock NTP-server (4 bytes)
        self.root_dispersion = 0
        # Indicator of clocks (4 bytes)
        self.ref_id = 0
        # Last update time on server (8 bytes)
        self.reference = 0
        # Time of sending packet from local machine (8 bytes)
        self.originate = 0
        # Time of receipt on server (8 bytes)
        self.receive = 0
        # Time of sending answer from server (8 bytes)
        self.transmit = transmit

    def pack(self):
        return struct.pack(NTPPacket._FORMAT,
                           (self.leap_indicator << 6) +
                           (self.version_number << 3) + self.mode,
                           self.stratum,
                           self.pool,
                           self.precision,
                           int(self.root_delay) + get_fraction(self.root_delay, 16),
                           int(self.root_dispersion) +
                           get_fraction(self.root_dispersion, 16),
                           self.ref_id,
                           int(self.reference),
                           get_fraction(self.reference, 32),
                           int(self.originate),
                           get_fraction(self.originate, 32),
                           int(self.receive),
                           get_fraction(self.receive, 32),
                           int(self.transmit),
                           get_fraction(self.transmit, 32))

    def unpack(self, data: bytes):
        unpacked_data = struct.unpack(NTPPacket._FORMAT, data)

        self.leap_indicator = unpacked_data[0] >> 6  # 2 bits
        self.version_number = unpacked_data[0] >> 3 & 0b111  # 3 bits
        self.mode = unpacked_data[0] & 0b111  # 3 bits

        self.stratum = unpacked_data[1]  # 1 byte
        self.pool = unpacked_data[2]  # 1 byte
        self.precision = unpacked_data[3]  # 1 byte

        # 2 bytes | 2 bytes
        self.root_delay = (unpacked_data[4] >> 16) + \
                          (unpacked_data[4] & 0xFFFF) / 2 ** 16
        # 2 bytes | 2 bytes
        self.root_dispersion = (unpacked_data[5] >> 16) + \
                               (unpacked_data[5] & 0xFFFF) / 2 ** 16

        # 4 bytes
        self.ref_id = str((unpacked_data[6] >> 24) & 0xFF) + " " + \
                      str((unpacked_data[6] >> 16) & 0xFF) + " " + \
                      str((unpacked_data[6] >> 8) & 0xFF) + " " + \
                      str(unpacked_data[6] & 0xFF)

        self.reference = unpacked_data[7] + unpacked_data[8] / 2 ** 32  # 8 bytes
        self.originate = unpacked_data[9] + unpacked_data[10] / 2 ** 32  # 8 bytes
        self.receive = unpacked_data[11] + unpacked_data[12] / 2 ** 32  # 8 bytes
        self.transmit = unpacked_data[13] + unpacked_data[14] / 2 ** 32  # 8 bytes

        return self

    def to_display(self):
        return "Leap indicator: {0.leap_indicator}\n" \
               "Version number: {0.version_number}\n" \
               "Mode: {0.mode}\n" \
               "Stratum: {0.stratum}\n" \
               "Pool: {0.pool}\n" \
               "Precision: {0.precision}\n" \
               "Root delay: {0.root_delay}\n" \
               "Root dispersion: {0.root_dispersion}\n" \
               "Ref id: {0.ref_id}\n" \
               "Reference: {0.reference}\n" \
               "Originate: {0.originate}\n" \
               "Receive: {0.receive}\n" \
               "Transmit: {0.transmit}" \
            .format(self)

def get_fraction(number, precision):
    return int((number - int(number)) * 2 ** precision)

if __name__ == '__main__':
    # Time difference between 1970 and 1900, seconds
    FORMAT_DIFF = (datetime.date(1970, 1, 1) - datetime.date(1900, 1, 1)).days * 24 * 3600
    # Waiting time for recv (seconds)
    WAITING_TIME = 5
    dest = ("pool.ntp.org", 123) #('<broadcast>', 67)  #

    answer = NTPPacket()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # s.bind(('0.0.0.0', 68))
        s.settimeout(WAITING_TIME)
        packet = NTPPacket(version_number=4, mode=3, transmit=time.time() + FORMAT_DIFF)
        s.sendto(packet.pack(), dest)
        data = s.recv(48)

        arrive_time = time.time() + FORMAT_DIFF
        print(answer.unpack(data).to_display())
        print('Arrive Time: ' + str(arrive_time))
