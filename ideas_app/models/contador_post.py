from ideas_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Contador_post():
    db_name = 'proyecto_ideas_brillantes'

    def __init__(self,data):
        self.contador = data['contador']




    @classmethod
    def get_total_post_by_user(cls,data):
        query = "SELECT count(user_id) AS contador FROM posts WHERE user_id = %(id)s"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print('RESULT DE get_total_post_by_user TIENE//////////', result)
        return result
    
    @classmethod
    def get_total_likes_by_user(cls,data):
        query = "SELECT sum(likes) AS contador FROM likes WHERE iduser_liked = %(id)s"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print('RESULT DE get_total_post_by_user TIENE//////////', result)
        return result
    
    @classmethod
    def get_total_likes_by_post(cls,data):
        query = "SELECT post_id, sum(likes) AS contador FROM likes WHERE post_id = %(id)s"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print('RESULT DE get_total_likes_by_post TIENE ##############', result)
        return result
