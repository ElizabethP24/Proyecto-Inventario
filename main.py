import mysql.connector
import os
from flask import Flask, render_template, request, redirect, url_for, flash

# Crear la aplicación Flask y configurar la carpeta estática
app = Flask(__name__, 
            static_folder='C:\\Users\\Eli\\Downloads\\ProyectoInventario\\static', 
            static_url_path='/static')

# Genera una clave secreta aleatoria
app.secret_key = os.urandom(24)

# Establecer la conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="huella_amor"
)

# Definir una ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Definir la ruta para el proceso de inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    # Obtener los datos del formulario
    username = request.form['username']
    password = request.form['password']

    # Realizar la consulta a la base de datos para verificar las credenciales
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM administradores WHERE usuarioadmin = %s AND contrasenaadmin = %s", (username, password))
    usuario = cursor.fetchone()
    cursor.close()

    # Verificar si se encontró un usuario con las credenciales proporcionadas
    if usuario:
        # Si las credenciales son válidas, redirigir al usuario a la página home.html
        return redirect(url_for('home'))
    else:
        # Si las credenciales no son válidas, mostrar un mensaje de error
        flash("Usuario o contraseña incorrectos. Inténtalo de nuevo.", "error")
        return redirect(url_for('index'))

# Definir la ruta para la página home.html
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/categories')
def categories():
    return render_template('categories.html')
@app.route('/client')
def client():
    return render_template('client.html')
@app.route('/inventory')
def inventory():
    return render_template('inventory.html')
@app.route('/products')
def products():
    return render_template('products.html')
@app.route('/providers')
def providers():
    # Llamar a la función que obtiene los proveedores
    proveedores = listar_proveedores()
    # Renderizar la plantilla con los datos de los proveedores
    return render_template('providers.html', proveedores=proveedores)

@app.route('/sales')
def sales():
    return render_template('sales.html')
@app.route('/guardar_proveedor', methods=['POST'])
def guardar_proveedor():
    # Obtener los datos del formulario
    dni = request.form['DNIProvider']
    nombre = request.form['NameProvider']
    direccion = request.form['addressProvider']
    telefono = request.form['phoneProvider']
    correo = request.form['emailProvider']
    categoria = request.form['webProvider']
    
    # Preparar la consulta de inserción
    consulta = "INSERT INTO proveedores (docproveedores, nombreprov, direccionprov, telefonoprov, correoprov, categoriaprod) VALUES (%s, %s, %s, %s, %s, %s)"
    valores = (dni, nombre, direccion, telefono, correo, categoria)
    
    try:
        # Crear un cursor y ejecutar la consulta
        cursor = conexion.cursor()
        cursor.execute(consulta, valores)
        conexion.commit()
        flash("Proveedor agregado exitosamente", "success")
        # Cerrar el cursor
        cursor.close()
        return redirect(url_for('providers'))
    except mysql.connector.Error as error:
        print("Error al insertar proveedor:", error)
        conexion.rollback()
        flash("Error al insertar proveedor: {}".format(error), "error")
        return redirect(url_for('providers'))
    
    
def listar_proveedores():
    print("Entrando en la función listar_proveedores()")
    proveedores = []
    try:
        # Establecer la conexión a la base de datos
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="huella_amor"
        )
        print("Conexión establecida correctamente")
        # Crear un cursor para ejecutar consultas SQL
        cursor = conexion.cursor()

        print("Ejecutando consulta SQL")
        # Ejecutar una consulta para obtener todos los proveedores
        cursor.execute("""
            SELECT docproveedores, nombreprov, direccionprov, telefonoprov, correoprov, categoriaprod 
            FROM proveedores
        """)

        # Obtener todos los registros de proveedores
        proveedores = cursor.fetchall()
        print("Proveedores obtenidos:", proveedores)  # Verificar los datos en la consola

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        proveedores = []
    
    finally:
        # Cerrar el cursor y la conexión en la sección finally
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
    
    return proveedores

if __name__ == '__main__':
    # Ejecutar la aplicación Flask
    app.run(debug=True)
