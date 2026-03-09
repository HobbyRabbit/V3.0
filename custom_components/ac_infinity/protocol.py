def checksum(data):

    return sum(data) & 0xFF


def build_packet(cmd, payload):

    length = len(payload) + 1

    frame = bytearray([0xAA, 0x55, length, cmd])

    frame.extend(payload)

    frame.append(checksum(frame[2:]))

    return frame


def parse_state(packet):

    temp_raw = (packet[4] << 8) | packet[5]

    temperature = temp_raw / 10

    humidity = packet[6]

    ports = {}

    for i in range(8):

        ports[i + 1] = packet[7 + i]

    return temperature, humidity, ports
