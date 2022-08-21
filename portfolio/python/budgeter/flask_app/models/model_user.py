# import the function that will return an instance of a connection
from flask_app import bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re

DATABASE = "budgeter_db"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.full_name = f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

# ---------- Create ---------- #
        
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s, %(password)s);"
        # comes back as the new row id
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result


# ---------- GET ---------- #

    @classmethod
    def get_one(cls,data):
        print(data)
        query  = "SELECT * FROM users WHERE id = %(id)s";
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return cls(result[0])


    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_users = []
            for user in results:
                all_users.append(cls(user))
            return all_users
        return False

    @classmethod
    def update_one(cls, data:dict) -> None:
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s ,email = %(email)s, first_name = %(first_name)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * FROM users WHERE email =%(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Didn't find a matching user
        if result:
            return cls(result[0])
        return False


    @staticmethod
    def validate_user(data:dict) -> bool:
        is_valid = True
        if len(data["first_name"]) < 1:
            flash("field is required", "err_users_first_name")
            is_valid = False
        elif len(data["first_name"]) < 3:
            flash("First name must be at least 2 characters", "err_users_first_name")
            is_valid = False

        if len(data["last_name"]) < 1:
            flash("field is required", "err_users_last_name")  
            is_valid = False
        elif len(data["last_name"]) < 3:
            flash("Lirst name must be at least 2 characters", "err_users_last_name")
            is_valid = False

        if len(data["email"]) < 1:
            flash("field is required", "err_users_email")
            is_valid = False
        elif not EMAIL_REGEX.match(data["email"]): 
            flash("Invalid Email address", "err_users_email")
            is_valid = False
        else:
            potential_user = User.get_one_by_email({"email": data["email"]})
            if potential_user:
                flash("Email already in use", "err_users_email")
                is_valid = False

        if len(data["password"]) < 1:
            flash("field is required", "err_users_password")
            is_valid = False

        if len(data["confirm_password"]) < 1:
            flash("field is required", "err_users_confirm_password")      
            is_valid = False 
        elif data["password"] != data["confirm_password"]:
            flash("Passwords do not match", "err_users_confirm_password")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(data:dict) -> bool:
        is_valid = True
        if len(data["email"]) < 1:
            flash("Field is required", "err_users_email_login")
            is_valid = False
        elif not EMAIL_REGEX.match(data["email"]): 
            flash("Invalid Email address", "err_users_email_login")
            is_valid = False
        else:
            potential_user = User.get_one_by_email({"email": data["email"]})
            if not potential_user:
                flash("Invalid Credentials", "err_users_email_login")
                is_valid = False

            # check hash
            elif not bcrypt.check_password_hash(potential_user.password, data["password"]):
                flash("Invalid Credentials", "err_users_password_login")
                is_valid = False

            # store id in session
            if (is_valid):
                session["uuid"] = potential_user.id

        if len(data["password"]) < 1:
            flash("Field is required", "err_users_password_login")
            is_valid = False


        return is_valid