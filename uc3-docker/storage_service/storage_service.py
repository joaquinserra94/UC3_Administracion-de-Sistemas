import os
import time
import sqlite3
from flask import Flask, request, jsonify

DB_FILE = "/app-data/classifications.db"
INPUT_FILE = "/app-data/classified.txt"

app = Flask(__name__)

# ======================================================
# 1. Setup de la base de datos (SQLite)
# ======================================================
def init_db():
    # Crea/Abre la BD
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Creamos la tabla si no existe
    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER,
            primo INTEGER,
            capicua INTEGER,
            feliz INTEGER
        )
    """)
    conn.commit()
    conn.close()

# ======================================================
# 2. Función para insertar un nuevo registro
# ======================================================
def insert_classification(numero, primo, capicua, feliz):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO results (numero, primo, capicua, feliz) VALUES (?, ?, ?, ?)",
              (numero, primo, capicua, feliz))
    conn.commit()
    conn.close()

# ======================================================
# 3. Bucle que lee "classified.txt" y carga en la BD
# ======================================================
def process_classified_file():
    last_position = 0
    while True:
        with open(INPUT_FILE, "r") as f:
            # Mover cursor a la última posición leída
            f.seek(last_position)

            lines = f.readlines()
            # Actualizar la posición
            last_position = f.tell()

        # Procesar líneas nuevas
        for line in lines:
            line = line.strip()
            if line:
                # Esperamos un formato: num,primo,capicua,feliz
                parts = line.split(",")
                if len(parts) == 4:
                    numero = int(parts[0])
                    primo = 1 if parts[1] == "True" else 0
                    capicua = 1 if parts[2] == "True" else 0
                    feliz = 1 if parts[3] == "True" else 0
                    insert_classification(numero, primo, capicua, feliz)

        # Espera un segundo antes de seguir
        time.sleep(1)

# ======================================================
# 4. Definir endpoints del servicio Flask
# ======================================================
@app.route("/capicuas")
def get_capicuas():
    # Ejemplo: /capicuas?max=1000
    max_val = request.args.get("max", None)
    query = "SELECT numero FROM results WHERE capicua=1"
    params = []

    if max_val:
        query += " AND numero < ?"
        params.append(max_val)

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()

    return jsonify([r[0] for r in rows])  # retornamos la lista de números

@app.route("/primos")
def get_primos():
    # Ejemplo: /primos
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT numero FROM results WHERE primo=1")
    rows = c.fetchall()
    conn.close()
    return jsonify([r[0] for r in rows])

@app.route("/felices")
def get_felices():
    # Ejemplo: /felices
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT numero FROM results WHERE feliz=1")
    rows = c.fetchall()
    conn.close()
    return jsonify([r[0] for r in rows])

# ======================================================
# 5. Arranque del servicio
# ======================================================
if __name__ == "__main__":
    # Asegurarse de que la BD esté inicializada
    init_db()

    # Lanzamos un "subproceso" para el bucle de lectura
    # Por simplicidad, lo hacemos de forma "pseudo-concurrente".
    # Una forma sencilla es usar threading.
    import threading
    t = threading.Thread(target=process_classified_file, daemon=True)
    t.start()

    # Iniciamos Flask en host 0.0.0.0 (para que sea accesible desde fuera del contenedor)
    app.run(host="0.0.0.0", port=5000, debug=False)
