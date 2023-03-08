from ideas_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Like():
    db_name = 'proyecto_ideas_brillantes'

    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.likes = data['likes']
        self.iduser_liked = data['iduser_liked']

        # self.first_name = data['first_name']
        # self.last_name = data['last_name']



    @classmethod
    def create_like(cls,data):
        query = "INSERT INTO likes (user_id, post_id, likes, iduser_liked) VALUES (%(user_id)s, %(post_id)s, %(likes)s, %(iduser_liked)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def verificar_si_el_post_no_tiene_like(cls,data):
        query = """ SELECT likes.id, likes.user_id, likes.post_id, likes.likes, likes.iduser_liked
                    FROM likes 
                    INNER JOIN users
                    ON (likes.user_id = users.id) AND (likes.user_id = %(user_id)s AND likes.post_id = %(post_id)s) AND (likes.likes = 0) AND (iduser_liked = 0); """
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print('TIPO DE DATO CUANDO RESULT RETORNA CARGADO: ', type(result))
        tipo = type(result)
        print('RESULT de verificar_si_existe_el_pos_by_iduser_liked TIENE:', result)

        if len(result) > 0:
            return cls(result[0])
        else:
            return None
    
    @classmethod
    def verificar_si_el_like_pertenece_alusuario(cls,data):
        query = """ SELECT likes.id, likes.user_id, likes.post_id, likes.likes, likes.iduser_liked
                    FROM likes 
                    INNER JOIN users
                    ON (likes.user_id = users.id) AND (likes.user_id = %(user_id)s AND likes.post_id = %(post_id)s) AND (likes.likes = 1) AND (iduser_liked = %(iduser_liked)s) """
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print('TIPO DE DATO CUANDO RESULT RETORNA CARGADO: ', type(result))
        tipo = type(result)
        print('RESULT de verificar_si_existe_el_pos_by_iduser_liked TIENE:', result)

        if len(result) > 0:
            return cls(result[0])
        else:
            return None
    
    @classmethod
    def get_like_by_user(cls,data):
        query = "SELECT * FROM likes WHERE iduser_liked = %(id)s"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print('Result de get_like_by_user TIENE:', result)
        all_likes_by_user =[]
        for row in result:
            all_likes_by_user.append(cls(row))
        print('TODOS LOS LIKES DE ESTE USUARIO:', all_likes_by_user)
        return all_likes_by_user
        # return cls(result)

    '''
    @classmethod
    def get_one_by_userid_postid_iduserliked(cls,data):
        query = """ SELECT likes.id, likes.user_id, likes.post_id, likes.likes , likes.dislikes, likes.iduser_liked, first_name, last_name
                    FROM likes 
                    INNER JOIN users
                    ON (likes.user_id = users.id) AND (likes = 1) AND (likes.user_id = %(user_id)s AND likes.post_id = %(post_id)s) AND (likes.iduser_liked = %(iduser_liked)s); """
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print('Result de get_one TIENE:', result)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
    '''


    # FALTA CORREGIR PORQUE ESTA MAL LA CONSULTA, ERA LA CONSULTA DE POST ANTES 
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
        query = "UPDATE likes SET likes = %(likes)s, iduser_liked = %(iduser_liked)s WHERE user_id = %(user_id)s and post_id = %(post_id)s and iduser_liked = 0"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def update_dislike(cls, data):
        query = "UPDATE likes SET likes = 0, iduser_liked = 0 WHERE user_id = %(user_id)s and post_id = %(post_id)s and iduser_liked = %(iduser_liked)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        # print('ESTOY EN EL DESTROY CON DATA:', data)
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND post_id = %(post_id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

