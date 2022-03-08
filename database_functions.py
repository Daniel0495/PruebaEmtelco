import sqlite3
import string


class database_manage():
    def __init__(self):
        self.con = sqlite3.connect('emtelco.db')

    def create_table(self):
        cur = self.con.cursor()
        try:
            cur.execute('''CREATE TABLE web_data
                       (identificacion int primary key, 
                       nombre text, 
                       genero text, 
                       numero int, 
                       correo text)''')
            self.con.commit()
            self.con.close()
        except:
            pass


    def insert_database(self, data: dict, update=False):
        cur = self.con.cursor()
        try:
            if type(data['id'])  != int:
                raise Exception('no es numerico')
            elif len(str(data['id'])) <6 or len(str(data['id'])) > 11:
                raise Exception('id no cumple los estándares')

            if len(data['nombre']) > 100:
                raise Exception('nombre desamido largo')
            elif len(set(string.digits) & set(data['nombre'])) > 0:
                raise Exception('el nombr eno puede tener numeros')

            if data['genero'] not in ['Masculino', 'Femenino', 'Otro']:
                raise Exception('genero no valido')

            if len(str(data['numero'])) != 10:
                raise Exception('el numero no tiene 10 digitos')
            elif str(data['numero'])[0] not in {'6', '3'}:
                raise Exception('el numero no cumple con el formato de inicio')

            if "@" not in str(data['correo']) or "." not in str(data['correo']):
                raise Exception('El correo no es valido')

            if update:
                query = """UPDATE web_data set nombre = ?, genero = ?, numero = ?, correo = ? WHERE identificacion = ?"""
                values = (data.get('nombre'), data.get('genero'), data.get('numero'), data.get('correo'), data.get('id'))
                cur.execute(query, values)

                self.con.commit()
                self.con.close()
                return 200
            else:
                query  = """ INSERT INTO web_data(identificacion, nombre, genero, numero, correo) VALUES (?,?,?,?, ?)"""
                values = (data.get('id'), data.get('nombre'), data.get('genero'), data.get('numero'), data.get('correo'))
                cur.execute(query, values)

                self.con.commit()
                self.con.close()
                return 200
        except Exception as e:
            print(e)
            return 400


    def drop_data(self, data: dict):
        cur = self.con.cursor()

        try:
            query = "DELETE FROM web_data WHERE identificacion=?",
            value = (data['id'])

            cur.execute(query, value)

            self.con.commit()
            self.con.close()
            return 200
        except Exception as e:
            print(e)
            return 400


    def read_data(self, data:dict):
        cur = self.con.cursor()

        if data:
            query = "SELECT * FROM web_data WHERE identificacion= ?"
            values = (data['id'],)
            cur.execute(query, values)
        else:
            query = "SELECT * FROM web_data"
            cur.execute(query)

        results = cur.fetchall()

        results_ = list(map(lambda x: {'identificacion': x[0],
                                       'nombre': x[1],
                                       'genero': x[2],
                                       'telefono': x[3],
                                       'correo': x[4]}, results))


        self.con.commit()
        self.con.close()
        return results_
