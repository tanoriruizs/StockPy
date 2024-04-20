import tkinter as tk
from tkinter import ttk, messagebox
import database
from ws.ws_inventory import InventoryWindow

class ProductScannerApp:
    def __init__(self, root, db_manager):
        self.root = root
        self.root.title("Control De Productos")
        self.db_manager = db_manager
        self.barcode_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 12))
        style.configure('TEntry', font=('Arial', 12))

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(main_frame, text="Código de Barras:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(main_frame, textvariable=self.barcode_var).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        ttk.Label(main_frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(main_frame, textvariable=self.name_var).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        ttk.Label(main_frame, text="Precio ($):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(main_frame, textvariable=self.price_var).grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        ttk.Label(main_frame, text="Cantidad:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(main_frame, textvariable=self.quantity_var).grid(row=3, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        ttk.Button(main_frame, text="Agregar Producto", command=self.add_product).grid(row=4, columnspan=2, pady=10)
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=5, columnspan=2, sticky="ew")
        ttk.Label(main_frame, text="Escanear Código de Barras:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.scan_entry = ttk.Entry(main_frame)
        self.scan_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        ttk.Button(main_frame, text="Buscar Producto", command=self.find_product).grid(row=7, columnspan=2, pady=10)

        ttk.Button(main_frame, text="Inventario", command=self.show_inventory).grid(row=8, columnspan=2, pady=10)

    def add_product(self):
        barcode = self.barcode_var.get()
        name = self.name_var.get()
        price = self.price_var.get()
        quantity = self.quantity_var.get()
        if barcode and name and price and quantity:
            try:
                price = float(price)
                quantity = int(quantity)
                result = self.db_manager.add_product(barcode, name, price, quantity)
                messagebox.showinfo("Resultado", result)
                self.barcode_var.set('')
                self.name_var.set('')
                self.price_var.set('')
                self.quantity_var.set('')
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Por favor complete todos los campos.")

    def find_product(self):
        barcode = self.scan_entry.get()
        if barcode:
            product = self.db_manager.find_product(barcode)
            if product:
                messagebox.showinfo("Producto Encontrado", f"Nombre: {product[0]}, Precio: ${product[1]}, Cantidad: {product[2]}")
            else:
                messagebox.showinfo("Producto no Encontrado", "El producto no existe en la base de datos.")
        else:
            messagebox.showerror("Error", "Por favor escanee un código de barras.")

    def show_inventory(self):
        inventory_window = InventoryWindow(self.db_manager)
        inventory_window.show()

if __name__ == "__main__":
    db_manager = database.DatabaseManager('db/productos.db')
    root = tk.Tk()
    app = ProductScannerApp(root, db_manager)
    root.mainloop()
