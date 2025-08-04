@echo off
echo ========================================
echo Загрузка проекта на GitHub
echo ========================================

echo.
echo 1. Проверяем установлен ли Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git не установлен!
    echo Скачайте Git с https://git-scm.com/
    echo Или установите GitHub Desktop
    pause
    exit /b 1
)

echo Git найден!
echo.

echo 2. Инициализируем Git репозиторий...
git init
if %errorlevel% neq 0 (
    echo Ошибка инициализации Git!
    pause
    exit /b 1
)

echo 3. Добавляем все файлы...
git add .
if %errorlevel% neq 0 (
    echo Ошибка добавления файлов!
    pause
    exit /b 1
)

echo 4. Создаем первый коммит...
git commit -m "Initial commit: Telegram userbot system with AI"
if %errorlevel% neq 0 (
    echo Ошибка создания коммита!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Готово! Теперь нужно:
echo ========================================
echo 1. Создайте репозиторий на GitHub.com
echo 2. Скопируйте URL репозитория
echo 3. Выполните команды:
echo    git remote add origin YOUR_REPO_URL
echo    git push -u origin main
echo.
echo Или используйте GitHub Desktop для простоты!
echo ========================================
pause 