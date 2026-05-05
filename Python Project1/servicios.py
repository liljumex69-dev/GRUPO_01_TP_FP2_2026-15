# ==============================================================================
# MÓDULO: servicios.py
# PROPÓSITO: Validación estricta de entrada y persistencia auditada
# AUTORES: Alfredo Anthony Chaupis Aquino, Jhon Brando Colca Heredia, Adrian Augusto Cuzcano Escobar,Johnny Alessis Giraldo Suarez
# CURSO: Fundamentos de Programación 2 - IS275
# ==============================================================================

import json  # Módulo estándar para serialización estructurada
import os  # Módulo para gestión de rutas y existencia de archivos

class ValidadorDatos:
    # Clase utilitaria que centraliza reglas de captura para evitar ruido en main.py
    @staticmethod
    def validar_texto_obligatorio(mensaje):
        while True:  # Bucle de reintento hasta cumplir condición
            texto = input(mensaje).strip()  # Lee entrada y elimina espacios laterales
            if len(texto) >= 3:  # Valida longitud mínima para evitar datos basura
                return texto  # Retorna valor limpio
            print("ERROR: Ingrese al menos 3 caracteres válidos.")  # Retroalimentación inmediata

    @staticmethod
    def validar_numero_positivo(mensaje):
        while True:  # Ciclo de validación numérica estricta
            try:
                valor = float(input(mensaje))  # Intenta conversión a flotante
                if valor > 0:  # Verifica positividad matemática
                    return valor  # Retorna número válido
                print("ERROR: El valor debe ser mayor a cero.")  # Mensaje de restricción
            except ValueError:  # Captura entrada alfanumérica accidental
                print("ERROR: Ingrese únicamente números válidos.")  # Guía de corrección

class PersistenciaJSON:
    # Clase responsable de guardar trazas operativas para auditoría y análisis
    ARCHIVO_DATOS = "historial_pedidos_pastipan.json"  # Nombre estandarizado de repositorio

    def guardar_registro(self, datos_pedido):
        try:  # Bloque de protección ante fallos de E/S
            if os.path.exists(self.ARCHIVO_DATOS):  # Verifica existencia previa
                with open(self.ARCHIVO_DATOS, 'r', encoding='utf-8') as archivo:
                    lista_pedidos = json.load(archivo)  # Deserializa contenido actual
            else:
                lista_pedidos = []  # Inicializa colección vacía en primera ejecución
            lista_pedidos.append(datos_pedido)  # Agrega nuevo registro al final
            with open(self.ARCHIVO_DATOS, 'w', encoding='utf-8') as archivo:
                json.dump(lista_pedidos, archivo, indent=4, ensure_ascii=False)  # Serializa con formato legible
        except Exception as e:
            print(f"ERROR DE PERSISTENCIA: {e}")  # Registro de fallo sin interrumpir flujo

    def cargar_historial(self):
        if os.path.exists(self.ARCHIVO_DATOS):  # Comprueba disponibilidad de datos
            try:
                with open(self.ARCHIVO_DATOS, 'r', encoding='utf-8') as archivo:
                    return json.load(archivo)  # Retorna lista de registros históricos
            except json.JSONDecodeError:
                return []  # Retorna vacío si archivo está corrupto
        return []  # Retorna vacío si no existe archivo