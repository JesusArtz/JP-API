import pymysql
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash
from jwt import encode, decode
from flask import jsonify
from __init__ import app


@dataclass
class DB:

    host = 'localhost'
    user = 'root'
    password = ''
    db = 'asesorias'

    def __post_init__(self):
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db
        )

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        return cursor
    
    def execute_read_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    
    def close_connection(self):
        self.connection.close()


@dataclass
class Usuario:

    data: dict
    db = DB()

    def login(self):

        if not all(keys in self.data for keys in ('control', 'password')):
            return jsonify({'message': 'Faltan datos'})

        
        user = self.db.execute_read_query(f"SELECT * FROM usuarios WHERE control = '{self.data['control']}'")
        print(user)
        password_correct = check_password_hash(user[0][4], self.data['password'])

        print(password_correct)
        if not password_correct:
            print("Error")
            return {'error': 'Invalid password'}
        
        print("Ok")
            
        return {'token':encode({'control':self.data['control']}, app.config['SECRET_KEY'], algorithm='HS256')}
        
        
    def register(self):

        if not all(keys in self.data for keys in ('control', 'nombre','apellido', 'password')):
            return False
        
        
        password_hash = generate_password_hash(self.data['password'], method='sha256')
        self.db.execute_query(f"INSERT INTO usuarios (control, nombre, apellido, password) VALUES ('{self.data['control']}', '{self.data['nombre']}', '{self.data['apellido']}', '{password_hash}')")
        return self.login()
        
       
        
    def get_user(self):

        if not all(keys in self.data for keys in ('control',)):
            return False
        
        try:
            user = self.db.execute_read_query(f"SELECT * FROM usuarios WHERE control = {self.data['control']} " )
            print(user)
            return jsonify({
                'id': user[0][0],
                'nombre': user[0][1],
                'apellido': user[0][2],
                'control': user[0][3]

            })
        except:
            return False
        
    def send_calificacion(self):

        if not all(keys in self.data for keys in ('calificacion', 'id_asesoria', 'token')):
            return jsonify({'message': 'Faltan datos'})
        control = decode(self.data['token'], app.config['SECRET_KEY'], algorithms=["HS256"])['control']
        try:
            user_id = self.db.execute_read_query(f"SELECT id FROM usuarios WHERE control = {control}")[0][0]
            self.db.execute_query(f"UPDATE evaluaciones SET calificacion = {self.data['calificacion']} WHERE id_asesoria = {self.data['id_asesoria']}")
            self.db.execute_query(f"INSERT INTO historial (id_asesoria, calificacion, id_usuario) VALUES ({self.data['id_asesoria']}, {self.data['calificacion']}, {user_id})")
            return jsonify({'message': 'Calificacion enviada'})
        except:
            return jsonify({'message': 'Error al enviar calificacion'})
        
    def create_asesoria(self):

        # Cuando se crea una asesoria, se crea una evaluacion con calificacion 0 y una materia con el nombre de la asesoria

        if not all(keys in self.data for keys in ('token', 'id_materia', 'nombre')):
            return jsonify({'message': 'Faltan datos'})
        
        control = decode(self.data['token'], app.config['SECRET_KEY'], algorithms=['HS256'])['control']
        user_id = self.db.execute_read_query(f"SELECT id FROM usuarios WHERE control = {control}")[0][0]
        self.db.execute_query(f"INSERT INTO materias (id_usuario, nombre) VALUES ({user_id}, '{self.data['nombre']}')")
        self.db.execute_query(f"INSERT INTO asesorias (id_usuario, id_materia, nombre) VALUES ({user_id}, {self.data['id_materia']}, '{self.data['nombre']}')")
        asesoria_id = self.db.execute_read_query(f"SELECT id FROM asesorias WHERE id_usuario = {user_id} AND id_materia = {self.data['id_materia']}")[0][0]
        self.db.execute_query(f"INSERT INTO evaluaciones (id_usuario, id_asesoria, calificacion) VALUES ({user_id}, {asesoria_id}, 0)")
        
        return jsonify({'message': 'Asesoria creada'})
    
    def get_asesorias(self):

        if not all(keys in self.data for keys in ('token',)):
            return jsonify({'message': 'Faltan datos'})
        
        control = decode(self.data['token'], app.config['SECRET_KEY'], algorithms=['HS256'])['control']

        try:
            user = self.db.execute_read_query(f"SELECT id FROM usuarios WHERE control = {control}")
            asesorias = self.db.execute_read_query(f"SELECT * FROM asesorias WHERE id_usuario = {user[0][0]}")
            """
            {
            "1": {
                "nombre": "Matematicas",
                "profesor": "Juan Perez",
                "id": 1
            }
            }
            """
            obj = {}
            for asesoria in asesorias:
                obj[asesoria[0]] = {
                    'materia': asesoria[3],
                    'profesor': self.db.execute_read_query(f"SELECT nombre FROM usuarios WHERE id = {asesoria[1]}")[0][0],
                    'id': asesoria[0]
                }
            return jsonify(obj)
        except:
            return False
        
        

    
