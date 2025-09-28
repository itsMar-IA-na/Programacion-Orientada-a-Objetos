"""
sistema_libros.py

Sistema de gestión de inventario de libros con interfaz Tkinter y persistencia en CSV.
Versión corregida y en español — lista para ejecutar en PyCharm.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from datetime import datetime

ARCHIVO_LIBROS = "libros.csv"
ENCABEZADOS = ["id", "isbn", "titulo", "autor", "editorial", "anio",
               "categoria", "cantidad", "precio", "descripcion"]


# ---------- Clase Libro ----------
class Libro:
    def __init__(self, id="", isbn="", titulo="", autor="", editorial="", anio=0,
                 categoria="", cantidad=0, precio=0.0, descripcion=""):
        self.id = str(id)
        self.isbn = str(isbn)
        self.titulo = str(titulo)
        self.autor = str(autor)
        # editoriales y demás los mantenemos como strings internamente
        self.editorial = str(editorial)
        try:
            self.anio = int(anio)
        except (ValueError, TypeError):
            self.anio = 0
        self.categoria = str(categoria)
        try:
            self.cantidad = int(cantidad)
        except (ValueError, TypeError):
            self.cantidad = 0
        try:
            self.precio = float(precio)
        except (ValueError, TypeError):
            self.precio = 0.0
        self.descripcion = str(descripcion)

    def a_lista(self):
        """Devuelve una lista de strings para insertar en el Treeview / CSV."""
        return [
            str(self.id),
            str(self.isbn),
            str(self.titulo),
            str(self.autor),
            str(self.editorial),
            str(self.anio),
            str(self.categoria),
            str(self.cantidad),
            f"{self.precio:.2f}",
            str(self.descripcion)
        ]

    @classmethod
    def desde_dict(cls, d):
        """Crear Libro desde un dict (por ejemplo leído del CSV)."""
        return cls(
            id=d.get("id", ""),
            isbn=d.get("isbn", ""),
            titulo=d.get("titulo", ""),
            autor=d.get("autor", ""),
            editorial=d.get("editorial", ""),
            anio=d.get("anio", 0),
            categoria=d.get("categoria", ""),
            cantidad=d.get("cantidad", 0),
            precio=d.get("precio", 0.0),
            descripcion=d.get("descripcion", "")
        )


# ---------- Clase GestorLibros ----------
class GestorLibros:
    def __init__(self, archivo=ARCHIVO_LIBROS):
        self.archivo = archivo
        # si no existe, crear con ejemplos
        if not os.path.exists(self.archivo):
            self._crear_con_ejemplos()

    def _crear_con_ejemplos(self):
        ejemplos = [
            Libro(id="B001", isbn="9780140449266", titulo="La Odisea", autor="Homero",
                  editorial="Penguin Classics", anio=2003, categoria="Clásicos", cantidad=5, precio=9.50,
                  descripcion="Traducción moderna"),
            Libro(id="B002", isbn="9780307277785", titulo="Sapiens", autor="Yuval Noah Harari",
                  editorial="Harper", anio=2015, categoria="Historia", cantidad=3, precio=12.99,
                  descripcion="Breve historia de la humanidad"),
            Libro(id="B003", isbn="9780131103627", titulo="The C Programming Language",
                  autor="Kernighan & Ritchie", editorial="Prentice Hall", anio=1988,
                  categoria="Programación", cantidad=2, precio=25.00, descripcion="Clásico técnico"),
        ]
        self.guardar_todos(ejemplos)

    def cargar_todos(self):
        libros = []
        if not os.path.exists(self.archivo):
            return libros
        try:
            with open(self.archivo, newline="", encoding="utf-8") as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    # Normalizar claves: asegurar que existan todas
                    row = {k: fila.get(k, "") for k in ENCABEZADOS}
                    libros.append(Libro.desde_dict(row))
        except Exception as e:
            # Si ocurre error, devolvemos lista vacía y mostramos aviso en consola
            print("Error al leer CSV:", e)
            return []
        return libros

    def guardar_todos(self, lista_libros):
        try:
            with open(self.archivo, "w", newline="", encoding="utf-8") as f:
                escritor = csv.writer(f)
                escritor.writerow(ENCABEZADOS)
                for libro in lista_libros:
                    escritor.writerow(libro.a_lista())
        except Exception as e:
            print("Error al guardar CSV:", e)

    def agregar_libro(self, libro: Libro):
        libros = self.cargar_todos()
        # si ID ya existe, sobrescribir
        exist = {l.id: l for l in libros}
        exist[libro.id] = libro
        self.guardar_todos(list(exist.values()))

    def actualizar_libro(self, libro_id: str, nuevo_libro: Libro) -> bool:
        libros = self.cargar_todos()
        modificado = False
        for i, l in enumerate(libros):
            if l.id == libro_id:
                libros[i] = nuevo_libro
                modificado = True
                break
        if modificado:
            self.guardar_todos(libros)
        return modificado

    def eliminar_libro(self, libro_id: str) -> bool:
        libros = self.cargar_todos()
        filtrado = [l for l in libros if l.id != libro_id]
        if len(filtrado) == len(libros):
            return False
        self.guardar_todos(filtrado)
        return True


# ---------- Interfaz gráfica ----------
class InterfazPrincipal:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("📚 Sistema de Gestión de Libros")
        self.ventana.geometry("1100x650")
        self.gestor = GestorLibros()
        self.libros = self.gestor.cargar_todos()
        self._crear_widgets()
        self.cargar_tabla()

    def _crear_widgets(self):
        # Marco formulario
        marco_formulario = ttk.LabelFrame(self.ventana, text="Información del libro", padding=8)
        marco_formulario.pack(fill="x", padx=8, pady=8)

        # Etiquetas visibles y claves internas sin acentos
        campos = [
            ("ID", "id"), ("ISBN", "isbn"), ("Título", "titulo"), ("Autor", "autor"),
            ("Editorial", "editorial"), ("Año", "anio"), ("Categoría", "categoria"),
            ("Cantidad", "cantidad"), ("Precio", "precio"), ("Descripción", "descripcion")
        ]
        self.entradas = {}
        # Grid: dos columnas de campo+entrada por fila
        fila = 0
        col = 0
        for etiqueta, clave in campos:
            lbl = ttk.Label(marco_formulario, text=f"{etiqueta}:")
            lbl.grid(row=fila, column=col * 2, padx=6, pady=4, sticky="w")
            ent = ttk.Entry(marco_formulario, width=28)
            ent.grid(row=fila, column=col * 2 + 1, padx=6, pady=4, sticky="w")
            self.entradas[clave] = ent
            col += 1
            if col >= 2:
                col = 0
                fila += 1

        # Botones
        marco_botones = ttk.Frame(self.ventana, padding=6)
        marco_botones.pack(fill="x", padx=8)

        ttk.Button(marco_botones, text="Agregar", command=self.agregar_libro).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Editar", command=self.editar_libro).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Eliminar", command=self.eliminar_libro).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Guardar cambios", command=self.guardar_cambios).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Importar CSV", command=self.importar_csv).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Exportar CSV", command=self.exportar_csv).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Limpiar campos", command=self.limpiar_campos).pack(side="left", padx=4)

        # Tabla (Treeview)
        marco_tabla = ttk.Frame(self.ventana, padding=6)
        marco_tabla.pack(fill="both", expand=True, padx=8, pady=8)

        columnas = ENCABEZADOS[:]
        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", selectmode="browse")
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize(), command=lambda c=col: self._ordenar_por(c, False))
            # ancho provisional
            if col in ("titulo", "autor"):
                self.tabla.column(col, width=220, anchor="w")
            elif col == "descripcion":
                self.tabla.column(col, width=260, anchor="w")
            elif col == "precio":
                self.tabla.column(col, width=90, anchor="e")
            else:
                self.tabla.column(col, width=100, anchor="w")

        # Forzar estilo para evitar texto invisible y ajustar altura de filas
        style = ttk.Style()
        style.configure("Treeview", foreground="black", rowheight=22)
        style.configure("Treeview.Heading", font=("TkDefaultFont", 9, "bold"))

        vsb = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tabla.pack(side="left", fill="both", expand=True)

        self.tabla.bind("<<TreeviewSelect>>", self.mostrar_detalles)

        # Barra de estado
        self.estado_var = tk.StringVar(value="Listo")
        etiqueta_estado = ttk.Label(self.ventana, textvariable=self.estado_var, relief="sunken", anchor="w")
        etiqueta_estado.pack(side="bottom", fill="x")

    # ---------- Operaciones sobre la tabla ----------
    def cargar_tabla(self):
        # vaciar
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # recargar lista desde gestor por si hubo cambios
        if self.libros is None:
            self.libros = []

        # insertar filas (si no hay libros, la tabla quedará vacía)
        for libro in self.libros:
            self.tabla.insert("", "end", values=libro.a_lista())

        # forzar refresco y ajustar anchos
        self.tabla.update_idletasks()
        self._ajustar_ancho_columnas()

    def _ajustar_ancho_columnas(self, ancho_max=450):
        """Ajusta ancho de columnas según contenido (estimación por caracteres)."""
        for col in self.tabla["columns"]:
            ancho = max(len(col) * 8 + 20, 80)
            for item in self.tabla.get_children():
                valor = str(self.tabla.set(item, col))
                ancho = max(ancho, min(len(valor) * 8 + 20, ancho_max))
            self.tabla.column(col, width=ancho)

    def mostrar_detalles(self, event=None):
        sel = self.tabla.selection()
        if not sel:
            return
        vals = self.tabla.item(sel[0], "values")
        # mapear valores a entradas según ENCABEZADOS
        for i, clave in enumerate(ENCABEZADOS):
            ent = self.entradas.get(clave)
            if ent is not None:
                ent.delete(0, tk.END)
                ent.insert(0, vals[i])

    # ---------- Validación/Construcción de Libro desde formulario ----------
    def _leer_formulario(self) -> (bool, Libro):
        """Lee entradas y devuelve (ok, libro). Si ok False, se muestran warnings."""
        datos = {}
        for clave in ENCABEZADOS:
            ent = self.entradas.get(clave)
            datos[clave] = ent.get().strip() if ent else ""

        # Validaciones básicas
        if not datos["id"] or not datos["titulo"]:
            messagebox.showwarning("Validación", "Debes ingresar al menos ID y Título.")
            return False, None

        # convertir anio, cantidad, precio
        try:
            anio = int(datos["anio"]) if datos["anio"] else 0
        except ValueError:
            messagebox.showwarning("Validación", "Año debe ser un entero.")
            return False, None
        try:
            cantidad = int(datos["cantidad"]) if datos["cantidad"] else 0
        except ValueError:
            messagebox.showwarning("Validación", "Cantidad debe ser un entero.")
            return False, None
        try:
            precio = float(datos["precio"]) if datos["precio"] else 0.0
        except ValueError:
            messagebox.showwarning("Validación", "Precio debe ser un número (ej. 12.50).")
            return False, None

        libro = Libro(
            id=datos["id"],
            isbn=datos["isbn"],
            titulo=datos["titulo"],
            autor=datos["autor"],
            editorial=datos["editorial"],
            anio=anio,
            categoria=datos["categoria"],
            cantidad=cantidad,
            precio=precio,
            descripcion=datos["descripcion"]
        )
        return True, libro

    # ---------- Botones: agregar / editar / eliminar / guardar ----------
    def agregar_libro(self):
        ok, libro = self._leer_formulario()
        if not ok:
            return
        # agregar y guardar inmediatamente
        self.gestor.agregar_libro(libro)
        self.libros = self.gestor.cargar_todos()
        self.cargar_tabla()
        self.estado_var.set(f"Libro {libro.id} agregado.")
        self.limpiar_campos()

    def editar_libro(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un libro para editar.")
            return
        ok, libro = self._leer_formulario()
        if not ok:
            return
        id_actual = self.tabla.item(sel[0], "values")[0]
        success = self.gestor.actualizar_libro(id_actual, libro)
        if success:
            self.libros = self.gestor.cargar_todos()
            self.cargar_tabla()
            self.estado_var.set(f"Libro {id_actual} modificado.")
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "No se pudo modificar el libro (ID no encontrado).")

    def eliminar_libro(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un libro para eliminar.")
            return
        id_actual = self.tabla.item(sel[0], "values")[0]
        resp = messagebox.askyesno("Confirmar", f"¿Eliminar el libro con ID {id_actual}?")
        if not resp:
            return
        success = self.gestor.eliminar_libro(id_actual)
        if success:
            self.libros = self.gestor.cargar_todos()
            self.cargar_tabla()
            self.estado_var.set(f"Libro {id_actual} eliminado.")
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "No se encontró el libro a eliminar.")

    def guardar_cambios(self):
        """Guarda toda la tabla en el CSV (sobrescribe)."""
        # construir lista de libros desde la tabla (por si se hicieron cambios directos)
        nueva_lista = []
        for item in self.tabla.get_children():
            vals = self.tabla.item(item, "values")
            # vals es lista de strings en el mismo orden de ENCABEZADOS
            d = {k: vals[i] for i, k in enumerate(ENCABEZADOS)}
            nueva_lista.append(Libro.desde_dict(d))
        # guardar
        self.gestor.guardar_todos(nueva_lista)
        self.libros = self.gestor.cargar_todos()
        self.cargar_tabla()
        self.estado_var.set(f"Cambios guardados ({datetime.now().strftime('%H:%M:%S')}).")

    # ---------- Import / Export ----------
    def importar_csv(self):
        ruta = filedialog.askopenfilename(title="Importar CSV", filetypes=[("Archivos CSV", "*.csv"), ("Todos", "*.*")])
        if not ruta:
            return
        try:
            with open(ruta, newline="", encoding="utf-8") as f:
                lector = csv.DictReader(f)
                importados = []
                for fila in lector:
                    # normalizar claves
                    row = {k: fila.get(k, "") for k in ENCABEZADOS}
                    importados.append(Libro.desde_dict(row))
            # merge por id: preferir importados
            existentes = {l.id: l for l in self.gestor.cargar_todos()}
            for l in importados:
                existentes[l.id] = l
            combinados = list(existentes.values())
            self.gestor.guardar_todos(combinados)
            self.libros = self.gestor.cargar_todos()
            self.cargar_tabla()
            messagebox.showinfo("Importar", f"Importados {len(importados)} registros (merge realizado).")
            self.estado_var.set(f"Importados {len(importados)} registros desde {os.path.basename(ruta)}.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo importar CSV: {e}")

    def exportar_csv(self):
        ruta = filedialog.asksaveasfilename(title="Exportar CSV", defaultextension=".csv",
                                            filetypes=[("Archivos CSV", "*.csv"), ("Todos", "*.*")])
        if not ruta:
            return
        try:
            libros = self.gestor.cargar_todos()
            with open(ruta, "w", newline="", encoding="utf-8") as f:
                escritor = csv.writer(f)
                escritor.writerow(ENCABEZADOS)
                for l in libros:
                    escritor.writerow(l.a_lista())
            messagebox.showinfo("Exportar", f"Exportado {len(libros)} registros a {ruta}")
            self.estado_var.set(f"Exportado {len(libros)} registros a {os.path.basename(ruta)}.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar CSV: {e}")

    def limpiar_campos(self):
        for ent in self.entradas.values():
            ent.delete(0, tk.END)
        self.estado_var.set("Campos limpiados.")

    # ---------- Ordenamiento ----------
    def _ordenar_por(self, col, descendente):
        # obtener pares (valor, id_item)
        datos = [(self.tabla.set(k, col), k) for k in self.tabla.get_children('')]
        # intentar orden numérico
        try:
            datos.sort(key=lambda t: float(t[0]) if t[0] != "" else 0.0, reverse=descendente)
        except ValueError:
            datos.sort(key=lambda t: t[0].lower(), reverse=descendente)
        for index, (val, k) in enumerate(datos):
            self.tabla.move(k, '', index)
        # invertir próxima vez
        self.tabla.heading(col, command=lambda c=col: self._ordenar_por(c, not descendente))


# ---------- Ejecutar aplicación ----------
def main():
    root = tk.Tk()
    app = InterfazPrincipal(root)
    root.mainloop()


if __name__ == "__main__":
    main()
