import tkinter as tk
from collections import deque

class HistorialDibujo:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Dibujo con Historial de Comandos")

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=4)

        self.undo_stack = deque(maxlen=10)
        self.redo_stack = deque()

        self.start_x = None
        self.start_y = None

        self.canvas.bind("<ButtonPress-1>", self.iniciar_dibujo)
        self.canvas.bind("<ButtonRelease-1>", self.finalizar_dibujo)

        # Botones
        tk.Button(root, text="Deshacer", width=20, command=self.deshacer).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(root, text="Rehacer", width=20, command=self.rehacer).grid(row=1, column=1, padx=10, pady=5)

        # Historial visual
        tk.Label(root, text="Historial de acciones (últimas 10)").grid(row=2, column=1)
        self.listbox_historial = tk.Listbox(root, height=10, width=30)
        self.listbox_historial.grid(row=3, column=1, padx=10, pady=5)

    def iniciar_dibujo(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def finalizar_dibujo(self, event):
        end_x, end_y = event.x, event.y
        line = self.canvas.create_line(self.start_x, self.start_y, end_x, end_y, fill="black", width=2)
        self.undo_stack.append(("draw", line))
        self.redo_stack.clear()
        self.actualizar_historial()

    def deshacer(self):
        if not self.undo_stack:
            return
        accion, obj_id = self.undo_stack.pop()
        if accion == "draw":
            self.canvas.itemconfigure(obj_id, state="hidden")
            self.redo_stack.append((accion, obj_id))
            self.actualizar_historial()

    def rehacer(self):
        if not self.redo_stack:
            return
        accion, obj_id = self.redo_stack.pop()
        if accion == "draw":
            self.canvas.itemconfigure(obj_id, state="normal")
            self.undo_stack.append((accion, obj_id))
            self.actualizar_historial()

    def actualizar_historial(self):
        self.listbox_historial.delete(0, tk.END)
        for i, (accion, obj_id) in enumerate(reversed(self.undo_stack)):
            self.listbox_historial.insert(tk.END, f"{len(self.undo_stack) - i}. {accion} (ID: {obj_id})")


root = tk.Tk()
app = HistorialDibujo(root)
root.mainloop()