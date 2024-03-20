import sqlite3 as sql
from random import randint
import formulario.form


def createDB():
    conn = sql.connect('DB/project_DB')
    conn.commit()
    conn.close()

def createTableUsers():
    conn = sql.connect('DB/project_DB')
    cursor = conn.cursor()
    cursor.execute(
        """-- Table usecrs
CREATE TABLE users (
  id_user INTEGER NOT NULL CONSTRAINT PK_users_id_user PRIMARY KEY AUTOINCREMENT,
  username TEXT CONSTRAINT nn_users_username NOT NULL,
  email TEXT CONSTRAINT nn_users_email NOT NULL,
  pass TEXT CONSTRAINT nn_users_pass NOT NULL,
  register_date DATE DEFAULT CURRENT_DATE,
  zip_code TEXT CONSTRAINT nn_users_zip_code NOT NULL,
  birth_date DATE CONSTRAINT nn_users_birth_date NOT NULL,
  CONSTRAINT uk_users_email UNIQUE (email),
  CONSTRAINT uk_users_username UNIQUE (username)
)
"""
    )
    conn.commit()
    conn.close()

def createTableGames():
    conn = sql.connect("DB/project_DB")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE games (
  id_game INTEGER NOT NULL CONSTRAINT PK_games_id_game PRIMARY KEY AUTOINCREMENT,
  id_user INTEGER,
  score INTEGER,
  lv INTEGER,
  start_time DATETIME,
  end_time DATETIME,
  CONSTRAINT uk_games_id_game UNIQUE (id_game),
  CONSTRAINT fk_games_id_user FOREIGN KEY (id_user) REFERENCES users (id_user)
)"""
    )
    conn.commit()
    conn.close()

def createTableRelationships():
    conn = sql.connect("DB/project_DB")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE relationships
(
  User_id_1 INTEGER NOT NULL,
  User_id_2 INTEGER NOT NULL,
  id_status INTEGER,
  CONSTRAINT PK_relationships PRIMARY KEY (User_id_1,User_id_2),
  CONSTRAINT fk_relationships_user_id_1 FOREIGN KEY (User_id_1) REFERENCES users (id_user),
  CONSTRAINT fk_relationships_user_id_2 FOREIGN KEY (User_id_2) REFERENCES users (id_user),
  CONSTRAINT fk_relationships_id_status FOREIGN KEY (id_status) REFERENCES relationships_statuses (id_status)
)"""
    )
    conn.commit()
    conn.close()

def createTableRelationshipsStatuses():
    conn = sql.connect("DB/project_DB")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE relationships_statuses
(
  id_status INTEGER NOT NULL,
  status TEXT,
  CONSTRAINT PK_relationships_statuses PRIMARY KEY (id_status)
)"""
    )

def createTableEmployees():
    conn = sql.connect("DB/project_DB")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE employees (
  employee_id INTEGER NOT NULL CONSTRAINT PK_employees_employee_id PRIMARY KEY AUTOINCREMENT,
  first_name TEXT CONSTRAINT nn_employees_first_name NOT NULL,
  last_name TEXT CONSTRAINT nn_employees_last_name NOT NULL,
  email TEXT CONSTRAINT nn_employees_email NOT NULL, -- Se corrigió el nombre de la restricción
  phone_number TEXT CONSTRAINT nn_employees_phone_number NOT NULL,
  hire_date DATE CONSTRAINT nn_employees_hire_date NOT NULL,
  salary INTEGER CONSTRAINT nn_employees_salary NOT NULL,
  department_id INTEGER CONSTRAINT nn_employees_department_id NOT NULL, -- Se mantuvo el mismo formato
  job_id INTEGER CONSTRAINT nn_employees_job_id NOT NULL, -- Se mantuvo el mismo formato
  CONSTRAINT uk_employees_email UNIQUE (email),
  CONSTRAINT uk_employees_phone_number UNIQUE (phone_number),
  CONSTRAINT fk_employees_department_id FOREIGN KEY (department_id) REFERENCES departments (department_id),
  CONSTRAINT fk_employees_job_id FOREIGN KEY (job_id) REFERENCES jobs (job_id)
)"""
    )
    conn.commit()
    conn.close()

def createTableDepartments():
    conn = sql.connect("DB/project_DB")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE departments (
  department_id INTEGER NOT NULL CONSTRAINT PK_departments_department_id PRIMARY KEY AUTOINCREMENT,
  department_name TEXT CONSTRAINT nn_departments_department_name NOT NULL,
  CONSTRAINT uk_departments_department_name UNIQUE (department_name)
)"""
    )

    conn.commit()
    conn.close()

def createTableJobs():
    conn = sql.connect("DB/project_DB")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE jobs (
  job_id INTEGER NOT NULL CONSTRAINT PK_jobs_job_id PRIMARY KEY AUTOINCREMENT,
  job_name TEXT CONSTRAINT nn_jobs_job_name NOT NULL
)"""
    )

    conn.commit()
    conn.close()

def insertUsers():
    conn = sql.connect('database/DB/project_DB')
    cursor = conn.cursor()

    # Insertar departamentos
    cursor.execute("INSERT INTO departments VALUES (NULL, 'Maintenance');")
    cursor.execute("INSERT INTO departments VALUES (NULL, 'Programming');")

    # Insertar trabajos
    cursor.execute("INSERT INTO jobs VALUES (NULL, 'Web Developer');")
    cursor.execute("INSERT INTO jobs VALUES (NULL, 'Game Programmer');")
    cursor.execute("INSERT INTO jobs VALUES (NULL, 'Data Developer');")
    cursor.execute("INSERT INTO jobs VALUES (NULL, 'Maintenance Technician');")

    # Inserts para Maintenance Technician
    cursor.executemany("INSERT INTO employees VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?);", [
        ('Joan', 'Garcia', 'joan.garcia@monlau.invaders.com', '612345678', '2000-01-01', 40000, 1, 4),
        ('Maria', 'Martínez', 'maria.martinez@monlau.invaders.com', '612345679', '2001-02-02', 40000, 1, 4)
    ])

    # Inserts para Web Developer
    cursor.executemany("INSERT INTO employees VALUES (NULL,  ?, ?, ?, ?, ?, ?, ?, ?);", [
        ('Jordi', 'Martí', 'jordi.marti@monlau.invaders.com', '612345680', '2002-03-03', 60000, 2, 1),
        ('Laia', 'Pujol', 'laia.pujol@monlau.invaders.com', '612345681', '2003-04-04', 60000, 2, 1),
        ('Pau', 'Gomez', 'pau.gomez@monlau.invaders.com', '612345682', '2004-05-05', 60000, 2, 1),
        ('Núria', 'Sánchez', 'nuria.sanchez@monlau.invaders.com', '612345683', '2005-06-06', 60000, 2, 1),
        ('Oriol', 'Ferrer', 'oriol.ferrer@monlau.invaders.com', '612345684', '2006-07-07', 60000, 2, 1),
        ('Anna', 'López', 'anna.lopez@monlau.invaders.com', '612345685', '2007-08-08', 60000, 2, 1)
    ])

    # Insertar relaciones de estado
    cursor.execute("INSERT INTO relationships_statuses VALUES (NULL, 'friends');")

    conn.commit()
    conn.close()


def introduce_game_level(username, score, level, start_time, end_time):
    conn = sql.connect('database/DB/project_DB')
    cursor = conn.cursor()

    # Obtener el id_user correspondiente al nombre de usuario proporcionado
    cursor.execute("SELECT id_user FROM users WHERE username = ?", (username,))
    user_row = cursor.fetchone()  # Recuperar la primera fila

    if user_row:
        id_user = user_row[0]  # Extraer el id_user de la tupla
        # Insertar el nuevo registro en la tabla games
        cursor.execute("INSERT INTO games (id_user, score, lv, start_time, end_time) VALUES (?, ?, ?, ?, ?);",
                       (id_user, score, level, start_time, end_time))
        conn.commit()
        conn.close()
        print("Datos del juego insertados correctamente.")
    else:
        print("No se encontró el usuario con el nombre proporcionado.")