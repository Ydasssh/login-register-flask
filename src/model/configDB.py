import mysql.connector


def connectionBD(): 
    miConexion = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        db='sistema_biblioteca'
        )
    if miConexion:
        print("Conexion exitosa")
    else:
        print("Error en la conexion")
    return miConexion


def getAllUsuarios():
    conexion=connectionBD()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `usuarios`")
    listaUsuarios=cursor.fetchall()
    conexion.commit()
    return listaUsuarios

def getUsuario(__correo, __contraseña):

    print("---------DATOS----------")
    print(__correo)
    print(__contraseña)

    try:
        conexion_DB = connectionBD()
        cursor = conexion_DB.cursor(dictionary=True)
        sql = "SELECT * FROM usuarios WHERE correo= %s AND contraseña = %s"
        valores = (__correo, __contraseña)
        cursor.execute(sql, valores)
        account = cursor.fetchone()

    except mysql.connector.Error as error:
            # Manejo del error y mensaje de error al usuario
            print("Error al ejecutar la consulta:", error)
            conexion_DB.rollback()
    finally:
        cursor.close()
        conexion_DB.close()

    return account

