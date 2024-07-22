@echo off
:: Setze den Skript-Pfad
set SCRIPT_PATH=%~dp0

:: Überprüfe, ob Python installiert ist
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python ist nicht installiert. Bitte installiere Python und füge es zu deinem PATH hinzu.
    exit /b 1
)

:: Virtuelle Umgebung erstellen
echo Erstelle virtuelle Umgebung...
python -m venv %SCRIPT_PATH%venv

:: Aktiviere die virtuelle Umgebung
echo Aktiviere die virtuelle Umgebung...
call %SCRIPT_PATH%venv\Scripts\activate

:: Installiere die Abhängigkeiten
echo Installiere die Abhängigkeiten...
pip install -r %SCRIPT_PATH%requirements.txt

:: Bestätigung der Installation
if %errorlevel% neq 0 (
    echo Fehler bei der Installation der Abhängigkeiten.
    exit /b 1
) else (
    echo Erfolgreich eingerichtet.
)

:: Flask-Anwendung starten
echo Starte die Flask-Anwendung...
python %SCRIPT_PATH%web.py

pause