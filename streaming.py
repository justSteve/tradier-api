import config, requests, json, sys
import asyncio
import websockets


url = "{}/markets/events/session".format(config.API_BASE_WEBSOCKET_URL)

headers = {
    'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN), 
    'Accept': 'application/json'
}


response = requests.post('https://api.tradier.com/v1/markets/events/session',
    data={},
    headers=headers
    #headers={'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN), 'Accept': 'application/json'}
)
json_response = response.json()
#print(response.status_code)
#print(json_response)

SESSION_ID = json_response['stream']['sessionid']

#print (SESSION_ID)


payload = {
    "symbols": ["spy"],
    "sessionid": SESSION_ID,
    "linebreak": True
}
payload_str = json.dumps(payload)  # Convert the payload dictionary to a JSON string

async def ws_connect():
    uri = "wss://ws.tradier.com/v1/markets/events"
    async with websockets.connect(uri, ssl=True, compression=None) as websocket:
        #payload = '{"symbols": ["SPY"], "sessionid": "SESSION_ID", "linebreak": true}'
        await websocket.send(payload_str)

        print(f">>> {payload}")

        async for message in websocket:
            print(f"<<< {message}")

asyncio.run(ws_connect())

