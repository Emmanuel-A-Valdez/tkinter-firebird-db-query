from tkinter import *
from tkinter import messagebox
from db_config import *

def fetch_item():
    if (
        code_text.get() == ""
        or warehouse_text.get() == ""
    ):
        messagebox.showerror("Campos requeridos", "Por favor llene todos los campos.")
        return
    code = code_text.get()
    warehouse = warehouse_text.get()

    # Execute the SELECT statement:
    cur.execute(
        f"select a.articulo_id, a.nombre, ex.existencia, ex.valor_unitario, ex.valor_total from articulos a join exival_art({code},{warehouse},current_date,'S') ex on a.articulo_id = ex.articulo_id;"
    )

    # Retrieve columns as a sequence and print that sequence:
    item_details = cur.fetchall()

    item_dict = {}

    item_dict["Codigo:"] = item_details[0][0]
    item_dict["Nombre:"] = item_details[0][1].replace(" ", "_")
    item_dict["Existencia:"] = str(item_details[0][2])
    item_dict["Precio_unitario:"] = f"{item_details[0][3]:.2f}"
    item_dict["Total:"] = f"{item_details[0][4]:.2f}"

    
    item_list.delete(0, END)
    item_list.insert(
        END,
        (item_details,),
    )
    clear_text()
    item_list.delete(0, END)
    for row in item_dict.items():
        item_list.insert(END, row)


def clear_text():
    code_entry.delete(0, END)
    warehouse_entry.delete(0, END)


# Create window object
app = Tk()
app.title("Existencias de Inventario")
app.geometry("700x350")


# Code
code_text = StringVar()
code_label = Label(app, text="Codigo", font=("bold", 14), pady=20, padx=10)
code_label.grid(row=0, column=0, sticky=W)
code_entry = Entry(app, textvariable=code_text)
code_entry.grid(row=0, column=1)

# Warehouse
warehouse_text = StringVar()
warehouse_label = Label(app, text="Almacen", font=("bold", 14), padx=10)
warehouse_label.grid(row=0, column=2)
warehouse_entry = Entry(app, textvariable=warehouse_text)
warehouse_entry.grid(row=0, column=3)

# Item List (Listbox)
item_list = Listbox(app, height=10, width=70, border=0)
item_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

# Create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=3)

# Set scroll to listbox
item_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=item_list.yview)

# Buttons
submit_btn = Button(app, text="Mandar Peticion", width=12, command=fetch_item)
submit_btn.grid(row=2, column=0)

# Start program
app.mainloop()