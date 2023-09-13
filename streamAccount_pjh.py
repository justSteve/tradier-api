import asyncio
import websockets
import config, requests, json, sys

response = requests.post('https://api.tradier.com/v1/accounts/events/session',
    data={},
    headers={'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN_pjk), 'Accept': 'application/json'}
)
json_response = response.json()
# print(response.status_code)
# print(json_response)


# Directly access 'sessionid' from the nested dictionary
session_id = json_response.get('stream', {}).get('sessionid', 'Default Value')
print (session_id)

async def connect_and_consume():
  uri = "wss://ws.tradier.com/v1/accounts/events"

  async with websockets.connect(uri) as websocket:
      payload_dict = {
          "events": ["order"],
          "sessionid": session_id,  # holds valid session ID
          "excludeAccounts": []
      }
      payload_json = json.dumps(payload_dict)
      await websocket.send(payload_json)

  print(payload_json)

  while True:
      print("entering 'true' loop")
      response = await websocket.recv()  # error fires here
      print(f"< {response}")

asyncio.get_event_loop().run_until_complete(connect_and_consume())