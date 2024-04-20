import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from openpyxl import Workbook

class InventoryWindow:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.window = tk.Toplevel()
        self.window.title("Inventario")
        self.create_widgets()

    def create_widgets(self):
        inventory_frame = ttk.Frame(self.window)
        inventory_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.tree = ttk.Treeview(inventory_frame, columns=("Barcode", "Name", "Price", "Quantity"), show="headings")
        self.tree.heading("Barcode", text="Código de Barras")
        self.tree.heading("Name", text="Nombre")
        self.tree.heading("Price", text="Precio ($)")
        self.tree.heading("Quantity", text="Cantidad")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.populate_tree()
        button_frame = ttk.Frame(inventory_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Editar Producto", command=self.edit_product).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Eliminar Producto", command=self.delete_product).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Exportar a Excel", command=self.export_to_excel).grid(row=0, column=2, padx=5)


    def populate_tree(self):
        cursor = self.db_manager.conn.cursor()
        cursor.execute('SELECT * FROM products')
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def edit_product(self):
        selected_item = self.tree.selection()
        if selected_item:
            product_data = self.tree.item(selected_item)['values']
            if product_data:
                barcode, name, price, quantity = product_data
                edit_window = tk.Toplevel(self.window)
                edit_window.title("Editar Producto")
                ttk.Label(edit_window, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
                ttk.Entry(edit_window, textvariable=tk.StringVar(value=name)).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
                ttk.Label(edit_window, text="Precio ($):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
                ttk.Entry(edit_window, textvariable=tk.StringVar(value=price)).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
                ttk.Label(edit_window, text="Cantidad:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
                ttk.Entry(edit_window, textvariable=tk.StringVar(value=quantity)).grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
                ttk.Button(edit_window, text="Guardar Cambios", command=lambda: self.save_changes(edit_window, barcode)).grid(row=3, columnspan=2, pady=10)
                self.center_window_on_screen(edit_window)
        else:
            messagebox.showerror("Error", "Por favor seleccione un producto para editar.")

    def save_changes(self, edit_window, barcode):
        name = edit_window.children['!entry'].get()
        price = float(edit_window.children['!entry2'].get())
        quantity = int(edit_window.children['!entry3'].get())
        cursor = self.db_manager.conn.cursor()
        cursor.execute('UPDATE products SET name = ?, price = ?, quantity = ? WHERE barcode = ?', (name, price, quantity, barcode))
        self.db_manager.conn.commit()
        edit_window.destroy()
        self.tree.delete(*self.tree.get_children())
        self.populate_tree()

    def delete_product(self):
        selected_item = self.tree.selection()
        if selected_item:
            confirmation = messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar este producto?")
            if confirmation:
                product_data = self.tree.item(selected_item)['values']
                barcode = product_data[0]
                cursor = self.db_manager.conn.cursor()
                cursor.execute('DELETE FROM products WHERE barcode = ?', (barcode,))
                self.db_manager.conn.commit()
                self.tree.delete(*self.tree.get_children())
                self.populate_tree()
        else:
            messagebox.showerror("Error", "Por favor seleccione un producto para eliminar.")

    def export_to_excel(self):
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if filename:
            wb = Workbook()
            ws = wb.active
            ws.append(["Código de Barras", "Nombre", "Precio ($)", "Cantidad"])

            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                ws.append(values)

            wb.save(filename)
            messagebox.showinfo("Éxito", f"Los datos se han exportado a '{filename}'.")

    def center_window_on_screen(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def show(self):
        self.window.mainloop()
