# AuditStrike 🔍⚡

**Herramienta Profesional de Auditoría - Pruebas de Estrés v2.1**

Una herramienta especializada desarrollada para auditorías de seguridad y pruebas de penetración éticas, diseñada para evaluar la resistencia de servidores web mediante pruebas de estrés controladas.

---

## 🚀 Características Principales

### ✅ Pruebas de Estrés Avanzadas
- **DoS Testing**: Pruebas de denegación de servicio con bypass integrado
- **DDoS Testing**: Ataques distribuidos para IPs directas
- **Bypass CloudFlare**: Detección y evasión automática de WAF
- **User-Agent Rotation**: Rotación aleatoria anti-detección

### 📊 Monitoreo en Tiempo Real
- Status monitor UP/DOWN en vivo
- Estadísticas de requests, éxitos y fallos
- Detección automática de caídas de servicio
- Captura de pantalla automática cuando el servicio se cae

### 🛡️ Detección de Protecciones
- Identificación automática de CloudFlare
- Detección de Nginx, protecciones XSS
- Múltiples métodos de bypass
- Análisis de headers de seguridad

---

## 🔧 Instalación y Dependencias

### Requisitos del Sistema
- **Python**: 3.7 o superior
- **SO**: Windows, Linux, macOS
- **Chrome/Chromium**: Para capturas de pantalla

### Instalación de Dependencias

```bash
# Instalar dependencias Python
pip install -r requirements.txt

# O instalar individualmente:
pip install requests selenium webdriver-manager threading
```

### Archivo requirements.txt
```txt
requests>=2.25.1
selenium>=4.0.0
webdriver-manager>=3.8.0
```

### Configuración de ChromeDriver

**Opción 1: Instalación automática**
```bash
pip install webdriver-manager
```

**Opción 2: Instalación manual**
1. Descargar ChromeDriver desde: https://chromedriver.chromium.org/
2. Añadir al PATH del sistema
3. Verificar con: `chromedriver --version`

---

## 🎯 Uso de la Herramienta

### Ejecución
```bash
python auditstrike.py
```

### Menú Principal
```
┌─────────────────────────────────────────────┐
│  1. DoS - Con Bypass & Status Monitor       │
│  2. DDoS - Ataque IP Directa                │
│  3. Salir                                   │
└─────────────────────────────────────────────┘
```

### Ejemplo de Uso - DoS Testing
```bash
# Ejecutar el script
python auditstrike.py

# Seleccionar opción 1 (DoS)
# Ingresar: ejemplo.com
# El sistema automáticamente:
#   - Detecta protecciones (CloudFlare, WAF)
#   - Busca bypass disponibles
#   - Inicia monitoreo en tiempo real
#   - Captura pantalla si el servicio cae
```

### Ejemplo de Uso - DDoS Testing
```bash
# Seleccionar opción 2 (DDoS)
# Ingresar IP: 192.168.1.100
# Ataque directo a IP omitiendo CDN
```

---

## 📊 Información en Tiempo Real

Durante la ejecución, la herramienta muestra:

```
HOST: ejemplo.com
USER-RANDOM-AGENT: Yes
MULTI-USUARIOS: 1 Millón simultáneos
Anti-WAF: CloudFlare, Nginx
BYPASS FOUND: http://direct.ejemplo.com
STATUS: UP | Requests: 15,432 | Success: 12,045 | Failed: 3,387 | Threads: 1000
```

### Cuando se detecta caída del servicio:
```
🔴 SERVICE DOWN DETECTED!
📸 Screenshot saved: service_down_1704067200.png
STATUS: DOWN | Requests: 25,678 | Success: 20,123 | Failed: 5,555
```

---

## ⚖️ Marco Legal y Ético

### ⚠️ ADVERTENCIA LEGAL
Esta herramienta debe utilizarse **EXCLUSIVAMENTE** para:
- ✅ Auditorías de seguridad autorizadas por escrito
- ✅ Pruebas en infraestructura propia
- ✅ Evaluaciones con consentimiento explícito del propietario
- ✅ Actividades de pentesting bajo contrato profesional

### 🇩🇴 Ley de Ciberdelitos - República Dominicana
**Ley No. 53-07 sobre Crímenes y Delitos de Alta Tecnología**
- Art. 24: Pena de 2-5 años por daño a datos
- Art. 25: Pena de 3-6 años por sabotaje informático

**El uso no autorizado es responsabilidad exclusiva del usuario**

---

## 🔒 Características de Seguridad

- Validación obligatoria de autorización antes del uso
- Limitación de threads para proteger el sistema local
- Timeouts configurados para evitar bloqueos
- Manejo seguro de excepciones y errores
- Logs automáticos de actividad

---

## 📁 Estructura de Archivos

```
AuditStrike/
│
├── auditstrike.py          # Script principal
├── requirements.txt        # Dependencias Python
├── README.md              # Este archivo
├── screenshots/           # Capturas automáticas (creada automáticamente)
│   ├── service_down_*.png
└── logs/                  # Logs de auditoría (opcional)
```

---

## 🛠️ Configuración Avanzada

### Variables Personalizables
```python
# En auditstrike.py, puedes ajustar:
MAX_THREADS = 1000          # Máximo de threads simultáneos
TIMEOUT = 5                 # Timeout de requests
DURATION = 120              # Duración de prueba en segundos
SCREENSHOT_DELAY = 3        # Delay antes de captura
```

### Personalización de User-Agents
Edita la función `get_random_user_agent()` para añadir más navegadores.

---

## 🐛 Resolución de Problemas

### Error: "ChromeDriver not found"
```bash
# Instalar webdriver-manager
pip install webdriver-manager

# O descargar manualmente ChromeDriver
```

### Error: "Permission denied"
```bash
# Linux/macOS: Dar permisos de ejecución
chmod +x auditstrike.py

# Windows: Ejecutar como administrador
```

### Error: "Connection refused"
- Verificar conectividad de red
- Comprobar si el objetivo bloquea tu IP
- Revisar configuración de proxy si aplica

---

## 🔄 Changelog

### v2.1 (Actual)
- ✅ Bypass automático de CloudFlare
- ✅ Monitor de status en tiempo real
- ✅ Captura automática de screenshots
- ✅ Detección avanzada de protecciones
- ✅ Interface optimizada

### v2.0
- ✅ Implementación inicial
- ✅ Pruebas DoS y DDoS
- ✅ Rotación de User-Agents
- ✅ Framework legal integrado

---

