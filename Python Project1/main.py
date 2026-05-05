# ==============================================================================
# MÓDULO: main.py
# PROPÓSITO: Interfaz CLI con flujos diferenciados y validación estricta de ubicación
# AUTORES: Alfredo Anthony Chaupis Aquino, Jhon Brando Colca Heredia, Adrian Augusto Cuzcano Escobar,Johnny Alessis Giraldo Suarez
# CURSO: Fundamentos de Programación 2 - IS275
# ==============================================================================

from entidades import Cliente, ClienteCorporativo, ItemPedido, CatalogoProductos, DireccionEntrega  # Importamos las clases de dominio necesarias desde el módulo entidades
from gestor import GestorDespacho, Pedido  # Importamos las clases principales del sistema (Pedido y GestorDespacho) desde el módulo gestor
from excepciones import PedidoError, DatosError  # Importamos nuestras excepciones personalizadas desde el módulo excepciones
from servicios import ValidadorDatos  # Importamos el validador de datos desde el módulo servicios
import subprocess  # Importamos el módulo subprocess para ejecutar comandos del sistema operativo (limpiar pantalla)
import os  # Importamos el módulo os para detectar el sistema operativo (Windows/Linux/Mac)
import sys  # Importamos el módulo sys para controlar la salida del programa (sys.exit())

def limpiar_pantalla():
    # Función auxiliar para limpiar la consola según el sistema operativo
    # Usa subprocess que es el estándar moderno y evita advertencias de linter
    comando = 'cls' if os.name == 'nt' else 'clear'  # Asignamos 'cls' si es Windows (os.name == 'nt'), sino asignamos 'clear' para Linux/Mac
    subprocess.call(comando, shell=True)  # Ejecutamos el comando de limpieza usando subprocess.call con shell=True para que funcione en la terminal

def mostrar_menu():
    # Función que dibuja el menú principal profesional en la consola
    # Usa caracteres de alineación para crear un formato visual atractivo y legible
    print("=" * 60)  # Imprimimos línea superior de separación (60 caracteres '=')
    print("   PASTIPAN - SISTEMA DE GESTIÓN LOGÍSTICA")  # Imprimimos el título del sistema centrado con espacios iniciales
    print("   Precisión en Registro y Eficiencia en Despacho")  # Imprimimos el subtítulo que describe el propósito del sistema
    print("=" * 60)  # Imprimimos línea de separación
    print("1. Registrar Pedido Minorista (Retail)")  # Imprimimos la opción 1 del menú para registro de clientes normales
    print("2. Registrar Pedido Corporativo (B2B)")  # Imprimimos la opción 2 del menú para registro de empresas
    print("3. Buscar y Ver Detalle de Pedido")  # Imprimimos la opción 3 del menú para búsqueda de pedidos
    print("4. Listar Todos los Pedidos")  # Imprimimos la opción 4 del menú para ver todos los pedidos registrados
    print("5. Gestionar Estado del Pedido (Avanzar Producción)")  # Imprimimos la opción 5 del menú para avanzar el estado del pedido
    print("6. Salir del Sistema")  # Imprimimos la opción 6 del menú para cerrar el programa
    print("=" * 60)  # Imprimimos línea inferior de separación

def capturar_direccion():
    # Función auxiliar que obliga al operador a completar datos geográficos críticos
    # Resuelve la problemática real de Pastipan: direcciones incompletas que generan reprocesos
    print("\n--- CAPTURA DE UBICACIÓN EXACTA (OBLIGATORIA) ---")  # Imprimimos encabezado de sección que indica que los datos son obligatorios
    calle = ValidadorDatos.validar_texto_obligatorio("Calle/Av principal: ")  # Llamamos al validador para capturar la calle principal (bloquea si está vacío)
    cruces = ValidadorDatos.validar_texto_obligatorio("Cruce de calles (Ej: Av. La Paz con Jr. Cusco): ")  # Llamamos al validador para capturar las intersecciones (crítico para ubicación)
    referencia = ValidadorDatos.validar_texto_obligatorio("Referencia visible cercana (Ej: Frente al parque Kennedy): ")  # Llamamos al validador para capturar un punto de referencia visible
    distrito = ValidadorDatos.validar_texto_obligatorio("Distrito: ")  # Llamamos al validador para capturar el distrito (necesario para ruteo)
    notas = input("Notas de acceso (Opcional - Ej: Portón negro, timbre 4B): ").strip()  # Capturamos notas opcionales y eliminamos espacios con strip()
    return DireccionEntrega(calle, cruces, referencia, distrito, notas)  # Creamos y retornamos un objeto DireccionEntrega con todos los datos capturados

def registrar_pedido_tipo(tipo_cliente, gestor):
    # Función genérica que maneja flujo diferenciado según segmento de cliente
    # Recibe el tipo de cliente ("minorista" o "corporativo") y el objeto gestor
    # Centraliza la lógica de registro evitando código duplicado
    limpiar_pantalla()  # Limpiamos la pantalla antes de mostrar el formulario de registro
    if tipo_cliente == "corporativo":  # Verificamos si el tipo de cliente es corporativo (B2B)
        print("--- REGISTRO DE PEDIDO CORPORATIVO (B2B) ---")  # Imprimimos encabezado específico para clientes corporativos
        nombre = ValidadorDatos.validar_texto_obligatorio("Razón Social: ")  # Capturamos la razón social de la empresa (valida que no esté vacío)
        ruc = ValidadorDatos.validar_texto_obligatorio("RUC Empresa: ")  # Capturamos el RUC de la empresa (obligatorio para facturación)
        contacto = ValidadorDatos.validar_texto_obligatorio("Persona de Recepción/Compras: ")  # Capturamos el nombre de la persona autorizada para recepcionar
        telefono = ValidadorDatos.validar_texto_obligatorio("Teléfono Corporativo: ")  # Capturamos el teléfono corporativo de contacto
        direccion = capturar_direccion()  # Llamamos a la función auxiliar que captura la dirección completa (misma validación para retail y corporativo)
        cliente = ClienteCorporativo("CORP-" + ruc[-4:], nombre, telefono, direccion, ruc, contacto)  # Creamos objeto ClienteCorporativo con ID basado en últimos 4 dígitos del RUC
    else:  # Si no es corporativo, es minorista (retail)
        print("--- REGISTRO DE PEDIDO MINORISTA (RETAIL) ---")  # Imprimimos encabezado específico para clientes minoristas
        nombre = ValidadorDatos.validar_texto_obligatorio("Nombre del Cliente: ")  # Capturamos el nombre completo del cliente (valida que no esté vacío)
        telefono = ValidadorDatos.validar_texto_obligatorio("Teléfono de Contacto: ")  # Capturamos el teléfono de contacto del cliente
        direccion = capturar_direccion()  # Llamamos a la función auxiliar que captura la dirección completa
        cliente = Cliente("CLI-" + nombre[:3].upper(), nombre, telefono, direccion)  # Creamos objeto Cliente con ID basado en primeras 3 letras del nombre en mayúsculas

    tipo_entrega = input("Tipo de Entrega (local/estandar/express/corporativo): ").strip().lower()  # Capturamos el tipo de entrega, eliminamos espacios y convertimos a minúsculas
    nuevo_pedido = Pedido("PED-" + str(len(gestor.coleccion_pedidos) + 1).zfill(4), cliente, tipo_entrega)  # Creamos objeto Pedido con ID secuencial (PED-0001, PED-0002, etc.)

    print("\n--- SELECCIÓN DE PRODUCTOS ---")  # Imprimimos encabezado de sección para selección de productos
    print(CatalogoProductos.listar_catalogo())  # Llamamos al método estático que imprime todos los productos del catálogo agrupados por categoría
    
    while True:  # Iniciamos bucle infinito para agregar múltiples productos al pedido
        codigo = input("\nCódigo de producto (o 'FIN' para terminar): ").strip().upper()  # Capturamos el código del producto, eliminamos espacios y convertimos a mayúsculas
        if codigo == 'FIN':  # Verificamos si el usuario escribió 'FIN' para terminar de agregar productos
            break  # Salimos del bucle while usando break (terminamos la agregación de productos)
        producto = CatalogoProductos.obtener_producto(codigo)  # Buscamos el producto en el catálogo usando el código ingresado
        if not producto:  # Verificamos si el producto no existe (obtener_producto retorna None si no encuentra)
            print("ERROR: Código no existe en catálogo.")  # Imprimimos mensaje de error indicando que el código es inválido
            continue  # Volvemos al inicio del bucle while para que el usuario ingrese otro código (continue salta al siguiente ciclo)
        cantidad = ValidadorDatos.validar_numero_positivo(f"Cantidad para {producto['nombre']}: ")  # Validamos que la cantidad sea un número positivo
        item = ItemPedido(producto['nombre'], int(cantidad), producto['precio'], producto['categoria'])  # Creamos objeto ItemPedido con nombre, cantidad, precio y categoría
        nuevo_pedido.agregar_item(item)  # Llamamos al método del pedido que agrega el ítem a la lista interna
        print(f">> Agregado: {item}")  # Imprimimos confirmación de que el ítem fue agregado (muestra cantidad, nombre y subtotal)

    try:  # Iniciamos bloque try para capturar excepciones de negocio durante el registro
        gestor.registrar_pedido(nuevo_pedido)  # Llamamos al método del gestor que valida y registra el pedido (puede lanzar PedidoError o DatosError)
        print("\nSUCCESS: Pedido registrado con validación geográfica completa.")  # Imprimimos mensaje de éxito confirmando que el pedido se registró correctamente
        nuevo_pedido.generar_hoja_despacho()  # Llamamos al método que imprime la hoja de despacho estandarizada para el conductor
    except (PedidoError, DatosError) as e:  # Capturamos excepciones personalizadas de negocio (PedidoError o DatosError)
        print(f"ERROR DE VALIDACIÓN: {e}")  # Imprimimos el mensaje de error específico de la excepción
    input("\nPresione Enter para continuar...")  # Pausamos la ejecución esperando que el usuario presione Enter

def ejecutar():
    # Función principal que contiene el bucle infinito del programa
    # Orquesta toda la interacción con el usuario y llama a las clases del sistema
    # Se ejecuta automáticamente cuando se corre main.py directamente
    gestor = GestorDespacho()  # Creamos una instancia del gestor que administrará la colección de pedidos
    while True:  # Iniciamos bucle infinito que mantiene el programa activo hasta que el usuario seleccione salir
        try:  # Iniciamos bloque try para capturar cualquier error inesperado durante la ejecución
            limpiar_pantalla()  # Limpiamos la pantalla antes de mostrar el menú principal
            mostrar_menu()  # Llamamos a la función que dibuja el menú con las 6 opciones disponibles
            opcion = input("Seleccione una opción (1-6): ").strip()  # Capturamos la opción seleccionada y eliminamos espacios con strip()
            
            if opcion == "1":  # Verificamos si el usuario seleccionó la opción 1 (Registrar Pedido Minorista)
                registrar_pedido_tipo("minorista", gestor)  # Llamamos a la función genérica pasando "minorista" como tipo de cliente
            elif opcion == "2":  # Verificamos si el usuario seleccionó la opción 2 (Registrar Pedido Corporativo)
                registrar_pedido_tipo("corporativo", gestor)  # Llamamos a la función genérica pasando "corporativo" como tipo de cliente
            elif opcion == "3":  # Verificamos si el usuario seleccionó la opción 3 (Buscar Pedido)
                limpiar_pantalla()  # Limpiamos la pantalla antes de mostrar el formulario de búsqueda
                id_bus = input("Ingrese ID del Pedido: ").strip()  # Capturamos el ID del pedido a buscar
                encontrado = gestor.buscar_pedido(id_bus)  # Llamamos al método de búsqueda del gestor
                if encontrado:  # Verificamos si se encontró el pedido (no es None)
                    print(encontrado)  # Imprimimos el detalle completo del pedido (llama a __str__)
                    encontrado.generar_hoja_despacho()  # Imprimimos también la hoja de despacho para el conductor
                else:  # Si no se encontró el pedido
                    print("INFO: Pedido no encontrado.")  # Imprimimos mensaje informativo
                input("\nPresione Enter para continuar...")  # Pausamos esperando Enter
            elif opcion == "4":  # Verificamos si el usuario seleccionó la opción 4 (Listar Pedidos)
                limpiar_pantalla()  # Limpiamos la pantalla antes de mostrar el listado
                print("--- LISTADO DE PEDIDOS EN MEMORIA ---")  # Imprimimos encabezado de sección
                gestor.listar_pedidos()  # Llamamos al método del gestor que imprime todos los pedidos
                input("\nPresione Enter para continuar...")  # Pausamos esperando Enter
            elif opcion == "5":  # Verificamos si el usuario seleccionó la opción 5 (Avanzar Estado)
                limpiar_pantalla()  # Limpiamos la pantalla antes de mostrar el formulario
                id_estado = input("Ingrese ID para avanzar estado: ").strip()  # Capturamos el ID del pedido a modificar
                pedido_mod = gestor.buscar_pedido(id_estado)  # Buscamos el pedido usando el método de búsqueda
                if pedido_mod:  # Verificamos si encontramos el pedido (no es None)
                    print(f"Estado actual: {pedido_mod._estado}")  # Imprimimos el estado actual del pedido
                    pedido_mod.avanzar_estado()  # Llamamos al método que avanza el estado (Patrón State)
                    print(f"Nuevo estado: {pedido_mod._estado}")  # Imprimimos el nuevo estado después de la transición
                else:  # Si no encontramos el pedido
                    print("ERROR: ID inválido.")  # Imprimimos mensaje de error
                input("\nPresione Enter para continuar...")  # Pausamos esperando Enter
            elif opcion == "6":  # Verificamos si el usuario seleccionó la opción 6 (Salir)
                print("Cerrando sistema Pastipan. Gracias por usar la plataforma.")  # Imprimimos mensaje de despedida
                sys.exit()  # Terminamos la ejecución del programa limpiamente usando sys.exit()
            else:  # Si el usuario ingresó una opción que no es 1-6
                print("ERROR: Opción no válida.")  # Imprimimos mensaje de error
                input("\nPresione Enter para continuar...")  # Pausamos esperando Enter
        except Exception as e:  # Captura general de cualquier error no previsto (Exception es la clase base de todas las excepciones)
            print(f"\nERROR CRÍTICO: {e}")  # Imprimimos el mensaje de error con detalles para depuración
            input("Presione Enter para reiniciar menú...")  # Pausamos y retornamos al menú principal

if __name__ == "__main__":  # Bloque estándar de Python que verifica si este archivo se ejecuta directamente (no fue importado)
    ejecutar()  # Llamamos a la función principal que inicia todo el sistema (punto de entrada del programa)