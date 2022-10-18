async def websocket_application(scope, receive, send):
    while True:
        event = await receive()

        print(event)

        if event['type'] == 'websocket.connect':
            print("conn")
            await send({
                'type': 'websocket.accept'
            })

        if event['type'] == 'websocket.disconnect':
            print("disc")
            break

        if event['type'] == 'websocket.receive':
            print("rec")
            if event['text'] == 'ping':
                print("ping")
                await send({
                    'type': 'websocket.send',
                    'text': 'pong!'
                })