
import asyncio
import os
import websockets

clients = set()

async def chat(websocket):
    clients.add(websocket)
    print("A user connected")
    try:
        async for message in websocket:
            print("Message:", message)
            for client in list(clients):
                if client != websocket:
                    try:
                        await client.send(message)
                    except websockets.exceptions.ConnectionClosed:
                        pass
    finally:
        clients.discard(websocket)

async def main():
    port = int(os.environ.get("PORT", 8765))
    async with websockets.serve(chat, "0.0.0.0", port):
        print(f"Chat server is running on port {port}!")
        await asyncio.Future()

asyncio.run(main())
