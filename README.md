📄 README.md COMPLETO (LISTO PARA COPIAR Y PEGAR)
# Gestión de Países – Proyecto Python (TPI)

Este proyecto implementa un sistema de gestión de países utilizando Python y archivos CSV.  
Permite cargar, consultar, filtrar, ordenar y analizar información de países mediante un menú interactivo en consola.

El programa cumple con la consigna del TPI y **no utiliza excepciones (`try/except`)**, sino validaciones previas.  
Además, el guardado de datos en CSV es **automático** cada vez que se realizan cambios.

---

## 📁 Estructura del proyecto



├── paises.csv # Archivo con los datos persistidos
├── main.py # Programa principal (menú y funciones)
└── README.md # Documentación del proyecto


---

## ✔️ Funcionalidades principales

### 1. Carga automática desde CSV
- El programa lee `paises.csv` al iniciar.
- Se validan:
  - existencia del archivo  
  - encabezados requeridos  
  - datos numéricos positivos  
  - campos no vacíos  
- Si una fila es inválida, se descarta sin lanzar excepciones.

---

### 2. Agregar país
Permite ingresar:
- Nombre  
- Población (entero positivo)  
- Superficie (entero positivo)  
- Continente  

El sistema **guarda automáticamente** el cambio en el archivo CSV.

---

### 3. Actualizar datos de un país
- Búsqueda por nombre o coincidencia parcial.  
- Modifica población y superficie.  
- Guardado automático.

---

### 4. Buscar país por nombre
Devuelve todos los países cuyo nombre contenga la cadena ingresada.

---

### 5. Filtrar países
Se puede filtrar por:
- Continente  
- Rango de población  
- Rango de superficie  

---

### 6. Ordenar países
Permite ordenar por:
- Nombre  
- Población  
- Superficie  

En orden ascendente o descendente.

---

### 7. Estadísticas
El sistema calcula:
- País con mayor población  
- País con menor población  
- Promedio de población  
- Promedio de superficie  
- Cantidad de países por continente  

---

### 8. Guardado automático
Cada vez que se agrega o actualiza un país, los datos se guardan automáticamente en `paises.csv`.

---

## 📄 Formato del archivo CSV

El archivo debe tener el siguiente encabezado:



nombre,poblacion,superficie,continente


Ejemplo:



Argentina,46044703,2780400,America
Francia,68042591,643801,Europa


---

## ▶️ Ejecución del programa

1. Instalar Python 3.10 o superior.  
2. Descargar los archivos del proyecto.  
3. Abrir una terminal en la carpeta.  
4. Ejecutar:



python main.py


Si `paises.csv` no existe, se generará automáticamente cuando agregues o actualices países.

---

## 🧩 Validaciones implementadas (sin try/except)

- Validación de existencia del CSV (uso de `os.path.exists`)
- Validación de encabezados obligatorios
- Validación de datos numéricos mediante `isdigit`
- Validación de valores positivos
- Verificación de campos no vacíos
- Validación de opciones de menú y rangos lógicos

---

## 🛠️ Tecnologías utilizadas

- Python 3  
- Módulo `csv`  
- Módulo `os`  
- Estructuras: listas, diccionarios, menús interactivos

---

## 👤 Autor

Proyecto realizado como Trabajo Práctico Integrador (TPI).  

