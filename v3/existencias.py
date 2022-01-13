from tkinter import *
from tkinter import messagebox
from db_config import *


class Application(Frame):
    HEIGHT = 700
    WIDTH = 700

    DB_OPTIONS = [
        "Web",
        "El Siglo",
    ]

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title("Existencias de Inventario")
        # Resize
        master.resizable(False, False)
        # Create list or item display
        self.select_display()
        # Widgets
        self.create_widgets()

    def select_display(self):
        # Canvas
        self.canvas = Canvas(self.master, height=700, width=700, bg="#00a2ed")
        self.canvas.pack()

        # List item selection frame
        self.li_frame = Frame(root, bg="#cccccc")
        self.li_frame.place(
            relx=0.5, rely=0.105, relwidth=0.85, relheight=0.05, anchor="n"
        )

        # Display item button
        self.item_btn = Button(
            self.li_frame,
            text="Ver Por Articulo",
            command=self.item_inputs,
        )
        self.item_btn.place(relwidth=0.5, relheight=1)

        # Display list button
        self.list_btn = Button(
            self.li_frame,
            text="Ver Por Lista",
            command=self.list_inputs,
        )
        self.list_btn.place(relx=0.505, relwidth=0.495, relheight=1)

    def create_widgets(self):
        # Dropdown frame
        self.dropdown_frame = Frame(self.master, bg="#cccccc", bd=2)
        self.dropdown_frame.place(
            relx=0.5, rely=0.05, relwidth=0.85, relheight=0.05, anchor="n"
        )

        # Dropdown
        self.dropdown_label = Label(
            self.dropdown_frame, text="Sucursales", font=("bold", 10)
        )
        self.dropdown_label.place(relwidth=0.15, relheight=1)
        self.default_db = StringVar()
        self.default_db.set(self.DB_OPTIONS[0])
        self.dropdown = OptionMenu(
            self.dropdown_frame, self.default_db, *self.DB_OPTIONS, command=self.set_db
        )
        self.dropdown.place(relx=0.15, relwidth=0.85, relheight=1)

        # Output
        self.item_list = Listbox(root, bg="#cccccc")
        self.item_list.place(
            relx=0.5, rely=0.275, relwidth=0.85, relheight=0.68, anchor="n"
        )

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

    def list_inputs(self):
        # Input frame
        self.input_frame = Frame(root, bg="#cccccc", bd=2)
        self.input_frame.place(
            relx=0.5, rely=0.16, relwidth=0.85, relheight=0.05, anchor="n"
        )

        # Warehouse
        self.warehouse_text = StringVar()
        self.warehouse_label = Label(
            self.input_frame, text="Almacen", font=("bold", 10)
        )
        self.warehouse_label.place(relwidth=0.15, relheight=1)
        self.warehouse_entry = Entry(self.input_frame, textvariable=self.warehouse_text)
        self.warehouse_entry.place(relx=0.15, relwidth=0.85, relheight=1)

        # Buttons
        self.submit_btn = Button(
            root,
            text="Mandar Peticion",
            command=lambda: self.fetch_list(self.warehouse_text.get()),
        )
        self.submit_btn.place(
            relx=0.5, rely=0.217, relwidth=0.85, relheight=0.05, anchor="n"
        )

    def item_inputs(self):
        # Input frame
        self.input_frame = Frame(root, bg="#cccccc", bd=2)
        self.input_frame.place(
            relx=0.5, rely=0.16, relwidth=0.85, relheight=0.05, anchor="n"
        )

        # Code
        self.code_text = StringVar()
        self.code_label = Label(self.input_frame, text="Codigo", font=("bold", 10))
        self.code_label.place(relwidth=0.15, relheight=1)
        self.code_entry = Entry(self.input_frame, textvariable=self.code_text)
        self.code_entry.place(relx=0.15, relwidth=0.35, relheight=1)

        # Warehouse
        self.warehouse_text = StringVar()
        self.warehouse_label = Label(
            self.input_frame, text="Almacen", font=("bold", 10)
        )
        self.warehouse_label.place(relx=0.51, relwidth=0.15, relheight=1)
        self.warehouse_entry = Entry(self.input_frame, textvariable=self.warehouse_text)
        self.warehouse_entry.place(relx=0.65, relwidth=0.35, relheight=1)

        # Buttons
        self.submit_btn = Button(
            root,
            text="Mandar Peticion",
            command=lambda: self.fetch_item(
                self.code_text.get(), self.warehouse_text.get()
            ),
        )
        self.submit_btn.place(
            relx=0.5, rely=0.217, relwidth=0.85, relheight=0.05, anchor="n"
        )

    def fetch_list(self, warehouse):
        if self.warehouse_text.get() == "":
            messagebox.showerror(
                "Campos requeridos", "Por favor llene todos los campos."
            )
            return

        # Execute the SELECT statement:
        cur.execute(
            f"select a.articulo_id, a.nombre, ex.existencia, ex.valor_unitario, ex.valor_total from articulos a left outer join exival_art(a.articulo_id,{warehouse},current_date,'S') ex on a.articulo_id = ex.articulo_id;"
        )

        # Retrieve columns as a sequence and print that sequence:
        item_details = cur.fetchall()

        items_list = []
        for i in item_details:
            item = {}

            item["Codigo:"] = i[0]
            item["Nombre:"] = i[1].replace(" ", "_")
            item["Existencia:"] = str(i[2])
            item["Precio_unitario:"] = f"{i[3]:.2f}"
            item["Total:"] = f"{i[4]:.2f}"
            items_list.append(item)

        self.clear_text()
        self.item_list.delete(0, END)

        for item_dict in items_list:
            for k, v in item_dict.items():
                self.item_list.insert(END, (k, v))
            self.item_list.insert(
                END,
                "------------------------------------------------------------------------------",
            )

    def fetch_item(self, code, warehouse):
        if self.code_text.get() == "" or self.warehouse_text.get() == "":
            messagebox.showerror(
                "Campos requeridos", "Por favor llene todos los campos."
            )
            return

        # Execute the SELECT statement:
        cur.execute(
            f"select a.articulo_id, a.nombre, ex.existencia, ex.valor_unitario, ex.valor_total from articulos a join exival_art({code},{warehouse},current_date,'S') ex on a.articulo_id = ex.articulo_id;"
        )

        # Retrieve columns as a sequence and print that sequence:
        item_details = cur.fetchall()

        item_dict = {}

        try:
            item_dict["Codigo:"] = item_details[0][0]
            item_dict["Nombre:"] = item_details[0][1].replace(" ", "_")
            item_dict["Existencia:"] = str(item_details[0][2])
            item_dict["Precio_unitario:"] = f"{item_details[0][3]:.2f}"
            item_dict["Total:"] = f"{item_details[0][4]:.2f}"
        except IndexError:
            messagebox.showerror("Codigo no existe", "Por favor intente de nuevo.")
            self.clear_text()
            return

        self.clear_text()
        self.item_list.delete(0, END)

        for row in item_dict.items():
            self.item_list.insert(END, row)

    def clear_text(self):
        try:
            self.code_entry.delete(0, END)
            self.warehouse_entry.delete(0, END)
        except:
            self.warehouse_entry.delete(0, END)


root = Tk()
app = Application(master=root)
app.mainloop()
