from flask_app.config.mysqlconnections import connectToMySQL
from flask import flash

class Tvshow:
    db_name="tvshows"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO tvshow (name, network, release_date, description, user_id) VALUES (%(name)s, %(network)s, %(release_date)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)



    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM tvshow JOIN users ON tvshow.user_id = users.id WHERE tvshow.id = %(id)s;"
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        return results[0] 

    @classmethod
    def update(cls, data):
        query = "UPDATE tvshow SET name=%(name)s, network =  %(network)s, release_date=%(release_date)s, description=%(description)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query= "SELECT * FROM tvshow;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_tvshows= []
        for row in results:
            all_tvshows.append(row)
        return all_tvshows
    
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM tvshow WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_tvshow(tvshow):
        is_valid = True
        if len(tvshow['name'])<3:
            flash('Name of the TV Show must be at least 3 characters', "tvshow")
            is_valid=False
        if len(tvshow['network'])<3:
            flash('Network must be at least 3 characters', "tvshow")
            is_valid=False
        if len(tvshow['description'])<3:
            flash('Description must be at least 3 characters', "tvshow")
            is_valid=False
        return is_valid


    @classmethod
    def addLike(cls, data):
        query = "INSERT INTO users_who_liked (tvshow_id,users_id) VALUES (%(tvshow_id)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def getUsersWhoLiked(cls, data):
        query = "SELECT * FROM users_who_liked LEFT JOIN tvshow ON users_who_liked.tvshow_id = tvshow.id LEFT JOIN users ON users_who_liked.users_id = users.id WHERE tvshow.id = %(tvshow_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        myTvshow = Tvshow.get_one(data)
        for row in results:
            myTvshow.users_who_liked.append(row['email'])
        myTvshow.likes=len(myTvshow.users_who_liked)
        print(myTvshow.users_who_liked)
        return myTvshow