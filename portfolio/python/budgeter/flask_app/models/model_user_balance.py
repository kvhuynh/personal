from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models import model_user
DATABASE = "budgeter_db"

class Show:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data["user_id"]
        self.title = data["title"]
        self.network = data["network"]
        self.description = data["description"]
        self.release_date = data["release_date"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# ---------- VALIDATE ---------- #

    @staticmethod
    def validate_show(data):
        is_valid = True
        if len(data["title"]) < 1:
            flash("Field required.", "err_show_title")
            is_valid = False
        
        elif len(data["title"]) < 3:
            flash("Title must be at least 3 characters long", "err_show_title")
            is_valid = False

        if len(data["network"]) < 1:
            flash("Field required.", "err_show_network" )
            is_valid = False
        elif len(data["network"]) < 3:
            flash("Network must be at least 3 characters long", "err_show_network")
            is_valid = False

        if len(data["release_date"]) < 1:
            flash("Release date required", "err_show_release_date")

        if len(data["description"]) < 1:
            flash("Field required.", "err_show_description")
            is_valid = False
        elif len(data["description"]) < 3:
            flash("Description must be at least 3 characters long", "err_show_description")
            is_valid = False

        return is_valid


# ---------- Create ---------- #

    @classmethod
    def create(cls, data):
        query = "INSERT INTO shows (user_id, title, network, description, release_date) VALUES (%(user_id)s, %(title)s,%(network)s,%(description)s, %(release_date)s);"
        # comes back as the new row id
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

# ---------- Read ---------- #
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email =%(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_one(cls,data):
        print(data)
        query  = "SELECT * FROM shows WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return cls(result[0])

    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM shows JOIN users ON users.id = shows.user_id"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_shows = []
            for show in results:
                show_instance = cls(show)
                user_data = {
                    "id": show["users.id"],
                    "created_at": show["users.created_at"],
                    "updated_at": show["users.updated_at"],
                    "first_name": show["first_name"],
                    "last_name": show["last_name"],
                    "email": show["email"],
                    "password": show["password"]
                }
                user = model_user.User(user_data)
                show_instance.name = user
                all_shows.append(show_instance)
                print(all_shows[0].name.first_name)
            return all_shows
        return results

# ---------- Update ---------- #
    @classmethod
    def update_one(cls, data) -> None:
        query = "UPDATE shows SET title = %(title)s, network = %(network)s, description = %(description)s, release_date = %(release_date)s WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)

# ---------- Delete ---------- #
    @classmethod
    def delete_one(cls, data: dict) -> None:
        query = "DELETE FROM shows WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data) 