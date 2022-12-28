import asyncio
import websockets

ws_url = "ws://domain_of_your_server:8000/ws/"

async def command_receiver():
    async with websockets.connect(ws_url) as websocket:
        while True:
            print("wait")

            message = await websocket.recv()
            await websocket.send("Received the command '{message}'")
            if message == "start":
                # run the start command
                ...
            elif message == "stop":
                # run the stop command
                ...
            else:
                print("else")
                await websocket.send("Unknown command")




loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

loop.run_until_complete(command_receiver())
loop.run_forever()