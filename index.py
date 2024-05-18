import mysql.connector

# Establecer la conexión
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="huella_amor"
)

# Verificar si la conexión fue exitosa
if conexion.is_connected():
    print("Conexión exitosa a la base de datos.")

# Realizar operaciones en la base de datos
# Por ejemplo, crear un cursor
cursor = conexion.cursor()

# Ejecutar una consulta
cursor.execute("SELECT * FROM administradores")

# Obtener los resultados
resultados = cursor.fetchall()
for fila in resultados:
    print(fila)

# Cerrar el cursor y la conexión
cursor.close()
conexion.close()
