import tkinter as tk
from tkinter import ttk, messagebox
import datetime


class AplicacionGUI(tk.Tk):
    """Clase principal de la aplicación.

    Decisiones de diseño:
    - Uso de ttk.Treeview como tabla por su facilidad para mostrar columnas.
    - Se mantienen los datos en memoria en self._data (lista de dicts) por si se desea
      añadir persistencia (guardar a CSV/JSON) más adelante.
    - Botón 'Limpiar' con comportamiento dual (borrar selección o limpiar entradas) para
      cumplir con el requisito de borrar "la información ingresada o seleccionada".
    """

    def __init__(self):
        super().__init__()
        self.title("Aplicación GUI Básica - Gestor de Entradas")
        self.geometry("720x460")
        self.resizable(True, True)

        # Contador de IDs para cada entrada
        self._id_counter = 1
        # Estructura de datos en memoria (opcional)
        self._data = []

        self._create_widgets()
        self._place_widgets()
        self._setup_bindings()

    def _create_widgets(self):
        # Frames para organización
        self.frame_inputs = ttk.LabelFrame(self, text="Entradas")
        self.frame_buttons = ttk.Frame(self)
        self.frame_table = ttk.Frame(self)

        # Campos de entrada
        self.lbl_nombre = ttk.Label(self.frame_inputs, text="Nombre:")
        self.entry_nombre = ttk.Entry(self.frame_inputs)

        self.lbl_descripcion = ttk.Label(self.frame_inputs, text="Descripción:")
        # Usamos un Text para descripción (multi-línea)
        self.text_descripcion = tk.Text(self.frame_inputs, height=4, wrap=tk.WORD)

        # Botones
        self.btn_agregar = ttk.Button(self.frame_buttons, text="Agregar", command=self.agregar_item)
        self.btn_limpiar = ttk.Button(self.frame_buttons, text="Limpiar", command=self.limpiar_accion)

        # Tabla (Treeview)
        columns = ("ID", "Nombre", "Descripción")
        self.tree = ttk.Treeview(self.frame_table, columns=columns, show="headings", selectmode="extended")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripción", text="Descripción")

        # Anchos de columna (se pueden ajustar)
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Nombre", width=180, anchor=tk.W)
        self.tree.column("Descripción", width=420, anchor=tk.W)

        # Scrollbars para la tabla
        self.v_scroll = ttk.Scrollbar(self.frame_table, orient=tk.VERTICAL, command=self.tree.yview)
        self.h_scroll = ttk.Scrollbar(self.frame_table, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        # Etiqueta de estado simple
        self.status_var = tk.StringVar(value="Listo")
        self.status = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)

    def _place_widgets(self):
        # Layout: pack frames, dentro de ellos usar grid
        self.frame_inputs.pack(fill=tk.X, padx=10, pady=8)
        self.frame_buttons.pack(fill=tk.X, padx=10, pady=4)
        self.frame_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        # Inputs grid
        self.lbl_nombre.grid(row=0, column=0, sticky=tk.W, padx=6, pady=4)
        self.entry_nombre.grid(row=0, column=1, sticky=tk.EW, padx=6, pady=4)
        self.lbl_descripcion.grid(row=1, column=0, sticky=tk.NW, padx=6, pady=4)
        self.text_descripcion.grid(row=1, column=1, sticky=tk.EW, padx=6, pady=4)

        # Make the second column expand when resizing
        self.frame_inputs.columnconfigure(1, weight=1)

        # Buttons
        self.btn_agregar.pack(side=tk.LEFT, padx=6)
        self.btn_limpiar.pack(side=tk.LEFT, padx=6)

        # Table packing
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        self.v_scroll.grid(row=0, column=1, sticky=tk.NS)
        self.h_scroll.grid(row=1, column=0, sticky=tk.EW, columnspan=2)

        self.frame_table.columnconfigure(0, weight=1)
        self.frame_table.rowconfigure(0, weight=1)

        # Status bar
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def _setup_bindings(self):
        # Enter para agregar desde entry_nombre
        self.entry_nombre.bind("<Return>", lambda e: self.agregar_item())
        # Ctrl+Enter en text_descripcion también agrega
        self.text_descripcion.bind("<Control-Return>", lambda e: self.agregar_item())
        # Doble click en fila carga datos a los inputs
        self.tree.bind("<Double-1>", lambda e: self.cargar_seleccion_en_inputs())

    def agregar_item(self):
        """Toma los datos de los campos y los inserta en la tabla.

        Validaciones simples: al menos uno de los campos debe tener texto.
        """
        nombre = self.entry_nombre.get().strip()
        descripcion = self.text_descripcion.get("1.0", tk.END).strip()

        if not nombre and not descripcion:
            messagebox.showwarning("Entrada vacía", "Por favor ingresa al menos Nombre o Descripción antes de agregar.")
            return

        item_id = self._id_counter
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insertar en tabla
        # Guardamos ID numérico como valor para poder luego buscar o eliminar si se desea
        self.tree.insert("", tk.END, iid=str(item_id), values=(item_id, nombre, descripcion))

        # Guardar en memoria (opcional, útil para persistencia futura)
        self._data.append({"id": item_id, "nombre": nombre, "descripcion": descripcion, "ts": timestamp})

        self._id_counter += 1

        # Limpiar entradas y actualizar estado
        self._limpiar_inputs(leave_focus_to=self.entry_nombre)
        self.status_var.set(f"Agregado ID {item_id} — {timestamp}")

    def limpiar_accion(self):
        """Si hay filas seleccionadas, las elimina. Si no hay selección, limpia los campos de entrada."""
        seleccion = self.tree.selection()
        if seleccion:
            # Confirmación para evitar borrados accidentales
            if messagebox.askyesno("Confirmar eliminación", f"¿Eliminar {len(seleccion)} elemento(s) seleccionados?"):
                for iid in seleccion:
                    # Intentar eliminar del almacenamiento en memoria (si existe)
                    try:
                        # Los valores guardados como strings; obtenemos el primer valor (ID)
                        values = self.tree.item(iid, "values")
                        if values:
                            id_val = int(values[0])
                            # Quitar del _data (si existe)
                            self._data = [d for d in self._data if d.get("id") != id_val]
                    except Exception:
                        pass
                    # Eliminar de la treeview
                    self.tree.delete(iid)
                self.status_var.set(f"Eliminados {len(seleccion)} elemento(s)")
        else:
            # Ninguna selección: limpiamos los campos de entrada
            self._limpiar_inputs()
            self.status_var.set("Campos limpiados")

    def _limpiar_inputs(self, leave_focus_to=None):
        """Limpia los widgets de entrada."""
        self.entry_nombre.delete(0, tk.END)
        self.text_descripcion.delete("1.0", tk.END)
        if leave_focus_to:
            leave_focus_to.focus_set()

    def cargar_seleccion_en_inputs(self):
        """Carga la fila seleccionada (la primera si hay varias) en los campos para editar/visualizar."""
        seleccion = self.tree.selection()
        if not seleccion:
            return
        iid = seleccion[0]
        values = self.tree.item(iid, "values")
        if not values:
            return
        # Los valores están en el orden (ID, Nombre, Descripción)
        _, nombre, descripcion = values
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, nombre)
        self.text_descripcion.delete("1.0", tk.END)
        self.text_descripcion.insert(tk.END, descripcion)
        self.entry_nombre.focus_set()
        self.status_var.set(f"Cargado ID {values[0]} para edición")


if __name__ == "__main__":
    app = AplicacionGUI()
    app.mainloop()

