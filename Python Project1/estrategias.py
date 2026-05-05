# ==============================================================================
# MÓDULO: estrategias.py
# PROPÓSITO: Implementar el Patrón Strategy para cálculo dinámico de costos de envío
# AUTORES: Alfredo Anthony Chaupis Aquino, Jhon Brando Colca Heredia, Adrian Augusto Cuzcano Escobar,Johnny Alessis Giraldo Suarez
# CURSO: Fundamentos de Programación 2 - IS275
# ==============================================================================

from abc import ABC, abstractmethod  # Importamos módulos para definir interfaces abstractas

class CalculadorCostoEnvio(ABC):
    # Clase abstracta que define el contrato común para todas las estrategias de envío
    # Garantiza polimorfismo seguro en la clase Pedido
    @abstractmethod
    def calcular(self, peso_total):
        # Método abstracto: cada estrategia define su propia fórmula de costo
        pass

    @abstractmethod
    def obtener_nombre(self):
        # Método abstracto: retorna etiqueta legible para reportes y UI
        pass

class EntregaLocal(CalculadorCostoEnvio):
    # Estrategia para clientes que recogen en tienda física
    # Elimina costo logístico y complejidad de ruta
    def calcular(self, peso_total):
        return 0.00  # Sin costo de transporte para recojo directo

    def obtener_nombre(self):
        return "Recojo en Tienda"  # Etiqueta para facturas y comprobantes

class DeliveryEstandar(CalculadorCostoEnvio):
    # Estrategia para despachos en zona metropolitana regular (24-48h)
    # Tarifa base más variable por peso volumétrico
    def calcular(self, peso_total):
        return 8.00 + (peso_total * 1.50)  # S/. 8 base + S/. 1.50/kg

    def obtener_nombre(self):
        return "Delivery Estándar"  # Identificador en hoja de despacho

class DeliveryExpress(CalculadorCostoEnvio):
    # Estrategia para entregas urgentes o productos perecibles prioritarios
    # Penaliza costo por velocidad de respuesta logística
    def calcular(self, peso_total):
        return 15.00 + (peso_total * 2.50)  # S/. 15 base + S/. 2.50/kg

    def obtener_nombre(self):
        return "Delivery Express (Mismo Día)"  # Etiqueta diferenciada

class EntregaCorporativa(CalculadorCostoEnvio):
    # Estrategia optimizada para pedidos B2B con rutas programadas
    # Precio fijo hasta umbral de peso, luego tarifa marginal reducida
    def calcular(self, peso_total):
        if peso_total <= 20:
            return 20.00  # Tarifa plana corporativa hasta 20kg
        return 20.00 + ((peso_total - 20) * 1.00)  # Excedente a S/. 1/kg

    def obtener_nombre(self):
        return "Entrega Corporativa Programada"  # Identificador B2B