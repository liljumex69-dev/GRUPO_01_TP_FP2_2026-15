# 📦 Sistema de Gestión Logística para Pastipan

> **Optimización del Proceso de Registro de Pedidos y Despacho mediante Programación Orientada a Objetos**

## 🎓 Contexto Académico
- **Curso:** IS275 – Fundamentos de Programación 2
- **Universidad:** Universidad Peruana de Ciencias Aplicadas (UPC)
- **Ciclo Académico:** 2026-15
- **Modalidad:** EPE – Ingeniería de Sistemas
- **Tipo de Entregable:** Trabajo Parcial / Final (Hito 1 y 2)

## 🏢 Empresa & Problemática Identificada
**Pastipan** es una empresa dedicada a la panificación y venta de bocaditos, con clientes minoristas y corporativos.  
🔍 **Problema Real:** El Call Center registra pedidos con direcciones incompletas (omitiendo cruces, referencias visibles y notas de acceso). Esto genera:
- ⏱️ Pérdida de 15-20 min/pedido en triangulación conductor–Call Center
- 💸 Aumento de costos operativos (combustible + horas-hombre)
- 📉 30% menos entregas efectivas por día
- 😞 Deterioro en la experiencia del cliente y frescura de productos

## ✨ Solución Propuesta
Sistema modular en **Python** que obliga la captura estructurada de ubicaciones, diferencia flujos retail/B2B, calcula costos de envío dinámicamente y gestiona el ciclo de vida del pedido con trazabilidad completa.

### ✅ Características Principales
- 📍 **Validación Estricta de Ubicación:** Bloquea registros si faltan calle, cruces, referencia o distrito.
- 🏢 **Diferenciación de Segmentos:** Formularios y reglas específicas para clientes minoristas vs. corporativos.
- 💰 **Descuento Automático B2B:** 10% aplicado polimórficamente en pedidos corporativos.
- 🚚 **Cálculo Dinámico de Envío:** Patrón `Strategy` con 4 modalidades (Local, Estándar, Express, Corporativa).
- 🔄 **Gestión de Estados Controlada:** Patrón `State` (`Registrado → Confirmado → Preparación → Ruta → Entregado`).
- 📄 **Hoja de Despacho Estandarizada:** Formato autoexplicativo para conductores (elimina llamadas de coordinación).
- 🧪 **Pruebas Unitarias:** `unittest` validando cálculos, descuentos, transiciones y validaciones.
- 💾 **Persistencia Ligera:** Historial en JSON para auditoría y análisis post-mortem.

## 🏗️ Arquitectura y Estructura del Proyecto
```text
GRUPO_XX_TP_FP2_2026-15/
├── 📄 README.md                          # Documentación técnica
├──  .gitignore                         # Configuración para ignorar archivos basura
│
├── 📁 PROYECTO_PASTIPAN/                 # CÓDIGO FUENTE PYTHON
│   ├── entidades.py                      # Modelo de dominio
│   ├── estados.py                        # Patrón State
│   ├── estrategias.py                    # Patrón Strategy
│   ├── excepciones.py                    # Jerarquía personalizada
│   ├── gestor.py                         # Núcleo de negocio
│   ├── main.py                           # Interfaz CLI + menú
│   ├── servicios.py                      # ValidadorDatos + PersistenciaJSON
│   └── test_negocio.py                   # Pruebas unitarias
│
└── 📁 DOCUMENTACION/                     # ENTREGABLES ACADÉMICOS
    ├── INFORME_PARCIAL.docx              # Informe estructurado
    ├── UML_DIAGRAMAS/                    # Diagramas exportados
    │   ├── diagrama_clases_general.png
    │   ├── diagrama_state.png
    │   └── diagrama_strategy.png
    └── EVIDENCIAS/                       # Capturas de sistema, Trello
```

## 🚀 Instalación y Ejecución
**Requisitos:** Python 3.8+ | Sin dependencias externas (biblioteca estándar)

```bash
# 1. Clonar o descargar el repositorio
git clone https://github.com/TU_USUARIO/GRUPO_XX_TP_FP2_2026-15.git
cd GRUPO_XX_TP_FP2_2026-15/PROYECTO_PASTIPAN

# 2. Ejecutar el sistema principal
python main.py

# 3. Seguir el menú interactivo (6 opciones):
#    1. Registrar Pedido Minorista
#    2. Registrar Pedido Corporativo
#    3. Buscar Pedido
#    4. Listar Pedidos
#    5. Avanzar Estado (Producción)
#    6. Salir
```

## 🧪 Pruebas Unitarias
Validación automática de lógica de negocio:
```bash
python -m unittest test_negocio.py -v
```

**Cobertura:**
- `test_calculo_total_con_delivery_estandar` → Cálculo matemático correcto
- `test_aplicacion_descuento_corporativo` → Herencia + polimorfismo B2B
- `test_transicion_estados_valida` → Patrón State
- `test_estado_terminal_bloquea_avance` → Integridad de negocio
- `test_direccion_incompleta_lanza_error` → Validación estricta

## 📚 Documentación y Entregables
- 📘 **Informe Word:** Estructura completa según rúbrica IS275 (Capítulos 1-2, Bibliografía APA, Anexos)
- 🎨 **Diagramas UML:** Generados con Mermaid (Clases, State, Strategy, Secuencia)
- 📊 **Gestión de Proyecto:** Tablero Trello con asignación por rol, cronograma y evidencias
-  **Control de Versiones:** GitHub con commits trazables por integrante
- 🎥 **Video Demostrativo:** [PEGAR ENLACE A YOUTUBE/DRIVE] (3-4 min)

## 👥 Equipo de Desarrollo

| Integrante | Archivos Python | Documentación | Gestión |
|------------|----------------|---------------|---------|
| **Anthony Chaupis Anquino** | `entidades.py`, `gestor.py` | Análisis (1.1), Objetivos (1.2) | Coordinación |
| **Jhonny Giraldo Suarez** | `servicios.py`, `excepciones.py`, `test_negocio.py` | Funcionalidades/HU (1.3) | Pruebas de calidad |
| **Adrian Cuscano Escobar** | `estrategias.py` | Bibliografía, Anexos, Diagramas UML | Diseño técnico |
| **Jhon Colca Heredia** | `main.py`, `estados.py` | Introducción, Cronograma (1.4), Flujo (2.1) | Trello, Git, Capturas |

---
**Contacto:** [U202524321@upc.edu.pe] | **Repositorio:** https://github.com/lijumex69-dev/GRUPO_01_TP_FP2_2026-15
```
