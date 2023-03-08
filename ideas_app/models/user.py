# from dojosninjas_app.models.ninja import Ninja
from ideas_app.config.mysqlconnection import connectToMySQL
from ideas_app import app
from flask import flash
import re # El módulo regex
from flask_bcrypt import Bcrypt
# from recetas_app.models.recipe import Recipe
bcrypt = Bcrypt(app)     # estamos creando un objeto llamado bcrypt,
                                # que se realiza invocando la función Bcrypt con nuestra aplicación como argumento


# crea un objeto de expresión regular que usaremos más adelante
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASS_REGEX = re.compile(r'^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$')
LETRAS_REGEX = re.compile(r'^[a-zA-Z]+$')

class User():
    db_name = "proyecto_ideas_brillantes"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.alias = data['alias']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        #self.recetas = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, alias, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(alias)s, %(email)s, %(password)s, NOW(), NOW())"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        result =  connectToMySQL(cls.db_name).query_db(query)
        # print('Contenido de result: ',result)
        users =[]
        for row in result:
            users.append(cls(row))
        return users

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        # print('Esto tiene el mostrar en la posición 0:', result[0])
        return cls(result[0])

    @classmethod
    def getEmail(cls, email):
        query = "select * from users where email = %(email)s;"
        mysql = connectToMySQL(cls.db_name)
        data = {
            'email': email
        }
        result = mysql.query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
    
    @classmethod
    def getId(cls, data):
        query = "select * from users where id = %(id)s;"
        mysql = connectToMySQL(cls.db_name)
        result = mysql.query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
    
    """
    @classmethod
    def get_recipe_and_user(cls):
        query = "SELECT * FROM users LEFT JOIN recipes ON  users.id = recipes.user_id"
        results =  connectToMySQL(cls.db_name).query_db(query)
        print('Contenido de results: ',results)
        user = cls(results[0])
        for result in results:
            receta_data = {
                'id': result['recipes.id'],
                'name': result['name'],
                'description': result['description'],
                'instructions': result['instructions'],
                'under30': result['under30'],
                'date_made': result['date_made'],
                'created_at': result['recipes.created_at'],
                'updated_at': result['recipes.updated_at'],
                'user_id': result['user_id']
            }
            user.recetas.append(Recipe(receta_data))
        return user """


    @classmethod
    def update(cls, data):
        # print('Estoy en el método UPDATE y soy el data: ', data)
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, alias=%(alias)s, email=%(email)s, password=%(password)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        # print('ESTOY EN EL DESTROY CON DATA:', data)
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @staticmethod
    def validate_register( user ):

        is_valid = True # asumimos que esto es true
        query = "select * from users where email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,user)
        if len(results) >= 1:
            flash("El email ya esta en uso.", "register")
        if not LETRAS_REGEX.match(user['first_name']): 
            flash("El nombre solo puede tener Letras", "register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "register")
            is_valid = False
        if not LETRAS_REGEX.match(user['last_name']): 
            flash("El apellido solo puede tener Letras", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Formato de Email incorrecto!", "register")
            is_valid = False
        if not PASS_REGEX.match(user['password']): 
            flash("La contraseña debe tener de 8 a 16 caracteres, al menos 1 dígito, al menos 1 minúscula y al menos 1 mayúscula.!", "register")
            is_valid = False    
        if (user['password'] != user['confir_password']):
            flash("Las contraseñas no coinciden", "register")
        return is_valid
    
