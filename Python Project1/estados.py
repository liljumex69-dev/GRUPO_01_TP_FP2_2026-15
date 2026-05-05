# ==============================================================================
# MÓDULO: estados.py
# PROPÓSITO: Implementar el Patrón State para gestionar transiciones del ciclo de vida del pedido
# AUTORES: Alfredo Anthony Chaupis Aquino, Jhon Brando Colca Heredia, Adrian Augusto Cuzcano Escobar,Johnny Alessis Giraldo Suarez
# CURSO: Fundamentos de Programación 2 - IS275
# ==============================================================================

from abc import ABC, abstractmethod  # Herramientas para abstracción de comportamiento

class EstadoPedido(ABC):
    # Clase abstracta que define el contrato de transición entre fases operativas
    @abstractmethod
    def siguiente(self, pedido):
        # Cada estado concreto decide a qué fase avanza el pedido
        pass

    def __str__(self):
        return self.__class__.__name__  # Retorna nombre de la clase para UI

class PedidoRegistrado(EstadoPedido):
    # Fase inicial: pedido ingresado, pendiente de validación de stock y ubicación
    def siguiente(self, pedido):
        from estados import Confirmado  # Importación local para evitar ciclos
        pedido._estado = Confirmado()  # Transición automática tras validación exitosa

class Confirmado(EstadoPedido):
    # Fase de producción: ingredientes verificados, orden en cola de cocina
    def siguiente(self, pedido):
        from estados import EnPreparacion  # Importación segura
        pedido._estado = EnPreparacion()  # Avance a línea de preparación

class EnPreparacion(EstadoPedido):
    # Fase operativa: productos en horno/montaje, control de calidad en curso
    def siguiente(self, pedido):
        from estados import ListoParaDespacho  # Importación diferida
        pedido._estado = ListoParaDespacho()  # Paso a zona de empaque y asignación

class ListoParaDespacho(EstadoPedido):
    # Fase logística: pedido empacado, conductor asignado, ruta optimizada
    def siguiente(self, pedido):
        from estados import EnRuta  # Importación local
        pedido._estado = EnRuta()  # Salida física del centro de distribución

class EnRuta(EstadoPedido):
    # Fase de tránsito: vehículo en movimiento hacia coordenadas de entrega
    def siguiente(self, pedido):
        from estados import Entregado  # Importación segura
        pedido._estado = Entregado()  # Confirmación de recepción física

class Entregado(EstadoPedido):
    # Fase terminal: cliente confirma recepción, cierra ciclo operativo
    def siguiente(self, pedido):
        from excepciones import PedidoError  # Importación de dominio
        raise PedidoError("El pedido ya fue entregado. No se permiten transiciones posteriores.")

class Cancelado(EstadoPedido):
    # Fase de excepción: pedido anulado por cliente o falta de stock
    def siguiente(self, pedido):
        from excepciones import PedidoError  # Importación de dominio
        raise PedidoError("No se puede avanzar un pedido en estado cancelado.")