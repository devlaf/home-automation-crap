#!/usr/bin/env python

import asyncio
import websockets

async def hello(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send("spin")

asyncio.get_event_loop().run_until_complete(
    hello('ws://narwhal.arctic:8765'))
