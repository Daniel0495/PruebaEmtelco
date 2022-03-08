from flask import Flask, request, make_response, jsonify
import requests
from database_functions import database_manage


app = Flask(__name__)


@app.route('/')
def home():
    print(help(str))
    return {'message': 'hola'}


@app.route('/crear', methods=['POST'])
def insert():
    data = request.json

    db = database_manage()
    status = db.insert_database(data)
    if status == 200:
        return make_response({'message': 'Datos insertados correctamente'}, status)
    else:
        return make_response({'message': 'Error al insertar los datos'}, status)


@app.route('/leer')
def read():
    data = request.json

    db = database_manage()
    results = db.read_data(data)
    return make_response(jsonify(results), 200)


@app.route('/borrar')
def delete():
    data = request.json

    db = database_manage()
    status = db.drop_data(data)
    return make_response({'message': 'Datos borrados correctamente'}, status)


@app.route('/actualizar', methods=['PUT'])
def update():
    data = request.json
    db = database_manage()
    status = db.insert_database(data)
    if status == 200:
        return make_response({'message': 'Datos insertados correctamente'}, status)
    else:
        return make_response({'message': 'Error al insertar los datos'}, status)


@app.route('/consulta-api')
def request_api():
    data = requests.get('https://gorest.co.in/public/v2/users/').json()
    data = list(map(lambda x: {'correo': x['email'],
                               'genero': x['gender'],
                               'id': x['id'],
                               'nombre': x['name']}, data))

    return make_response(jsonify(data), 200)



if __name__ == '__main__':
    db = database_manage()
    db.create_table()
    app.run()