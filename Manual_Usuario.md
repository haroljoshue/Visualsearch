# Manual de Usuario y Guía de Resultados

Esta guía técnica y metodológica describe el funcionamiento, la arquitectura general y la interpretación de los datos recopilados durante las evaluaciones del Test de Búsqueda Visual.

---

## 1. Fundamento del Test

Esta aplicación es un entorno de evaluación cognitiva basado en el clásico **Test de Búsqueda Visual** (Treisman & Gelade, 1980). Su propósito es medir la capacidad de atención selectiva, la velocidad de procesamiento de información y la eficiencia del participante al identificar estímulos objetivo frente a distractores de diversa complejidad bajo condiciones de movimiento dinámico.

---

## 2. Arquitectura del Sistema

El sistema opera mediante la integración de dos componentes principales:

1. **Interfaz de Usuario (HTML, CSS, Javascript):** Es el entorno interactivo visible en el navegador. Se encarga de la generación espacial de los estímulos, del control temporal de los ensayos, de las animaciones físicas y de capturar los tiempos de reacción basándose en las entradas de teclado del participante (`S` para Presente, `N` para Ausente).
2. **Servidor y Almacenamiento (Python, Flask, Pandas):** Es la capa lógica encargada de estructurar las métricas de respuesta enviadas desde la interfaz. Organiza la persistencia de los datos escribiendo en formato de base de datos plana (`.csv`), gestionando el historial de evaluaciones clínicas y procesando la exportación del informe a formatos de hoja de cálculo tradicionales (**Excel**).

---

## 3. Protocolo del Ensayo

Cada sesión consta de **30 ensayos** estructurados de forma secuencial:

* **Cruz de Fijación (`+`):** Se muestra durante un intervalo fijo de 1.5 segundos (1500 ms) para pre-orientar la mirada del participante hacia el centro del campo de búsqueda.
* **Presentación del Estímulo (Máximo 5 segundos):** Los elementos aparecen en movimiento vertical. El participante cuenta con un margen de 5.0 segundos para registrar su respuesta antes de que se considere ensayo nulo por tiempo límite.
* **Retroalimentación de Desempeño:** Tras registrar la entrada, el sistema expone un aviso breve (Acierto, Error o Tiempo Agotado) antes del siguiente ensayo.

---

## 4. Análisis e Interpretación de Resultados

Al concluir los 30 ensayos, se procesan los datos acumulados para emitir un diagnóstico clínico cuantitativo:

### A. Métricas Clínicas Principales:
* **Tiempo de Reacción (TR) Promedio:** Refleja la latencia media (en milisegundos) asociada a los ensayos resueltos correctamente. Menores tiempos expresan una mayor velocidad de procesamiento visual.
* **Precisión (Tasa de Acierto):** Muestra el porcentaje de respuestas acertadas. Permite correlacionar la velocidad con el nivel de control y eficacia atencional del participante.

### B. Clasificación de la Eficiencia Atencional:

El diagnóstico contrasta el desempeño visual entre las siguientes dinámicas de búsqueda:

1. **Búsqueda de Características (Procesamiento en Paralelo):**
   * **Dinámica:** El objetivo difiere por un solo rasgo obvio respecto a los distractores (ej. una manzana roja entre manzanas verdes).
   * **Efecto Cognitivo:** Produce un fenómeno de "Pop-out" (destaque automático). La velocidad de procesamiento suele ser alta y el tiempo de reacción permanece constante sin afectarse por la cantidad de distractores en pantalla.
2. **Búsqueda de Conjunción (Procesamiento Serial):**
   * **Dinámica:** El objetivo comparte características combinadas con los distractores (ej. un icono de red social con notificación roja entre otros iconos que varían en logo, número y posición).
   * **Efecto Cognitivo:** Requiere un escaneo secuencial e intencional. El tiempo de reacción promedio aumenta de forma lineal conforme se incrementa la densidad de elementos en pantalla.

---

## 5. Historial Clínico y Acceso Restringido

Para salvaguardar la confidencialidad y la integridad de los registros:

* **Clave de Acceso Evaluador:** Se requiere ingresar la contraseña autorizada **`170805`** en el panel de validación para desplegar el historial consolidado.
* **Gráficos Estadísticos:** Se presentan análisis visuales automáticos que muestran el comportamiento del tiempo de reacción promedio frente al volumen de aciertos y la distribución demográfica de las evaluaciones guardadas.
* **Mantenimiento del Historial:** Los evaluadores disponen de herramientas para depurar registros individuales mediante la opción de eliminación (`🗑️`), borrar el registro histórico completo o exportar la planilla completa a Excel.

---

## 6. Acceso Móvil Automatizado (Código QR)

Para facilitar la administración del test desde dispositivos móviles:
* **Generación de QR Dinámico:** Al iniciar la aplicación en un servidor web local o público, la pantalla de inicio autogenera y despliega un **Código QR** correspondiente a su dirección URL actual.
* **Uso:** El evaluador puede abrir la aplicación en su computadora y proyectar o mostrar la pantalla de inicio; los participantes solo necesitan escanear el código QR con la cámara de sus celulares para ser dirigidos inmediatamente al test móvil sin necesidad de ingresar la dirección web manualmente.

---

## 7. Despliegue en Servidores Públicos (Alternativa Render)

Además de Railway, **Render** (render.com) es una alternativa gratuita y sumamente sencilla para hospedar la aplicación:
1. Inicie sesión en **Render** usando su cuenta de GitHub.
2. Cree un **"New Web Service"** y seleccione el repositorio del proyecto.
3. Defina los siguientes parámetros:
   * **Runtime:** `Python`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `gunicorn app:app`
4. Render desplegará el proyecto y generará una URL pública y segura (https://...) que cargará de forma automática el código QR en la pantalla de inicio.
