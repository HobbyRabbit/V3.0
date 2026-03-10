def status_request():
    return bytes([0xA1, 0x01, 0x00])


def set_port(port, state):

    return bytes([
        0xA2,
        port,
        1 if state else 0
    ])


def set_speed(speed):

    return bytes([
        0xA3,
        speed
    ])
