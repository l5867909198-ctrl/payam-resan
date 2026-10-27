
import asyncio
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
    async with websockets.serve(chat, "0.0.0.0", 8765):
        print("Chat server is running!")
        await asyncio.Future()

asyncio.run(main())
