# Bügelperlen Designer

Der **Bügelperlen Designer** ist eine Webanwendung, die es ermöglicht, Bilder in Bügelperlen-Vorlagen zu konvertieren. Die Anwendung verwendet Flask für das Web-Framework, PIL (Python Imaging Library) für die Bildbearbeitung und matplotlib für die Erstellung der Vorlagen.

## Features

- **Bild-Upload und Skalierung**: Lade ein Bild hoch und skaliere es auf die gewünschte Größe.
- **Konvertierung zu Bügelperlen**: Wandle das Bild in eine Bügelperlen-Vorlage um, wobei die Farben automatisch an die nächstgelegenen Farben der Bügelperlen-Palette angepasst werden.
- **PDF-Erstellung**: Generiere ein PDF-Dokument mit der Vorlage, einschließlich Titel, Bildgröße und der Anzahl der benötigten Perlen.
- **Vorschau der Vorlage**: Stelle eine Vorschau der erstellten Vorlage zur Verfügung.
- **Farbauswahl**: Wähle aus verschiedenen Farbpaletten, um die Vorlage anzupassen.
- **Fortschrittsanzeige**: Verfolge den Fortschritt der Bildverarbeitung in Echtzeit.

## Installation

1. **Repository klonen**
   ```sh
   git clone https://github.com/deinbenutzername/buegelperlen-designer.git
   cd buegelperlen-designer

2. **Installation**
   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt

3. **Anwendung Starten**
  ```sh
  Führe dazu die Start.bat aus danach wird die Virtuelle Umgebung eingerichtet, Die Pakete installiert, Und das Script gestartet. Der Webbrowser öffnet sich automatisch




