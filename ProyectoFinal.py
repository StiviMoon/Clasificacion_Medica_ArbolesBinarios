import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from PIL import Image, ImageTk
import pydot
import os

# Cargar datos
data = pd.read_excel("pacientes_diabetes_1.xlsx")
data.columns = [
    "Edad",
    "Nivel_Glucosa",
    "Presion_Arterial",
    "IMC",
    "Historial_Familiar",
    "Resultado",
]

# Separar características y etiquetas
X = data[["Edad", "Nivel_Glucosa", "Presion_Arterial", "IMC", "Historial_Familiar"]]
y = data["Resultado"]

# Entrenar el modelo de árbol de decisión
model = DecisionTreeClassifier(random_state=0)
model.fit(X, y)


# Clase para crear imágenes zoomables
class ZoomableImage:
    def __init__(self, master, image_path):
        self.master = master
        self.image_path = image_path
        self.original_image = Image.open(image_path)
        self.image = self.original_image

        # Canvas para desplazamiento y zoom
        self.canvas = tk.Canvas(master)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.photo_image = ImageTk.PhotoImage(self.image)
        self.image_id = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.photo_image
        )
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

        # Barras de desplazamiento
        self.h_scroll = ttk.Scrollbar(
            master, orient=tk.HORIZONTAL, command=self.canvas.xview
        )
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.config(xscrollcommand=self.h_scroll.set)

        self.v_scroll = ttk.Scrollbar(
            master, orient=tk.VERTICAL, command=self.canvas.yview
        )
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=self.v_scroll.set)

        # Botones de zoom
        ttk.Button(master, text="Zoom In", command=self.zoom_in).pack(side=tk.LEFT)
        ttk.Button(master, text="Zoom Out", command=self.zoom_out).pack(side=tk.LEFT)
        ttk.Button(master, text="Cerrar", command=master.destroy).pack(
            side=tk.BOTTOM, pady=10
        )

    def zoom_in(self):
        self._zoom(1.1)

    def zoom_out(self):
        self._zoom(0.9)

    def _zoom(self, factor):
        new_size = (int(self.image.width * factor), int(self.image.height * factor))
        self.image = self.original_image.resize(new_size, Image.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.image_id, image=self.photo_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))


def mostrar_imagen(imagen_path, titulo="Imagen"):
    ventana = tk.Toplevel()
    ventana.title(titulo)
    ventana.geometry("900x700")
    ZoomableImage(ventana, imagen_path)


def crear_carpeta_paciente(nombre, cedula):
    carpeta = f"{nombre}_{cedula}"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    return carpeta


def generar_imagen_camino(nombre, cedula, patient_data):
    dot_data = export_graphviz(
        model,
        out_file=None,
        feature_names=X.columns,
        class_names=model.classes_,
        filled=True,
        rounded=True,
        special_characters=True,
        node_ids=True,
    )
    graph = pydot.graph_from_dot_data(dot_data)[0]

    node_id = 0
    while model.tree_.children_left[node_id] != model.tree_.children_right[node_id]:
        feature_index = model.tree_.feature[node_id]
        threshold = model.tree_.threshold[node_id]
        feature_value = patient_data[0][feature_index]

        if feature_value <= threshold:
            next_node = model.tree_.children_left[node_id]
        else:
            next_node = model.tree_.children_right[node_id]

        # Resalta el nodo actual en el camino
        graph_node = graph.get_node(str(node_id))[0]
        graph_node.set_fillcolor("green")

        node_id = next_node

    # Resalta el nodo final
    graph.get_node(str(node_id))[0].set_fillcolor("green")

    carpeta = crear_carpeta_paciente(nombre, cedula)
    imagen_path = os.path.join(carpeta, "camino_recorrido.png")
    graph.write_png(imagen_path)
    return imagen_path


def diagnosticar():
    try:
        nombre = nombre_entry.get()
        cedula = cedula_entry.get()
        if not nombre or not cedula:
            messagebox.showerror("Error", "Por favor, ingrese nombre y cédula.")
            return

        # Extraer datos del formulario
        edad = int(edad_entry.get())
        nivel_glucosa = int(nivel_glucosa_entry.get())
        presion_arterial = int(presion_arterial_entry.get())
        imc = float(imc_entry.get())
        historial_familiar = int(historial_familiar_entry.get())

        # Crear la instancia del paciente
        patient_data = [
            [edad, nivel_glucosa, presion_arterial, imc, historial_familiar]
        ]

        # Realizar predicción
        resultado = model.predict(pd.DataFrame(patient_data, columns=X.columns))[0]
        messagebox.showinfo("Resultado", f"El resultado es: {resultado}")

        # Generar y mostrar imagen del camino recorrido en el árbol de decisión
        camino_path = generar_imagen_camino(nombre, cedula, patient_data)
        mostrar_imagen(camino_path, "Camino Recorrido en el Árbol de Decisión")

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese datos válidos.")


# Crear la interfaz gráfica
root = tk.Tk()
root.title("Diagnóstico de Diabetes")
root.configure(bg="#f0f8ff")

form_frame = tk.Frame(root, bg="#ffffff", borderwidth=2, relief="groove")
form_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)

labels = [
    "Nombre:",
    "Cédula:",
    "Edad:",
    "Nivel de Glucosa:",
    "Presión Arterial:",
    "IMC:",
    "Historial Familiar (0/1):",
]
entries = []

for i, text in enumerate(labels):
    ttk.Label(form_frame, text=text, background="#ffffff").grid(
        column=0, row=i, padx=10, pady=10, sticky=tk.W
    )
    entry = ttk.Entry(form_frame, width=30)
    entry.grid(column=1, row=i, padx=10, pady=10)
    entries.append(entry)

(
    nombre_entry,
    cedula_entry,
    edad_entry,
    nivel_glucosa_entry,
    presion_arterial_entry,
    imc_entry,
    historial_familiar_entry,
) = entries

# Botón de diagnóstico
diagnosticar_btn = ttk.Button(form_frame, text="Diagnosticar", command=diagnosticar)
diagnosticar_btn.grid(column=0, row=len(labels), columnspan=2, pady=20)

# Configuración de ventana principal
root.geometry("400x400")
root.mainloop()
