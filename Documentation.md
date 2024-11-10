
# Documentación para Ejecución del Código de Diagnóstico de Diabetes

## Requerimientos
- Python 3.7 o superior.
- Instalar libreria Grafica export_graphviz (Instalador según S.O)
- Sistema operativo compatible con las bibliotecas especificadas (probado en Windows/Linux).

## Instalación
1. Clona el repositorio o copia el código en tu máquina local.
2. Descarga el archivo de datos `pacientes_diabetes_1.xlsx` y asegúrate de que se encuentre en el mismo directorio que el código.
3. Instala las dependencias ejecutando los siguientes comandos en la terminal.

### Guía de instalación de dependencias
1. Descarga y coloca el archivo `requirements.txt` en el mismo directorio que el código.
2. Ejecuta el siguiente comando para instalar todas las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Ejecución
1. Asegúrate de que el archivo `pacientes_diabetes_1.xlsx` está en el mismo directorio que el código.
2. Ejecuta el código:

   ```bash
   python nombre_del_archivo.py
   ```

3. La aplicación abrirá una interfaz gráfica donde podrás ingresar los datos del paciente y obtener el diagnóstico y la imagen del árbol de decisión.

## Descripción de los archivos
- `requirements.txt`: Archivo de texto con las dependencias necesarias.
- `nombre_del_archivo.py`: El script principal que contiene la aplicación de diagnóstico.

