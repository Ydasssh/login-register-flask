from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from passlib.hash import bcrypt
import bcrypt
from model.configDB import *


class User:
    def __init__(self, id, correo, contraseña):
        self.id = id
        self.correo = correo
        self.contraseña = contraseña

class LoginForm(FlaskForm):
    correo = StringField('correo', validators=[DataRequired()])
    contraseña = PasswordField('contraseña', validators=[DataRequired()])

    # def imprimir_datos(self):
    #     print("----------------DATOS----------------")
    #     print("CORREO: ", self.correo.data)
    #     print("CONTRASEÑA: ", self.contraseña.data)

    submit = SubmitField('Login')

class FormularioRegistro(FlaskForm):
    nombre_usuario = StringField('nombre_usuario', validators=[DataRequired()])
    correo = StringField('correo', validators=[DataRequired()])
    contraseña = PasswordField('contraseña', validators=[DataRequired()])
    confirmar_contraseña = PasswordField('confirmar_contraseña', validators=[DataRequired(), EqualTo('contraseña')])
    submit = SubmitField('Registrar')

def is_valid_login(correo, contraseña):
    # Hace una consulta para revisar si el correo existe
    db_connection = connectionBD()
    cursor = db_connection.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE correo = %s"
    cursor.execute(query, (correo,))
    usuario = cursor.fetchone()
    print("usuarios: ", usuario)
    cursor.close()
    db_connection.close()


    # Verifica si la contraseña en texto plano coincide con la contraseña hasheada en la BD
    if usuario and bcrypt.checkpw(contraseña.encode('utf-8'), usuario['contraseña'].encode('utf-8')):
        return User(usuario['id'], usuario['correo'], usuario['contraseña'])
    return None

def hashear_contraseña(contraseña):
    # Generar un salt aleatorio y hashear la contraseña
    salt = bcrypt.gensalt()
    contraseña_hasheada = bcrypt.hashpw(contraseña.encode('utf-8'), salt)
    return contraseña_hasheada

def registrar_usuario(nombre_usuario, correo, contraseña, id_rol):
    conexion_db = connectionBD()
    cursor = conexion_db.cursor()

    try:
        # Verificar si el nombre de usuario o el correo ya están en uso
        sql = "SELECT * FROM usuarios WHERE nombre_usuario = %s OR correo = %s"
        cursor.execute(sql, (nombre_usuario, correo))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            if usuario_existente[1] == nombre_usuario:
                flash('El nombre de usuario ingresado ya se encuentra en uso', 'error')
            elif usuario_existente[2] == correo:
                flash('El correo ingresado ya se encuentra en uso', 'error')
            return False
        else:
            # Insertar el nuevo usuario en la base de datos
            sql = "INSERT INTO usuarios (id, nombre_usuario, correo, contraseña, id_rol) VALUES (NULL, %s, %s, %s,%s)"
            valores = (nombre_usuario, correo, contraseña, id_rol)
            cursor.execute(sql, valores)
            conexion_db.commit()
            return True
        
    except mysql.connector.Error as e:
        print("Error:", e)
        conexion_db.rollback()
        return False
    finally:
        cursor.close()
        conexion_db.close()