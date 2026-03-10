class ACInfinityDecoder:

    def __init__(self):

        self.state = {
            "temperature": None,
            "humidity": None,
            "fan_speed": 0,
            "ports": [False]*8
        }

    def decode(self, data):

        try:

            if len(data) < 8:
                return self.state

            header = data[0]

            if header == 0xB1:

                temp = data[6]
                hum = data[7]

                self.state["temperature"] = float(temp)
                self.state["humidity"] = float(hum)

            if header == 0xB2:

                speed = data[3]
                self.state["fan_speed"] = speed

            if header == 0xB3:

                mask = data[3]

                for i in range(8):
                    self.state["ports"][i] = bool(mask & (1 << i))

        except Exception:
            pass

        return self.state
