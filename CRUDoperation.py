from tkinter import *
from tkinter import ttk, messagebox
from pymongo import MongoClient
from bson.objectid import ObjectId

#MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["TechProductDB"]
collection = db["customers"]

#Functions
def show_data():
    tree.delete(*tree.get_children())
    for data in collection.find():
        tree.insert("", END, values=(str(data["_id"]), data["product"], data["name"], data["email"], data["phone"], data["age"], data["gender"]))

def add_data():
    product = entry_product.get()
    name = entry_name.get()
    email = entry_email.get()
    phone = entry_phone.get()
    age = entry_age.get()
    gender = entry_gender.get()

    if product and name and email and phone and age and gender:
        collection.insert_one({"product": product, "name": name, "email": email, "phone": phone, "age": age, "gender": gender})
        show_data()
    else:
        messagebox.showerror("Error", "Fill all fields")

def delete_data():
    selected = tree.selection()
    if selected:
        _id = tree.item(selected[0])["values"][0]
        collection.delete_one({"_id": ObjectId(_id)})
        show_data()

def update_data():
    selected = tree.selection()
    if selected:
        _id = tree.item(selected[0])["values"][0]
        collection.update_one({"_id": ObjectId(_id)}, {"$set": {
            "product": entry_product.get(),
            "name": entry_name.get(),
            "email": entry_email.get(),
            "phone": entry_phone.get(),
            "age": entry_age.get(),
            "gender": entry_gender.get()
        }})
        show_data()

#GUI
root = Tk()
root.title("MongoDB CRUD - Tech Products Database")
root.geometry("900x600")   # normal fixed size window

# Labels and Entries
Label(root, text="Product").grid(row=0, column=0)
entry_product = Entry(root); entry_product.grid(row=0, column=1)

Label(root, text="Name").grid(row=1, column=0)
entry_name = Entry(root); entry_name.grid(row=1, column=1)

Label(root, text="Email").grid(row=2, column=0)
entry_email = Entry(root); entry_email.grid(row=2, column=1)

Label(root, text="Phone").grid(row=3, column=0)
entry_phone = Entry(root); entry_phone.grid(row=3, column=1)

Label(root, text="Age").grid(row=4, column=0)
entry_age = Entry(root); entry_age.grid(row=4, column=1)

Label(root, text="Gender").grid(row=5, column=0)
entry_gender = Entry(root); entry_gender.grid(row=5, column=1)

Button(root, text="Add", command=add_data).grid(row=6, column=0, pady=5)
Button(root, text="Update", command=update_data).grid(row=6, column=1)
Button(root, text="Delete", command=delete_data).grid(row=6, column=2)

columns = ("ID","Product","Name","Email","Phone","Age","Gender")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor="center")

tree.grid(row=7, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")

show_data()
root.mainloop()
