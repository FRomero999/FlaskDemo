# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, request
from flask_mysqldb import MySQL

# Cargando la aplicación Flask
app = Flask(__name__)

# Configuramos la base de datos
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pacoromero'
app.config['MYSQL_DB'] = 'ejemplo'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Montamos el controlador web y sus rutas

@app.route('/')
def hello():
    return render_template("helloworld.html")

# ------------------------------

@app.route('/<string:nombre>')
def saludar(nombre):
    return render_template("saludar.html",persona_a_saludar=nombre)

# ------------------------------

@app.route('/<int:id>')
def saludarId(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT nombre FROM alumnos WHERE id = %s",[id] )
    resultado = cur.fetchone()
    print(resultado)
    cur.close()
    # return render_template("saludar.html",persona_a_saludar=resultado['nombre'])
    return redirect('/'+resultado['nombre'])

# ------------------------------

@app.route('/todos')
def saludar_todos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM alumnos")
    resultado = cur.fetchall()
    print(resultado)
    cur.close()
    return render_template("saludar_varios.html",gente = resultado)

# ------------------------------

@app.route('/listado')
def listado():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM alumnos")
    resultado = cur.fetchall()
    print(resultado)
    cur.close()
    return render_template("listado.html",gente = resultado)

# ------------------------------

@app.route('/nuevo',methods=('GET', 'POST'))
def nuevo():
    if request.method == 'POST':

        print(request.form)

        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        curso = request.form['curso']
        edad = request.form['edad']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO alumnos (nombre, apellidos, edad, curso) VALUES (%s, %s, %s, %s)',
                         [nombre,apellidos,edad,curso])
        mysql.connection.commit()
        cur.close()
        return redirect('/listado')

    return render_template('nuevo.html')


# Ejecutamos la aplicación con el servidor web interno que incorpora
app.run()
