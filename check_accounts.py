import sqlite3
import os

def print_table_schema(conn, table_name):
    """Выводит схему таблицы"""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    
    print(f"\nСхема таблицы '{table_name}':")
    print("ID | Имя столбца | Тип | Обязательный | По умолчанию | PK")
    print("-" * 70)
    
    for row in cursor.fetchall():
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")

def print_all_accounts(conn):
    """Выводит все аккаунты из таблицы account"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM account")
    
    accounts = cursor.fetchall()
    
    print("\nСписок аккаунтов:")
    print("ID | Логин | Пароль (хеш) | Email")
    print("-" * 70)
    
    for account in accounts:
        print(f"{account[0]} | {account[1]} | {account[2][:20]}... | {account[3]}")
    
    print(f"\nВсего аккаунтов: {len(accounts)}")

# Подключаемся к базе данных
db_path = "instance/database.db"

if not os.path.exists(db_path):
    print(f"Ошибка: файл базы данных не найден по пути {db_path}")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    print(f"Успешное подключение к базе данных {db_path}")
    
    # Выводим схему таблицы account
    print_table_schema(conn, "account")
    
    # Выводим все аккаунты
    print_all_accounts(conn)
    
    conn.close()
    
except sqlite3.Error as e:
    print(f"Ошибка при работе с базой данных: {e}") 