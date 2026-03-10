import csv
import time
from .const import CSV_LOG


class PacketLogger:

    def log(self, direction, data):

        with open(CSV_LOG, "a", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                time.time(),
                direction,
                data.hex()
            ])
