import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from PIL import Image, ImageTk
import pydot
import os
import tkinter as tk
from tkinter import ttk

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

        # Limpiar entradas
        nombre_entry.delete(0, tk.END)
        cedula_entry.delete(0, tk.END)
        edad_entry.delete(0, tk.END)
        nivel_glucosa_entry.delete(0, tk.END)
        presion_arterial_entry.delete(0, tk.END)
        imc_entry.delete(0, tk.END)
        historial_familiar_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese datos válidos.")


# Crear la ventana principal
root = tk.Tk()
root.title("Diagnóstico de Diabetes")
root.configure(bg="#f5f5f5")
root.geometry("500x600")  # Tamaño más amplio y alto para mejor presentación

# Marco del formulario
form_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
form_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Título del formulario
form_title = tk.Label(
    form_frame,
    text="Formulario de Diagnóstico de Diabetes",
    bg="#ffffff",
    font=("Helvetica", 16, "bold"),
    fg="#333333",
)
form_title.pack(pady=(10, 20))

# Lista de etiquetas y entradas
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

# Crear etiquetas y entradas
for text in labels:
    label = tk.Label(
        form_frame, text=text, bg="#ffffff", font=("Helvetica", 12), anchor="w"
    )
    label.pack(fill="x", padx=20, pady=(5, 0))

    entry = ttk.Entry(form_frame, font=("Helvetica", 12))
    entry.pack(fill="x", padx=20, pady=5)
    entries.append(entry)

# Asignar las entradas a variables
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
diagnosticar_btn.pack(pady=5)

# Estilo adicional para el botón (opcional)
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10), padding=10)

# Pie de página
footer = tk.Label(
    root,
    text="© 2024 Diagnóstico Inteligente. Todos los derechos reservados.",
    bg="#f5f5f5",
    font=("Helvetica", 10),
    fg="#666666",
)
footer.pack(side="bottom", pady=10)

# Ejecutar la ventana principal
root.mainloop()
