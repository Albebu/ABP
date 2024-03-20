import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import re
from datetime import datetime

def encrypt_password(password):
    password_bytes = password.encode('utf-8')
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(password_bytes)
    encrypted_password = hash_algorithm.hexdigest()
    return encrypted_password

def register_user():
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    zip_code = zip_code_entry.get()
    birth_date = birth_date_entry.get()

    if len(password) < 5:
        messagebox.showerror("Error", "La contraseña debe tener al menos 5 caracteres.")
        return

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror("Error", "El correo electrónico ingresado no es válido.")
        return

    if not re.match(r"^\d{5}$", zip_code):
        messagebox.showerror("Error", "El código postal debe tener 5 dígitos.")
        return

    try:
        # Convertir la fecha al formato europeo DD-MM-YYYY
        birth_date = datetime.strptime(birth_date, "%d-%m-%Y").strftime("%Y-%m-%d")

        conn = sqlite3.connect('database/DB/project_DB')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "El usuario ya existe.")
        else:
            cursor.execute("INSERT INTO users (username, email, pass, zip_code, birth_date) VALUES (?, ?, ?, ?, ?)",
                           (username, email, encrypt_password(password), zip_code, birth_date))
            conn.commit()
            conn.close()
            messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente.")
            clear_fields()

    except ValueError:
        messagebox.showerror("Error", "Formato de fecha incorrecto. Utilice DD-MM-YYYY.")

def clear_fields():
    username_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    zip_code_entry.delete(0, tk.END)
    birth_date_entry.delete(0, tk.END)

def login_user():
    # Obtener los datos del formulario de inicio de sesión
    username = login_username_entry.get()
    password = login_password_entry.get()

    # Verificar las condiciones
    if len(password) < 5:
        messagebox.showerror("Error", "La contraseña debe tener al menos 5 caracteres.")
        return

    # Conectar a la base de datos
    conn = sqlite3.connect('database/DB/project_DB')
    cursor = conn.cursor()

    # Verificar si el usuario y la contraseña son correctos
    cursor.execute("SELECT username FROM users WHERE username = ? AND pass = ?", (username, encrypt_password(password)))
    existing_user = cursor.fetchone()

    if existing_user:
        messagebox.showinfo("Inicio de sesión exitoso", "¡Bienvenido, {}!".format(username))
        # Guardar el nombre de usuario en una variable global
        global logged_in_user
        logged_in_user = username
        root.destroy()
    else:
        messagebox.showerror("Error de inicio de sesión", "Nombre de usuario o contraseña incorrectos.")

    conn.close()

root = tk.Tk()
root.title("Formulario de Registro e Inicio de Sesión")

register_frame = tk.Frame(root)
register_frame.pack(padx=10, pady=10)

username_label = tk.Label(register_frame, text="Nombre de usuario:")
username_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
username_entry = tk.Entry(register_frame)
username_entry.grid(row=0, column=1, padx=5, pady=5)

email_label = tk.Label(register_frame, text="Correo electrónico:")
email_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
email_entry = tk.Entry(register_frame)
email_entry.grid(row=1, column=1, padx=5, pady=5)

password_label = tk.Label(register_frame, text="Contraseña:")
password_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
password_entry = tk.Entry(register_frame, show="*")
password_entry.grid(row=2, column=1, padx=5, pady=5)

zip_code_label = tk.Label(register_frame, text="Código postal:")
zip_code_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
zip_code_entry = tk.Entry(register_frame)
zip_code_entry.grid(row=3, column=1, padx=5, pady=5)

birth_date_label = tk.Label(register_frame, text="Fecha de Nacimiento (DD-MM-YYYY):")
birth_date_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
birth_date_entry = tk.Entry(register_frame)
birth_date_entry.grid(row=4, column=1, padx=5, pady=5)

register_button = tk.Button(register_frame, text="Registrar", command=register_user)
register_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

	# Elementos del formulario de inicio de sesión
login_frame = tk.Frame(root)
login_frame.pack(padx=10, pady=10)

login_username_label = tk.Label(login_frame, text="Nombre de usuario:")
login_username_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
login_username_entry = tk.Entry(login_frame)
login_username_entry.grid(row=0, column=1, padx=5, pady=5)

login_password_label = tk.Label(login_frame, text="Contraseña:")
login_password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
login_password_entry = tk.Entry(login_frame, show="*")
login_password_entry.grid(row=1, column=1, padx=5, pady=5)

login_button = tk.Button(login_frame, text="Iniciar Sesión", command=login_user)
login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Variable global para almacenar el nombre de usuario registrado
logged_in_user = ""

root.mainloop()
