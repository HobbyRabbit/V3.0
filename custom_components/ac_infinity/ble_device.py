import asyncio
import logging

from bleak import BleakClient
from bleak_retry_connector import establish_connection

from .const import SERVICE_UUID, WRITE_UUID, NOTIFY_UUID

_LOGGER = logging.getLogger(__name__)


class ACInfinityBLE:

    def __init__(self, address):

        self.address = address
        self.client: BleakClient | None = None
        self.connected = False

        self._notify_event = asyncio.Event()
        self._buffer = None

    async def connect(self):

        _LOGGER.debug("Connecting to %s", self.address)

        self.client = await establish_connection(
            BleakClient,
            self.address,
            "ac_infinity",
            timeout=20
        )

        await self.client.start_notify(
            NOTIFY_UUID,
            self._notification_handler
        )

        self.connected = True

    async def disconnect(self):

        if self.client:
            await self.client.disconnect()

        self.connected = False

    def _notification_handler(self, sender, data):

        _LOGGER.debug("BLE Notify: %s", data.hex())

        self._buffer = data
        self._notify_event.set()

    async def send(self, payload: bytes):

        await self.client.write_gatt_char(
            WRITE_UUID,
            payload,
            response=False
        )

    async def request(self, payload: bytes):

        self._notify_event.clear()

        await self.send(payload)

        try:
            await asyncio.wait_for(self._notify_event.wait(), timeout=5)
        except asyncio.TimeoutError:
            _LOGGER.warning("BLE timeout")
            return None

        return self._buffer

    async def get_status(self):

        cmd = bytes([
            0xAA, 0x55,
            0x01,
            0x00
        ])

        data = await self.request(cmd)

        if not data:
            return {}

        return self.parse_status(data)

    def parse_status(self, data):

        try:

            fan_speed = data[5]
            temperature = data[6]
            humidity = data[7]

            return {
                "speed": fan_speed,
                "temperature": temperature,
                "humidity": humidity
            }

        except Exception as e:
            _LOGGER.error("Parse error %s", e)
            return {}
