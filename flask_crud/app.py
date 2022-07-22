from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL



app = Flask(__name__)

#mysql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'flask_contacts'
mysql = MySQL(app)

#settings
app.secret_key ='mysecretkey'

#index
@app.route('/')
def index():    
    return render_template('index.html')

#boss_rrhh
@app.route('/boss')
def boss():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()    
    return render_template('boss.html', contacts = data)

#rrhh
@app.route('/rrhh')
def rrhh():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('rrhh.html', contacts = data)

#add contacts-formulario
@app.route('/add_contact' , methods=['POST'])
def add_contact():
    if request.method == 'POST':
        rut = request.form['rut']
        nombres = request.form['nombres']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']       
        sexo = request.form['sexo']
        correo = request.form['correo']
        telefono = request.form['telefono']
        fecha_ingreso = request.form['fecha_ingreso']
        estado = request.form['estado']           
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (rut,nombres,apellido_paterno,apellido_materno,sexo,correo,telefono,fecha_ingreso,estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',(rut,nombres,apellido_paterno,apellido_materno,sexo,correo,telefono,fecha_ingreso,estado))
        mysql.connection.commit()
        flash('Contacto agregado')
        return redirect(url_for('rrhh'))
    
#add contacts-render        
@app.route('/edit/<string:id>')
def get_contact(id):
    cur = mysql.connection.cursor()        
    cur.execute('SELECT * FROM contacts WHERE id = {0}'.format(id))
    data = cur.fetchall()    
    return render_template('edit-contact.html', contact = data[0])

#add contacts-edit 
@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        rut = request.form['rut']
        nombres = request.form['nombres']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']       
        sexo = request.form['sexo']
        correo = request.form['correo']
        telefono = request.form['telefono']
        fecha_ingreso = request.form['fecha_ingreso']
        estado = request.form['estado']    
        cur = mysql.connection.cursor()       
        cur.execute('update contacts set rut = %s, nombres = %s, apellido_paterno = %s, apellido_materno = %s, sexo = %s, correo = %s, telefono = %s, fecha_ingreso = %s, estado = %s where id = %s',(rut,nombres,apellido_paterno,apellido_materno,sexo,correo,telefono,fecha_ingreso,estado,id))                     
        mysql.connection.commit()
        flash('Contact updated')
        return redirect(url_for('rrhh'))
    
@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact removed')
    return redirect(url_for('rrhh'))

if __name__ == '__main__':
    app.run(port = 3000, debug=True)