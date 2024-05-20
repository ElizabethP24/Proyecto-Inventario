import mysql.connector
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename

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

# Configuración de la carpeta de subida
UPLOAD_FOLDER = 'ProyectoInventario/static/assets/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/categories')
def categories():
    # Llamar a la función que obtiene las categorias
    categorias = listar_categorias()
    # Renderizar la plantilla con los datos de las categorias
    return render_template('categories.html', categorias=categorias)

@app.route('/admin')
def admin():
    # Llamar a la función que obtiene los administradores
    administradores = listar_administradores()
    # Renderizar la plantilla con los datos de los administradores
    return render_template('admin.html', administradores=administradores)

@app.route('/client')
def client():
    # Llamar a la función que obtiene los clientes
    clientes= listar_clientes()
    # Renderizar la plantilla con los datos de los clientes
    return render_template('client.html', clientes=clientes)

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
    
    
@app.route('/guardar_categoria', methods=['POST'])
def guardar_categoria():
    # Obtener los datos del formulario
    nombre = request.form['NameCategory']
    descripcion = request.form['descriptionCategory']
        
    # Preparar la consulta de inserción
    consulta = "INSERT INTO categorias (nombrecat, descripcioncat) VALUES (%s, %s)"
    valores = (nombre, descripcion)
    
    try:
        # Crear un cursor y ejecutar la consulta
        cursor = conexion.cursor()
        cursor.execute(consulta, valores)
        conexion.commit()
        flash("Categoría agregado exitosamente", "success")
        # Cerrar el cursor
        cursor.close()
        return redirect(url_for('categories'))
    except mysql.connector.Error as error:
        print("Error al insertar categoria:", error)
        conexion.rollback()
        flash("Error al insertar categoria: {}".format(error), "error")
        return redirect(url_for('categories'))
    
@app.route('/guardar_administrador', methods=['POST'])
def guardar_administrador():
    # Obtener los datos del formulario
    documento = request.form['DNIAdmin']
    nombre = request.form['NameAdmin']
    telefono = request.form['phoneAdmin']
    correo = request.form['emailAdmin']
    usuario = request.form['UserNameAdmin']
    contrasena = request.form['passwordAdmin']
    avatar = request.form['avatarAdmin']
    
        
    # Preparar la consulta de inserción
    consulta = "INSERT INTO administradores (docadmin, nombreadmin, telefonoadmin, correoadmin, usuarioadmin, contrasenaadmin, avataradmin) VALUES (%s, %s,%s, %s,%s, %s,%s)"
    valores = (documento, nombre, telefono, correo, usuario, contrasena, avatar)
    
    try:
        # Crear un cursor y ejecutar la consulta
        cursor = conexion.cursor()
        cursor.execute(consulta, valores)
        conexion.commit()
        flash("Administrador agregado exitosamente", "success")
        # Cerrar el cursor
        cursor.close()
        return redirect(url_for('admin'))
    except mysql.connector.Error as error:
        print("Error al insertar administrador:", error)
        conexion.rollback()
        flash("Error al insertar administrador: {}".format(error), "error")
        return redirect(url_for('admin'))
    
@app.route('/guardar_cliente', methods=['POST'])
def guardar_cliente():
    # Obtener los datos del formulario
    dni = request.form['DNIClient']
    nombre = request.form['NameClient']
    direccion = request.form['addressClient']
    telefono = request.form['phoneClient']
    correo = request.form['emailClient']
        
    # Preparar la consulta de inserción
    consulta = "INSERT INTO clientes (doccliente,nombrecliente, direccioncliente,telefonocliente,correocliente ) VALUES (%s, %s, %s, %s, %s)"
    valores = (dni, nombre, direccion, telefono, correo)
    
    try:
        # Crear un cursor y ejecutar la consulta
        cursor = conexion.cursor()
        cursor.execute(consulta, valores)
        conexion.commit()
        flash("Cliente agregado exitosamente", "success")
        # Cerrar el cursor
        cursor.close()
        return redirect(url_for('client'))
    except mysql.connector.Error as error:
        print("Error al insertar cliente:", error)
        conexion.rollback()
        flash("Error al insertar cliente: {}".format(error), "error")
        return redirect(url_for('client'))
    
def ejecutar_consulta(consulta, valores):
    try:
        if not conexion.is_connected():
            conexion.connect()  # Reconnect if connection is closed
        cursor = conexion.cursor()
        cursor.execute(consulta, valores)
        conexion.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error:
        print("Error al ejecutar consulta:", error)
        conexion.rollback()
        return False
    
@app.route('/guardar_producto', methods=['POST'])
def guardar_producto():
    # Obtener los datos del formulario
    codigo = request.form['CodeProduct']
    nombre = request.form['NameProduct']
    unidades = request.form['StockProduct']
    precio = request.form['PriceProduct']
    categoria = request.form['CategoryProduct']
    proveedor = request.form['provider_id']
    descripcion = request.form['DescriptionProduct']
    marca = request.form['markProduct']
    fecha = request.form['dateProduct']
    estado = request.form['statusProduct']
    imagen = request.files['fileProduct']  # Obtener el objeto de archivo completo
        
    # Preparar la consulta de inserción
    consulta = "INSERT INTO productos (idproductos, nombreprod, unidadesprod, precioprod, categoriaprod, proveedorprod, descripcionprod, marcaprod, fecharegistro, estatusprod, imagenprod ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    valores = (codigo, nombre, unidades, precio, categoria, proveedor, descripcion, marca, fecha, estado, imagen.filename)  # Guardar solo el nombre del archivo en la base de datos
    
    try:
        if ejecutar_consulta(consulta, valores):
            # Pasar el archivo completo a la función upload_product()
            upload_product(imagen)
            flash("Producto agregado exitosamente", "success")
        else:
            flash("Error al insertar producto", "error")
    except Exception as e:
        print("Error:", e)
        flash("Error al insertar producto", "error")
    
    return redirect(url_for('products'))

def upload_product(file):
    if file.filename == '':
        flash('No se ha seleccionado ningún archivo')
        return redirect(url_for('products'))  
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Verificar si el directorio existe, y si no, crearlo
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        file.save(filepath)
        
        flash('Archivo subido exitosamente', 'success')
        return redirect(url_for('products'))
    else:
        flash('Tipo de archivo no permitido', 'error')
        return redirect(url_for('products'))
    
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

def listar_categorias():
    print("Entrando en la función listar_categorias()")
    categorias = []
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
        # Ejecutar una consulta para obtener todos las categorias
        cursor.execute("""
            SELECT nombrecat, descripcioncat
            FROM categorias
        """)

        # Obtener todos los registros las categorias
        categorias = cursor.fetchall()
        print("Categorias obtenidos:", categorias)  # Verificar los datos en la consola

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        categorias = []
    
    finally:
        # Cerrar el cursor y la conexión en la sección finally
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
    
    return categorias

def listar_administradores():
    print("Entrando en la función listar_administradores()")
    administradores = []
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
        # Ejecutar una consulta para obtener todos las categorias
        cursor.execute("""
            SELECT docadmin, nombreadmin, telefonoadmin, correoadmin, avataradmin
            FROM administradores
        """)

        # Obtener todos los registros las categorias
        administradores = cursor.fetchall()
        print("Administradores obtenidos:", administradores)  # Verificar los datos en la consola

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        administradores = []
    
    finally:
        # Cerrar el cursor y la conexión en la sección finally
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
    
    return administradores

def listar_clientes():
    print("Entrando en la función listar_clientes()")
    clientes = []
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
        # Ejecutar una consulta para obtener todos los clientes
        cursor.execute("""
            SELECT doccliente, nombrecliente, direccioncliente, telefonocliente, correocliente 
            FROM clientes
        """)

        # Obtener todos los registros de clientes
        proveedores = cursor.fetchall()
        print("Clientes obtenidos:", clientes)  # Verificar los datos en la consola

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        clientes = []
    
    finally:
        # Cerrar el cursor y la conexión en la sección finally
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
    
    return proveedores

@app.route('/validate_provider/<provider_id>', methods=['GET'])
def validate_provider(provider_id):
    exists = check_provider_exists(provider_id)
    return jsonify({'exists': exists})

def check_provider_exists(provider_id):
    # Conéctate a tu base de datos y realiza la consulta para verificar si el proveedor existe
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM proveedores WHERE docproveedores = %s", (provider_id,))
    result = cursor.fetchone()
    cursor.close()
    conexion.close()
    return result[0] > 0
    


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    # Ejecutar la aplicación Flask
    app.run(debug=True)
