import asyncio
import logging

from bleak import BleakClient

from .const import WRITE_UUID, NOTIFY_UUID
from .protocol import build_packet, parse_state

_LOGGER = logging.getLogger(__name__)


class ACInfinityBLE:

    def __init__(self, address):

        self.address = address

        self.client = BleakClient(address)

        self.temperature = None
        self.humidity = None
        self.ports = {}

        self._event = asyncio.Event()

    async def connect(self):

        if self.client.is_connected:
            return

        await self.client.connect()

        await self.client.start_notify(
            NOTIFY_UUID,
            self._notification_handler
        )

    async def disconnect(self):

        if self.client.is_connected:
            await self.client.disconnect()

    def _notification_handler(self, sender, data):

        if data[0] != 0xAA:
            return

        cmd = data[3]

        if cmd == 0x20:

            temp, hum, ports = parse_state(data)

            self.temperature = temp
            self.humidity = hum
            self.ports = ports

            self._event.set()

    async def request_state(self):

        packet = build_packet(0x10, [])

        self._event.clear()

        await self.client.write_gatt_char(WRITE_UUID, packet)

        try:
            await asyncio.wait_for(self._event.wait(), 5)
        except asyncio.TimeoutError:
            _LOGGER.warning("AC Infinity controller timeout")

        return {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "ports": self.ports
        }

    async def set_speed(self, port, speed):

        packet = build_packet(0x11, [port, speed])

        await self.client.write_gatt_char(WRITE_UUID, packet)

    async def set_power(self, port, state):

        packet = build_packet(0x12, [port, 1 if state else 0])

        await self.client.write_gatt_char(WRITE_UUID, packet)
