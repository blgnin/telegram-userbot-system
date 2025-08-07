@echo off
echo ========================================
echo Пуш проекта на GitHub
echo ========================================

echo.
echo 1. Проверяем Git...
git --version
if %errorlevel% neq 0 (
    echo ОШИБКА: Git не найден!
    pause
    exit /b 1
)

echo.
echo 2. Проверяем статус...
git status

echo.
echo 3. Проверяем remote...
git remote -v

echo.
echo 4. Пробуем запушить...
git push -u origin main

echo.
echo 5. Проверяем результат...
git status

echo.
echo ========================================
echo Готово! Проверь GitHub:
echo https://github.com/blgn1n/telegram-userbot-system
echo ========================================
pause 