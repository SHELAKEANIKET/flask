from app.utils.db import mysql

class Admin:
    @staticmethod
    def login_admin(email):
       cur = mysql.connection.cursor()
       cur.execute("SELECT * FROM admin WHERE email = %s", (email,))
       admin = cur.fetchone()
       cur.close()
       return admin