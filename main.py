import mysql.connector
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image 
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from graphviz import Digraph
from datetime import date, datetime
import json

# Crear la aplicación Flask y configurar la carpeta estática
app = Flask(__name__, 
            static_folder='D:\\ELIZA\SISTEMAS\\INGENIERIA\\SEMESTRE II\\ESTRUCT DATOS APLICADA\\ProyectoInventario\\static', 
            static_url_path='/static')


@app.route('/arbol.json')
def get_arbol_json():
    return send_from_directory('D:\\ELIZA\\SISTEMAS\\INGENIERIA\\SEMESTRE II\\ESTRUCT DATOS APLICADA\\ProyectoInventario', 'arbol.json') 

# Genera una clave secreta aleatoria
app.secret_key = os.urandom(24)

# Establecer la conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="huella_amor"
)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'D:\\ELIZA\SISTEMAS\\INGENIERIA\\SEMESTRE II\\ESTRUCT DATOS APLICADA\\ProyectoInventario\\static\\assets\\img'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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
    
    # Establecer la conexión a la base de datos
    conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="huella_amor"
)
    try:
        cursor = conexion.cursor()
        tables = ['administradores', 'categorias', 'clientes', 'proveedores', 'categorias', 'productos', 'ventas']
        counts = {}

        for table in tables:
            query = f"SELECT COUNT(*) FROM {table}"
            cursor.execute(query)
            counts[table] = cursor.fetchone()[0]

        cursor.close()
        conexion.close()

        return render_template('home.html', counts=counts)
    except Exception as e:
        print(f"Error al obtener los registros: {e}")
        return render_template('home.html', counts={})
    

@app.route('/inventory')
def inventory():
    # Llamar a la función que obtiene el inventario
    inventario = listar_inventario()
    # Renderizar la plantilla con los datos del inventario
    return render_template('inventory.html', inventario=inventario)

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

@app.route('/products')
def products():
    # Llamar a la función que obtiene los productos
    productos = listar_productos()
    # Renderizar la plantilla con los datos de los productos
    return render_template('products.html', productos=productos)

@app.route('/client')
def client():
    # Llamar a la función que obtiene los clientes
    clientes= listar_clientes()
    # Renderizar la plantilla con los datos de los clientes
    return render_template('client.html', clientes=clientes)

@app.route('/sales')
def sales():
    # Llamar a la función que obtiene las ventas
    ventas= listar_ventas()
    # Renderizar la plantilla con los datos de las ventas
    return render_template('sales.html', ventas=ventas)

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
        # Actualizar el árbol
        construir_y_guardar_arbol()
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
        # Actualizar el árbol
        construir_y_guardar_arbol()
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
        
        # Verificar si los cambios se han guardado correctamente
        cursor.execute("SELECT * FROM administradores WHERE docadmin = %s", (documento,))
        administrador = cursor.fetchone()
        if administrador:
            print("Administrador agregado correctamente a la base de datos.")

        flash("Administrador agregado exitosamente", "success")
        # Cerrar el cursor
        cursor.close()
        
        # Actualizar el árbol
        construir_y_guardar_arbol()
        print("Árbol reconstruido y guardado después de agregar administrador.")
        
        return redirect(url_for('admin'))
    except mysql.connector.Error as error:
        print("Error al insertar administrador:", error)
        conexion.rollback()
        flash("Error al insertar administrador: {}".format(error), "error")
        return redirect(url_for('admin'))@app.route('/guardar_cliente', methods=['POST'])
    
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
        # Actualizar el árbol
        construir_y_guardar_arbol()
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
    
    
@app.route('/obtener_producto/<codigo>', methods=['GET'])
def obtener_producto(codigo):
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT nombreprod, precioprod, unidadesprod, categoria FROM productos WHERE idproductos = %s", (codigo,))
        producto = cursor.fetchone()
        cursor.close()
        
        # Imprimir el resultado para diagnosticar
        print(producto)
        
        if producto:
            # Manejar el caso donde 'categoria' podría no estar presente
            categoria = producto.get('categoria', 'Categoría no especificada')
            return jsonify({
                "nombre": producto['nombreprod'],
                "precio": producto['precioprod'],
                "unidades": producto['unidadesprod'],
                "categoria": categoria
            }), 200
        else:
            return jsonify({"error": "Producto no encontrado"}), 404
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500


@app.route('/obtener_cliente/<dni>', methods=['GET'])
def obtener_cliente(dni):
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT nombrecliente FROM clientes WHERE doccliente = %s", (dni,))
        cliente = cursor.fetchone()
        cursor.close()
        if cliente:
            return jsonify({"nombre": cliente['nombrecliente']}), 200
        else:
            return jsonify({"error": "Cliente no encontrado"}), 404
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500


@app.route('/guardar_venta', methods=['POST'])
def guardar_venta():
    # Obtener los datos del formulario
    fecha = request.form.get('dateSales', '')
    codigoprod = request.form.get('CodeProduct', '')
    nombreprod = request.form.get('NameProduct', '')
    cantidad = request.form.get('StockProduct', '')
    precio = request.form.get('PriceProduct', '')
    dni = request.form.get('DNIClient', '')
    nombre = request.form.get('NameClient', '')
    pago = request.form.get('Pay', '')

    # Validación de datos
    if not (fecha and codigoprod and nombreprod and cantidad and precio and dni and nombre and pago):
        flash("Por favor, complete todos los campos del formulario.", "error")
        return redirect(url_for('sales'))

    try:
        cantidad = int(cantidad)
        precio = float(precio)
    except ValueError:
        flash("Unidades y Precio deben ser números válidos.", "error")
        return redirect(url_for('sales'))

    # Calcular el total
    total = cantidad * precio

    try:
        # Conectar a la base de datos
        if not conexion.is_connected():
            conexion.connect()

        cursor = conexion.cursor()

        # Obtener la cantidad actual del producto y la categoría
        cursor.execute("SELECT unidadesprod, categoriaprod FROM productos WHERE idproductos = %s", (codigoprod,))
        producto = cursor.fetchone()

        if producto:
            unidades_disponibles = int(producto[0])
            categoria = producto[1]  # Obtiene la categoría del producto

            if unidades_disponibles >= cantidad:
                # Calcular la nueva cantidad
                nueva_cantidad = unidades_disponibles - cantidad

                # Actualizar la cantidad del producto en la base de datos
                cursor.execute("UPDATE productos SET unidadesprod = %s WHERE idproductos = %s", (nueva_cantidad, codigoprod))

                # Preparar la consulta de inserción para la venta
                consulta_venta = """
                INSERT INTO ventas (fecharegistro, idprod, productovent, unidadesvent, preciovent, categoria, doccliente, nombrecliente, mediopago, totalvent)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores_venta = (fecha, codigoprod, nombreprod, cantidad, precio, categoria, dni, nombre, pago, total)
                cursor.execute(consulta_venta, valores_venta)

                # Confirmar los cambios
                conexion.commit()

                flash("Venta agregada exitosamente", "success")
                # Actualizar el árbol
                construir_y_guardar_arbol()
            else:
                flash("No hay suficiente stock disponible", "error")
        else:
            flash("Producto no encontrado", "error")

        cursor.close()
        conexion.close()
        return redirect(url_for('sales'))

    except mysql.connector.Error as error:
        print("Error al insertar venta:", error)
        conexion.rollback()
        flash("Error al insertar venta: {}".format(error), "error")
        return redirect(url_for('sales'))



    
@app.route('/guardar_producto', methods=['POST'])
def guardar_producto():
    try:
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
        imagen = request.files['fileProduct']
        
        consulta = "INSERT INTO productos (idproductos, nombreprod, unidadesprod, precioprod, categoria, proveedorprod, descripcionprod, marcaprod, fecharegistro, estatusprod, imagenprod) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (codigo, nombre, unidades, precio, categoria, proveedor, descripcion, marca, fecha, estado, imagen.filename)
        
        if ejecutar_consulta(consulta, valores):
            if upload_product(imagen):
                flash("Producto agregado exitosamente", "success")
                # Actualizar el árbol
                construir_y_guardar_arbol()
            else:
                flash("Error al subir la imagen del producto", "error")
        else:
            flash("Error al insertar producto en la base de datos", "error") 
    except Exception as e:
        print("Error:", e)
        flash(f"Error al insertar producto: {e}", "error")
    
    return redirect(url_for('products'))


def upload_product(file):
    if file.filename == '':
        flash('No se ha seleccionado ningún archivo', 'error')
        return False
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            try:
                os.makedirs(app.config['UPLOAD_FOLDER'])
            except Exception as e:
                flash(f'Error al crear el directorio: {e}', 'error')
                return False
        
        try:
            file.save(filepath)
            # Verificar si el archivo guardado es una imagen válida
            try:
                with Image.open(filepath) as img:
                    img.verify()  # Verifica que el archivo es una imagen válida
                flash('Archivo subido exitosamente', 'success')
                return True
            except (IOError, SyntaxError) as e:
                flash(f'El archivo subido no es una imagen válida: {e}', 'error')
                os.remove(filepath)  # Eliminar el archivo no válido
                return False
        except Exception as e:
            flash(f'Error al guardar el archivo: {e}', 'error')
            return False
    else:
        flash('Tipo de archivo no permitido', 'error')
        return False

    
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
            SELECT docproveedores, nombreprov, direccionprov, telefonoprov, correoprov, categoria
            FROM proveedores
        """)

        # Obtener todos los registros de proveedores
        proveedores = cursor.fetchall()
        print("Proveedores obtenidos:", proveedores)  # Verificar los datos en la consola
        # Actualizar el árbol
        construir_y_guardar_arbol()

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
            SELECT idcategorias,nombrecat, descripcioncat
            FROM categorias
        """)

        # Obtener todos los registros las categorias
        categorias = cursor.fetchall()
        print("Categorias obtenidos:", categorias)  # Verificar los datos en la consola
        # Actualizar el árbol
        construir_y_guardar_arbol()

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
        # Actualizar el árbol
        construir_y_guardar_arbol()
        print("Árbol reconstruido y guardado después de actualizar administrador.")

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
        # Actualizar el árbol
        construir_y_guardar_arbol()

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

def listar_productos():
    print("Entrando en la función listar_productos)")
    productos = []
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
        # Ejecutar una consulta para obtener todos los productops
        cursor.execute("""
            SELECT idproductos, nombreprod, unidadesprod, precioprod, categoria, proveedorprod, descripcionprod, marcaprod, fecharegistro, estatusprod, imagenprod 
            FROM productos
        """)

        # Obtener todos los registros de productos
        productos = cursor.fetchall()
        print("Productos obtenidos:", productos)  # Verificar los datos en la consola
        # Actualizar el árbol
        construir_y_guardar_arbol()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        productos = []
    
    finally:
        # Cerrar el cursor y la conexión en la sección finally
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
    
    return productos

def listar_ventas():
    print("Entrando en la función listar_ventas()")
    ventas = []
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
        # Ejecutar una consulta para obtener todos los ventas
        cursor.execute("""
            SELECT idventas, fecharegistro,idprod, productovent, unidadesvent, preciovent, doccliente, nombrecliente,mediopago,categoria, totalvent 
            FROM ventas
        """)

        # Obtener todos los registros de ventas
        ventas = cursor.fetchall()
        print("Ventas obtenidos:",ventas)  # Verificar los datos en la consola
        # Actualizar el árbol
        construir_y_guardar_arbol()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        ventas = []
    
    finally:
        # Cerrar el cursor y la conexión en la sección finally
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
    
    return ventas

def listar_inventario():
    print("Entrando en la función listar_inventary)")
    inventario = []
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
        # Ejecutar una consulta para obtener todos los productops
        cursor.execute("""
            SELECT idproductos, nombreprod, unidadesprod, precioprod, categoria, proveedorprod, descripcionprod, marcaprod, fecharegistro, estatusprod, imagenprod 
            FROM productos
        """)

        # Obtener todos los registros de inventario
        inventario = cursor.fetchall()
        print("Inventario obtenido:", inventario)  # Verificar los datos en la consola
        # Actualizar el árbol
        construir_y_guardar_arbol()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        inventario = []
    
    finally:
        # Cerrar el cursor y la conexión en la sección finally
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
    
    return inventario

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

    ################################################### Árbol #####################################################
# Definir nodos
class Nodo:
    def __init__(self, nombre, datos=None):
        self.nombre = nombre
        self.datos = datos or []
        self.hijos = []

    def agregar_hijo(self, nodo_hijo):
        self.hijos.append(nodo_hijo)

    def __repr__(self):
        return f"Nodo({self.nombre}, {self.datos})"

    def a_diccionario(self):
        return {
            "nombre": self.nombre,
            "datos": self.datos,
            "hijos": [hijo.a_diccionario() for hijo in self.hijos]
        }

    @classmethod
    def desde_diccionario(cls, data):
        nodo = cls(data["nombre"], data["datos"])
        for hijo_data in data["hijos"]:
            nodo.agregar_hijo(cls.desde_diccionario(hijo_data))
        return nodo

# Conexión base de datos
DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/huella_amor'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Cargar las tablas
metadata = MetaData()
metadata.reflect(bind=engine)
administradores = Table('administradores', metadata, autoload_with=engine)
clientes = Table('clientes', metadata, autoload_with=engine)
productos = Table('productos', metadata, autoload_with=engine)
proveedores = Table('proveedores', metadata, autoload_with=engine)
ventas = Table('ventas', metadata, autoload_with=engine)

def convertir_a_serializable(obj):
    """Convierte un objeto a un formato serializable por JSON."""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Tipo {type(obj)} no es serializable")

def obtener_datos_por_categoria(tabla, categoria_columna):
    if categoria_columna is None:
        rows = session.query(tabla).all()
    else:
        rows = session.query(tabla).filter_by(categoria=categoria_columna).all()
    
    datos = []
    for row in rows:
        row_dict = {}
        for col in row._mapping.keys():
            val = row._mapping[col]
            row_dict[col] = convertir_a_serializable(val) if isinstance(val, (date, datetime)) else val
        datos.append(row_dict)
    return datos

#
def construir_arbol():
    raiz = Nodo("Inventario Huella de Amor")

    categorias = ["Alimentos", "Medicamentos", "Juguetes", "Accesorios"]
    tablas = [
        ("Ventas", ventas),
        ("Proveedores", proveedores),
        ("Productos", productos),
        ("Usuarios", [
            ("Administradores", administradores),
            ("Clientes", clientes)
        ])
    ]

    for nombre_principal, tabla in tablas:
        nodo_principal = Nodo(nombre_principal)
        if nombre_principal == "Usuarios":
            for sub_nombre, sub_tabla in tabla:
                nodo_sub = Nodo(sub_nombre, obtener_datos_por_categoria(sub_tabla, None))
                nodo_principal.agregar_hijo(nodo_sub)
        else:
            for categoria in categorias:
                nodo_sub = Nodo(categoria, obtener_datos_por_categoria(tabla, categoria))
                nodo_principal.agregar_hijo(nodo_sub)

        raiz.agregar_hijo(nodo_principal)

    return raiz

def guardar_arbol_en_archivo(arbol, archivo):
    with open(archivo, 'w') as file:
        json.dump(arbol.a_diccionario(), file, indent=4)

def cargar_arbol_desde_archivo(archivo):
    with open(archivo, 'r') as file:
        data = json.load(file)
        return Nodo.desde_diccionario(data)

def visualizar_arbol(nodo):
    dot = Digraph()

    def agregar_nodo(dot, nodo):
        dot.node(nodo.nombre, label=nodo.nombre)
        for hijo in nodo.hijos:
            dot.edge(nodo.nombre, hijo.nombre)
            agregar_nodo(dot, hijo)

    agregar_nodo(dot, nodo)
    return dot

# Construir y mostrar el árbol
arbol = construir_arbol()
print(arbol)

# Guardar el árbol en un archivo
guardar_arbol_en_archivo(arbol, 'arbol.json')

# Cargar el árbol desde un archivo
arbol_cargado = cargar_arbol_desde_archivo('arbol.json')
print(arbol_cargado)

# Visualizar el árbol
dot = visualizar_arbol(arbol_cargado)
dot.render('arbol_visual', format='pdf')

def construir_y_guardar_arbol():
    arbol = construir_arbol()
    guardar_arbol_en_archivo(arbol, 'arbol.json')
    print("Árbol reconstruido y guardado")

@app.route('/actualizar_administrador/<docadmin>', methods=['POST'])
def actualizar_administrador(docadmin):
    try:
        datos = (
            request.form['DNIAdmin'],
            request.form['NameAdmin'],
            request.form['phoneAdmin'],
            request.form['emailAdmin'],
            request.form['UserNameAdmin'],
            request.form['passwordAdmin'],
            request.form['avatarAdmin']
        )
        actualizar_administrador_en_bd(docadmin, datos)
        flash("Administrador actualizado exitosamente", "success")
        # Actualizar el árbol
        construir_y_guardar_arbol()
        return redirect(url_for('admin'))
    except mysql.connector.Error as error:
        print("Error al actualizar administrador:", error)
        conexion.rollback()
        flash("Error al actualizar administrador: {}".format(error), "error")
        return redirect(url_for('editar_administrador', docadmin=docadmin))

@app.route('/editar_administrador/<docadmin>')
def editar_administrador(docadmin):
    administrador = obtener_administrador_por_docadmin(docadmin)
    return render_template('editar_admin.html', administrador=administrador)

@app.route('/eliminar_administrador/<docadmin>')
def eliminar_administrador(docadmin):
    try:
        eliminar_administrador_de_bd(docadmin)
        flash("Administrador eliminado exitosamente", "success")
        return redirect(url_for('admin'))
    except mysql.connector.Error as error:
        print("Error al eliminar administrador:", error)
        conexion.rollback()
        flash("Error al eliminar administrador: {}".format(error), "error")
        return redirect(url_for('admin'))

def obtener_administrador_por_docadmin(docadmin):
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT docadmin, nombreadmin, telefonoadmin, correoadmin, usuarioadmin, avataradmin FROM administradores WHERE docadmin = %s"
    cursor.execute(query, (docadmin,))
    administrador = cursor.fetchone()
    cursor.close()
    return administrador

def eliminar_administrador_de_bd(docadmin):
    cursor = conexion.cursor()
    query = "DELETE FROM administradores WHERE docadmin = %s"
    cursor.execute(query, (docadmin,))
    conexion.commit()
    cursor.close()
    # Actualizar el árbol
    construir_y_guardar_arbol()
    print("Árbol reconstruido y guardado después de eliminar administrador.")


def actualizar_administrador_en_bd(docadmin, datos):
    cursor = conexion.cursor()
    query = "UPDATE administradores SET docadmin = %s, nombreadmin = %s, telefonoadmin = %s, correoadmin = %s, usuarioadmin = %s, contrasenaadmin = %s, avataradmin = %s WHERE docadmin = %s"
    cursor.execute(query, datos + (docadmin,))
    conexion.commit()
    cursor.close()
    # Actualizar el árbol
    construir_y_guardar_arbol()
    print("Árbol reconstruido y guardado después de actualizar administrador.")

@app.route('/actualizar_proveedor/<string:docproveedor>', methods=['POST'])
def actualizar_proveedor(docproveedor):
    try:
        datos = (
            request.form['DNIProvider'],
            request.form['NameProvider'],
            request.form['addressProvider'],
            request.form['phoneProvider'],
            request.form['emailProvider'],
            request.form['webProvider']
        )
        actualizar_proveedor_en_bd(docproveedor, datos)
        flash("Proveedor actualizado exitosamente", "success")
        # Actualizar el árbol
        construir_y_guardar_arbol()
        print("Árbol reconstruido y guardado después de actualizar administrador.")
        return redirect(url_for('providers'))
    except mysql.connector.Error as error:
        print("Error al actualizar proveedor:", error)
        conexion.rollback()
        flash("Error al actualizar proveedor: {}".format(error), "error")
        return redirect(url_for('editar_proveedor', docproveedor=docproveedor))

@app.route('/editar_proveedor/<docproveedor>')
def editar_proveedor(docproveedor):
    proveedor = obtener_proveedor_por_docproveedor(docproveedor)
    return render_template('editar_proveedor.html', proveedor=proveedor)


@app.route('/eliminar_proveedor/<docproveedor>')
def eliminar_proveedor(docproveedor):
    try:
        eliminar_proveedor_de_bd(docproveedor)
        flash("Proveedor eliminado exitosamente", "success")
        return redirect(url_for('providers'))
    except mysql.connector.Error as error:
        print("Error al eliminar proveedor:", error)
        conexion.rollback()
        flash("Error al eliminar proveedor: {}".format(error), "error")
        return redirect(url_for('providers'))

def obtener_proveedor_por_docproveedor(docproveedor):
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT docproveedores, nombreprov, direccionprov, telefonoprov, correoprov, categoria FROM proveedores WHERE docproveedores = %s"
    cursor.execute(query, (docproveedor,))
    proveedor = cursor.fetchone()
    cursor.close()
    return proveedor

def eliminar_proveedor_de_bd(docproveedor):
    cursor = conexion.cursor()
    query = "DELETE FROM proveedores WHERE docproveedores = %s"
    cursor.execute(query, (docproveedor,))
    conexion.commit()
    cursor.close()
    # Actualizar el árbol
    construir_y_guardar_arbol()
    print("Árbol reconstruido y guardado después de actualizar administrador.")

def actualizar_proveedor_en_bd(docproveedor, datos):
    cursor = conexion.cursor()
    query = "UPDATE proveedores SET docproveedores = %s, nombreprov = %s, direccionprov = %s, telefonoprov = %s, correoprov = %s, categoria = %s WHERE docproveedores = %s"
    cursor.execute(query, datos + (docproveedor,))
    conexion.commit()
    cursor.close()
    # Actualizar el árbol
    construir_y_guardar_arbol()
    print("Árbol reconstruido y guardado después de actualizar administrador.")
    
@app.route('/actualizar_categoria/<int:idcategoria>', methods=['POST'])
def actualizar_categoria(idcategoria):
    try:
        datos = (
            request.form['NameCategory'],
            request.form['descriptionCategory'],
            idcategoria
        )
        actualizar_categoria_en_bd(datos)
        flash("Categoría actualizada exitosamente", "success")
        # Actualizar el árbol
        construir_y_guardar_arbol()
        print("Árbol reconstruido y guardado después de actualizar administrador.")
        return redirect(url_for('categories'))
    except mysql.connector.Error as error:
        print("Error al actualizar categoría:", error)
        conexion.rollback()
        flash("Error al actualizar categoría: {}".format(error), "error")
        return redirect(url_for('editar_categoria', idcategoria=idcategoria))

@app.route('/editar_categoria/<int:idcategoria>')
def editar_categoria(idcategoria):
    categoria = obtener_categoria_por_id(idcategoria)
    return render_template('editar_categoria.html', categoria=categoria)

@app.route('/eliminar_categoria/<int:idcategoria>')
def eliminar_categoria(idcategoria):
    try:
        eliminar_categoria_de_bd(idcategoria)
        flash("Categoría eliminada exitosamente", "success")
        return redirect(url_for('categories'))
    except mysql.connector.Error as error:
        print("Error al eliminar categoría:", error)
        conexion.rollback()
        flash("Error al eliminar categoría: {}".format(error), "error")
        return redirect(url_for('categories'))
    
def obtener_categoria_por_id(idcategoria):
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT idcategorias, nombrecat, descripcioncat FROM categorias WHERE idcategorias = %s"
    cursor.execute(query, (idcategoria,))
    categoria = cursor.fetchone()
    cursor.close()
    return categoria

def eliminar_categoria_de_bd(idcategoria):
    cursor = conexion.cursor()
    query = "DELETE FROM categorias WHERE idcategorias = %s"
    cursor.execute(query, (idcategoria,))
    conexion.commit()
    cursor.close()
    # Actualizar el árbol
    construir_y_guardar_arbol()
    print("Árbol reconstruido y guardado después de actualizar administrador.")

def actualizar_categoria_en_bd(datos):
    cursor = conexion.cursor()
    query = "UPDATE categorias SET nombrecat = %s, descripcioncat = %s WHERE idcategorias = %s"
    cursor.execute(query, datos)
    conexion.commit()
    cursor.close()
    # Actualizar el árbol
    construir_y_guardar_arbol()
    print("Árbol reconstruido y guardado después de actualizar administrador.")
    
@app.route('/actualizar_cliente/<int:idcliente>', methods=['POST'])
def actualizar_cliente(idcliente):
    try:
        datos = (
            request.form['DNIClient'],
            request.form['NameClient'],
            request.form['addressClient'],
            request.form['phoneClient'],
            request.form['emailClient'],
            idcliente
        )
        actualizar_cliente_en_bd(datos)
        flash("Cliente actualizado exitosamente", "success")
        # Actualizar el árbol
        construir_y_guardar_arbol()
        print("Árbol reconstruido y guardado después de actualizar administrador.")
        return redirect(url_for('client'))
    except mysql.connector.Error as error:
        print("Error al actualizar cliente:", error)
        conexion.rollback()
        flash("Error al actualizar cliente: {}".format(error), "error")
        return redirect(url_for('editar_clientes', idcliente=idcliente))

@app.route('/editar_cliente/<int:idcliente>')
def editar_cliente(idcliente):
    cliente = obtener_cliente_por_id(idcliente)
    return render_template('editar_clientes.html', cliente=cliente)

@app.route('/eliminar_cliente/<int:idcliente>')
def eliminar_cliente(idcliente):
    try:
        eliminar_cliente_de_bd(idcliente)
        flash("Cliente eliminado exitosamente", "success")
        return redirect(url_for('client'))
    except mysql.connector.Error as error:
        print("Error al eliminar cliente:", error)
        conexion.rollback()
        flash("Error al eliminar cliente: {}".format(error), "error")
        return redirect(url_for('client'))

def obtener_cliente_por_id(idcliente):
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT doccliente, nombrecliente, direccioncliente, telefonocliente, correocliente FROM clientes WHERE doccliente = %s"
    cursor.execute(query, (idcliente,))
    cliente = cursor.fetchone()
    cursor.close()
    return cliente

def eliminar_cliente_de_bd(doccliente):
    cursor = conexion.cursor()
    query = "DELETE FROM clientes WHERE doccliente = %s"
    cursor.execute(query, (doccliente,))
    conexion.commit()
    cursor.close()
    # Actualizar el árbol
    construir_y_guardar_arbol()
    print("Árbol reconstruido y guardado después de actualizar administrador.")

def actualizar_cliente_en_bd(datos):
    cursor = conexion.cursor()
    query = "UPDATE clientes SET doccliente = %s, nombrecliente = %s, direccioncliente = %s, telefonocliente = %s, correocliente = %s WHERE doccliente = %s"
    cursor.execute(query, datos)
    conexion.commit()
    cursor.close()
    # Actualizar el árbol
    construir_y_guardar_arbol()
    print("Árbol reconstruido y guardado después de actualizar administrador.")
    
@app.route('/actualizar_producto/<int:idproducto>', methods=['POST'])
def actualizar_producto(idproducto):
    try:
        datos = (
            request.form['NameProduct'],
            request.form['StockProduct'],
            request.form['PriceProduct'],
            request.form['CategoryProduct'],
            request.form['provider_id'],
            request.form['DescriptionProduct'],
            request.form['markProduct'],
            request.form['dateProduct'],
            request.form['statusProduct'],
            request.form['fileProduct'],
            idproducto
        )
        actualizar_producto_en_bd(datos)
        flash("Producto actualizado exitosamente", "success")
        # Actualizar el árbol
        construir_y_guardar_arbol()
        print("Árbol reconstruido y guardado después de actualizar administrador.")
        return redirect(url_for('products'))
    except mysql.connector.Error as error:
        print("Error al actualizar producto:", error)
        conexion.rollback()
        flash("Error al actualizar producto: {}".format(error), "error")
        return redirect(url_for('editar_producto', idproducto=idproducto))

@app.route('/editar_producto/<int:idproducto>')
def editar_producto(idproducto):
    producto = obtener_producto_por_id(idproducto)
    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar_producto/<int:idproducto>')
def eliminar_producto(idproducto):
    try:
        eliminar_producto_de_bd(idproducto)
        flash("Producto eliminado exitosamente", "success")
        return redirect(url_for('products'))
    except mysql.connector.Error as error:
        print("Error al eliminar producto:", error)
        conexion.rollback()
        flash("Error al eliminar producto: {}".format(error), "error")
        return redirect(url_for('products'))

def obtener_producto_por_id(idproducto):
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT idproductos, nombreprod, unidadesprod, precioprod, categoria, proveedorprod, descripcionprod, marcaprod, imagenprod FROM productos WHERE idproductos = %s"
    cursor.execute(query, (idproducto,))
    producto = cursor.fetchone()
    cursor.close()
    return producto

def eliminar_producto_de_bd(idproducto):
    cursor = conexion.cursor()
    query = "DELETE FROM productos WHERE idproductos = %s"
    cursor.execute(query, (idproducto,))
    conexion.commit()
    cursor.close()
    # Actualizar el árbol
    construir_y_guardar_arbol()
    print("Árbol reconstruido y guardado después de actualizar administrador.")

def actualizar_producto_en_bd(datos):
    cursor = conexion.cursor()
    query = "UPDATE productos SET nombreprod = %s, unidadesprod = %s, precioprod = %s, categoria = %s, proveedorprod = %s, descripcionprod = %s, marcaprod = %s, fecharegistro = %s, estatusprod = %s, imagenprod = %s WHERE idproductos = %s"
    cursor.execute(query, datos)
    conexion.commit()
    cursor.close()
    # Actualizar el árbol
    construir_y_guardar_arbol()
    print("Árbol reconstruido y guardado después de actualizar administrador.")
    
@app.route('/actualizar_venta/<int:idventa>', methods=['POST'])
def actualizar_venta(idventa):
    try:
        datos = (
            request.form['dateSales'],
            request.form['NameProduct'],
            request.form['StockProduct'],
            request.form['PriceProduct'],
            request.form['DNIClient'],
            request.form['NameClient'],
            request.form['Pay'],
            request.form['TotalPay'],
            request.form['CodeProduct'],
            idventa
        )
        actualizar_venta_en_bd(datos)
        flash("Venta actualizada exitosamente", "success")
        # Actualizar el árbol
        construir_y_guardar_arbol()
        print("Árbol reconstruido y guardado después de actualizar administrador.")
        return redirect(url_for('sales'))
    except mysql.connector.Error as error:
        print("Error al actualizar venta:", error)
        conexion.rollback()
        flash("Error al actualizar venta: {}".format(error), "error")
        return redirect(url_for('editar_venta', idventa=idventa))


@app.route('/editar_venta/<int:idventa>')
def editar_venta(idventa):
    venta = obtener_venta_por_id(idventa)
    return render_template('editar_venta.html', venta=venta)


@app.route('/eliminar_venta/<int:idventa>')
def eliminar_venta(idventa):
    try:
        eliminar_venta_de_bd(idventa)
        flash("Venta eliminada exitosamente", "success")
        return redirect(url_for('sales'))
    except mysql.connector.Error as error:
        print("Error al eliminar venta:", error)
        conexion.rollback()
        flash("Error al eliminar venta: {}".format(error), "error")
        return redirect(url_for('sales'))


def obtener_venta_por_id(idventa):
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT idventas, fecharegistro, productovent, unidadesvent, preciovent, doccliente, nombrecliente, mediopago, totalvent, categoria, idprod FROM ventas WHERE idventas = %s"
    cursor.execute(query, (idventa,))
    venta = cursor.fetchone()
    cursor.close()
    return venta


def eliminar_venta_de_bd(idventa):
    cursor = conexion.cursor()
    query = "DELETE FROM ventas WHERE idventas = %s"
    cursor.execute(query, (idventa,))
    conexion.commit()
    cursor.close()
    # Actualizar el árbol
    construir_y_guardar_arbol()
    print("Árbol reconstruido y guardado después de actualizar administrador.")


def actualizar_venta_en_bd(datos):
    cursor = conexion.cursor()
    query = "UPDATE ventas SET fecharegistro = %s, productovent = %s, unidadesvent = %s, preciovent = %s, doccliente = %s, nombrecliente = %s, mediopago = %s, totalvent = %s, idprod = %s WHERE idventas = %s"
    cursor.execute(query, datos)
    conexion.commit()
    cursor.close()
    # Actualizar el árbol
    construir_y_guardar_arbol()
    print("Árbol reconstruido y guardado después de actualizar administrador.")
    
if __name__ == '__main__':
    # Ejecutar la aplicación Flask
    app.run(debug=True)