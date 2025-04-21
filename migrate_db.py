from app import app, db
from models import Database
import sqlite3
import os

def migrate_database():
    with app.app_context():
        # Проверяем, существует ли файл базы данных
        db_path = os.path.join('instance', 'site.db')
        if not os.path.exists(db_path):
            print("База данных не найдена. Создаем новую...")
            db.create_all()
            return
        
        # Подключаемся к базе данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Проверяем, существует ли столбец game_file
        cursor.execute("PRAGMA table_info(database)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'game_file' not in columns:
            print("Добавляем столбец game_file в таблицу database...")
            cursor.execute("ALTER TABLE database ADD COLUMN game_file VARCHAR(255)")
            conn.commit()
            print("Столбец game_file успешно добавлен!")
        else:
            print("Столбец game_file уже существует.")
        
        conn.close()

if __name__ == "__main__":
    migrate_database()
    print("Миграция завершена.") 