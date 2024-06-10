**PROYECTO INVENTARIO**

**RESUMEN**

El Sistema de Gestión de Inventario es una aplicación diseñada para ayudar a las empresas a gestionar eficientemente su inventario de productos. Permite llevar un registro detallado de los productos disponibles, su cantidad, ubicación, proveedores, precios y otras características relevantes. El sistema facilita la administración del inventario, la realización de pedidos de reposición, el seguimiento de las ventas y la generación de informes para tomar decisiones informadas.

**FUNCIONALIDADES**

- Inicio de sesión: Los usuarios autorizados inician sesión en el sistema utilizando sus credenciales.
- Dashboard: Al iniciar sesión, los usuarios son dirigidos a un panel de control que muestra un resumen del estado actual del inventario, alertas, informes destacados, etc.
- Gestión de inventario: Los usuarios pueden acceder a las funciones de registro, visualización, edición y búsqueda de productos en el inventario.
- Seguimiento de ventas: El sistema registra automáticamente las ventas realizadas y actualiza el inventario en consecuencia.
- Pedidos de reposición: Cuando la cantidad de un producto cae por debajo del umbral mínimo, se genera una alerta y se facilita la realización de pedidos de reposición.
- Informes y análisis: Los usuarios pueden generar informes personalizados para analizar el rendimiento del inventario y tomar decisiones informadas.
- Seguridad y acceso: El sistema garantiza la seguridad de la información del inventario mediante el control de acceso basado en roles y privilegios de los usuarios.

**DESCRIPCIÓN DEL PROYECTO**

Este proyecto es un sistema de gestión de administradores desarrollado utilizando el lenguaje de programación Python y el framework web Flask. Flask es un microframework ligero y flexible que permite desarrollar aplicaciones web rápidamente con un diseño limpio y sencillo.

El sistema permite agregar nuevos administradores, listar administradores existentes, y realizar búsquedas de administradores en la base de datos. El frontend del proyecto utiliza HTML, CSS, y JavaScript junto con la biblioteca de componentes de Material Design Lite (MDL) para proporcionar una interfaz de usuario moderna y responsiva.



**REQUISITOS PARA LA INSTALACIÓN Y EJECUCIÓN DEL CÓDIGO**

- **PRERREQUISITOS**

Asegúrate de tener instalado lo siguiente en tu sistema:

Python 3.7 o superior: Puedes descargar Python desde python.org.pip: El gestor de paquetes de Python. Generalmente viene incluido con Python, pero puedes verificar su instalación ejecutando pip --version en la terminal.

- **INSTALAR DEPENDENCIAS**

Instala las dependencias necesarias utilizando pip:

*pip install* 

- **INICIA EL SERVIDOR DE DESARROLLO DE FLASK**

*flask run*

- **ENLAZAR BASE DE DATOS**

Crear base de datos y enlazarla en el archivo main.py

Crear tabla de usuarios y configurar las credenciales para poder ingresar al aplicativo.

**PRUEBAS**

1. **Al ejecutar el código accede al login**

![](Aspose.Words.1b82731a-8c92-4c5e-bc98-688519052c16.001.png)**

2. **Al ingresar el usuario y contraseña guardados en base de datos accede al dashboard**

![](Aspose.Words.1b82731a-8c92-4c5e-bc98-688519052c16.002.png)

3. **Al ingresar en la opción Proveedores nos carga el formulario para ingresar un proveedor nuevo**

![](Aspose.Words.1b82731a-8c92-4c5e-bc98-688519052c16.003.png)

4. **Al seleccionar la lista nos cargan los registros de la base de datos** 

![](Aspose.Words.1b82731a-8c92-4c5e-bc98-688519052c16.004.png)

5. **En los registros aparecen las opciones Editar y Eliminar**

![](Aspose.Words.1b82731a-8c92-4c5e-bc98-688519052c16.005.png)

6. **En la opción productos podemos ver el catálogo de todos los registros**

![](Aspose.Words.1b82731a-8c92-4c5e-bc98-688519052c16.006.png)

7. **En la opción Inventario podemos apreciar los productos con el stock actualizado** 

![](Aspose.Words.1b82731a-8c92-4c5e-bc98-688519052c16.007.png)

