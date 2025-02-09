from flask import Flask, jsonify, request
from flask.views import MethodView

app = Flask('app')

class HelloWorld(MethodView):

    def get(self, variable: int):
        return jsonify(
            {
                'variable': variable, 
                'hello2':'world2'
            }
        )
    
    def post(self):
        json_data = request.json
        print(json_data)

        return jsonify(
            {'status':200}
        )

def hello_world():
    return jsonify(
        {
            'hello':'world'
        }
    )

# app.add_url_rule('/hello/', view_func=hello_world, methods = ['GET'])
app.add_url_rule('/hello/<int:variable>', view_func=HelloWorld.as_view('main'), methods = ['GET'])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
    