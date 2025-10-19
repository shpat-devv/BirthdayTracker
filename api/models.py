from .database import Database

db = Database("birthdays.db")

class User:
    def __init__(self, name, email, password):
        self.user_id = None
        self.name = name
        self.email = email
        self.password = password

    def get_creds(self):
        db.connect()
        result = db.cursor.execute(
            "SELECT * FROM users WHERE email = ?", (self.email,)
        ).fetchone()
        db.disconnect()
        return result is not None
    
    def verify(self): #id checking
        db.connect()
        result = db.cursor.execute(
            "SELECT * FROM users WHERE user_id = ?", (self.user_id,)
        ).fetchone()
        db.disconnect()
        return result is not None
    
    def exists(self): #email & password checking
        db.connect()
        result = db.cursor.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?", (self.email, self.password)
        ).fetchone()

        if result == None:
            print("User not found...")
            return False
        else:
            print("User found")
            return True

    def get_birthdays(self):
        db.connect()
        result = db.cursor.execute(
            "SELECT * FROM birthdays WHERE user_id = ?", (self.user_id,)
        ).fetchall()
        db.disconnect()
        return result

    def save(self):
        db.connect()
        if self.exists():
            print("User Already exists, ignoring save")
        else:
            user_dict = {"name": self.name, "email": self.email, "password": self.password}
            db.insert("users", user_dict)
            
        db.connection.commit()
        db.disconnect()
        print(f"User {self.name} saved successfully.")

    def delete(self):
        db.connect()
        db.cursor.execute("DELETE FROM users WHERE user_id = ?", (self.user_id,))
        db.connection.commit()
        db.disconnect()
        print(f"User {self.name} deleted successfully.")


class Birthday:
    def __init__(self, birthday_id, name, day, month, user_id):
        self.birthday_id = birthday_id
        self.name = name
        self.day = day
        self.month = month
        self.user_id = user_id

    def save(self):
        db.connect()
        result = db.cursor.execute(
            "SELECT * FROM birthdays WHERE birthday_id = ?", (self.birthday_id,)
        ).fetchone()

        if result:
            db.cursor.execute(
                "UPDATE birthdays SET name = ?, day = ?, month = ?, user_id = ? WHERE birthday_id = ?",
                (self.name, self.day, self.month, self.user_id, self.birthday_id)
            )
        else:
            db.cursor.execute(
                "INSERT INTO birthdays (birthday_id, name, day, month, user_id) VALUES (?, ?, ?, ?, ?)",
                (self.birthday_id, self.name, self.day, self.month, self.user_id)
            )

        db.connection.commit()
        db.disconnect()
        print(f"Birthday {self.name} saved successfully.")

    def delete(self):
        db.connect()
        db.cursor.execute("DELETE FROM birthdays WHERE birthday_id = ?", (self.birthday_id,))
        db.connection.commit()
        db.disconnect()
        print(f"Birthday {self.name} deleted successfully.")

    @staticmethod
    def add_bday(name, month, day, user_id):
        db.connect()
        db.cursor.execute(
            "INSERT INTO birthdays (name, month, day, user_id) VALUES (?, ?, ?, ?)",
            (name, month, day, user_id)
        )
        db.connection.commit()
        db.disconnect()
        print(f"Added new birthday for {name}.")

    @staticmethod
    def get_bdays(user_id=None):
        db.connect()
        if user_id:
            entries = db.cursor.execute(
                "SELECT * FROM birthdays WHERE user_id = ?", (user_id,)
            ).fetchall()
        else:
            entries = db.cursor.execute("SELECT * FROM birthdays").fetchall()
        db.disconnect()
        return entries
