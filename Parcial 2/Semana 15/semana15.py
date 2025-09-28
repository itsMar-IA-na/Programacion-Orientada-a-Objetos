import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os
import webbrowser
from datetime import datetime
import uuid

try:
    from tkcalendar import DateEntry
    USE_TKCALENDAR = True
except ImportError:
    USE_TKCALENDAR = False


class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas - Tkinter")
        self.tasks = []  # lista de dicts: id, text, priority, due_date, completed
        self.filename = "tasks_data.json"

        self.create_widgets()
        self.load_tasks()
        self.update_task_list()

        # Generar README automáticamente al iniciar
        self.generate_readme()

    def create_widgets(self):
        top_frame = ttk.Frame(self.root, padding="5")
        top_frame.pack(fill="x")

        self.task_entry = ttk.Entry(top_frame)
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        self.priority_var = tk.StringVar(value="Normal")
        self.priority_menu = ttk.Combobox(
            top_frame, textvariable=self.priority_var, state="readonly",
            values=["Baja", "Normal", "Alta"]
        )
        self.priority_menu.pack(side="left", padx=5)

        if USE_TKCALENDAR:
            self.due_date_entry = DateEntry(top_frame, width=12, background='darkblue',
                                            foreground='white', borderwidth=2)
        else:
            self.due_date_entry = ttk.Entry(top_frame, width=12)
            self.due_date_entry.insert(0, "YYYY-MM-DD")
        self.due_date_entry.pack(side="left", padx=5)

        ttk.Button(top_frame, text="Añadir", command=self.add_task).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Completar", command=self.mark_completed).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Eliminar", command=self.delete_task).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Cargar ejemplo", command=self.load_sample_tasks).pack(side="left", padx=5)

        filter_frame = ttk.Frame(self.root, padding="5")
        filter_frame.pack(fill="x")

        ttk.Label(filter_frame, text="Buscar:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.update_task_list())
        ttk.Entry(filter_frame, textvariable=self.search_var).pack(side="left", fill="x", expand=True, padx=5)

        self.filter_var = tk.StringVar(value="Todas")
        status_cb = ttk.Combobox(
            filter_frame, textvariable=self.filter_var, state="readonly",
            values=["Todas", "Activas", "Completadas"]
        )
        status_cb.pack(side="left", padx=5)
        self.filter_var.trace_add("write", lambda *args: self.update_task_list())

        self.priority_filter_var = tk.StringVar(value="Todas")
        prio_cb = ttk.Combobox(
            filter_frame, textvariable=self.priority_filter_var, state="readonly",
            values=["Todas", "Baja", "Normal", "Alta"]
        )
        prio_cb.pack(side="left", padx=5)
        self.priority_filter_var.trace_add("write", lambda *args: self.update_task_list())

        columns = ("Tarea", "Prioridad", "Vencimiento", "Estado")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", selectmode="extended", height=20)
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Tarea":
                self.tree.column(col, width=220)
            elif col == "Vencimiento":
                self.tree.column(col, width=210, anchor="center")
            else:
                self.tree.column(col, width=300, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree.bind("<Double-1>", lambda e: self.mark_completed())
        self.root.bind("<Delete>", lambda e: self.delete_task())
        self.root.bind("<Control-n>", lambda e: self.task_entry.focus())

        self.status_var = tk.StringVar(value="Listo")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(fill="x", side="bottom")

        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Importar CSV", command=self.import_csv)
        file_menu.add_command(label="Exportar CSV", command=self.export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Generar README", command=self.generate_readme)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        self.root.config(menu=menu_bar)

    def add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            messagebox.showwarning("Aviso", "La tarea no puede estar vacía")
            return
        priority = self.priority_var.get()
        due_date = self.get_due_date()
        new_task = {
            "id": str(uuid.uuid4()),
            "text": text,
            "priority": priority,
            "due_date": due_date,
            "completed": False
        }
        self.tasks.append(new_task)
        self.task_entry.delete(0, tk.END)
        self.save_tasks()
        self.update_task_list()
        self.status_var.set("Tarea añadida")

    def get_due_date(self):
        if USE_TKCALENDAR:
            try:
                return self.due_date_entry.get_date().strftime("%Y-%m-%d")
            except Exception:
                return ""
        else:
            raw = self.due_date_entry.get().strip()
            if raw == "YYYY-MM-DD" or raw == "":
                return ""
            try:
                datetime.strptime(raw, "%Y-%m-%d")
                return raw
            except ValueError:
                return ""

    def mark_completed(self):
        for item in self.tree.selection():
            tags = self.tree.item(item, "tags")
            if not tags:
                continue
            tid = tags[0]
            task = next((t for t in self.tasks if t.get("id") == tid), None)
            if task:
                task["completed"] = not bool(task.get("completed", False))
        self.save_tasks()
        self.update_task_list()
        self.status_var.set("Estado cambiado")

    def delete_task(self):
        sel = self.tree.selection()
        if not sel:
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar las tareas seleccionadas?"):
            return
        ids_to_remove = []
        for item in sel:
            tags = self.tree.item(item, "tags")
            if tags:
                ids_to_remove.append(tags[0])
        self.tasks = [t for t in self.tasks if t.get("id") not in ids_to_remove]
        self.save_tasks()
        self.update_task_list()
        self.status_var.set("Eliminadas tareas seleccionadas")

    def update_task_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        search_text = (self.search_var.get() or "").lower()
        filter_status = self.filter_var.get()
        filter_priority = self.priority_filter_var.get()

        for task in self.tasks:
            text = task.get("text", "")
            due = task.get("due_date", "") or ""
            completed = bool(task.get("completed", False))
            priority = task.get("priority", "Normal")

            if search_text and (search_text not in text.lower() and search_text not in due.lower()):
                continue
            if filter_status == "Activas" and completed:
                continue
            if filter_status == "Completadas" and not completed:
                continue
            if filter_priority != "Todas" and priority != filter_priority:
                continue

            state_str = "Completada" if completed else "Pendiente"
            values = (text, priority, due, state_str)
            self.tree.insert("", "end", values=values, tags=(task.get("id"),))

    def save_tasks(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                normalized = []
                for t in loaded:
                    if not isinstance(t, dict):
                        continue
                    normalized.append({
                        "id": t.get("id", str(uuid.uuid4())),
                        "text": t.get("text", ""),
                        "priority": t.get("priority", "Normal"),
                        "due_date": t.get("due_date", "") or "",
                        "completed": bool(t.get("completed", False))
                    })
                self.tasks = normalized
            except Exception:
                self.tasks = []

    def export_csv(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file:
            with open(file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["id", "text", "priority", "due_date", "completed"])
                writer.writeheader()
                writer.writerows(self.tasks)
            self.status_var.set("Exportado a CSV")

    def import_csv(self):
        file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file:
            return
        try:
            imported = []
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    text = row.get("text") or row.get("task") or ""
                    if not text:
                        continue
                    imported.append({
                        "id": row.get("id", str(uuid.uuid4())),
                        "text": text,
                        "priority": row.get("priority", "Normal"),
                        "due_date": row.get("due_date", "") or "",
                        "completed": row.get("completed", "").strip().lower() in ("true", "1", "yes", "y")
                    })
            self.tasks.extend(imported)
            self.save_tasks()
            self.update_task_list()
            self.status_var.set(f"Importadas {len(imported)} tareas desde CSV")
        except Exception as ex:
            messagebox.showerror("Error al importar", f"No se pudo importar: {ex}")

    def load_sample_tasks(self):
        samples = [
            {"id": str(uuid.uuid4()), "text": "Hacer el examen de Estadística", "priority": "Alta",
             "due_date": "", "completed": False},
            {"id": str(uuid.uuid4()), "text": "Ir a hacer ejercicio (2 hrs)", "priority": "Normal",
             "due_date": "", "completed": False},
            {"id": str(uuid.uuid4()), "text": "Hacer el deber de programación", "priority": "Alta",
             "due_date": "", "completed": False},
            {"id": str(uuid.uuid4()), "text": "Revisar grabaciones del seminario", "priority": "Baja",
             "due_date": "", "completed": False},
        ]
        existing_texts = {t.get("text") for t in self.tasks}
        added = 0
        for s in samples:
            if s["text"] not in existing_texts:
                self.tasks.append(s)
                added += 1
        self.save_tasks()
        self.update_task_list()
        self.status_var.set(f"Cargadas {added} tareas de ejemplo")

    def generate_readme(self):
        readme_content = (
            "# Lista de Tareas en Tkinter\n\n"
            "Aplicación de escritorio hecha con **Python y Tkinter** para gestionar tus tareas.\n\n"
            "## Características\n"
            "- Añadir nuevas tareas con prioridad y fecha de vencimiento\n"
            "- Marcar tareas como completadas o pendientes (doble clic o botón)\n"
            "- Eliminar tareas seleccionadas\n"
            "- Filtrar por estado (todas, activas, completadas)\n"
            "- Filtrar por prioridad (baja, normal, alta)\n"
            "- Buscar tareas por texto o fecha\n"
            "- Importar y exportar tareas en formato CSV\n"
            "- Cargar ejemplos de tareas\n\n"
            "## Cómo usar\n"
            "1. Escribe una tarea en el campo de texto.\n"
            "2. Selecciona la prioridad (Baja, Normal o Alta).\n"
            "3. (Opcional) Define la fecha de vencimiento.\n"
            "4. Haz clic en **Añadir** para guardarla.\n\n"
            "### Acciones rápidas\n"
            "- Doble clic en una tarea → marcar como completada o pendiente\n"
            "- Tecla **Delete** → elimina las tareas seleccionadas\n"
            "- Ctrl+N → enfoca el cuadro de texto para añadir nueva tarea\n\n"
            "## Requisitos\n"
            "- Python 3.x\n"
            "- Tkinter (incluido en la mayoría de instalaciones)\n"
            "- Opcional: tkcalendar (`pip install tkcalendar`) para seleccionar fechas con calendario\n\n"
            "## Notas\n"
            "- Las tareas se guardan automáticamente en `tasks_data.json`.\n"
            "- El README se genera automáticamente cada vez que se ejecuta el programa.\n"
        )
        try:
            file_path = os.path.abspath("README.md")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(readme_content)
            self.status_var.set("README.md generado automáticamente")
        except Exception as ex:
            messagebox.showerror("Error", f"No se pudo generar README.md: {ex}")


if __name__ == "__main__":
    root = tk.Tk()
    TaskManager(root)
    root.mainloop()
