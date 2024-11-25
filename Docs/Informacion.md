# Diagnóstico de Diabetes con Árbol de Decisión

Esta es una aplicación sencilla para diagnosticar diabetes utilizando un modelo de árbol de decisión. El proyecto utiliza **Python**, **Tkinter** y **Scikit-learn** para proporcionar una interfaz gráfica fácil de usar donde se ingresan los datos de los pacientes y se obtiene un diagnóstico.

## Características

- **Manejo de Datos**: La aplicación carga un conjunto de datos de registros de pacientes (`pacientes_diabetes_1.xlsx`) y entrena un **Clasificador de Árbol de Decisión** para predecir si un paciente es diabético o no según varios parámetros de salud.
  
- **Proceso de Diagnóstico**: Los usuarios pueden ingresar los datos del paciente, como la edad, el nivel de glucosa, la presión arterial, el IMC y el historial familiar de diabetes, para recibir un diagnóstico (Diabético/No Diabético).
  
- **Visualización**: Después del diagnóstico, la aplicación genera una representación visual del proceso de toma de decisiones dentro del árbol de decisión, destacando el camino seguido para llegar al diagnóstico.

- **Imágenes Zoomables**: La visualización del árbol de decisión puede ser aumentada/disminuida, ofreciendo una forma interactiva de explorar cómo se tomaron las decisiones.

- **Carpetas Específicas del Paciente**: Para cada paciente, se crea una carpeta que contiene el resultado del diagnóstico y una visualización del camino tomado en el árbol de decisión para ese paciente en particular.

## Librerías Utilizadas
- **Pandas**: Para la manipulación de datos.
- **Tkinter**: Para construir la interfaz gráfica de usuario.
- **Scikit-learn**: Para entrenar el clasificador de árbol de decisión.
- **PIL (Pillow)**: Para el manejo y redimensionamiento de imágenes.
- **pydot**: Para crear y renderizar el gráfico del árbol de decisión.

## Cómo Usar
1. Asegúrate de tener Python 3.x instalado.
2. Instala las bibliotecas necesarias utilizando el siguiente comando:
   ```bash
   pip install pandas scikit-learn pillow pydot
