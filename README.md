# 🤝 LinkedIn Networking Suite

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/[tu-usuario]/linkedin-networking-suite?style=social)](https://github.com/[tu-usuario]/linkedin-networking-suite/stargazers)

> Una suite completa de Python para organizar y mejorar tu networking con recruiters de IT en LinkedIn de manera **legítima y efectiva**.

[English](#english-version) | [Español](#versión-en-español)

---

## 📸 Capturas de Pantalla / Screenshots

<div align="center">

![Menú Principal](https://github.com/[tu-usuario]/linkedin-networking-suite/blob/main/screenshots/menu_principal.png)
*Menú Principal*

![Gestión de Contactos](https://github.com/[tu-usuario]/linkedin-networking-suite/blob/main/screenshots/contactos.png)
*Gestión de Contactos*

![Estadísticas](https://github.com/[tu-usuario]/linkedin-networking-suite/blob/main/screenshots/estadisticas.png)
*Estadísticas y Análisis*

</div>

---

## ✨ Características / Features

### 🎯 Core Features
- **📥 Importación Automática**: Importa todas tus conexiones de LinkedIn en segundos (método oficial CSV)
- **💬 Generador de Mensajes**: Templates personalizables para conectar y hacer follow-up
- **⏰ Sistema de Recordatorios**: Nunca olvides un follow-up importante
- **📊 Exportación a Excel**: Análisis completo de tu red de contactos
- **📈 Estadísticas**: Métricas sobre tu networking y tasa de respuesta
- **🔍 Búsqueda Avanzada**: Encuentra contactos por empresa, cargo, habilidades

### 🌟 Why This Tool?
- ✅ **100% Legal**: Usa el exportador oficial de LinkedIn (no scraping)
- ✅ **Privacy First**: Todos tus datos se almacenan localmente
- ✅ **Open Source**: Código libre y modificable
- ✅ **No API Required**: No necesita aprobación de LinkedIn
- ✅ **Cross-platform**: Funciona en Windows, Mac, Linux


---

## 🛠️ Instalación / Installation

### Requisitos Previos / Prerequisites

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/[tu-usuario]/linkedin-networking-suite.git
cd linkedin-networking-suite
```

### Paso 2: Crear Entorno Virtual (Opcional pero Recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar

```bash
# Copiar archivo de configuración
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# Editar .env según tus prefericiones (opcional)
```

### Paso 5: Ejecutar

```bash
python main.py
```

---

## 📖 Cómo Usar / How to Use

### Flujo Básico / Basic Workflow

1. **Exportar tus conexiones desde LinkedIn**
   - Perfil → Configuración → Datos → "Obtener copia de mis datos"
   - Selecciona "Conexiones" → Formato CSV
   - Espera el email (10 min - 24 horas)

2. **Importar a la Suite**
   ```bash
   python main.py
   → 6 (Importar desde LinkedIn)
   → 2 (Importar archivo CSV)
   → [nombre del CSV]
   → Confirmar
   ```

3. **Generar Mensajes Personalizados**
   ```bash
   → 2 (Generador de Mensajes)
   → 1 (Mensaje de conexión)
   → Selecciona contacto
   → Elige template
   → Copiar y pegar en LinkedIn
   ```

4. **Configurar Recordatorios**
   ```bash
   → 3 (Recordatorios)
   → 2 (Crear recordatorio)
   → Selecciona contacto y días
   ```

5. **Exportar y Analizar**
   ```bash
   → 4 (Exportar Datos)
   → 5 (Reporte completo)
   ```

### Guías Completas / Complete Guides

- 📘 [Guía de Importación](GUIA_IMPORTACION.md)
- 📗 [Cómo Exportar desde LinkedIn](COMO_EXPORTAR_LINKEDIN.md)

---

## 📁 Estructura del Proyecto / Project Structure

```
linkedin-networking-suite/
├── main.py                 # Aplicación principal
├── database.py             # Módulo de base de datos (SQLite)
├── message_generator.py    # Generador de mensajes
├── reminder_system.py      # Sistema de recordatorios
├── export_manager.py       # Exportación a Excel
├── csv_importer.py         # Importador de CSV de LinkedIn
├── requirements.txt        # Dependencias
├── .env.example           # Configuración de ejemplo
├── .gitignore             # Archivos ignorados por Git
├── LICENSE                # Licencia MIT
├── README.md              # Este archivo
├── GUIA_IMPORTACION.md    # Guía de importación
├── COMO_EXPORTAR_LINKEDIN.md  # Guía de exportación
├── ejemplo_contactos.csv  # CSV de ejemplo
└── data/                  # Directorio de datos (creado automáticamente)
    └── contacts.db        # Base de datos SQLite
```

---

## 🎨 Tecnologías Usadas / Tech Stack

- **Python 3.8+**: Lenguaje principal
- **SQLite**: Base de datos local
- **Pandas**: Manejo y análisis de datos
- **OpenPyXL**: Exportación a Excel
- **python-dotenv**: Manejo de variables de entorno

---

## 📊 Roadmap

- [ ] Interfaz web con Flask/FastAPI
- [ ] Integración con Gmail para seguimiento por email
- [ ] Sistema de etiquetas y categorías
- [ ] Análisis con IA de mejores momentos para contactar
- [ ] Integración con calendario (Google Calendar)
- [ ] Modo multi-usuario

---

## 🤝 Contribuir / Contributing

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles (opcional).

---

## 📝 Licencia / License

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

## ⚠️ Disclaimer / Aviso Legal

Esta herramienta está diseñada exclusivamente para fines organizativos y educativos. **NO**:

- ❌ Automatiza conexiones en LinkedIn
- ❌ Hace scraping de LinkedIn
- ❌ Envía mensajes automáticamente
- ❌ Violata términos de servicio de LinkedIn

Esta herramienta **SÍ**:

- ✅ Organiza contactos manualmente agregados
- ✅ Genera mensajes que tú envías manualmente
- ✅ Hace seguimiento de interacciones
- ✅ Te recuerda hacer follow-up

Úsala bajo tu propia responsabilidad y de acuerdo con los términos de servicio de LinkedIn.

---

## 🙏 Agradecimientos / Acknowledgments

- Inspirado por la necesidad real de organizar networking de IT
- Construido con Python y amor al código limpio
- Gracias a todos los que contribuyen al proyecto

---

## 📧 Contacto / Contact

- **Author**: Luciano Paz
- **GitHub**: @LucianoPazG https://github.com/LucianoPazG
- **LinkedIn**: https://www.linkedin.com/in/luciano-paz-593803230/

---

## ⭐ ¡Si te gusta el proyecto, dale una estrella! / If you like this project, give it a star!

[![GitHub Stars](https://img.shields.io/github/stars/[tu-usuario]/linkedin-networking-suite?style=social)](https://github.com/[tu-usuario]/linkedin-networking-suite/stargazers)

---

<div align="center">

**Hecho con ❤️ por Luciano Paz**

</div>

---

# English Version

## 🤝 LinkedIn Networking Suite

> Complete Python suite to organize and improve your networking with IT recruiters on LinkedIn in a **legitimate and effective** way.

---

## ✨ Features

### Core Capabilities
- **📥 Auto Import**: Import all your LinkedIn connections in seconds (official CSV method)
- **💬 Message Generator**: Customizable templates for connections and follow-ups
- **⏰ Reminder System**: Never forget an important follow-up
- **📊 Excel Export**: Complete analysis of your network
- **📈 Statistics**: Metrics on your networking and response rates
- **🔍 Advanced Search**: Find contacts by company, role, skills

### Why This Tool?
- ✅ **100% Legal**: Uses LinkedIn's official exporter (no scraping)
- ✅ **Privacy First**: All your data stored locally
- ✅ **Open Source**: Free and modifiable code
- ✅ **No API Required**: No LinkedIn approval needed
- ✅ **Cross-platform**: Works on Windows, Mac, Linux

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Quick Start

```bash
# Clone the repository
git clone https://github.com/[your-username]/linkedin-networking-suite.git
cd linkedin-networking-suite

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env

# Run
python main.py
```

---

## 📖 How to Use

### Basic Workflow

1. **Export your LinkedIn connections**
   - Profile → Settings → Data → "Get a copy of your data"
   - Select "Connections" → CSV format
   - Wait for email (10 min - 24 hours)

2. **Import to the Suite**
   ```bash
   python main.py
   → 6 (Import from LinkedIn)
   → 2 (Import CSV file)
   → [CSV filename]
   → Confirm
   ```

3. **Generate Personalized Messages**
   ```bash
   → 2 (Message Generator)
   → 1 (Connection message)
   → Select contact
   → Choose template
   → Copy and paste to LinkedIn
   ```

4. **Set Reminders**
   ```bash
   → 3 (Reminders)
   → 2 (Create reminder)
   → Select contact and days
   ```

5. **Export and Analyze**
   ```bash
   → 4 (Export Data)
   → 5 (Full report)
   ```

---

## 🎨 Tech Stack

- **Python 3.8+**: Main language
- **SQLite**: Local database
- **Pandas**: Data handling and analysis
- **OpenPyXL**: Excel export
- **python-dotenv**: Environment variables

---

## 📊 Roadmap

- [ ] Web interface with Flask/FastAPI
- [ ] Gmail integration for email follow-up
- [ ] Tags and categories system
- [ ] AI-powered best time to contact analysis
- [ ] Calendar integration (Google Calendar)
- [ ] Multi-user mode

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

This tool is designed exclusively for organizational and educational purposes. It **DOES NOT**:

- ❌ Automate LinkedIn connections
- ❌ Scrape LinkedIn
- ❌ Send messages automatically
- ❌ Violate LinkedIn Terms of Service

This tool **DOES**:

- ✅ Organize manually added contacts
- ✅ Generate messages that you send manually
- ✅ Track interactions
- ✅ Remind you to follow up

Use at your own risk and in accordance with LinkedIn's Terms of Service.

---

## 📧 Contact

- **Author**: Luciano Paz
- **GitHub**: @LucianoPazG https://github.com/LucianoPazG
- **LinkedIn**: https://www.linkedin.com/in/luciano-paz-593803230/

---

## ⭐ If you like this project, give it a star!

<div align="center">

**Made with ❤️ by Luciano Paz**

</div>
