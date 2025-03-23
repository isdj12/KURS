import sqlite3
import os
from werkzeug.security import generate_password_hash
import datetime

# Подключаемся к базе данных
db_path = "instance/database.db"

if not os.path.exists(db_path):
    print(f"Ошибка: файл базы данных не найден по пути {db_path}")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print(f"Успешное подключение к базе данных {db_path}")
    
    # Генерируем хеш для пароля
    test_login = f"test_user_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    test_password = generate_password_hash("test_password")
    test_email = f"{test_login}@example.com"
    
    # Добавляем тестовый аккаунт
    cursor.execute(
        "INSERT INTO account (login, password, pochta) VALUES (?, ?, ?)",
        (test_login, test_password, test_email)
    )
    
    # Сохраняем изменения
    conn.commit()
    
    # Получаем ID добавленного аккаунта
    new_account_id = cursor.lastrowid
    
    print(f"Тестовый аккаунт успешно добавлен! ID: {new_account_id}")
    print(f"Логин: {test_login}")
    print(f"Email: {test_email}")
    
    # Проверяем, что аккаунт действительно добавился
    cursor.execute("SELECT * FROM account WHERE id = ?", (new_account_id,))
    account = cursor.fetchone()
    
    if account:
        print("Аккаунт успешно найден в базе данных!")
    else:
        print("Ошибка: аккаунт не найден в базе данных после добавления!")
    
    conn.close()
    
except sqlite3.Error as e:
    print(f"Ошибка при работе с базой данных: {e}") 