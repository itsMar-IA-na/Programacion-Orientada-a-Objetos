import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import json
import os

# Intentamos importar DateEntry desde tkcalendar. Si no está, lo notificamos.
try:
    from tkcalendar import DateEntry
    has_dateentry = True
except Exception:
    has_dateentry = False

DATA_FILE = "agenda_eventos.json"


class AgendaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agenda Personal - Mejorada")
        self.geometry("1020x680")
        self.resizable(False, False)

        # Layout principal
        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Grid config
        self.main_frame.columnconfigure(0, weight=3)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Crear componentes
        self._create_treeview_frame()
        self._create_input_frame()
        self._create_actions_frame()

        # Cargar (o inicializar) eventos
        self._load_or_initialize_events()

    def _create_treeview_frame(self):
        frame = ttk.Frame(self.main_frame)
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ttk.Label(frame, text="Eventos programados", font=("Segoe UI", 12, "bold")).pack(anchor="w")

        columns = ("fecha", "hora", "descripcion")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.column("fecha", width=110, anchor="center")
        self.tree.column("hora", width=80, anchor="center")
        self.tree.column("descripcion", width=520, anchor="w")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind doble clic para editar
        self.tree.bind("<Double-1>", self._on_tree_double_click)

    def _create_input_frame(self):
        frame = ttk.LabelFrame(self.main_frame, text="Agregar / Editar evento", padding=10)
        frame.grid(row=0, column=1, sticky="nsew")

        # Fecha
        ttk.Label(frame, text="Fecha (DD/MM/YYYY):").grid(row=0, column=0, sticky="w")
        if has_dateentry:
            self.date_entry = DateEntry(frame, date_pattern="dd/MM/yyyy")
            self.date_entry.grid(row=0, column=1, padx=5, pady=3, sticky="ew")
        else:
            self.date_entry = ttk.Entry(frame)
            self.date_entry.insert(0, date.today().strftime("%d/%m/%Y"))
            self.date_entry.grid(row=0, column=1, padx=5, pady=3, sticky="ew")
            ttk.Label(frame, text="(pip install tkcalendar para calendario)", foreground="orange").grid(row=1, column=0, columnspan=2, sticky="w")

        # Hora
        ttk.Label(frame, text="Hora (HH:MM):").grid(row=2, column=0, sticky="w", pady=(8,0))
        self.time_entry = ttk.Entry(frame)
        self.time_entry.insert(0, "07:30")
        self.time_entry.grid(row=2, column=1, padx=5, pady=(8,0), sticky="ew")

        # Descripción (Text)
        ttk.Label(frame, text="Descripción:").grid(row=3, column=0, sticky="nw", pady=(8,0))
        self.desc_text = tk.Text(frame, width=30, height=6, wrap="word")
        self.desc_text.grid(row=3, column=1, padx=5, pady=(8,0), sticky="ew")

        # Buttons: agregar y limpiar
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(10,0), sticky="ew")
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        add_btn = ttk.Button(btn_frame, text="Agregar Evento", command=self.add_event)
        add_btn.grid(row=0, column=0, padx=(0,5), sticky="ew")

        clear_btn = ttk.Button(btn_frame, text="Limpiar campos", command=self._clear_input_fields)
        clear_btn.grid(row=0, column=1, padx=(5,0), sticky="ew")

    def _create_actions_frame(self):
        frame = ttk.Frame(self.main_frame)
        frame.grid(row=1, column=1, sticky="nsew", pady=(10,0))

        del_btn = ttk.Button(frame, text="Eliminar Evento Seleccionado", command=self.delete_selected_event)
        del_btn.pack(fill=tk.X, pady=(0,6))

        save_btn = ttk.Button(frame, text="Guardar en archivo", command=self._save_events_to_file)
        save_btn.pack(fill=tk.X, pady=(0,6))

        exit_btn = ttk.Button(frame, text="Salir", command=self._on_exit)
        exit_btn.pack(fill=tk.X)

    # -------------------- Lógica de eventos --------------------
    def add_event(self):
        """Agregar evento validando formatos, confirmar y ordenar lista."""
        fecha_text = self.date_entry.get().strip()
        hora_text = self.time_entry.get().strip()
        descripcion = self.desc_text.get("1.0", tk.END).strip()

        if not fecha_text or not hora_text or not descripcion:
            messagebox.showwarning("Campos incompletos", "Por favor completa fecha, hora y descripción.")
            return

        # Validar fecha
        try:
            fecha_dt = datetime.strptime(fecha_text, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Formato fecha inválido", "La fecha debe estar en formato DD/MM/YYYY.")
            return

        # Validar hora
        try:
            hora_dt = datetime.strptime(hora_text, "%H:%M")
        except ValueError:
            messagebox.showerror("Formato hora inválido", "La hora debe estar en formato HH:MM (24 horas).")
            return

        fecha_display = fecha_dt.strftime("%d/%m/%Y")
        hora_display = hora_dt.strftime("%H:%M")

        # Insertar en Treeview
        self.tree.insert("", tk.END, values=(fecha_display, hora_display, descripcion))

        # Ordenar
        self._sort_tree_by_datetime()

        # Limpiar y confirmar
        self._clear_input_fields()
        messagebox.showinfo("Evento agregado", f"Evento agregado: {fecha_display} {hora_display} — \"{descripcion[:40]}\"")

    def delete_selected_event(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selecciona un evento", "Por favor selecciona el evento que deseas eliminar.")
            return

        item = selected[0]
        values = self.tree.item(item, "values")
        fecha, hora, desc = values[0], values[1], values[2][:80] + ("..." if len(values[2])>80 else "")
        confirm = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar el evento del {fecha} a las {hora}?\n\n\"{desc}\"")
        if confirm:
            for it in selected:
                self.tree.delete(it)

    def _on_exit(self):
        if messagebox.askyesno("Salir", "¿Deseas guardar los eventos antes de salir?"):
            self._save_events_to_file()
        self.destroy()

    # -------------------- Utilidades --------------------
    def _clear_input_fields(self):
        if has_dateentry:
            # dejar la fecha actual en el DateEntry
            self.date_entry.set_date(date.today())
        else:
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, date.today().strftime("%d/%m/%Y"))
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "07:30")
        self.desc_text.delete("1.0", tk.END)

    def _save_events_to_file(self):
        items = self.tree.get_children()
        eventos = []
        for it in items:
            fecha, hora, desc = self.tree.item(it, "values")
            eventos.append({"fecha": fecha, "hora": hora, "descripcion": desc})
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(eventos, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Guardado", f"{len(eventos)} evento(s) guardado(s) en {DATA_FILE}.")
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No fue posible guardar los eventos:\n{e}")

    def _load_or_initialize_events(self):
        """Si existe archivo JSON lo carga; si no, crea 3 eventos de ejemplo."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    eventos = json.load(f)
                for ev in eventos:
                    self.tree.insert("", tk.END, values=(ev.get("fecha", ""), ev.get("hora", ""), ev.get("descripcion", "")))
                self._sort_tree_by_datetime()
                return
            except Exception:
                # Si falla la lectura, seguiremos con eventos por defecto
                pass

        # Agregamos 3 eventos de ejemplo (fecha = hoy)
        hoy = date.today().strftime("%d/%m/%Y")
        ejemplos = [
            (hoy, "07:30", "Ir a entrenar al gym"),
            (hoy, "15:00", "Ir a entrenar muay thai"),
            (hoy, "18:00", "Asistir a la tutoría de Matemática II"),
        ]
        for f, h, d in ejemplos:
            self.tree.insert("", tk.END, values=(f, h, d))
        self._sort_tree_by_datetime()

    def _sort_tree_by_datetime(self):
        """Ordena los ítems del Treeview por fecha+hora ascendente."""
        items = list(self.tree.get_children())

        def key_fn(item):
            fecha, hora, _ = self.tree.item(item, "values")
            try:
                dt = datetime.strptime(f"{fecha} {hora}", "%d/%m/%Y %H:%M")
            except Exception:
                # Si hay formato inválido, poner muy atrás
                dt = datetime.max
            return dt

        items_sorted = sorted(items, key=key_fn)

        # Reinsertar en orden
        for i, it in enumerate(items_sorted):
            self.tree.move(it, "", i)

    # -------------------- Edición por doble clic --------------------
    def _on_tree_double_click(self, event):
        item_id = self.tree.focus()
        if not item_id:
            return
        values = self.tree.item(item_id, "values")
        if not values:
            return
        fecha, hora, desc = values
        EditDialog(self, item_id, fecha, hora, desc, self._on_edit_saved)

    def _on_edit_saved(self, item_id, new_fecha, new_hora, new_desc):
        """Callback cuando el diálogo de edición guarda cambios."""
        self.tree.item(item_id, values=(new_fecha, new_hora, new_desc))
        self._sort_tree_by_datetime()
        messagebox.showinfo("Evento editado", "Los cambios fueron guardados correctamente.")


# -------------------- Dialogo de edición --------------------
class EditDialog(tk.Toplevel):
    def __init__(self, parent, item_id, fecha, hora, desc, callback):
        super().__init__(parent)
        self.title("Editar evento")
        self.resizable(False, False)
        self.item_id = item_id
        self.callback = callback
        self.geometry("360x260")
        self.transient(parent)
        self.grab_set()

        ttk.Label(self, text="Fecha (DD/MM/YYYY):").pack(anchor="w", padx=10, pady=(10,0))
        if has_dateentry:
            self.date_entry = DateEntry(self, date_pattern="dd/MM/yyyy")
            try:
                self.date_entry.set_date(datetime.strptime(fecha, "%d/%m/%Y"))
            except Exception:
                pass
            self.date_entry.pack(fill="x", padx=10, pady=3)
        else:
            self.date_entry = ttk.Entry(self)
            self.date_entry.pack(fill="x", padx=10, pady=3)
            self.date_entry.insert(0, fecha)

        ttk.Label(self, text="Hora (HH:MM):").pack(anchor="w", padx=10, pady=(8,0))
        self.time_entry = ttk.Entry(self)
        self.time_entry.pack(fill="x", padx=10, pady=3)
        self.time_entry.insert(0, hora)

        ttk.Label(self, text="Descripción:").pack(anchor="w", padx=10, pady=(8,0))
        self.desc_text = tk.Text(self, width=40, height=5, wrap="word")
        self.desc_text.pack(padx=10, pady=3, fill="both")
        self.desc_text.insert("1.0", desc)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=(8,10))
        save_btn = ttk.Button(btn_frame, text="Guardar", command=self._on_save)
        save_btn.pack(side="left", expand=True, fill="x", padx=(0,5))
        cancel_btn = ttk.Button(btn_frame, text="Cancelar", command=self._on_cancel)
        cancel_btn.pack(side="left", expand=True, fill="x", padx=(5,0))

    def _on_save(self):
        new_fecha = self.date_entry.get().strip()
        new_hora = self.time_entry.get().strip()
        new_desc = self.desc_text.get("1.0", tk.END).strip()

        # Validaciones
        try:
            datetime.strptime(new_fecha, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Formato fecha inválido", "La fecha debe estar en formato DD/MM/YYYY.")
            return
        try:
            datetime.strptime(new_hora, "%H:%M")
        except ValueError:
            messagebox.showerror("Formato hora inválido", "La hora debe estar en formato HH:MM (24 horas).")
            return
        if not new_desc:
            messagebox.showwarning("Descripción vacía", "La descripción no puede quedar vacía.")
            return

        # Llamar al callback del padre
        self.callback(self.item_id, new_fecha, new_hora, new_desc)
        self.destroy()

    def _on_cancel(self):
        self.destroy()


if __name__ == "__main__":
    if not has_dateentry:
        print("Aviso: tkcalendar no está instalado.")
        print("Para instalarlo ejecuta: File - Settings - Project - Python project - install tkcalendar")
    app = AgendaApp()
    app.mainloop()
