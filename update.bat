taskkill /f /im main.exe

xcopy /y "temp\Fun-Prank-Bot-For-Younger-Brother-main\*" ".\"

rmdir /s /q "temp"
del "update.zip"

main.exe