from utils import *
from flask import Flask , render_template, request, redirect , url_for
from flask import Flask, g
from flask import render_template
from flask import redirect
from flask import session
from flask import request
from flask import jsonify
from datetime import datetime, date
from flask.helpers import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, DateTimeField
from wtforms.validators import AnyOf, InputRequired, Length, Email, EqualTo, NumberRange
from wtforms.widgets import TextArea
import sqlite3
import hashlib
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = "gva\"Yf124.pi'iFb@j6Pn^:FpA*m`)"

def connection():
    con = sqlite3.connect("plataforma_notas.db")
    return con

def activate_foreign_keys_check(cur):
    pragma_statement = "PRAGMA foreign_keys = ON"
    cur.execute(pragma_statement)
    pragma_test = "PRAGMA foreign_keys"
    cur.execute(pragma_test)
    pragma = cur.fetchone()
    print(pragma) 
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('Login.html') 
    
    else:
        if request.form:
            errores = ""
            usuario = request.form['usuario']
            contrasena = request.form['contrasena']
            # if (not isUsernameValid(usuario)) | (not isPasswordValid(contrasena)) :
            if (not isUsernameValid(usuario)) :
                errores += "Su usuario no es válido. Por favor, verifique los datos ingresados \n" 
            if not isPasswordValid(contrasena):
                errores += "Debe ingresar una contraseña válida"
       
            if not errores: 
                if usuario == "jpaterninal":
                    con = connection()
                    cur = con.cursor()
                    login_statement = "SELECT *, roles.rol_name FROM tabla_usuarios as tu inner join roles on tu.rolel_code = roles.rol_code where tu.user_name=? and tu.password=?;"
                    cur.execute(login_statement, [usuario, contrasena])
                    usuario = cur.fetchall()
                    cur.close()
                    return redirect(url_for('landingAdministrador'))
                else:
                    if (request.form['rol'] == 'E'):
                        con = connection()
                        cur = con.cursor()
                        hash_func = hashlib.sha256()
                        encoded_pwd = contrasena.encode()
                        hash_func.update(encoded_pwd)
                        login_statement = "SELECT *  FROM tabla_usuarios as tu inner join roles on tu.rolel_code = roles.rol_code where tu.user_name=? and tu.password= ? and tu.rolel_code=?"
                        cur.execute(login_statement, [usuario, hash_func.hexdigest(), 3])
                        usuario = cur.fetchall()
                        cur.close()
                        return redirect(url_for('landingEstudiante'))
                    
                    elif (request.form['rol'] == 'P'):
                        con = connection()
                        cur = con.cursor()
                        hash_func = hashlib.sha256()
                        encoded_pwd = contrasena.encode()
                        hash_func.update(encoded_pwd)
                        login_statement = "SELECT * FROM tabla_usuarios as tu inner join roles on tu.rolel_code = roles.rol_code where tu.user_name=? and tu.password= ? and tu.rolel_code=?"
                        cur.execute(login_statement, [usuario, hash_func.hexdigest(), 2])
                        usuario = cur.fetchall()
                        cur.close()
                        return redirect(url_for('landingProfesor'))
                    elif  (request.form['rol'] == 'A'):
                        con = connection()
                        cur = con.cursor()
                        hash_func = hashlib.sha256()
                        encoded_pwd = contrasena.encode()
                        hash_func.update(encoded_pwd)
                        login_statement = "SELECT * FROM tabla_usuarios as tu inner join roles on tu.rolel_code = roles.rol_code where tu.user_name=? and tu.password= ? and tu.rolel_code=?"
                        cur.execute(login_statement, [usuario, hash_func.hexdigest(), 1])
                        usuario = cur.fetchall()
                        cur.close()
                        return redirect(url_for('landingAdministrador'))
            else:
                return render_template('Login.html', error=errores)
            # return render_template('Login.html')
            
@app.route('/estudiante')
def landingEstudiante(): 
    return render_template('landingEstudiante.html')

@app.route('/profesor')
def landingProfesor(): 
    return render_template('landingProfesor.html')

@app.route('/administrador')
def landingAdministrador(): 
    return render_template('landingAdministrador.html')  
  
@app.route('/estudiante/info')
def profileInformation_Estudiante(): 
    return render_template('profileInformation_Estudiante.html')

@app.route('/estudiante/asignaturas')
def asignaturas_Estudiante(): 
    return render_template('asignaturas_Estudiante.html')

@app.route('/estudiante/actividades')
def actividadesNotas(): 
    return render_template('actividadesNotas.html')

@app.route('/profesor/info')
def profileInformation_Profesor(): 
    return render_template('profileInformation_Profesor.html')

@app.route('/profesor/asignaturas')
def asignaturas_Profesor(): 
    return render_template('asignaturas_Profesor.html')

@app.route('/administrador/asignatura/consultar')
def buscarAsignatura_Admin(): 
    return render_template('buscarAsignatura_Admin.html')


@app.route('/administrador/asignatura/actualizar', methods=['GET', 'POST'])
def editarAsignatura_Admin(): 
    if request.method == "GET":
        return render_template('editarAsignatura_Admin.html')
    else:
        if request.form:
            subject_code = request.form['codigoAsignatura']
            subject_name = request.form['nombreAsignatura']
            user_code = request.form['codigoUsuario']
            codigo = 0
            if request.form['rol'] == 'E':
                codigo = 3
            elif request.form['rol'] == 'P':
                codigo = 2
            elif request.form['rol'] == 'A':
                codigo = 1
            errores = ""
            exito = ""
            if (subject_code == ''):
                errores = "Para editar una asignatura debe ingresar su código"
            if (subject_name == '') & (len(subject_name) <=1):
                errores += "Debe escribir un nombre válido de asignatura. "
            if (user_code == '') & (len(user_code) <=2):
                errores += "Debe escribir un nombre de usuario válido "
            if (codigo == 0):
                errores += "Debe seleccionar el rol del usuario relacionado con la asignatura"

            if not errores:
                con = connection()
                cur = con.cursor()
                update_statement = "UPDATE tabla_asignaturas SET subject_name = ? , user_code = ? , role_code = ? WHERE subject_code = ? "
                cur.execute(update_statement, [subject_name, user_code, codigo, subject_code])
                cur.close()
                con.commit()
                exito = 'La asignatura ha sido editada exitosamente'
                return render_template('editarAsignatura_Admin.html', error=exito)
            
            else:
                return render_template('editarAsignatura_Admin.html', error=errores)

@app.route('/administrador/asignatura/eliminar' , methods=['GET', 'POST','PUT' ,'DELETE'])
def eliminarAsignatura_Admin(): 
    if request.method == "GET":
        return render_template('eliminarAsignatura_Admin.html')
    else:
        if request.method == 'DELETE':
            user_code = request.form['codigoUsuario']
            # codigo = codigo
            subject_code = request.form['codigoAsignatura']
            errores = ""
            exito = ""
            if (subject_code == '') & (user_code== ''):
                errores += "Debe ingresar al menos uno de los dos campos "
            if not errores:
                con = connection()
                cur = con.cursor()
                delete_statement = "DELETE FROM tabla_asignaturas WHERE ((user_code = ?) or (subject_code = ?) )"
                cur.execute(delete_statement, [user_code , subject_code])
                cur.close()
                con.commit()
                exito += 'La asignación de asignatura ha sido eliminada'
                return render_template('eliminarAsignatura_Admin.html', error=exito)
            else: 
                errores+= "Los campos ingresados no se encuentran en la base de datos"
                return render_template('eliminarAsignatura_Admin.html', error=errores)           

@app.route('/administrador/asignatura/crear', methods=['GET', 'POST'])
def crearAsignatura_Admin(): 
    if request.method == "GET":
        return render_template('crearAsignatura_Admin.html')
    else:
        if request.form:
            subject_name = request.form['nombreAsignatura']
            user_code = request.form['codigoUsuario']
            codigo = 0 
            if request.form['rol'] == 'E':
                codigo = 3
            elif request.form['rol'] == 'P':
                codigo = 2
            elif request.form['rol'] == 'A':
                codigo = 1
            errores = ""
            exito = ""
            if (subject_name == '') & (len(subject_name) <=1):
                errores += "Debe escribir un nombre de asignatura válido. "
            if (user_code == '') & (len(user_code) <=2):
                errores += "Debe escribir un código de usuario válido, para realizar la asignación"
            if (codigo == 0) :
                errores += "Debe ingresar el rol del usuario en la asignatura"
                
            if not errores:
                con = connection()
                cur = con.cursor()
                create_statement = "INSERT INTO tabla_asignaturas (subject_name , user_code, role_code) VALUES (? , ? , ?)"
                cur.execute(create_statement, [subject_name,  user_code, codigo ])
                cur.close()
                con.commit()
                exito = 'La asignatura se ha registrado exitosamente'
                return render_template('crearAsignatura_Admin.html', error=exito)            
            else:
                return render_template('crearAsignatura_Admin.html', error=errores)


@app.route('/profesor/actividad')
def gestionActividades_Profesor(): 
    return render_template('gestionActividades_profesor.html')

@app.route('/profesor/actividad/crear' , methods=['GET', 'POST'])
def crearActividad(): 
    if request.method == "GET":
        return render_template('crearActividad.html')
    else:
        if request.form:
            activity_name = request.form['nombreActividad']
            subject_code = request.form['codigoAsignatura']
            activity_description = request.form['descripcionActividad']
            errores = ""
            exito = ""
            if (activity_name == '') & (len(activity_name) <=1):
                errores += "Debe escribir un nombre de actividad válido. "
            if (subject_code == '') & (len(subject_code) <=2):
                errores += "Debe escribir un código de asignatura válido"
            if (activity_description == 0) :
                errores += "Debe ingresar el rol del usuario en la asignatura"
                
            if not errores:
                con = connection()
                cur = con.cursor()
                create_statement = "INSERT INTO tabla_actividades (activity_name , subject_code, activity_desc) VALUES (? , ? , ?)"
                cur.execute(create_statement, [activity_name,  subject_code, activity_description ])
                cur.close()
                con.commit()
                exito = 'La actividad se ha registrado exitosamente'
                return render_template('crearActividad.html', error=exito)            
            else:
                return render_template('crearActividad.html', error=errores)

@app.route('/profesor/actividad/consultar')
def consultarActividad(): 
    return render_template('consultarActividad.html')

@app.route('/profesor/actividad/actualizar' , methods=['GET', 'POST'])
def actualizarActividad(): 
    if request.method == "GET":
            return render_template('actualizarActividad.html')
    else:
        if request.form:
            subject_code = request.form['codigoAsignatura']
            activity_code = request.form['codigoActividad']
            activity_name = request.form['nombreActividad']
            activity_description = request.form['descripcionActividad']
    
            if (subject_code == ''):
                errores = "Para editar actividad debe ingresar el código de la asignatura a la que pertenece"
            if (activity_code == ''):
                errores += "Debe escribir un código válido de actividad "
            if (activity_name == '') & (len(activity_name) <=2):
                errores += "Debe escribir un nombre de actividad válido "
            if (activity_description == ''):
                errores += "Debe escribir la descripción de actividad"

            if not errores:
                con = connection()
                cur = con.cursor()
                update_statement = "UPDATE tabla_actividades SET activity_name = ? , activity_description = ? WHERE subject_code = ? AND activity_code = ? "
                cur.execute(update_statement, [activity_name, activity_description, subject_code, activity_code])
                cur.close()
                con.commit()
                exito = 'La actividad ha sido editada exitosamente'
                return render_template('actualizarActividad.html', error=exito)
            
            else:
                return render_template('actualizarActividad.html', error=errores)

@app.route('/profesor/actividad/eliminar' , methods=['GET', 'POST'])
def eliminarActividad(): 
    if request.method == "GET":
            return render_template('eliminarActividad.html')
    else:
        if request.method == 'DELETE':
            subject_code = request.form['codigoAsignatura']
            activity_code = request.form['codigoActividad']
            errores = ""
            exito = ""
            if (subject_code == '') | (activity_code== ''):
                errores += "Debe llenar todos los campos "
            if not errores:

                con = connection()
                cur = con.cursor()
                delete_statement = "DELETE FROM tabla_actividades WHERE ((subject_code = ?) and (activity_code = ?) )"

                cur.execute(delete_statement, [subject_code , activity_code])
                cur.close()
                con.commit()
                exito += 'La actividad ha sido eliminada exitosamente'
                return render_template('eliminarActividad.html', error=exito)
            else: 
                errores+= "Los campos ingresados no se encuentran en la base de datos"
                return render_template('eliminarActividad.html', error=errores)

@app.route('/profesor/nota/crear' , methods=['GET', 'POST'])
def crearNota(): 
    if request.method == "GET":
            return render_template('crearNota.html')
    else:
        if request.form:
            subject_code = request.form['codigoAsignatura']
            activity_code = request.form['codigoActividad']
            student_code = request.form['codigoEstudiante']
            grade = request.form['notaEstudiante']
            errores = ""
            exito = ""
            if (subject_code == ''):
                errores += "Debe escribir un código de asignatura válido. "
            if (activity_code == '') :
                errores += "Debe escribir un código de actividad"
            if (student_code == '') :
                errores += "Debe ingresar código de estudiante al cual se le asignará la nota"
            if (grade == '') :
                errores += "Debe ingresar una nota válida"  
            if not errores:
                con = connection()
                cur = con.cursor()
                create_statement = "INSERT INTO tabla_notas (subject_code , activity_code, user_code, grade) VALUES (? , ? , ?, ?)"
                cur.execute(create_statement, [subject_code,  activity_code, student_code , grade])
                cur.close()
                con.commit()
                exito = 'La nota de la actividad se ha registrado exitosamente'
                return render_template('crearNota.html', error=exito)            
            else:
                return render_template('crearNota.html', error=errores)

@app.route('/profesor/nota/consultar')
def consultarNota(): 
    return render_template('consultarNota.html')

@app.route('/profesor/nota/actualizar')
def actualizarNota(): 
    return render_template('actualizarNota.html')


@app.route('/administrador/info')
def profileInformation_Admin(): 
    return render_template('profileInformation_Admin.html')

@app.route('/administrador/asignaturas')
def asignaturas_Administrador(): 
    return render_template('gestionAsignaturas_Admin.html')

@app.route('/administrador/actividad')
def gestionActividades_Admin(): 
    return render_template('gestionActividades_Admin.html')

@app.route('/administrador/actividad/crear' , methods=['GET', 'POST'])
def crearActividad_Admin(): 
    if request.method == "GET":
        return render_template('crearActividad_Admin.html')
    else:
        if request.form:
            activity_name = request.form['nombreActividad']
            subject_code = request.form['codigoAsignatura']
            activity_description = request.form['descripcionActividad']
            errores = ""
            exito = ""
            if (activity_name == '') & (len(activity_name) <=1):
                errores += "Debe escribir un nombre de actividad válido. "
            if (subject_code == '') & (len(subject_code) <=2):
                errores += "Debe escribir un código de asignatura válido"
            if (activity_description == 0) :
                errores += "Debe ingresar el rol del usuario en la asignatura"
                
            if not errores:
                con = connection()
                cur = con.cursor()
                create_statement = "INSERT INTO tabla_actividades (activity_name , subject_code, activity_description) VALUES (? , ? , ?)"
                cur.execute(create_statement, [activity_name,  subject_code, activity_description ])
                cur.close()
                con.commit()
                exito = 'La actividad se ha registrado exitosamente'
                return render_template('crearActividad_Admin.html', error=exito)            
            else:
                return render_template('crearActividad_Admin.html', error=errores)

@app.route('/administrador/actividad/consultar' )
def consultarActividad_Admin(): 
    return render_template('consultarActividadAdmin.html')

@app.route('/administrador/actividad/actualizar' , methods=['GET', 'POST'])
def actualizarActividad_Admin(): 
    if request.method == "GET":
            return render_template('actualizarActividad_Admin.html')
    else:
        if request.form:
            subject_code = request.form['codigoAsignatura']
            activity_code = request.form['codigoActividad']
            activity_name = request.form['nombreActividad']
            activity_description = request.form['descripcionActividad']
    
            if (subject_code == ''):
                errores = "Para editar actividad debe ingresar el código de la asignatura a la que pertenece"
            if (activity_code == ''):
                errores += "Debe escribir un código válido de actividad "
            if (activity_name == '') & (len(activity_name) <=2):
                errores += "Debe escribir un nombre de actividad válido "
            if (activity_description == ''):
                errores += "Debe escribir la descripción de actividad"

            if not errores:
                con = connection()
                cur = con.cursor()
                update_statement = "UPDATE tabla_actividades SET activity_name = ? , activity_description = ? WHERE subject_code = ? AND activity_code = ? "
                cur.execute(update_statement, [activity_name, activity_description, subject_code, activity_code])
                cur.close()
                con.commit()
                exito = 'La actividad ha sido editada exitosamente'
                return render_template('actualizarActividad_Admin.html', error=exito)
            
            else:
                return render_template('actualizarActividad_Admin.html', error=errores)

@app.route('/administrador/actividad/eliminar' , methods=['GET', 'POST'])
def eliminarActividad_Admin(): 
    if request.method == "GET":
            return render_template('eliminarActividad_Admin.html')
    else:
        if request.method == 'DELETE':
            subject_code = request.form['codigoAsignatura']
            activity_code = request.form['codigoActividad']
            errores = ""
            exito = ""
            if (subject_code == '') | (activity_code== ''):
                errores += "Debe llenar todos los campos "
            if not errores:

                con = connection()
                cur = con.cursor()
                delete_statement = "DELETE FROM tabla_actividades WHERE ((subject_code = ?) and (activity_code = ?) )"

                cur.execute(delete_statement, [subject_code , activity_code])
                cur.close()
                con.commit()
                exito += 'La actividad ha sido eliminada exitosamente'
                return render_template('eliminarActividad_Admin.html', error=exito)
            else: 
                errores+= "Los campos ingresados no se encuentran en la base de datos"
                return render_template('eliminarActividad_Admin.html', error=errores)
            

@app.route('/administrador/nota/crear' , methods=['GET', 'POST'])
def crearNota_Admin(): 
    if request.method == "GET":
            return render_template('crearNota_Admin.html')
    else:
        if request.form:
            subject_code = request.form['codigoAsignatura']
            activity_code = request.form['codigoActividad']
            student_code = request.form['codigoEstudiante']
            grade = request.form['notaEstudiante']
            errores = ""
            exito = ""
            if (subject_code == ''):
                errores += "Debe escribir un código de asignatura válido. "
            if (activity_code == '') :
                errores += "Debe escribir un código de actividad"
            if (student_code == '') :
                errores += "Debe ingresar código de estudiante al cual se le asignará la nota"
            if (grade == '') :
                errores += "Debe ingresar una nota válida"  
            if not errores:
                con = connection()
                cur = con.cursor()
                create_statement = "INSERT INTO tabla_notas (subject_code , activity_code, user_code, grade) VALUES (? , ? , ?, ?)"
                cur.execute(create_statement, [subject_code,  activity_code, student_code , grade])
                cur.close()
                con.commit()
                exito = 'La nota de la actividad se ha registrado exitosamente'
                return render_template('crearNota_Admin.html', error=exito)            
            else:
                return render_template('crearNota_Admin.html', error=errores)

@app.route('/administrador/nota/consultar')
def consultarNota_Admin(): 
    return render_template('consultarNota_Admin.html')

@app.route('/administrador/nota/actualizar')
def actualizarNota_Admin(): 
    return render_template('actualizarNota_Admin.html')


@app.route('/administrador/controles')
def gestionUsuarios_Admin(): 
    return render_template('gestionUsuarios_Admin.html')

@app.route('/administrador/usuarios/consultar')
def buscarUsuarios_Admin(): 
    return render_template('buscarUsuarios_Admin.html')

@app.route('/administrador/usuarios/actualizar', methods=['GET', 'POST'])
def editarUsuarios_Admin(): 
    if request.method == "GET":
        return render_template('editarUsuarios_Admin.html')
    else:
        if request.form:
            user_code = request.form['codigo']
            nombre = request.form['nombre']
            apellido1 = request.form['apellido1']
            apellido2 = request.form['apellido2']
            usuario = request.form['usuario']
            if request.form['rol'] == 'E':
                codigo = 3
            elif request.form['rol'] == 'P':
                codigo = 2
            elif request.form['rol'] == 'A':
                codigo = 1
            errores = ""
            exito = ""
            if (user_code == ''):
                errores = "Para editar un usuario debe ingresar su código"
            if (nombre == '') & (len(nombre) <=1):
                errores += "Debe escribir un nombre válido. "
            if (apellido1 == '') & (len(apellido1) <=2):
                errores += "Debe escribir un apellido válido. "
            if (apellido2 == '') & (len(apellido2) <=2):
                errores += "Debe escribir un apellido válido. "
            if (usuario == '') & (not isUsernameValid(usuario)):
                errores += "Debe escribir un nombre de usuario válido. "

            
            if not errores:
                con = connection()
                cur = con.cursor()
                update_statement = "UPDATE tabla_usuarios SET name = ? , user_name = ? , last_name = ?,  last_name_2 = ? , rolel_code = ? WHERE user_code = ? "
                cur.execute(update_statement, [nombre, usuario, apellido1, apellido2, codigo, user_code ])
                cur.close()
                con.commit()
                exito = 'El usuario ha sido editado exitosamente'
                return render_template('editarUsuarios_Admin.html', error=exito)
            
            else:
                return render_template('editarUsuarios_Admin.html', error=errores)

@app.route('/administrador/usuarios/eliminar' , methods=['GET', 'POST','PUT' ,'DELETE'])
def eliminarUsuarios_Admin(): 
    if request.method == "GET":
        return render_template('eliminarUsuarios_Admin.html')
    else:
        if request.method == 'DELETE':
            user_code = request.form['codigo']
            # codigo = codigo
            usuario = request.form['usuario']
            errores = ""
            exito = ""
            if (usuario == '') & (user_code== ''):
                errores += "Debe ingresar al menos uno de los dos campos "
            if not errores:

                con = connection()
                cur = con.cursor()
                delete_statement = "DELETE FROM tabla_usuarios WHERE ((user_code = ?) or (user_name = ?) )"

                cur.execute(delete_statement, [user_code , usuario])
                cur.close()
                con.commit()
                exito += 'El usuario ha sido eliminado exitosamente'
                return render_template('eliminarUsuarios_Admin.html', error=exito)
            else: 
                errores+= "Los campos ingresados no se encuentran en la base de datos"
                return render_template('eliminarUsuarios_Admin.html', error=errores)
            
            

@app.route('/administrador/usuarios/crear', methods=['GET', 'POST'])
def crearUsuarios_Admin(): 
    if request.method == "GET":
        return render_template('crearUsuarios_Admin.html')
    else:
        if request.form:
            nombre = request.form['nombre']
            apellido1 = request.form['apellido1']
            apellido2 = request.form['apellido2']
            usuario = request.form['usuario']
            contrasena = request.form['contrasena']
            if request.form['rol'] == 'E':
                codigo = 3
            elif request.form['rol'] == 'P':
                codigo = 2
            elif request.form['rol'] == 'A':
                codigo = 1
            elif request.form['rol'] == '':
                codigo = ''
            errores = ""
            exito = ""
            if (nombre != '') & (len(nombre) <=1):
                errores += "Debe escribir un nombre válido. "
            if (apellido1 != '') & (len(apellido1) <=2):
                errores += "Debe escribir un apellido válido. "
            if (apellido2 != '') & (len(apellido2) <=2):
                errores += "Debe escribir un apellido válido. "
            if (usuario != '') & (not isUsernameValid(usuario)):
                errores += "Debe escribir un nombre de usuario válido. "
            if (contrasena != '') & (not isPasswordValid(contrasena)):
                errores += "Contraseña no cumple con los requisitos de seguridad. "
            
            if not errores:
                con = connection()
                cur = con.cursor()
                hash_func = hashlib.sha256()
                encoded_pwd = contrasena.encode()
                hash_func.update(encoded_pwd)
                create_statement = "INSERT INTO tabla_usuarios (user_name , password, name, last_name, last_name_2, rolel_code) VALUES (? , ? , ? , ?, ? ,?)"
                cur.execute(create_statement, [usuario, hash_func.hexdigest(), nombre, apellido1, apellido2, codigo ])
                cur.close()
                con.commit()
                exito = 'El usuario se ha registrado exitosamente'
                return render_template('crearUsuarios_Admin.html', error=exito)
            
            else:
                return render_template('crearUsuarios_Admin.html', error=errores)

