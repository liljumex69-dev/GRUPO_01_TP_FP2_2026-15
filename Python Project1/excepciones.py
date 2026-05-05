# ==============================================================================
# MÓDULO: excepciones.py
# PROPÓSITO: Definir jerarquía de excepciones personalizadas para el sistema
# AUTORES: Alfredo Anthony Chaupis Aquino, Jhon Brando Colca Heredia, Adrian Augusto Cuzcano Escobar,Johnny Alessis Giraldo Suarez
# CURSO: Fundamentos de Programación 2 - IS275
# ==============================================================================

class ErrorLogistica(Exception):
    # Clase base para todas las excepciones del sistema logístico
    # Permite capturar errores específicos sin mezclarlos con errores genéricos
    pass

class PedidoError(ErrorLogistica):
    # Excepción lanzada ante violaciones de reglas de negocio en pedidos
    # Ejemplo: intentar avanzar estado inválido o registrar sin ubicación válida
    pass

class DatosError(ErrorLogistica):
    # Excepción lanzada cuando los datos de entrada fallan validaciones estructurales
    # Ejemplo: direcciones incompletas, RUC inválido o referencias vacías
    pass