import re
import mysql.connector

def conectar():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="coltis_productos",
    )
    return db