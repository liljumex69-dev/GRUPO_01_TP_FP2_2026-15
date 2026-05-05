# ==============================================================================
# MÓDULO: test_negocio.py
# PROPÓSITO: Pruebas unitarias para validar lógica de negocio y comportamiento de clases
# AUTORES: Alfredo Anthony Chaupis Aquino, Jhon Brando Colca Heredia, Adrian Augusto Cuzcano Escobar,Johnny Alessis Giraldo Suarez
# CURSO: Fundamentos de Programación 2 - IS275
# ==============================================================================

import unittest
from entidades import Cliente, DireccionEntrega, ItemPedido, CatalogoProductos
from estrategias import DeliveryEstandar, EntregaCorporativa
from estados import PedidoRegistrado, Confirmado, Entregado
from gestor import Pedido
from excepciones import PedidoError, DatosError

class TestLogisticaNegocio(unittest.TestCase):
    # Suite de pruebas que valida el cumplimiento de reglas de negocio y patrones

    def setUp(self):
        # Configuración inicial reutilizable para cada prueba
        direccion = DireccionEntrega("Av. Javier Prado", "Con Las Begonias", "Frente a Real Plaza", "San Isidro")
        self.cliente = Cliente("CLI-001", "María González", "987654321", direccion)
        self.pedido = Pedido("PED-TEST-01", self.cliente, "estandar")

    def test_calculo_total_con_delivery_estandar(self):
        # Valida que el cálculo de productos + envío sea matemáticamente correcto
        item1 = ItemPedido("Torta Chocolate", 1, 45.00, "Tortas")
        item2 = ItemPedido("Empanadas", 2, 18.00, "Bocaditos")
        self.pedido.agregar_item(item1)
        self.pedido.agregar_item(item2)
        # Productos: 45 + 36 = 81. Peso: 3kg. Envío: 8 + (3*1.5) = 12.5. Total: 93.5
        esperado = 93.50
        obtenido = self.pedido.calcular_total_pedido()
        self.assertAlmostEqual(esperado, obtenido, places=2, msg="El cálculo de total no coincide con la fórmula de negocio")

    def test_aplicacion_descuento_corporativo(self):
        # Valida que la herencia y polimorfismo apliquen descuento B2B correctamente
        from entidades import ClienteCorporativo
        dir_corp = DireccionEntrega("Av. Canaval", "Con Los Sauces", "Torre Norte", "San Isidro")
        cliente_corp = ClienteCorporativo("CORP-001", "Empresa SAC", "01-2345678", dir_corp, "20123456789", "Carlos M.")
        pedido_corp = Pedido("PED-CORP-01", cliente_corp, "corporativo")
        # CORRECCIÓN: Se quitó el paréntesis extra al final
        pedido_corp.agregar_item(ItemPedido("Desayuno Premium", 50, 18.00, "Corporativo"))
        
        # CÁLCULO REAL:
        # Subtotal: 50 * 18 = 900.
        # Peso: 50kg -> Envío Corporativo: 20 + (30*1) = 50.
        # Total Bruto: 950. Descuento 10% sobre total: 95.
        # Total Final: 855.
        esperado = 855.00  # <-- AQUÍ ESTÁ EL CAMBIO PRINCIPAL
        
        obtenido = pedido_corp.calcular_total_pedido()
        self.assertAlmostEqual(esperado, obtenido, places=2, msg="El descuento corporativo no se aplicó correctamente")

    def test_transicion_estados_valida(self):
        # Valida el Patrón State: transición secuencial sin errores
        estado_inicial = self.pedido._estado
        self.assertIsInstance(estado_inicial, PedidoRegistrado, msg="Estado inicial incorrecto")
        self.pedido.avanzar_estado()
        self.assertIsInstance(self.pedido._estado, Confirmado, msg="Transición a Confirmado falló")

    def test_estado_terminal_bloquea_avance(self):
        # Valida que Entregado lance excepción al intentar avanzar (integridad de negocio)
        self.pedido._estado = Entregado()
        with self.assertRaises(PedidoError, msg="No se lanzó excepción al avanzar estado terminal"):
            self.pedido.avanzar_estado()

    def test_direccion_incompleta_lanza_error(self):
        # Valida validación estricta de ubicación (problema operativo real)
        direccion_mala = DireccionEntrega("Av. Larco", "", "", "Miraflores")
        with self.assertRaises(DatosError, msg="Se permitió dirección incompleta"):
            direccion_mala.validar_integridad()

if __name__ == "__main__":
    unittest.main(verbosity=2)  # Ejecuta pruebas con salida detallada