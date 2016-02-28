import time
import usocket
import ustruct

from ws2812 import WS2812

# UDP_IP = "192.168.1.254"
UDP_IP = "0.0.0.0"
UDP_PORT = 6454

# led stuff
CHAIN_LEN = 32
chain = WS2812(CHAIN_LEN)
initrgbdata = [(255, 102, 0), (127, 21, 0), (63, 10, 0), (31, 5, 0),
        (15, 2, 0), (7, 1, 0), (0, 0, 0), (0, 0, 0),
        (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
        (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
        (0, 0, 0), (0, 0, 0), (0, 255, 0), (0, 0, 0),
        (0, 0, 0), (0, 0, 0), (0, 0, 255), (0, 0, 0),
        (0, 0, 0), (0, 0, 0), (0, 255, 255), (0, 0, 0),
        (0, 0, 0), (0, 0, 0), (0, 0, 255), (0, 0, 0)
]
chain.show(initrgbdata)

def connectSocket():
    # connect to artnet port
    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # addr = socket.getaddrinfo(UDP_IP, UDP_PORT, socket.AF_INET, socket.SOCK_DGRAM)[0][4]
    # print(addr)
    sock.bind((UDP_IP, UDP_PORT))
    # sock.settimeout(1)
    sock.setblocking(0)
    return sock

sock = connectSocket()

ARTNET_header = "Art-Net".encode()

def main():
    global initrgbdata
    global ARTNET_header
    global sock

    while True:
        # initrgbdata = initrgbdata[1:] + initrgbdata[0:1]
        # print(initrgbdata)
        time.sleep_ms(25)
        chain.show(initrgbdata)

        # print("waiting to receive message")
        # sn = sock.getsockname()
        try:
            data = sock.recv(530)
            # print("received data: ", len(data))
        except:
            # print("no data")
            continue

        # print "received bytes: ", len(data)

        if data[0:7] != ARTNET_header:
            # print("no artnet packet")
            continue
        # else:
        #     print("found artnet packet")

        opcode = ustruct.unpack('H', data[8:10])[0]
        # print(hex(opcode))

        if opcode == 0x5000:
            data_length = ustruct.unpack('>H', data[16:18])[0]
            rgbdata = []
            ndx = 0
            while ndx <= data_length and ndx < CHAIN_LEN:
                rgb = [0, 0, 0]
                i = 0
                while ndx+i < data_length and i < 3:
                    rgb[i] = int(data[18+ndx+i])
                    # print(str(data[18+ndx+i]))
                    i += 1
                rgbdata.append(tuple(rgb))
                ndx += 3
            # chain.show(rgbdata[0:CHAIN_LEN-1])
            # print(rgbdata[0])
            initrgbdata = rgbdata[0:CHAIN_LEN]
            # chain.show(rgbdata)

main()
