# Dataset Zoo Madrid

**Autores:** Diego Carbonell | Guillermo Morató  
**Asignatura:** Tipología y ciclo de vida de los datos – Actividad 1 (UOC)

---

## Descripción del proyecto

El objetivo de esta actividad es la **creación de un dataset original** a partir de la información disponible en el sitio web del **Zoo de Madrid**.  
Para ello, se ha desarrollado un script en Python que utiliza **Selenium** y **Requests** para realizar **web scraping**, recopilando datos sobre los animales del zoo y descargando sus imágenes asociadas.

El resultado final es un **archivo CSV** que contiene los datos estructurados de cada animal y una **carpeta de imágenes** con las fotografías correspondientes.

---

## Estructura del proyecto

```
scraping_zoomadrid/
│
├── dataset/                          # Capeta con el Dataset final con los datos extraídos.
│   └── animales_zoomadrid.csv           
│
├── imagenes/                         # Carpeta de salida con las imágenes descargadas.
│   └── 0XX-nombre-animal.jpg
│
├── source/                               # Carpera principal del código.         
│   └── main.py                           # Script principal del scraping.
│   └── requirements.txt                  # Dependencias necesarias para ejecutar el código.
│  
├── READNE.md
│
└── license.txt                       # Licencia del proyecto.
```

---

## Requisitos previos

- **Python 3.8 o superior**
- Navegador instalado (**Google Chrome** o **Mozilla Firefox**)
- Librerías de Python incluidas en `requirements.txt`:

```bash
selenium>=4.0.0
webdriver-manager>=3.8.0
requests>=2.25.0
```

Instálalas ejecutando:

```bash
pip install -r requirements.txt
```

---

## Ejecución del proyecto

1. Replica o descarga este repositorio.
2. Instala las dependencias necesarias.
3. Ejecuta el script principal:

   ```bash
   python main.py --browser chrome
   ```

   *(Puedes sustituir `chrome` por `firefox` si prefieres ese navegador).*

Durante la ejecución:
- Se abrirá el navegador y comenzará el proceso de scraping.
- Se mostrarán en consola los animales procesados y las imágenes descargadas.
- Al finalizar, se generará el archivo `animales_zoomadrid.csv` y la carpeta `imagenes/`.

---

## Inputs del programa

El programa **no requiere entrada manual del usuario**.  
Toda la información se obtiene automáticamente del sitio web oficial del Zoo de Madrid:

- [https://www.zoomadrid.com/descubre-el-zoo/animales-y-continentes/animales](https://www.zoomadrid.com/descubre-el-zoo/animales-y-continentes/animales)

El dataset completo se encuentra publicado en **Zenodo** en formato CSV:  
- (https://doi.org/10.5281/zenodo.17551836)

---

## Outpus generadas

- **Imágenes:** fotografías de los animales descargadas en la carpeta `imagenes/`.  
- **Archivo CSV:** `animales_zoomadrid.csv`, con los siguientes campos:
  - Nombre común  
  - Nombre científico  
  - Clase  
  - Continente  
  - Hábitat  
  - Dieta  
  - Peso  
  - Tamaño  
  - Estado de conservación  
  - URL de la ficha  
  - Archivo de imagen descargado

---

## Acciones que realiza el programa

Al ejecutar `main.py`, el programa realiza las siguientes tareas:

1. **Inicializa el navegador**  
   - Crea una instancia de **Chrome** o **Firefox** mediante **Selenium**, según la opción indicada por el usuario (`--browser chrome` o `--browser firefox`).  
   - Configura el tamaño de la ventana y la estrategia de carga de páginas.

2. **Accede a la página principal del Zoo de Madrid**  
   - Carga la URL principal con la lista de animales.

3. **Gestiona el banner de cookies**  
   - Pulsa el botón **“Rechazar todas”** si aparece, para continuar sin interrupciones.

4. **Carga todos los animales disponibles**  
   - Pulsa repetidamente el botón **“Muéstrame más”** hasta que se muestren todas las tarjetas de animales.

5. **Obtiene los enlaces de detalle**  
   - Extrae todos los enlaces “**Ver Detalles**” de cada animal, evitando duplicados.

6. **Recorre y analiza cada ficha individual**  
   - Extrae los datos de cada animal:
     - Nombre común y científico  
     - Clase, continente, hábitat, dieta  
     - Peso y tamaño  
     - Estado de conservación  
     - Imagen principal y URL de la ficha

7. **Descarga las imágenes**  
   - Guarda las imágenes de los animales en la carpeta `imagenes/`, con nombres normalizados (`001-elefante.jpg`, etc.).

8. **Genera el dataset final**  
   - Guarda todos los datos recopilados en `animales_zoomadrid.csv`, incluyendo la ruta de cada imagen descargada.

9. **Finaliza la ejecución**  
   - Cierra el navegador y muestra un resumen por consola.

---

## Licencia

**Tipo de licencia:** [CC BY-NC-SA 4.0 – Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)

Esta licencia permite:

- **Compartir**: copiar y redistribuir el material en cualquier medio o formato.  
- **Adaptar**: remezclar, transformar y crear a partir del material.  

Siempre que se cumplan las siguientes condiciones:

1. **Atribución (BY)** – Debe otorgarse el crédito adecuado a los autores originales del dataset y citar la fuente del sitio web del Zoo de Madrid.  
2. **No comercial (NC)** – No se puede utilizar el material con fines comerciales.  
3. **Compartir igual (SA)** – Si se remezcla o transforma el dataset, debe distribuirse bajo la misma licencia.

El contenido del dataset procede de información **pública y accesible** en el portal del [Zoo de Madrid](https://www.zoomadrid.com/), pero el proceso de recopilación, limpieza y estructuración de los datos ha sido desarrollado por los autores de este proyecto.

---

## Notas finales

Este trabajo se ha realizado como parte de la **Actividad 1** de la asignatura *Tipología y ciclo de vida de los datos* (UOC).  
El propósito principal ha sido **obtener datos reales mediante técnicas de web scraping** para generar un dataset original y reproducible.

---
