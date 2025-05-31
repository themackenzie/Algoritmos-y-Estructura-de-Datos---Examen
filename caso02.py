import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict, deque
import random

class GrafoCiudad:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Rutas en Ciudad Altiplánica")

        self.grafo = defaultdict(list)
        self.nodos_pos = {}
        self.canvas_size = 500

        self.crear_widgets()

    def crear_widgets(self):
        frame_controls = ttk.Frame(self.root)
        frame_controls.grid(row=0, column=0, sticky="n")

        ttk.Label(frame_controls, text="Agregar Nodo:").grid(row=0, column=0)
        self.entry_nodo = ttk.Entry(frame_controls)
        self.entry_nodo.grid(row=0, column=1)
        ttk.Button(frame_controls, text="Agregar", command=self.agregar_nodo).grid(row=0, column=2)

        ttk.Label(frame_controls, text="Conectar:").grid(row=1, column=0)
        self.entry_conexion1 = ttk.Entry(frame_controls, width=10)
        self.entry_conexion1.grid(row=1, column=1)
        self.entry_conexion2 = ttk.Entry(frame_controls, width=10)
        self.entry_conexion2.grid(row=1, column=2)
        ttk.Button(frame_controls, text="Conectar", command=self.conectar_nodos).grid(row=1, column=3)

        ttk.Label(frame_controls, text="Buscar ruta entre:").grid(row=2, column=0)
        self.entry_inicio = ttk.Entry(frame_controls, width=10)
        self.entry_inicio.grid(row=2, column=1)
        self.entry_destino = ttk.Entry(frame_controls, width=10)
        self.entry_destino.grid(row=2, column=2)
        ttk.Button(frame_controls, text="Verificar Ruta", command=self.verificar_ruta).grid(row=2, column=3)
        ttk.Button(frame_controls, text="Mostrar Todas", command=self.mostrar_rutas).grid(row=3, column=3)

        self.text_resultado = tk.Text(frame_controls, height=10, width=50)
        self.text_resultado.grid(row=4, column=0, columnspan=4, pady=5)

        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.grid(row=0, column=1, padx=10, pady=10)

    def agregar_nodo(self):
        nodo = self.entry_nodo.get().strip()
        if nodo and nodo not in self.nodos_pos:
            x = random.randint(50, self.canvas_size - 50)
            y = random.randint(50, self.canvas_size - 50)
            self.nodos_pos[nodo] = (x, y)
            self.dibujar_nodo(nodo, x, y)
            self.entry_nodo.delete(0, tk.END)

    def conectar_nodos(self):
        a = self.entry_conexion1.get().strip()
        b = self.entry_conexion2.get().strip()
        if a in self.nodos_pos and b in self.nodos_pos:
            self.grafo[a].append(b)
            self.grafo[b].append(a)
            self.dibujar_arista(a, b)
            self.entry_conexion1.delete(0, tk.END)
            self.entry_conexion2.delete(0, tk.END)

    def dibujar_nodo(self, nombre, x, y):
        r = 15
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="lightblue")
        self.canvas.create_text(x, y, text=nombre)

    def dibujar_arista(self, a, b):
        x1, y1 = self.nodos_pos[a]
        x2, y2 = self.nodos_pos[b]
        self.canvas.create_line(x1, y1, x2, y2, fill="black")

    def verificar_ruta(self):
        inicio = self.entry_inicio.get().strip()
        destino = self.entry_destino.get().strip()
        if inicio not in self.grafo or destino not in self.grafo:
            self.text_resultado.insert(tk.END, "Nodos no válidos\n")
            return

        visitado = set()
        cola = deque([inicio])
        while cola:
            actual = cola.popleft()
            if actual == destino:
                self.text_resultado.insert(tk.END, f"Ruta encontrada de {inicio} a {destino}\n")
                return
            visitado.add(actual)
            for vecino in self.grafo[actual]:
                if vecino not in visitado:
                    cola.append(vecino)
        self.text_resultado.insert(tk.END, f"No hay ruta entre {inicio} y {destino}\n")

    def mostrar_rutas(self):
        inicio = self.entry_inicio.get().strip()
        destino = self.entry_destino.get().strip()
        if inicio not in self.grafo or destino not in self.grafo:
            self.text_resultado.insert(tk.END, "Nodos no válidos\n")
            return

        resultado = []
        self.dfs(inicio, destino, [], set(), resultado)
        if resultado:
            self.text_resultado.insert(tk.END, f"Rutas posibles de {inicio} a {destino}:\n")
            for ruta in resultado:
                self.text_resultado.insert(tk.END, " -> ".join(ruta) + "\n")
        else:
            self.text_resultado.insert(tk.END, "No hay rutas posibles\n")

    def dfs(self, actual, destino, camino, visitado, resultado):
        camino.append(actual)
        visitado.add(actual)
        if actual == destino:
            resultado.append(list(camino))
        else:
            for vecino in self.grafo[actual]:
                if vecino not in visitado:
                    self.dfs(vecino, destino, camino, visitado, resultado)
        camino.pop()
        visitado.remove(actual)




root = tk.Tk()
app = GrafoCiudad(root)
root.mainloop()