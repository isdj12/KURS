import os
import sqlite3
from app import app, db

# Путь к файлу базы данных
db_path = os.path.join(app.instance_path, 'database.db')

# Удаляем существующую базу данных, если она существует
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"База данных {db_path} удалена")

# Создаем новую базу данных с новой схемой
with app.app_context():
    db.create_all()
    print("Создана новая база данных с обновленной схемой")

print("Сброс базы данных завершен успешно") 