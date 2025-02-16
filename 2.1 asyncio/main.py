import asyncio
from aiohttp import ClientSession
import more_itertools

import os
import requests


#get count of People
response = requests.get(f'https://swapi.dev/api/people/')
if response.status_code == 200:
    MAX_PEOPLE_ID = response.json()['count']
else:
    raise ConnectionError('Cant connect to https://swapi.dev/api/people/')


MAX_REQUESTS = int(os.getenv('MAX_REQUESTS'))
URL = os.getenv('URL')


# async def get_request(session:ClientSession, current_id: int):
#     #get people
#     result = await session.get(f'{URL}people/{current_id}/')
#     data = await result.json() 
#     pass
#     return 0

async def get_json_from_url(session:ClientSession, url:str)->dict:
    
    result = await session.get(f'{url}')
    if result.status_code == 200:
        return await result.json() 
    else:    
        return {}


async def main():
    async with ClientSession() as session:

        for people_id in range(1, MAX_PEOPLE_ID):
            
    print('Done!')

if __name__ == '__main__':
    asyncio.run(main())