import asyncio
import logging

from bleak import BleakClient

from .const import WRITE_UUID, NOTIFY_UUID, BLE_TIMEOUT
from .protocol import build_packet, parse_state

_LOGGER = logging.getLogger(__name__)


class ACInfinityBLE:

    def __init__(self, address):

        self.address = address
        self.client = BleakClient(address)

        self.temperature = None
        self.humidity = None
        self.ports = {}

        self._response_event = asyncio.Event()
        self._command_lock = asyncio.Lock()

    async def connect(self):

        if self.client.is_connected:
            return

        await self.client.connect()

        await self.client.start_notify(
            NOTIFY_UUID,
            self._notification_handler,
        )

    async def disconnect(self):

        if self.client.is_connected:
            await self.client.disconnect()

    def _notification_handler(self, sender, data):

        if len(data) < 5:
            return

        if data[0] != 0xAA or data[1] != 0x55:
            return

        cmd = data[3]

        if cmd == 0x20:

            temp, hum, ports = parse_state(data)

            self.temperature = temp
            self.humidity = hum
            self.ports = ports

            self._response_event.set()

    async def _send_command(self, packet):

        async with self._command_lock:

            await self.client.write_gatt_char(WRITE_UUID, packet)

    async def request_state(self):

        packet = build_packet(0x10, [])

        self._response_event.clear()

        await self._send_command(packet)

        try:
            await asyncio.wait_for(
                self._response_event.wait(),
                BLE_TIMEOUT,
            )
        except asyncio.TimeoutError:
            _LOGGER.warning("AC Infinity BLE response timeout")

        return {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "ports": self.ports,
        }

    async def set_speed(self, port, speed):

        packet = build_packet(0x11, [port, speed])

        await self._send_command(packet)

    async def set_power(self, port, state):

        packet = build_packet(0x12, [port, 1 if state else 0])

        await self._send_command(packet)
