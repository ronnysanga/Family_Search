# Family Search

Aplicación de gestión de árboles genealógicos que permite registrar personas y sus relaciones familiares de forma intuitiva.

## 🚀 Características

- Registro de personas con información detallada
- Gestión de relaciones familiares (padres, madres, cónyuges, hermanos)
- Visualización de árbol genealógico ascendente
- Búsqueda avanzada de personas
- Interfaz de línea de comandos (CLI) intuitiva

## 🛠️ Requisitos Previos

- Python 3.8 o superior
- MySQL 8.0 o superior
- pip (gestor de paquetes de Python)

## 🚀 Configuración Inicial

1. **Clonar el repositorio**
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd Family_Search
   ```

2. **Crear y activar entorno virtual (recomendado)**
   ```bash
   # En Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate

   # En Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**
   - Crear una base de datos MySQL llamada `family_search`
   - Copiar el archivo `.env.example` a `.env`
   - Configurar las credenciales en el archivo `.env`:
     ```
     HOSTNAME=localhost
     DB_PORT=3306
     USERNAME=tu_usuario
     PASSWORD=tu_contraseña
     DATABASE=family_search
     ```

5. **Población inicial (opcional)**
   El proyecto incluye scripts para poblar la base de datos con información de ejemplo. Esto es útil para pruebas iniciales.
   ```bash
   # Ejecutar script de población (si está disponible)
   # python scripts/populate_database.py
   ```

## 🏃‍♂️ Ejecutar la Aplicación

```bash
python app.py
```

## 🗃️ Estructura del Proyecto

```
Family_Search/
├── database/           # Configuración de la base de datos
├── models/             # Modelos de datos
├── services/           # Lógica de negocio
├── utils/              # Utilidades y helpers
├── views/              # Vistas y menús
│   ├── family_tree/    # Vistas del árbol genealógico
│   ├── person/         # Vistas de personas
│   └── menus/          # Menús de navegación
├── .env.example        # Ejemplo de configuración
├── app.py             # Punto de entrada de la aplicación
└── requirements.txt    # Dependencias del proyecto
```

## 🔍 Uso

1. **Registrar una nueva persona**
   - Seleccione la opción de registro en el menú principal
   - Complete la información solicitada

2. **Gestionar relaciones familiares**
   - Acceda al menú de relaciones familiares
   - Seleccione dos personas y el tipo de relación
   - La aplicación manejará automáticamente las relaciones recíprocas

3. **Visualizar árbol genealógico**
   - Seleccione la opción de árbol genealógico
   - Elija ver su propio árbol o buscar una persona específica

## 📝 Notas Adicionales

- Se recomienda realizar copias de seguridad periódicas de la base de datos
- El proyecto está en desarrollo activo, pueden existir características en desarrollo
- Para problemas o sugerencias, por favor abra un issue en el repositorio