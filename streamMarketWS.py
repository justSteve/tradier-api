import asyncio
import websockets
import config
import requests
import json
import sys


async def ws_connect():

    response = requests.post('https://api.tradier.com/v1/accounts/events/session',
                             data={},
                             headers={'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN_pjk), 'Accept': 'application/json'})
    json_response = response.json()
    # Directly access 'sessionid' from the nested dictionary
    session_id = json_response.get('stream', {}).get(
        'sessionid', 'Default Value')
    print("my sessionid = " + session_id)

    uri = "wss://ws.tradier.com/v1/markets/events"

    async with websockets.connect(uri, ssl=True, compression=None) as websocket:

        # payload = f'{{"symbols": ["SPX"], "sessionid": "session_id", "linebreak": "true", "filter": "trade", "format": "json"}}'
        payload = f'{{"symbols": ["SPX"], "sessionid": "{session_id}"}}'
        # payload = '{"symbols": ["SPX"], "sessionid": "' + session_id + '"}'
        print(f">>> {payload}")

        await websocket.send(payload)

        async for message in websocket:
            print(f"<<< {message}")

asyncio.run(ws_connect())
