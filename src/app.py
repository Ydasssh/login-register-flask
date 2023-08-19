from flask import Flask, render_template, redirect, url_for, flash, session
from config import config
from controller.func import *
from controller.validators import is_valid_email


app = Flask(__name__)
app.secret_key = 'as6aJa7sasUASD092hacd*!"E]A[D*a¨d"]'


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # Descomentar si quiere imprimir datos (tambien en la funcion)
    # form.imprimir_datos()

    if form.validate_on_submit():
        correo = form.correo.data
        contraseña = form.contraseña.data

        if not is_valid_email(correo):
            flash('Ingrese un correo válido', 'error')
            return render_template('auth/login.html', form=form)


        user = is_valid_login(correo, contraseña)

        if user:
            session['user'] = user.__dict__
            return redirect(url_for('inicio'))
        else:
            flash('Credenciales invalidas', 'error')

    return render_template('auth/login.html', form=form)

@app.route('/registro', methods=['GET', 'POST'])
def registrar():
    formulario = FormularioRegistro()
    print(formulario)

    if formulario.validate_on_submit():
        nombre_usuario = formulario.nombre_usuario.data
        correo = formulario.correo.data
        contraseña = formulario.contraseña.data

        # manejo de roles, quitar si no va utilizar
        id_rol = 2 

        if not is_valid_email(correo):
            flash('Ingrese un correo válido', 'error')
            return render_template('auth/registro.html', form=formulario)

        contraseña_hasheada = hashear_contraseña(contraseña)

        if registrar_usuario(nombre_usuario, correo, contraseña_hasheada, id_rol):
            flash('Registro exitoso. ¡Ahora puedes iniciar sesión!', 'success')
            return redirect(url_for('login'))
        
    return render_template('auth/registro.html', form=formulario)

@app.route('/inicio')
def inicio():
    return render_template('sitio/index.html')


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(port=3000)

