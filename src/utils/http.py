# utils.http

# import json
# import aiohttp
import requests

def get_http(uri, API):
    response = requests.get(uri, auth=API.auth)
    if response.status_code == 200:
        if 'was not found' in response.text:
            return None
        else:
            return response.json()


def post_http(uri, API, headers, data=None, json=None):
    if json:
        response = requests.get(uri, auth=API.auth, headers=headers, json=json)
    elif data:
        response = requests.get(uri, auth=API.auth, headers=headers, data=data)
    return response.json()


# async def get_http(uri, API):
#     if 'http://' in uri:
#         ssl_state = False
#     else:
#         ssl_state = True
#     async with aiohttp.ClientSession(auth=API.auth) as session:
#         async with session.get(uri, headers=API.headers, ssl=ssl_state) as resp:
#             response = await resp.text()
#     if response:
#         if 'was not found' in response:
#             return None
#         else:
#             return json.loads(response)


# async def post_http(uri, API, headers, data=None, json=None):
#     if 'http://' in uri:
#         ssl_state = False
#     else:
#         ssl_state = True
#     async with aiohttp.ClientSession(auth=API.auth) as session:
#         if json:
#             async with session.post(uri, headers=headers, ssl=ssl_state, json=json) as resp:
#                 return await resp.text()
#         elif data:
#             async with session.post(uri, headers=headers, ssl=ssl_state, data=data) as resp:
#                 return await resp.text()
