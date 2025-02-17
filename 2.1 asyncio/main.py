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


async def get_json(session:ClientSession, url_list:list[str], tag:str = None)->list[dict]:
    result = []
    if type(url_list) == str:
        url_list = [url_list]
    for url in url_list:
        await asyncio.sleep(TIME_SLEEP_REQUESTS) 
        response = await session.get(f'{url}')
        if response.status == 200:
            if not tag:
                result.append(await response.json())
            else:
                json_resp = await response.json()
                result.append(json_resp.get(tag))
        else:    
            result.append({})
    return result if len(result) > 1 else result[0] if len(result) != 0 else []



async def get_data_toDB(session:ClientSession, people_id: int):

    data = await get_json(session=session, url_list=f'{URL}people/{people_id}')
    if not data:
        return {}
    tasks = []
    
    tasks.append(get_json(session=session, url_list=data.get('films'), tag='title'))
    tasks.append(get_json(session=session, url_list=data.get('species'), tag='name'))
    tasks.append(get_json(session=session, url_list=data.get('starships'), tag='name'))
    tasks.append(get_json(session=session, url_list=data.get('vehicles'), tag='name')) #TODO: add homeworld with tag 'name'
    
    returns = await asyncio.gather(*tasks)
    
    if returns:
        films = returns[0]
        species = returns[1]
        starships = returns[2]
        vehicles = returns[3]
    else:
        films = []
        species = []
        starships = []
        vehicles = []
        
    new_data = {
        'id':people_id,
        'birth_year':data.get('birth_year'),
        'eye_color':data.get('eye_color'),
        'films':films,
        'gender':data.get('gender'),
        'hair_color':data.get('hair_color'),
        'height':data.get('height'),
        'homeworld':data.get('homeworld'),
        'mass':data.get('mass'),
        'name':data.get('name'),
        'skin_color':data.get('skin_color'),
        'species':species,
        'starships':starships,
        'vehicles':vehicles
    }
    print('\n\n')
    print(new_data)
# insert_people_corut = insert_people(result)
    # task = asyncio.create_task(insert_people_corut)

async def main():
    async with ClientSession() as session:
        for people_id in range(1, MAX_PEOPLE_ID):
            task = asyncio.create_task(get_data_toDB(session = session, people_id = people_id))
            print('add task___________________________________________________')
            

        tasks = asyncio.all_tasks()
        tasks.remove(asyncio.current_task())
        print('End Program\nFINISH ALL TASKS_____________________________________')
        if tasks != None:
            for task in tasks:
                await task
            
    print('Done!')

if __name__ == '__main__':
    asyncio.run(main())