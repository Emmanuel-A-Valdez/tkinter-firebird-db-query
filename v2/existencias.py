from tkinter import *
from tkinter import messagebox
from db_config import *


height = 700
width = 700

db_options = [
    "Web",
    "El Siglo",
]


def set_db(*args):
    from firebird.driver import connect

    # Set branch/database
    con = connect(f"{default_db.get()}")

    global cur
    cur = con.cursor()


def fetch_item(code, warehouse):
    if code_text.get() == "" or warehouse_text.get() == "":
        messagebox.showerror("Campos requeridos", "Por favor llene todos los campos.")
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
        clear_text()
        return

    clear_text()
    item_list.delete(0, END)
    for row in item_dict.items():
        item_list.insert(END, row)


def clear_text():
    code_entry.delete(0, END)
    warehouse_entry.delete(0, END)


# Create window object
root = Tk()
root.title("Existencias de Inventario")
root.resizable(False, False)
canvas = Canvas(root, height=height, width=width, bg="#00a2ed")
canvas.pack()

# Dropdown frame
dropdown_frame = Frame(root, bg="#cccccc", bd=2)
dropdown_frame.place(relx=0.5, rely=0.05, relwidth=0.85, relheight=0.05, anchor="n")

# Dropdown
dropdown_label = Label(dropdown_frame, text="Sucursales", font=("bold", 10))
dropdown_label.place(relwidth=0.15, relheight=1)
default_db = StringVar()
default_db.set(db_options[0])
dropdown = OptionMenu(dropdown_frame, default_db, *db_options, command=set_db)
dropdown.place(relx=0.15, relwidth=0.85, relheight=1)


# Input frame
input_frame = Frame(root, bg="#cccccc", bd=2)
input_frame.place(relx=0.5, rely=0.1, relwidth=0.85, relheight=0.05, anchor="n")

# Code
code_text = StringVar()
code_label = Label(input_frame, text="Codigo", font=("bold", 10))
code_label.place(relwidth=0.15, relheight=1)
code_entry = Entry(input_frame, textvariable=code_text)
code_entry.place(relx=0.15, relwidth=0.35, relheight=1)

# # Warehouse
warehouse_text = StringVar()
warehouse_label = Label(input_frame, text="Almacen", font=("bold", 10))
warehouse_label.place(relx=0.51, relwidth=0.15, relheight=1)
warehouse_entry = Entry(input_frame, textvariable=warehouse_text)
warehouse_entry.place(relx=0.65, relwidth=0.35, relheight=1)

# Output
item_list = Listbox(root, bg="#cccccc")
item_list.place(relx=0.5, rely=0.25, relwidth=0.85, relheight=0.70, anchor="n")

# Buttons
submit_btn = Button(
    root,
    text="Mandar Peticion",
    command=lambda: fetch_item(code_text.get(), warehouse_text.get()),
)
submit_btn.place(relx=0.5, rely=0.16, relwidth=0.85, relheight=0.05, anchor="n")


# Create scrollbar
scrollbar = Scrollbar(item_list)
scrollbar.place(relx=0.98, relwidth=0.02, relheight=1)

# Set scroll to listbox
item_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=item_list.yview)

# Start program
root.mainloop()
