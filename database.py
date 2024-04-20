import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                barcode TEXT PRIMARY KEY,
                name TEXT,
                price REAL,
                quantity INTEGER
            )
        ''')
        self.conn.commit()

    def add_product(self, barcode, name, price, quantity):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM products WHERE barcode = ?', (barcode,))
            existing_product = cursor.fetchone()
            if existing_product:
                return "¡El producto ya existe en la base de datos!"
            else:
                cursor.execute('INSERT INTO products (barcode, name, price, quantity) VALUES (?, ?, ?, ?)', (barcode, name, price, quantity))
                self.conn.commit()
                return "Producto agregado correctamente."
        except Exception as e:
            return str(e)

    def find_product(self, barcode):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM products WHERE barcode = ?', (barcode,))
        return cursor.fetchone()

    def close_connection(self):
        self.conn.close()
