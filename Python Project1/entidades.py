# ==============================================================================
# MÓDULO: entidades.py
# PROPÓSITO: Modelar las clases de dominio con captura estructurada de ubicaciones y segmentos
# AUTORES: Alfredo Anthony Chaupis Aquino, Jhon Brando Colca Heredia, Adrian Augusto Cuzcano Escobar,Johnny Alessis Giraldo Suarez
# CURSO: Fundamentos de Programación 2 - IS275
# ==============================================================================

class DireccionEntrega:
    # Clase que encapsula datos geográficos para eliminar ambigüedades en despacho
    # Resuelve la problemática de triangulación con el Call Center
    def __init__(self, calle_principal, cruces, referencia_exacta, distrito, notas_acceso=""):
        self.calle_principal = calle_principal.strip()  # Vía principal obligatoria
        self.cruces = cruces.strip()  # Intersecciones de referencia (calle A con calle B)
        self.referencia_exacta = referencia_exacta.strip()  # Punto visible cercano (farmacia, parque, etc.)
        self.distrito = distrito.strip()  # Zona administrativa para ruteo
        self.notas_acceso = notas_acceso.strip()  # Códigos, pisos, portones, instrucciones de seguridad

    def validar_integridad(self):
        # Método que garantiza que todos los campos críticos estén completos
        if not all([self.calle_principal, self.cruces, self.referencia_exacta, self.distrito]):
            from excepciones import DatosError  # Importación condicional
            raise DatosError("La dirección está incompleta. Se requieren calle, cruces, referencia y distrito.")
        return True  # Retorna verdadero si pasa validación estructural

    def __str__(self):
        # Genera formato legible para conductor y comprobante de entrega
        linea = f"{self.calle_principal} (cruce: {self.cruces})"
        if self.referencia_exacta:
            linea += f" | Ref: {self.referencia_exacta}"
        linea += f" | {self.distrito}"
        if self.notas_acceso:
            linea += f" | Acceso: {self.notas_acceso}"
        return linea  # Retorna cadena formateada para hoja de despacho

class Cliente:
    # Clase base para clientes minoristas (consumo final)
    def __init__(self, id_cliente, nombre, telefono, direccion):
        self.id_cliente = id_cliente  # Identificador único generado por sistema
        self.nombre = nombre  # Nombre completo del titular
        self.telefono = telefono  # Contacto principal para coordinación
        self.direccion = direccion  # Objeto DireccionEntrega validado

class ClienteCorporativo(Cliente):
    # Clase derivada para empresas con facturación y logística B2B
    def __init__(self, id_cliente, nombre, telefono, direccion, ruc, contacto_compras):
        super().__init__(id_cliente, nombre, telefono, direccion)  # Hereda estructura base
        self.ruc = ruc  # Registro Único de Contribuyente obligatorio para facturas
        self.contacto_compras = contacto_compras  # Persona autorizada para recepcionar
        self.descuento_corporativo = 0.10  # Política comercial: 10% fijo en volumen

    def aplicar_descuento(self, monto_total):
        # Calcula precio final tras aplicar bonificación B2B
        return monto_total * (1 - self.descuento_corporativo)  # Retorna monto reducido

    def __str__(self):
        return f"{self.nombre} | RUC: {self.ruc} | Contacto: {self.contacto_compras}"  # Formato corporativo

class ItemPedido:
    # Clase que representa línea de detalle en un pedido
    def __init__(self, nombre, cantidad, precio_unitario, categoria):
        self.nombre = nombre  # Nombre comercial del producto
        self.cantidad = cantidad  # Unidades solicitadas
        self.precio_unitario = precio_unitario  # Tarifa vigente del catálogo
        self.categoria = categoria  # Clasificación para reportes analíticos

    def obtener_subtotal(self):
        return self.cantidad * self.precio_unitario  # Cálculo de línea sin redondeo intermedio

    def __str__(self):
        return f"{self.cantidad}x {self.nombre} ({self.categoria}) | S/. {self.obtener_subtotal():.2f}"  # Formato legible

class CatalogoProductos:
    # Repositorio centralizado para evitar errores de transcripción manual
    PRODUCTOS = {
        "TOR-001": {"nombre": "Torta de Chocolate 1kg", "precio": 45.00, "categoria": "Tortas"},
        "TOR-002": {"nombre": "Torta de Fresa 1kg", "precio": 45.00, "categoria": "Tortas"},
        "BOC-S01": {"nombre": "Empanadas (docena)", "precio": 18.00, "categoria": "Bocaditos Salados"},
        "BOC-S02": {"nombre": "Tequeños (docena)", "precio": 20.00, "categoria": "Bocaditos Salados"},
        "BOC-D01": {"nombre": "Mini Tortas (docena)", "precio": 30.00, "categoria": "Bocaditos Dulces"},
        "PAN-001": {"nombre": "Pan Francés (unidad)", "precio": 0.50, "categoria": "Panadería"},
        "COR-001": {"nombre": "Desayuno Corporativo Básico (p/p)", "precio": 12.00, "categoria": "Corporativo"},
        "COR-002": {"nombre": "Desayuno Corporativo Premium (p/p)", "precio": 18.00, "categoria": "Corporativo"}
    }

    @staticmethod
    def obtener_producto(codigo):
        return CatalogoProductos.PRODUCTOS.get(codigo.upper())  # Búsqueda segura sin excepción

    @staticmethod
    def listar_catalogo():
        lista = []  # Inicializa contenedor de líneas
        categoria_actual = ""  # Controla impresión de encabezados
        for codigo, datos in CatalogoProductos.PRODUCTOS.items():
            if datos['categoria'] != categoria_actual:
                categoria_actual = datos['categoria']
                lista.append(f"\n=== {categoria_actual.upper()} ===")  # Separador visual
            lista.append(f"[{codigo}] {datos['nombre']} - S/. {datos['precio']:.2f}")  # Línea formateada
        return "\n".join(lista)  # Retorna bloque completo