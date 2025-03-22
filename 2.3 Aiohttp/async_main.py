from aiohttp import web
from async_db import User, Advertisment, async_session, init_db, close_db
import asyncio
from sqlalchemy import select, delete

app = web.Application()

# Обработчик для корневого пути
async def handle_root(request):
    return web.json_response({
        'status_code': 200,
        'message': 'Welcome to the API'
    })

class UserView(web.View):
    async def get(self):
        async with async_session() as session:
            query = await session.execute(select(User))
            users = query.scalars().all()
            data = {usr.id: {'token': usr.token, 'username': usr.username} for usr in users}
            return web.json_response({
                'status_code': 200,
                'message': 'Ok',
                'data': data
            })

    async def post(self):
        data = await self.request.json()
        user_name = data.get('username')
        token = data.get('token')
        if not user_name or not token:
            return web.json_response({
                'status_code': 400,
                'message': 'Wrong data'
            }, status=400)

        async with async_session() as session:
            new_user = User(username=user_name, token=token)
            session.add(new_user)
            await session.commit()
            return web.json_response({
                'status_code': 201,
                'message': 'User created',
                'data': {
                    'id': new_user.id,
                    'username': user_name,
                    'token': token
                }
            }, status=201)

class AdViewList(web.View):
    async def get(self):
        async with async_session() as session:
            query = await session.execute(select(Advertisment))
            ads = query.scalars().all()
            data = {ad.id: {'header': ad.header, 'description': ad.description, 'user': ad.user, 'created_at': str(ad.created_at)} for ad in ads}
            return web.json_response({
                'status_code': 200,
                'message': 'Ok',
                'data': data
            })

class AdView(web.View):
    async def get(self):
        ad_id = int(self.request.match_info['ad_id'])
        async with async_session() as session:
            query = await session.execute(select(Advertisment).where(Advertisment.id == ad_id))
            ad = query.scalars().first()
            if not ad:
                return web.json_response({
                    'status_code': 404,
                    'message': 'Not found'
                }, status=404)
            data = {ad.id: {'header': ad.header, 'description': ad.description, 'user': ad.user, 'created_at': str(ad.created_at)}}
            return web.json_response({
                'status_code': 200,
                'message': 'Ok',
                'data': data
            })

    async def post(self):
        data = await self.request.json()
        header = data.get('header')
        description = data.get('description')
        token = self.request.headers.get('token')
        if not header or not description or not token:
            return web.json_response({
                'status_code': 400,
                'message': 'Wrong json data'
            }, status=400)

        async with async_session() as session:
            user = await session.execute(select(User).where(User.token == token))
            user = user.scalars().first()
            if not user:
                return web.json_response({
                    'status_code': 401,
                    'message': 'Unauthorized'
                }, status=401)

            adv = Advertisment(header=header, description=description, user=user.id)
            session.add(adv)
            await session.commit()
            return web.json_response({
                'status_code': 201,
                'message': 'Advertisement created',
                'data': {
                    'id': adv.id,
                    'header': adv.header,
                    'description': adv.description
                }
            }, status=201)

    async def delete(self):
        ad_id = int(self.request.match_info['ad_id'])
        async with async_session() as session:
            await session.execute(delete(Advertisment).where(Advertisment.id == ad_id))
            await session.commit()
            return web.json_response({
                'status_code': 204,
                'message': 'Ok'
            }, status=204)

    async def patch(self):
        ad_id = int(self.request.match_info['ad_id'])
        data = await self.request.json()
        header = data.get('header')
        description = data.get('description')
        if not header and not description:
            return web.json_response({
                'status_code': 400,
                'message': 'Wrong json data'
            }, status=400)

        async with async_session() as session:
            adv = await session.execute(select(Advertisment).where(Advertisment.id == ad_id))
            adv = adv.scalars().first()
            if not adv:
                return web.json_response({
                    'status_code': 404,
                    'message': 'Not found'
                }, status=404)

            if header:
                adv.header = header
            if description:
                adv.description = description
            await session.commit()
            return web.json_response({
                'status_code': 200,
                'message': 'Ok',
                'data': {
                    'id': adv.id,
                    'header': adv.header,
                    'description': adv.description
                }
            })

# Регистрация маршрутов
app.router.add_get('/', handle_root)  # Маршрут для корневого пути
app.router.add_routes([
    web.get('/user/', UserView),  # GET для получения списка пользователей
    web.post('/user/', UserView),  # POST для создания пользователя
    web.get('/adv/', AdViewList),  # GET для получения списка объявлений
    web.post('/adv/', AdView),  # POST для создания объявления
    web.get('/adv/{ad_id}', AdView),  # GET для получения одного объявления
    web.delete('/adv/{ad_id}', AdView),  # DELETE для удаления объявления
    web.patch('/adv/{ad_id}', AdView),  # PATCH для обновления объявления
])

async def init_app():
    await init_db()
    return app

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app, host='127.0.0.1', port=5000)
    loop.run_until_complete(close_db())