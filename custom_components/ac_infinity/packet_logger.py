import csv
import os
import time
from .const import CSV_LOG


class PacketLogger:

    def __init__(self):

        if not os.path.exists(CSV_LOG):

            with open(CSV_LOG, "w", newline="") as f:

                writer = csv.writer(f)

                writer.writerow([
                    "timestamp",
                    "direction",
                    "packet"
                ])

    def log(self, direction, data):

        with open(CSV_LOG, "a", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                time.time(),
                direction,
                data.hex()
            ])
