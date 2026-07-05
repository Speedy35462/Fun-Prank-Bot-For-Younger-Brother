@echo off
setlocal enabledelayedexpansion

echo ====================================
echo      UPDATE FUN PRANK BOT       
echo ====================================

echo Closing the old version of the bot...
taskkill /F /IM main.exe >nul 2>&1
timeout /t 3 /nobreak >nul

:: 2. Проверяем, распаковался ли архив во временную папку
if not exist "temp\Fun-Prank-Bot-For-Younger-Brother-main" (
    echo [ERROR] Update failed: temporary folder not found.
    pause
    exit /b
)

:: 3. Копируем новые файлы поверх старых
echo Copying new files...
xcopy "temp\Fun-Prank-Bot-For-Younger-Brother-main\*" "." /E /H /C /I /Y >nul

:: 4. Очищаем мусор
echo Clearing temporary files...
rmdir /S /Q temp >nul 2>&1
if exist update.zip del /Q update.zip >nul

:: 5. Запускаем обновленного бота
echo Starting the updated bot...
start "" "main.exe"

echo Update completed successfully!
timeout /t 2 >nul
exit