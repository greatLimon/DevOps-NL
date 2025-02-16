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
TIME_SLEEP_REQUESTS = int(os.getenv('TIME_SLEEP_REQUESTS', 0))
URL = os.getenv('URL')


async def get_json(session:ClientSession, url:str)->dict:
    
    result = await session.get(f'{url}')
    if result.status == 200:
        return await result.json() 
    else:    
        return {}



async def get_data_toDB(people_id: int):
    async with ClientSession() as session:
        data = await get_json(session=session, url=f'{URL}people/{people_id}')
        if data == {}:
            return {}
        new_data = {
            'id':people_id,
            'birth_year':data.get('birth_year'),
            'eye_color':data.get('eye_color'),
            'films':[await get_json(session=session, url = film) for film in data.get('films')],
            'gender':data.get('gender'),
            'hair_color':data.get('hair_color'),
            'height':data.get('height'),
            'homeworld':data.get('homeworld'),
            'mass':data.get('mass'),
            'name':data.get('name'),
            'skin_color':data.get('skin_color'),
            'species':[await get_json(session=session, url = film) for film in data.get('species')],
            'starships':[await get_json(session=session, url = film) for film in data.get('starships')],
            'vehicles':[await get_json(session=session, url = film) for film in data.get('vehicles')]
        }
        print('\n\n')
        print(new_data)
    # insert_people_corut = insert_people(result)
    # task = asyncio.create_task(insert_people_corut)

async def main():
    
    for people_id in range(1, MAX_PEOPLE_ID):
        task = asyncio.create_task(get_data_toDB(people_id = people_id))
        print('add task___________________________________________________')
        await asyncio.sleep(TIME_SLEEP_REQUESTS)

    tasks = asyncio.all_tasks()
    tasks.remove(asyncio.current_task())
    print('End Program\nFINISH ALL TASKS_____________________________________')
    if tasks != None:
        for task in tasks:
            await task
            
    print('Done!')

if __name__ == '__main__':
    asyncio.run(main())