from tkinter import *
from tkinter import messagebox
from db_config import *


class Application(Frame):
    HEIGHT = 600
    WIDTH = 1100

    DB_OPTIONS = [
        "Web",
        "El Siglo",
    ]

    SEARCH = [
        "Articulo",
        "Lista",
        "Nombre",
    ]

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title("Existencias de Inventario")
        # Resize
        master.resizable(False, False)
        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Canvas
        self.canvas = Canvas(
            self.master, height=self.HEIGHT, width=self.WIDTH, bg="#ffffff"
        )
        self.canvas.pack()

        self.query_frame = Frame(
            self.master,
            bd=2,
        )
        self.query_frame.place(relwidth=0.5, relheight=1)

        self.dialog_frame = Frame(
            self.master,
            bg="#eeeeee",
            bd=4,
        )
        self.dialog_frame.place(relx=0.5, relwidth=0.5, relheight=1)

        # Dropdown frame
        self.dropdown_frame = Frame(self.query_frame, bg="#cccccc", bd=2)
        self.dropdown_frame.place(
            relx=0.5, rely=0.03, relwidth=0.95, relheight=0.1, anchor="n"
        )

        # Branch dropdown
        self.branch_dropdown_label = Label(
            self.dropdown_frame, text="Sucursales", font=("bold", 10)
        )
        self.branch_dropdown_label.place(relwidth=0.27, relheight=0.5)
        self.default_db = StringVar()
        self.default_db.set(self.DB_OPTIONS[0])
        self.branch_dropdown = OptionMenu(
            self.dropdown_frame, self.default_db, *self.DB_OPTIONS, command=self.set_db
        )
        self.branch_dropdown.place(relx=0.27, relwidth=0.73, relheight=0.5)

        # Search dropdown
        self.search_dropdown_label = Label(
            self.dropdown_frame, text="Buscar Por", font=("bold", 10)
        )
        self.search_dropdown_label.place(rely=0.5, relwidth=0.27, relheight=0.5)
        self.default_search = StringVar()
        self.default_search.set(self.SEARCH[2])
        self.search_dropdown = OptionMenu(
            self.dropdown_frame,
            self.default_search,
            *self.SEARCH,
            command=self.set_search,
        )
        self.search_dropdown.place(relx=0.27, rely=0.5, relwidth=0.73, relheight=0.5)

        # Input frame
        self.input_frame = Frame(self.query_frame, bg="#cccccc", bd=2)
        self.input_frame.place(
            relx=0.5, rely=0.145, relwidth=0.95, relheight=0.1, anchor="n"
        )

        # Name
        self.name_text = StringVar()
        self.name_label = Label(self.input_frame, text="Nombre", font=("bold", 10))
        self.name_label.place(relwidth=0.15, relheight=0.5)
        self.name_entry = Entry(self.input_frame, textvariable=self.name_text)
        self.name_entry.place(relx=0.15, relwidth=0.35, relheight=0.5)

        # Warehouse
        self.warehouse_text = StringVar()
        self.warehouse_label = Label(
            self.input_frame, text="Almacen", font=("bold", 10)
        )
        self.warehouse_label.place(relx=0.51, relwidth=0.15, relheight=0.5)
        self.warehouse_entry = Entry(self.input_frame, textvariable=self.warehouse_text)
        self.warehouse_entry.place(relx=0.65, relwidth=0.35, relheight=0.5)

        # Name search button
        self.name_submit_btn = Button(
            self.input_frame,
            text="Mandar Peticion",
            command=lambda: self.fetch_items_by_name(
                self.name_text.get(),
                self.warehouse_text.get(),
            ),
        )
        self.name_submit_btn.place(
            relx=0.5, rely=0.55, relwidth=1, relheight=0.48, anchor="n"
        )

        # Output
        self.item_list = Listbox(self.dialog_frame, bg="#cccccc")
        self.item_list.place(relwidth=1, relheight=1)

        # Create scrollbar
        self.scrollbar = Scrollbar(self.item_list)
        self.scrollbar.place(relx=0.98, relwidth=0.02, relheight=1)

        # Set scroll to listbox
        self.item_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.item_list.yview)

    def set_db(self, *args):
        from firebird.driver import connect

        # Set branch/database
        con = connect(f"{self.default_db.get()}")

        global cur
        cur = con.cursor()

    def set_search(self, *args):
        if self.default_search.get() == "Lista":
            self.search_by_list()
        elif self.default_search.get() == "Articulo":
            self.search_by_code()
        else:
            self.search_by_name()

    def search_by_list(self):
        # Warehouse
        self.warehouse_text = StringVar()
        self.warehouse_label = Label(
            self.input_frame, text="Almacen", font=("bold", 10)
        )
        self.warehouse_label.place(relwidth=0.15, relheight=0.5)
        self.warehouse_entry = Entry(self.input_frame, textvariable=self.warehouse_text)
        self.warehouse_entry.place(relx=0.15, relwidth=0.35, relheight=0.5)

        # No Inventory
        self.inventory_text = StringVar()
        self.inventory_label = Label(
            self.input_frame, text="Inventario", font=("bold", 10)
        )
        self.inventory_label.place(relx=0.5, relwidth=0.15, relheight=0.5)
        self.inventory_entry = Entry(self.input_frame, textvariable=self.inventory_text)
        self.inventory_entry.place(relx=0.65, relwidth=0.35, relheight=0.5)

        # Button
        self.submit_btn = Button(
            self.input_frame,
            text="Mandar Peticion",
            command=lambda: self.fetch_list(self.warehouse_text.get()),
        )
        self.submit_btn.place(
            relx=0.5, rely=0.55, relwidth=1, relheight=0.48, anchor="n"
        )

    def search_by_code(self):
        # Code
        self.code_text = StringVar()
        self.code_label = Label(self.input_frame, text="Codigo", font=("bold", 10))
        self.code_label.place(relwidth=0.15, relheight=0.5)
        self.code_entry = Entry(self.input_frame, textvariable=self.code_text)
        self.code_entry.place(relx=0.15, relwidth=0.35, relheight=0.5)

        # Warehouse
        self.warehouse_text = StringVar()
        self.warehouse_label = Label(
            self.input_frame, text="Almacen", font=("bold", 10)
        )
        self.warehouse_label.place(relx=0.51, relwidth=0.15, relheight=0.5)
        self.warehouse_entry = Entry(self.input_frame, textvariable=self.warehouse_text)
        self.warehouse_entry.place(relx=0.65, relwidth=0.35, relheight=0.5)

        # Button
        self.submit_btn = Button(
            self.input_frame,
            text="Mandar Peticion",
            command=lambda: self.fetch_item_by_code(
                self.code_text.get(), self.warehouse_text.get()
            ),
        )
        self.submit_btn.place(
            relx=0.5, rely=0.55, relwidth=1, relheight=0.48, anchor="n"
        )

    def search_by_name(self, *args):
        # Name
        self.name_text = StringVar()
        self.name_label = Label(self.input_frame, text="Nombre", font=("bold", 10))
        self.name_label.place(relwidth=0.15, relheight=0.5)
        self.name_entry = Entry(self.input_frame, textvariable=self.name_text)
        self.name_entry.place(relx=0.15, relwidth=0.35, relheight=0.5)

        # Warehouse
        self.warehouse_text = StringVar()
        self.warehouse_label = Label(
            self.input_frame, text="Almacen", font=("bold", 10)
        )
        self.warehouse_label.place(relx=0.51, relwidth=0.15, relheight=0.5)
        self.warehouse_entry = Entry(self.input_frame, textvariable=self.warehouse_text)
        self.warehouse_entry.place(relx=0.65, relwidth=0.35, relheight=0.5)

        # Name search button
        self.name_submit_btn = Button(
            self.input_frame,
            text="Mandar Peticion",
            command=lambda: self.fetch_items_by_name(
                self.name_text.get(),
                self.warehouse_text.get(),
            ),
        )
        self.name_submit_btn.place(
            relx=0.5, rely=0.55, relwidth=1, relheight=0.48, anchor="n"
        )

    def fetch_list(self, warehouse):
        if self.warehouse_text.get() == "":
            messagebox.showerror(
                "Campos requeridos", "Por favor llene todos los campos."
            )
            return

        # Execute the SELECT statement:
        if self.inventory_text.get() == "0":
            cur.execute(
                f"""SELECT DISTINCT a.articulo_id, a.nombre, d.clave_articulo, ex.existencia, ex.valor_unitario, ex.valor_total 
            FROM articulos a
            JOIN doctos_in_det d ON a.articulo_id = d.articulo_id
            LEFT OUTER JOIN exival_art(a.articulo_id,{warehouse},current_date,'S') ex ON a.articulo_id = ex.articulo_id
            WHERE d.clave_articulo IS NOT NULL AND ex.existencia <= 0
            ORDER BY a.nombre ASC;"""
            )
        else:
            cur.execute(
                f"""SELECT DISTINCT a.articulo_id, a.nombre, d.clave_articulo, ex.existencia, ex.valor_unitario, ex.valor_total 
                FROM articulos a
                JOIN doctos_in_det d ON a.articulo_id = d.articulo_id
                LEFT OUTER JOIN exival_art(a.articulo_id,{warehouse},current_date,'S') ex ON a.articulo_id = ex.articulo_id
                WHERE d.clave_articulo IS NOT NULL
                ORDER BY a.nombre ASC;"""
            )

        # Retrieve columns as a sequence and print that sequence:
        item_details = cur.fetchall()
        self.clear_text()
        self.item_list.delete(0, END)
        for i in item_details:
            self.item_list.insert(
                END,
                f"""Codigo: {i[2]}""",
            )
            self.item_list.insert(
                END,
                f"""Nombre: {i[1].replace(" ", "_")}""",
            )
            self.item_list.insert(
                END,
                f"""Existencia: {str(i[3])}""",
            )
            self.item_list.insert(
                END,
                f"""Precio Unitario: {i[4]:.2f}""",
            )
            self.item_list.insert(
                END,
                f"""Total: {i[5]:.2f}""",
            )
            self.item_list.insert(
                END,
                "-----------------------------------------------------------------------------------------------------",
            )

    def fetch_item_by_code(self, code, warehouse):
        if self.code_text.get() == "" or self.warehouse_text.get() == "":
            messagebox.showerror(
                "Campos requeridos", "Por favor llene todos los campos."
            )
            return

        # Execute the SELECT statement:
        cur.execute(
            f"""SELECT DISTINCT d.articulo_id 
            FROM doctos_in_det d 
            WHERE lower(d.clave_articulo) = '{code.lower()}';"""
        )
        item_code = cur.fetchall()[0][0]
        cur.execute(
            f"""SELECT a.articulo_id, a.nombre, d.clave_articulo, ex.existencia, ex.valor_unitario, ex.valor_total 
            FROM articulos a JOIN doctos_in_det d ON a.articulo_id = d.articulo_id 
            JOIN exival_art({item_code},{warehouse},current_date,'S') ex ON a.articulo_id = ex.articulo_id;"""
        )

        # Retrieve columns as a sequence and print that sequence:
        item_details = cur.fetchall()

        self.clear_text()
        self.item_list.delete(0, END)
        try:
            self.item_list.insert(
                END,
                f"""Codigo: {item_details[0][2]}""",
            )
            self.item_list.insert(
                END,
                f"""Nombre: {item_details[0][1].replace(" ", "_")}""",
            )
            self.item_list.insert(
                END,
                f"""Existencia: {str(item_details[0][3])}""",
            )
            self.item_list.insert(
                END,
                f"""Precio Unitario: {item_details[0][4]:.2f}""",
            )
            self.item_list.insert(
                END,
                f"""Total: {item_details[0][5]:.2f}""",
            )
        except IndexError:
            messagebox.showerror("Codigo no existe", "Por favor intente de nuevo.")
            self.clear_text()
            return

    def fetch_items_by_name(self, param, warehouse):
        if self.name_text.get() == "" or self.warehouse_text.get() == "":
            messagebox.showerror(
                "Campos requeridos", "Por favor llene todos los campos."
            )
            return

        # Execute the SELECT statement:
        cur.execute(
            f"""SELECT DISTINCT a.nombre, d.clave_articulo, ex.existencia, ex.valor_unitario, ex.valor_total
            FROM articulos a 
            JOIN doctos_in_det d ON a.articulo_id = d.articulo_id 
            LEFT OUTER JOIN exival_art(a.articulo_id,{warehouse},current_date,'S') ex ON a.articulo_id = ex.articulo_id
            WHERE lower(a.nombre) LIKE '%{param.lower()}%' AND d.clave_articulo IS NOT NULL 
            ORDER BY a.nombre ASC;
            """
        )

        # Retrieve columns as a sequence and print that sequence:
        item_details = cur.fetchall()
        self.name_entry.delete(0, END)
        self.warehouse_entry.delete(0, END)
        self.item_list.delete(0, END)
        for i in item_details:
            self.item_list.insert(
                END,
                f"""Codigo: {i[1]}""",
            )
            self.item_list.insert(
                END,
                f"""Nombre: {i[0].replace(" ", "_")}""",
            )
            self.item_list.insert(
                END,
                f"""Existencia: {str(i[2])}""",
            )
            self.item_list.insert(
                END,
                f"""Precio Unitario: {i[3]:.2f}""",
            )
            self.item_list.insert(
                END,
                f"""Total: {i[4]:.2f}""",
            )
            self.item_list.insert(
                END,
                "-----------------------------------------------------------------------------------------------------",
            )

    def clear_text(self):
        try:
            self.code_entry.delete(0, END)
            self.warehouse_entry.delete(0, END)
        except:
            self.inventory_entry.delete(0, END)
            self.warehouse_entry.delete(0, END)


root = Tk()
app = Application(master=root)
app.mainloop()
