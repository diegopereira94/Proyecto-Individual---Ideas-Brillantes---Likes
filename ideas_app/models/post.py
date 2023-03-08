# from dojosninjas_app.models.ninja import Ninja
from ideas_app.config.mysqlconnection import connectToMySQL
from flask import flash
from ideas_app.models.like import Like


class Post():
    db_name = 'proyecto_ideas_brillantes'

    def __init__(self,data):
        self.id = data['id']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.idUser = data['idUser']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.alias = data['alias']

        # self.post_id = data['post_id']
        # self.likes = data['likes']
        # self.iduser_liked = data['iduser_liked']



    @classmethod
    def save(cls,data):
        query = "INSERT INTO posts (description, created_at, updated_at, user_id) VALUES (%(description)s, NOW(), NOW(), %(user_id)s)"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print('result en SAVE POST', result)
        return result

    @classmethod
    def get_all(cls):
        query = """ SELECT posts.id AS id, description, posts.created_at, posts.updated_at, posts.user_id, users.id AS idUser, first_name, last_name, alias
                FROM posts INNER JOIN users
                ON posts.user_id = users.id; """
        result =  connectToMySQL(cls.db_name).query_db(query)
        print('Contenido de result===============: ',result)
        all_post =[]
        for row in result:
            all_post.append(cls(row))
        # print('ALL RECIPES:', all_recipes)
        print('TODOS LOS POST:', all_post)
        return all_post

    @classmethod
    def get_one_post_by_id(cls,data):
        query = """SELECT posts.id, description, posts.created_at, posts.updated_at, posts.user_id, users.id AS idUser, first_name, last_name, alias
                    FROM posts 
                    INNER JOIN users
                    ON posts.user_id = users.id
                    WHERE posts.id = %(id)s"""
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print('Result de get_one_post_by_id TIENE:', result)
        return cls(result[0])

    '''
    @classmethod
    def get_all(cls):
        query = "SELECT posts.id AS id, description, posts.created_at, posts.updated_at, user_id, users.id AS idUser, first_name, last_name, alias FROM posts JOIN users ON posts.user_id = users.id"
        result =  connectToMySQL(cls.db_name).query_db(query)
        # print('Contenido de result: ',result)
        all_post =[]
        for row in result:
            all_post.append(cls(row))
        # print('ALL RECIPES:', all_recipes)
        print('TODOS LOS POST:', all_post)
        return all_post
    '''

    

    '''
    @classmethod
    def getId(cls, data):
        query = "select * from users where id = %(id)s;"
        mysql = connectToMySQL('login')
        result = mysql.query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
    '''

    @classmethod
    def update(cls, data):
        query = "UPDATE posts SET description=%(description)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        # print('ESTOY EN EL DESTROY CON DATA:', data)
        query = "DELETE FROM posts WHERE id = %(post_id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    
    @staticmethod
    def validate_post(data):
        is_valid = True
        
        if len(data['description']) < 2:
            is_valid = False;
            flash("El post debe tener al menos 2 caracteres", "post")
        return is_valid
