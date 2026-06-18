# Manual de Usuario y Guia de Resultados: Test de Busqueda Visual

Esta guia describe de forma metodologica el funcionamiento de la aplicacion, la interpretacion de los datos recolectados y como se estructura la herramienta tanto a nivel psicologico como tecnologico.

---

## 1. Fundamento Psicologico del Test

El proposito de esta aplicacion es evaluar procesos cognitivos fundamentales:

* **Atencion Selectiva:** La capacidad para enfocar la mente en un estimulo especifico (objetivo) ignorando de forma activa otros elementos distractores.
* **Velocidad de Procesamiento (Latencia):** El tiempo en milisegundos que le toma al cerebro percibir una escena, tomar una decision y realizar una respuesta motora.
* **Carga Cognitiva:** Evaluacion de como la cantidad de distractores en pantalla afecta el tiempo de respuesta del evaluado.

---

## 2. Como Funciona el Test en la Aplicacion

Cada sesion consta de un bloque de **30 ensayos**:

1. **Cruz de Fijacion (+):** Aparece durante 1.5 segundos en el centro para orientar la mirada del participante hacia el area donde surgiran los estimulos.
2. **Presentacion de Estimulos (Maximo 5 segundos):** Los elementos aparecen en movimiento vertical continuo. El participante debe identificar si el objetivo esta presente.
3. **Entrada de Respuesta:**
   - Si el objetivo **esta presente**, se presiona la tecla **S** (o el boton verde **SI [S]**).
   - Si el objetivo **no esta presente**, se presiona la tecla **N** (o el boton rojo **NO [N]**).
4. **Retroalimentacion Inmediata:** El sistema muestra si la respuesta fue un "Acierto", "Error" o si se agoto el tiempo ("Tiempo Agotado") antes de pasar al siguiente ensayo.

---

## 3. Metricas y Analisis de Resultados

Al finalizar, la aplicacion procesa los datos y los presenta en un panel clinico de diagnostico con las siguientes variables:

* **TR Paralela (Tiempo de Reaccion en Busqueda Paralela):** Tiempo promedio en los ensayos donde el objetivo se distingue por una sola caracteristica (ej. color o forma diferente), generando un efecto de destaque automatico ("Pop-out"). El tiempo de respuesta es bajo y estable.
* **TR Serial (Tiempo de Reaccion en Busqueda Serial):** Tiempo promedio cuando el objetivo comparte multiples rasgos con los distractores. Requiere un analisis secuencial y consciente, aumentando el tiempo linealmente segun el numero de elementos.
* **Pendiente de Busqueda:** Medicion en milisegundos por elemento. Si es baja (menor o igual a 8 ms), refleja un procesamiento de filtrado automatico preatentivo. Si es alta, indica busqueda serial exhaustiva y mayor esfuerzo mental.
* **Precision Global y Errores:** Porcentaje de aciertos frente al total de intentos y recuento de fallos.
* **Diagnostico Clinico:** Clasificacion automatica entre procesamiento paralelo (eficiente) y serial (guiado/exhaustivo) segun el efecto de pendiente.

---

## 4. Arquitectura Tecnologica Simplificada

La aplicacion combina dos tecnologias basicas para funcionar como un instrumento digital:

* **El Frente de la Aplicacion (HTML y Javascript):**
  - **HTML** define la estructura visual del test (botones, formularios y el lienzo canvas).
  - **Javascript** ejecuta la logica en el navegador en tiempo real. Controla la fisica de los movimientos de los estimulos, mide la latencia exacta de las respuestas en milisegundos y proporciona la retroalimentacion visual instantanea.
* **El Servidor Trasero (Python y Flask):**
  - **Python** (con el modulo **Flask**) recibe las respuestas enviadas por la aplicacion a traves de la red y las escribe permanentemente en un archivo local plano (`.csv`).
  - Tambien calcula las formulas estadisticas (medias, pendientes) y se encarga de empaquetar y exportar la informacion a archivos de **Excel** estructurados para que puedan ser analizados facilmente en otros programas.
