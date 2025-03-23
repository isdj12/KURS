@echo off
echo Удаление конфиденциальных файлов и временных директорий...

:: Удаляем базу данных
if exist instance\*.db del /Q instance\*.db

:: Удаляем временные файлы и кэш
if exist __pycache__ rmdir /S /Q __pycache__
if exist .pytest_cache rmdir /S /Q .pytest_cache
if exist .coverage del /Q .coverage
if exist htmlcov rmdir /S /Q htmlcov

:: Удаляем виртуальное окружение
if exist .venv rmdir /S /Q .venv

:: Удаляем служебные директории
if exist "базы учу" rmdir /S /Q "базы учу"
if exist "static copy" rmdir /S /Q "static copy"

:: Удаляем учебные файлы и тестовые файлы
if exist база.py del /Q база.py

:: Удаляем все .log файлы
del /S /Q *.log

echo Конфиденциальные файлы и временные директории удалены!

:: Создание пустой структуры для загрузки изображений
if not exist item.image mkdir item.image

echo.
echo Репозиторий очищен и готов к публикации.
echo Для публикации в новый репозиторий выполните следующие команды:
echo git init
echo git add .
echo git commit -m "Initial commit"
echo git branch -M main
echo git remote add origin https://github.com/username/new-repo.git
echo git push -u origin main
echo. 