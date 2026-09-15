@echo off
chcp 65001 >nul
color 0A
cls
echo.
echo ========================================
echo  GENERANDO PDF DE 30+ PAGINAS
echo ========================================
echo.
cd /d "%~dp0"

REM Intentar con python
python generar_pdf_30_paginas.py
if errorlevel 1 (
    echo.
    echo ERROR: Python no encontrado en PATH
    echo.
    echo Intenta con la ruta completa...
    C:\Users\alo81\AppData\Local\Programs\Python\Python311\python.exe generar_pdf_30_paginas.py
)

if errorlevel 1 (
    echo.
    echo ERROR: No se pudo generar el PDF
    echo Por favor, instala Python desde https://www.python.org/downloads/
    pause
) else (
    echo.
    echo ==========================================
    echo ✅ PDF GENERADO CORRECTAMENTE
    echo ==========================================
    echo.
    pause
)
