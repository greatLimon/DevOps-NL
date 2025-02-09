from flask import Flask, jsonify, request
from flask.views import MethodView

from db import session, Advertisment, User


#Flask
app = Flask('app')

class UserView(MethodView):
    
    def get(self):
        query = session.query(User).all()
        # print(query)
        data = {}
        for usr in query:
            data[usr.id] = {'token': usr.token, 'username': usr.username}
        return jsonify({
                'status_code': 200,
                'message': 'Ok',
                'data' : data
                })

    def post(self):
        try:
            user_name = request.headers.get('username')
            token = request.headers.get('token')
        except:
            return jsonify({
                'status_code': 400,
                'message': 'Wrong data'    
                })
        try:
            new_user = User(username = user_name, token = token)
            session.add(new_user)
            session.commit()
            return jsonify({
                    'status_code': 201,
                    'message': 'User created',
                    'data' : 
                        {
                        'id': new_user.id,
                        'username': user_name,
                        'token': token
                        }    
                    })
        except:
            session.rollback()
            return jsonify({
                'status_code': 503,
                'message': 'Service Unavailable'
                })


class AdViewList(MethodView):

    def get(self):
        query = session.query(Advertisment).all()
        data = {}
        for obj in query:
            data[obj.id] = {'header': obj.header, 
                            'description': obj.description, 
                            'user': obj.user,
                            'created_at': obj.created_at
                            }
            
        return jsonify({
                'status_code': 200,
                'message': 'Ok',
                'data' : data
                })

class AdView(MethodView):

    def get(self, ad_id:int):
        query = session.query(Advertisment).filter(Advertisment.id == ad_id).all()
        data = {}
        for obj in query:
            data[obj.id] = {'header': obj.header, 
                            'description': obj.description, 
                            'user': obj.user,
                            'created_at': obj.created_at
                            }
        return jsonify({
                'status_code': 200,
                'message': 'Ok',
                'data' : data
                })

    def post(self):
        try:
            json_data = request.json

            header = json_data.get('header')
            description = json_data.get('description')
        except:
            return jsonify({
                'status_code': 400,
                'message': 'Wrong json data'    
                })
        try:
            token = request.headers.get('token')
            user = session.query(User).filter(User.token == token).first()
        except:
            return jsonify({
                'status_code': 401,
                'message': 'Unauthorized'    
                })
        try:
            adv = Advertisment(header = header, description = description, user = user.id)
            session.add(adv)
            session.commit()
            return jsonify({
                    'status_code': 201,
                    'message': 'User created',
                    'data' : {
                        'id': adv.id,
                        'header': adv.header,
                        'description': adv.description
                    }  
                    })
        except:
            session.rollback()
            return jsonify({
                'status_code': 503,
                'message': 'Service Unavailable'
                })


    def delete(self, ad_id:int):
        try:
            query = session.query(Advertisment).filter(Advertisment.id == ad_id).delete()
            session.commit()
            return jsonify(
                {
                'status_code': 204,
                'message': 'Ok',
                'data' : query
                }
            )
        except:
            session.rollback()
            return jsonify(
                {
                    'status_code': 503,
                    'message': 'Service Unavailable'
                }
            )

    def patch(self, ad_id:int):
        try:
            adv = session.query(Advertisment).filter(Advertisment.id == ad_id).first()
            json_data = request.json
            header = json_data.get('header')
            description = json_data.get('description')
            if header != None:
                adv.header = header
            if description != None:
                adv.description = description

        except:             
            return jsonify({
                'status_code': 400,
                'message': 'Wrong json data'    
                })
        try:
            session.add(adv)
            session.commit
        except:
            session.rollback()
            return jsonify({
                    'status_code': 201,
                    'message': 'OK',
                    'data' : adv  
                    })
            


app.add_url_rule('/adv/', view_func=AdViewList.as_view('adv_list'), methods=['GET'])
app.add_url_rule('/adv/', view_func=AdView.as_view('adv_create'), methods=['POST'])
app.add_url_rule('/adv/<int:ad_id>', view_func=AdView.as_view('adv'), methods=['GET', 'DELETE', 'PATCH'])
app.add_url_rule('/user/', view_func=UserView.as_view('user'), methods = ['GET', 'POST'])

if __name__ == '__main__':

    #db
    
    # header = 'Продаю стол'
    # description = 'Классный стол'
    # User = 'Admin'
    # new_adv = Advertisment(header = header, description = description, user = User)
    # session.add(new_adv)
    # session.commit()

    # print(new_adv.id)

    # print(sess.query(Advertisment).all())
    #Flask
    app.run(host='127.0.0.1', port=5000)
    