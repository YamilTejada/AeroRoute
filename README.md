# AeroRoute - Optimizador de Rutas y Redes de Vuelo

AeroRoute es una aplicación web interactiva que permite visualizar aeropuertos y rutas aéreas globales sobre un mapa tridimensional de alto rendimiento, optimizar rutas de vuelo usando algoritmos de grafos (BFS y Dijkstra), y calcular redes de expansión mínima (MST) a través del algoritmo de Kruskal.

La aplicación cuenta con una arquitectura de base de datos híbrida (Supabase en la nube con fallback automático a SQLite local) lo que garantiza su funcionamiento sin conexión o ante caídas del servicio cloud.

---

## 🛠️ Tecnologías Utilizadas

### Backend (Python)
* **FastAPI**: Framework web rápido y moderno para la creación de la API.
* **SQLAlchemy**: ORM para interactuar con la base de datos de manera agnóstica (PostgreSQL / SQLite).
* **Uvicorn**: Servidor ASGI para ejecutar la aplicación FastAPI.
* **SQLite / PostgreSQL (Supabase)**: Motores de base de datos para persistencia de datos.

### Frontend (React + JavaScript)
* **React 19**: Librería para construir la interfaz de usuario de forma modular y reactiva.
* **Vite**: Herramienta de compilación rápida para el frontend.
* **Deck.gl**: Biblioteca de visualización de mapas WebGL de alto rendimiento, ideal para renderizar miles de aeropuertos y arcos de rutas en 3D.
* **Tailwind CSS v4**: Framework de diseño y estilos modernos.
* **Axios**: Cliente HTTP para realizar peticiones a la API del backend.

---

## 📐 Cómo Funciona y Arquitectura

1. **Gestión de Datos e Ingesta:**
   Al iniciar, el backend intenta conectarse a la base de datos de **Supabase (PostgreSQL)** en la nube. 
   * **Si está disponible:** Trabaja directamente en la nube.
   * **Si está caída o inactiva (Fallback local):** Cambia automáticamente a una base de datos local **SQLite** (`local_airports.db`). Si esta base de datos local está vacía, el sistema lee los archivos CSV (`airports.csv` y `routes.csv` ubicados en `backend/data/`), importa todos los datos (1,772 aeropuertos y 16,696 rutas) y los guarda localmente para futuros inicios rápidos.

2. **Algoritmos de Grafos Implementados:**
   * **BFS (Breadth-First Search / Búsqueda en Amplitud):** Calcula la ruta óptima minimizando la cantidad de escalas entre dos aeropuertos.
   * **Dijkstra:** Calcula la ruta óptima minimizando la distancia real en kilómetros entre el origen y el destino.
   * **Kruskal (MST - Minimum Spanning Tree):** Genera la red óptima de vuelos (Árbol de Expansión Mínima) para conectar todos los aeropuertos de un país seleccionado (o a nivel global) usando la menor distancia total acumulada y asegurando que no existan ciclos.

---

## ⚙️ Requisitos de Instalación y Despliegue

Sigue estos pasos para desplegar el proyecto localmente en tu computadora.

### 1. Clonar el repositorio
Asegúrate de estar en el directorio raíz del proyecto:
`c:\Aeropuertos_Complejidad`

---

### 2. Configurar el Backend (Python)

1. **Crear un entorno virtual (Aula Virtual):**
   Abre una terminal en la carpeta `backend/` y crea el entorno virtual llamado `myenv`:
   ```bash
   cd backend
   python -m venv myenv
   ```

2. **Activar el entorno virtual:**
   * **En Windows (PowerShell):**
     ```powershell
     .\myenv\Scripts\activate
     ```
   * **En macOS/Linux:**
     ```bash
     source myenv/bin/activate
     ```

3. **Instalar dependencias de Python:**
   Con el entorno virtual activo, instala las librerías necesarias utilizando el archivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Variables de Entorno (Opcional):**
   Puedes configurar el archivo `backend/.env` para conectar el backend con Supabase:
   ```env
   DB_USER=tu_usuario_supabase
   DB_PASSWORD=tu_contraseña_supabase
   DB_HOST=tu_host_supabase
   DB_PORT=5432
   DB_NAME=postgres
   ```
   *Si no tienes credenciales de Supabase o está caído, el sistema levantará SQLite local automáticamente usando los CSVs de `backend/data/`.*

5. **Iniciar el servidor backend:**
   Ejecuta el servidor con Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```
   El backend estará disponible en `http://localhost:8000`.

---

### 3. Configurar el Frontend (React)

1. **Navegar a la carpeta frontend:**
   Abre una nueva terminal en la carpeta raíz del proyecto y entra a `frontend/`:
   ```bash
   cd frontend
   ```

2. **Instalar módulos de Node (`node_modules`):**
   Instala todas las dependencias del proyecto usando npm:
   ```bash
   npm install
   ```

3. **Iniciar el servidor de desarrollo del frontend:**
   Inicia la aplicación con Vite:
   ```bash
   npm run dev
   ```
   El frontend estará disponible en `http://localhost:5173`.

---

## 📁 Estructura del Proyecto

```text
Aeropuertos_Complejidad/
├── backend/
│   ├── data/                 # Contiene los archivos semilla .csv
│   │   ├── airports.csv      # Listado de 1,772 aeropuertos
│   │   └── routes.csv        # Listado de 16,696 rutas aéreas
│   ├── myenv/                # Entorno virtual de Python
│   ├── database.py           # Configuración y fallback de bases de datos
│   ├── main.py               # Endpoints de la API y lógica de algoritmos
│   ├── models_database.py    # Declaración de modelos con SQLAlchemy
│   ├── requirements.txt      # Dependencias del backend
│   └── local_airports.db     # Base de datos SQLite local autocreada
└── frontend/
    ├── node_modules/         # Dependencias instaladas de Node.js
    ├── src/
    │   ├── components/       # Panel de control y visualización de mapas (deck.gl)
    │   ├── services/         # api.js para conectar con el backend
    │   ├── App.jsx           # Componente principal de React
    │   └── main.jsx          # Punto de entrada de React
    ├── package.json          # Configuración del proyecto frontend
    └── tailwind.config.js    # Configuración de estilos Tailwind
```
