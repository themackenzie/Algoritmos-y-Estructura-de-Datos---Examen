import tkinter as tk
from tkinter import ttk
import heapq

class Paciente:
    def __init__(self, nombre, dni, emergencia, tiempo):
        self.nombre = nombre
        self.dni = dni
        self.emergencia = int(emergencia)
        self.tiempo = int(tiempo)

    def __lt__(self, other):
        return self.emergencia < other.emergencia

class SistemaEmergencia:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Emergencia Hospitalaria")

        self.pacientes = []
        self.atendidos = []
        self.total_tiempo = 0

        self.crear_widgets()

    def crear_widgets(self):
        frame_input = ttk.Frame(self.root)
        frame_input.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(frame_input, text="Nombre:").grid(row=0, column=0)
        self.entry_nombre = ttk.Entry(frame_input)
        self.entry_nombre.grid(row=0, column=1)

        ttk.Label(frame_input, text="DNI:").grid(row=0, column=2)
        self.entry_dni = ttk.Entry(frame_input)
        self.entry_dni.grid(row=0, column=3)

        ttk.Label(frame_input, text="Nivel Emergencia (1-5):").grid(row=1, column=0)
        self.entry_emergencia = ttk.Entry(frame_input)
        self.entry_emergencia.grid(row=1, column=1)

        ttk.Label(frame_input, text="Tiempo Atención (min):").grid(row=1, column=2)
        self.entry_tiempo = ttk.Entry(frame_input)
        self.entry_tiempo.grid(row=1, column=3)

        ttk.Button(frame_input, text="Agregar Paciente", command=self.agregar_paciente).grid(row=2, column=0, columnspan=4, pady=10)

        frame_listas = ttk.Frame(self.root)
        frame_listas.grid(row=1, column=0, padx=10, pady=10)

        ttk.Label(frame_listas, text="Pacientes Pendientes (por gravedad)").grid(row=0, column=0)
        self.lista_pacientes = tk.Listbox(frame_listas, width=80)
        self.lista_pacientes.grid(row=1, column=0)

        ttk.Button(frame_listas, text="Atender Siguiente Paciente", command=self.atender_paciente).grid(row=2, column=0, pady=10)

        self.label_estadisticas = ttk.Label(self.root, text="Pacientes atendidos: 0 | Tiempo total de atención: 0 min")
        self.label_estadisticas.grid(row=2, column=0, padx=10, pady=5)

    def agregar_paciente(self):
        nombre = self.entry_nombre.get()
        dni = self.entry_dni.get()
        emergencia = self.entry_emergencia.get()
        tiempo = self.entry_tiempo.get()

        if not (nombre and dni and emergencia.isdigit() and tiempo.isdigit()):
            return

        paciente = Paciente(nombre, dni, int(emergencia), int(tiempo))
        heapq.heappush(self.pacientes, paciente)
        self.actualizar_lista()

        self.entry_nombre.delete(0, tk.END)
        self.entry_dni.delete(0, tk.END)
        self.entry_emergencia.delete(0, tk.END)
        self.entry_tiempo.delete(0, tk.END)

    def atender_paciente(self):
        if self.pacientes:
            paciente = heapq.heappop(self.pacientes)
            self.atendidos.append(paciente)
            self.total_tiempo += paciente.tiempo
            self.actualizar_lista()
            self.actualizar_estadisticas()

    def actualizar_lista(self):
        self.lista_pacientes.delete(0, tk.END)
        for paciente in sorted(self.pacientes):
            self.lista_pacientes.insert(tk.END, f"{paciente.nombre} | DNI: {paciente.dni} | Emergencia: {paciente.emergencia} | Tiempo: {paciente.tiempo} min")

    def actualizar_estadisticas(self):
        self.label_estadisticas.config(
            text=f"Pacientes atendidos: {len(self.atendidos)} | Tiempo total de atención: {self.total_tiempo} min"
        )





root = tk.Tk()
app = SistemaEmergencia(root)
root.mainloop()