import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "outputs" / "classificacoes.db"


def create_database():
    DB_PATH.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classificacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_arquivo TEXT,
            classe_prevista TEXT,
            confianca REAL,
            data_hora TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_classification(nome_arquivo, classe_prevista, confianca):
    create_database()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO classificacoes (
            nome_arquivo,
            classe_prevista,
            confianca,
            data_hora
        )
        VALUES (?, ?, ?, ?)
    """, (
        nome_arquivo,
        classe_prevista,
        float(confianca),
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    ))

    connection.commit()
    connection.close()


def get_classifications():
    create_database()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            id,
            nome_arquivo,
            classe_prevista,
            confianca,
            data_hora
        FROM classificacoes
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    return rows