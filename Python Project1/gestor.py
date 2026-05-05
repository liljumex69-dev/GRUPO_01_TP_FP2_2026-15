# ==============================================================================
# MÓDULO: gestor.py
# PROPÓSITO: Núcleo de negocio, orquestación de pedidos y generación de hojas de despacho
# AUTORES: Alfredo Anthony Chaupis Aquino, Jhon Brando Colca Heredia, Adrian Augusto Cuzcano Escobar,Johnny Alessis Giraldo Suarez
# CURSO: Fundamentos de Programación 2 - IS275
# ==============================================================================

from entidades import Cliente, ClienteCorporativo, ItemPedido, CatalogoProductos, DireccionEntrega
from estados import PedidoRegistrado
from estrategias import EntregaLocal, DeliveryEstandar, DeliveryExpress, EntregaCorporativa
from servicios import PersistenciaJSON
from excepciones import PedidoError

class Pedido:
    # Clase principal que encapsula datos del cliente, items, estado y estrategia de despacho
    def __init__(self, id_pedido, cliente, tipo_entrega="Estandar"):
        self.id_pedido = id_pedido  # Identificador único con prefijo operativo
        self.cliente = cliente  # Referencia a objeto Cliente o ClienteCorporativo
        self.lista_items = []  # Contenedor de líneas de detalle
        self._estado = PedidoRegistrado()  # Estado inicial antes de validación
        self._mapear_estrategia(tipo_entrega)  # Asigna calculador de costo según selección

    def _mapear_estrategia(self, tipo):
        # Método privado que selecciona polimórficamente la estrategia de envío
        mapa = {
            "local": EntregaLocal(),
            "express": DeliveryExpress(),
            "corporativo": EntregaCorporativa()
        }
        self.estrategia_envio = mapa.get(tipo.lower(), DeliveryEstandar())  # Default a estándar

    def agregar_item(self, item):
        self.lista_items.append(item)  # Incorpora línea al detalle del pedido

    def calcular_total_pedido(self):
        suma_productos = sum(item.obtener_subtotal() for item in self.lista_items)  # Acumula subtotales
        peso_total = sum(item.cantidad for item in self.lista_items)  # Estima peso volumétrico (1kg/unidad)
        costo_envio = self.estrategia_envio.calcular(peso_total)  # Aplica fórmula polimórfica
        total_base = suma_productos + costo_envio  # Suma productos + logística
        if isinstance(self.cliente, ClienteCorporativo):  # Verifica segmento B2B
            total_base = self.cliente.aplicar_descuento(total_base)  # Aplica bonificación contractual
        return total_base  # Retorna monto final validado

    def avanzar_estado(self):
        self._estado.siguiente(self)  # Delega transición al objeto estado actual

    def generar_hoja_despacho(self):
        # Método que imprime formato estandarizado para conductor y Call Center
        print("\n" + "=" * 60)
        print(f"HOJA DE DESPACHO - {self.id_pedido}")
        print("=" * 60)
        print(f"CLIENTE: {self.cliente.nombre}")
        print(f"TELÉFONO: {self.cliente.telefono}")
        if isinstance(self.cliente, ClienteCorporativo):
            print(f"CONTACTO RECEPCIÓN: {self.cliente.contacto_compras}")
        print(f"DIRECCIÓN EXACTA: {self.cliente.direccion}")
        print(f"TIPO ENTREGA: {self.estrategia_envio.obtener_nombre()}")
        print("-" * 60)
        print("DETALLE DE PRODUCTOS:")
        for item in self.lista_items:
            print(f"  - {item}")
        print("-" * 60)
        print(f"TOTAL A COBRAR: S/. {self.calcular_total_pedido():.2f}")
        print("FIRMA CONFORMIDAD CLIENTE: _______________________")
        print("=" * 60)

    def __str__(self):
        items_str = "\n    - ".join([str(item) for item in self.lista_items])
        return (f"--- Pedido #{self.id_pedido} ---\n"
                f"  Cliente: {self.cliente.nombre}\n"
                f"  Estado: {self._estado}\n"
                f"  Envío: {self.estrategia_envio.obtener_nombre()}\n"
                f"  Items:\n    - {items_str}\n"
                f"  TOTAL FINAL: S/. {self.calcular_total_pedido():.2f}\n")

class GestorDespacho:
    # Fachada que administra colección de pedidos y persistencia
    def __init__(self):
        self.coleccion_pedidos = []  # Lista en memoria para sesión activa

    def registrar_pedido(self, pedido):
        if not pedido.lista_items:
            raise PedidoError("No se puede registrar un pedido sin productos.")
        pedido.cliente.direccion.validar_integridad()  # Fuerza validación geográfica antes de guardar
        self.coleccion_pedidos.append(pedido)  # Agrega a colección operativa
        persistencia = PersistenciaJSON()  # Instancia servicio de trazabilidad
        persistencia.guardar_registro({  # Guarda resumen para auditoría
            "id": pedido.id_pedido,
            "cliente": pedido.cliente.nombre,
            "direccion": str(pedido.cliente.direccion),
            "total": pedido.calcular_total_pedido(),
            "estado": str(pedido._estado)
        })

    def buscar_pedido(self, id_busqueda):
        for pedido in self.coleccion_pedidos:
            if pedido.id_pedido == id_busqueda:
                return pedido  # Retorna referencia directa si coincide
        return None  # Retorna nulo si no hay coincidencia

    def listar_pedidos(self):
        if not self.coleccion_pedidos:
            print("INFO: No hay pedidos registrados en la sesión actual.")
            return
        for p in self.coleccion_pedidos:
            print(p)
            print("-" * 40)