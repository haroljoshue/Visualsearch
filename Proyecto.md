# Guia de Presentacion: Test de Busqueda Visual

Esta guia contiene la estructura detallada y el contenido teorico-practico del Test de Busqueda Visual. Explica el paradigma cognitivo, la temporalidad de los estimulos y el rol de las herramientas tecnologicas como instrumentos de evaluacion clinica y experimental.

---

## 1. Fundamento Teorico y Paradigma Cognitivo

### El Paradigma de Busqueda Visual
Basado en la **Teoria de la Integracion de Caracteristicas** (*Feature Integration Theory*) propuesta por **Anne Treisman y Garry Gelade en 1980**. Este paradigma es una herramienta fundamental en la psicologia cognitiva para estudiar la atencion selectiva y los mecanismos de procesamiento de la informacion visual.

### Procesos Cognitivos Evaluados
* **Atencion Selectiva y Focalizada:** Capacidad del sujeto para seleccionar un estimulo relevante (objetivo) y procesarlo activamente mientras inhibe de forma voluntaria los estimulos irrelevantes (distractores).
* **Velocidad de Procesamiento (Latencia):** El tiempo requerido para percibir el entorno, tomar una decision cognitiva y ejecutar una respuesta motora voluntaria.
* **Procesamiento de la Informacion:** Como el cerebro organiza espacialmente los estimulos dinamicamente (en movimiento) antes de emitir una respuesta.

---

## 2. Estructura y Tiempos de Presentacion de los Estimulos

Cada sesion experimental consta de **30 ensayos secuenciales**. El control de los tiempos es riguroso para asegurar la validez interna del experimento y evitar sesgos de fatiga o anticipacion:

| Fase del Ensayo | Duracion / Tiempo | Funcion Psicologica y Control de Variables |
| :--- | :--- | :--- |
| **1. Cruz de Fijacion (`+`)** | **1.5 segundos (1500 ms)** | Centra la mirada y el foco atencional del participante en un unico punto neutro. Esto reduce el impacto de movimientos oculares previos (sacadas) y prepara al cerebro para recibir el estimulo visual. |
| **2. Estimulos en Movimiento** | **Maximo 5.0 segundos (5000 ms)** | Es la ventana temporal donde se desplazan los elementos. El participante debe procesar la escena y presionar `S` (Presente) o `N` (Ausente). Si supera este tiempo, se registra como "ensayo nulo por omision", indicando una falla de respuesta en el tiempo limite tolerado. |
| **3. Retroalimentacion (Feedback)** | **Breve (Milisegundos)** | Muestra un aviso en pantalla indicando "Acierto", "Error" o "Tiempo Agotado". Sirve como refuerzo de conducta y ayuda a mantener el nivel de alerta (*arousal*) y motivacion a lo largo del test. |

---

## 3. Dinamicas de Procesamiento Visual Analizadas

El test evalua y contrasta dos tipos de busqueda que utiliza el cerebro para resolver retos visuales:

### A. Busqueda de Caracteristicas (Procesamiento en Paralelo)
* **Como funciona:** El objetivo difiere de los distractores por una sola propiedad fisica elemental y evidente (ej. una manzana roja rodeada de manzanas verdes).
* **Fenomeno de Pop-out:** La deteccion es automatica, refleja e inconsciente. El tiempo de reaccion del participante es sumamente bajo y se mantiene constante sin importar si hay 5 o 50 distractores en la pantalla.

### B. Busqueda de Conjuncion (Procesamiento Serial)
* **Como funciona:** El objetivo comparte atributos cruzados con los distractores (ej. un icono especifico rodeado de elementos que varian en formas, colores y numeros).
* **Busqueda Activa:** Requiere atencion controlada, consciente e intencional. El cerebro debe analizar cada elemento uno por uno. El tiempo de reaccion aumenta de forma lineal a medida que se añaden mas distractores al campo de busqueda.

---

## 4. El Instrumento Tecnologico desde la Perspectiva Psicologica

En lugar de ver el software como un desarrollo de ingenieria de sistemas, para la psicologia actua como un **instrumento de laboratorio digital**:

* **El Entorno Experimental (HTML, CSS y Javascript):**
  * Equivale a la clasica "caja de estimulacion". Se encarga de proyectar con precision sistematica los elementos visuales en la pantalla y capturar la latencia exacta (en milisegundos) entre la aparicion de la imagen y la respuesta motora en el teclado.
* **El Registro y Analisis de Datos (Python y Flask):**
  * Funciona como la libreta de anotaciones automatizada del investigador. En lugar de registrar a mano cada respuesta, el software tabula el porcentaje de precision (aciertos y errores) y la velocidad de respuesta en una planilla digital (.csv). Esto permite al psicologo enfocarse unicamente en la interpretacion clinica del rendimiento cognitivo del evaluado.