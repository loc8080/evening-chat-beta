import asyncio
import websockets
import history_lib

clients = []

async def handler(websocket):
    clients.append(websocket)

    try:

        for i in history_lib.get_history():
            await websocket.send(i)

        nickname:str = await websocket.recv()

        for client in clients:
            await client.send(f"🔵 {nickname} Присоендинился!")

        while True:
            message:str = await websocket.recv()
            print(f"[{nickname}] {message}")
            history_lib.add_history(f"[{nickname}] {message}")

            for client in clients:
                try:
                    if message.startswith("/clear"):
                        history_lib.clear_history()
                        await client.send("🪄 Чат очищен!")
                    else:
                        await client.send(f"[{nickname}] {message}")
                except:
                    pass  # Не даем упавшему клиенту мешать другим

    except websockets.exceptions.ConnectionClosed as er:
        print(f"Client disconnected: {er}")

    finally:
        if websocket in clients:
            clients.remove(websocket)

        for client in clients:
            await client.send(f"🔴 {nickname} Отсоендинился!")

async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    await server.wait_closed()

asyncio.run(main())
