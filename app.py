from utils import *
from flask import Flask , render_template, request, redirect , url_for

app = Flask(__name__)

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
                if (request.form['rol'] == 'E'):
                    return redirect(url_for('landingEstudiante'))
                elif (request.form['rol'] == 'P'):
                    return redirect(url_for('landingProfesor'))
                elif  (request.form['rol'] == 'A'):
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

@app.route('/profesor/actividad')
def gestionActividades_Profesor(): 
    return render_template('gestionActividades_profesor.html')

@app.route('/profesor/actividad/crear')
def crearActividad(): 
    return render_template('crearActividad.html')

@app.route('/profesor/actividad/consultar')
def consultarActividad(): 
    return render_template('consultarActividad.html')

@app.route('/profesor/actividad/actualizar')
def actualizarActividad(): 
    return render_template('actualizarActividad.html')

@app.route('/profesor/actividad/eliminar')
def eliminarActividad(): 
    return render_template('eliminarActividad.html')

@app.route('/profesor/nota/crear')
def crearNota(): 
    return render_template('crearNota.html')

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
    return render_template('asignaturas_Administrador.html')

@app.route('/administrador/actividad')
def gestionActividades_Admin(): 
    return render_template('gestionActividades_Admin.html')

@app.route('/administrador/actividad/crear')
def crearActividad_Admin(): 
    return render_template('crearActividad_Admin.html')

@app.route('/administrador/actividad/consultar')
def consultarActividad_Admin(): 
    return render_template('consultarActividadAdmin.html')

@app.route('/administrador/actividad/actualizar')
def actualizarActividad_Admin(): 
    return render_template('actualizarActividad_Admin.html')

@app.route('/administrador/actividad/eliminar')
def eliminarActividad_Admin(): 
    return render_template('eliminarActividad_Admin.html')

@app.route('/administrador/nota/crear')
def crearNota_Admin(): 
    return render_template('crearNota_Admin.html')

@app.route('/administrador/nota/consultar')
def consultarNota_Admin(): 
    return render_template('consultarNota_Admin.html')

@app.route('/control', methods=['GET', 'POST'])
def controlUsuarios(): 
    if request.method == "GET":
        return render_template('controlUsuarios.html')
    else:
        if request.form:
            codigo = request.form['codigo']
            nombre = request.form['nombre']
            apellido1 = request.form['apellido1']
            apellido2 = request.form['apellido2']
            usuario = request.form['usuario']
            contrasena = request.form['contrasena']
            
            errores = ""
            exito = ""
            if ((codigo != '') | (codigo == None )) & (len(codigo) <=1):
                errores += "Debe escribir un código válido. "
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
                exito = 'La cuenta ha sido registrada exitosamente'
                return redirect(url_for('landingAdministrador'))
            
            else:
                return render_template('controlUsuarios.html', error=errores)

