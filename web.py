#################### Bügelperlen Designer ################## web.py ##################
from flask import Flask, render_template, request, send_file, flash, url_for, jsonify
from PIL import Image
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Circle
from matplotlib.backends.backend_svg import FigureCanvasSVG
import cProfile
import pstats
from io import StringIO, BytesIO
from fpdf import FPDF
from svglib.svglib import svg2rlg
from datetime import datetime
from reportlab.graphics import renderPDF
from werkzeug.utils import secure_filename
import os
import colorama
from colorama import Fore, Style
import os
import subprocess
from flask import Flask
import webbrowser
import threading
import time
from flask import Flask
import webbrowser
import threading
import time
import signal
import sys
from werkzeug.serving import make_server

app = Flask(__name__)

# Event für das Beenden des Threads
stop_event = threading.Event()
colorama.init(autoreset=True)
#####################################################################################
# Lade Farbpaletten
from farbpalette import erstelle_farbpalette
# Globale Variable für den Fortschritt
progress = {}
# Initialisierung der Flask-Anwendung
app = Flask(__name__)
app.secret_key = '6J9-#&;cWa<!:3i(Wnx,m5Wsf/_@^1:='  # Geheimschlüssel für Flash-Nachrichten

# Verzeichniseinstellungen
PORT=4444
UPLOAD_FOLDER = 'upload'
OUTPUT_FOLDER = 'output'
PROFILING_FOLDER = 'debug/Profilings'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(PROFILING_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

############## Debug Settings ##############
Profiling=True
Testmode=False
############################################
if Profiling==True:
        pr = cProfile.Profile()
        pr.enable()
################### Hilfsfunktion für das Logging und Anzeigen von Nachrichten ##############################
def consolelog(module_name, status, message, msg_type="INFO"):
    if msg_type == "INFO":
        print(f"{Fore.CYAN}{module_name}]{Fore.WHITE} {status}: {message}{Style.RESET_ALL}")
    elif msg_type == "WARNING":
        print(f"{Fore.YELLOW}!WARNUNG![{module_name}] {status}: {message}{Style.RESET_ALL}")
    elif msg_type == "DANGER":
        print(f"{Fore.RED}!FEHLER![{module_name}] {status}: {message}{Style.RESET_ALL}")
    else:
        print(f"[{msg_type}] [{module_name}] {status}: {message}")

def update_progress(task_id, status, percentage):
    progress[task_id] = {'status': status, 'percentage': percentage}

    consolelog("Modul: Progressbar-Web-UI |","INFO", status+" |"+str(percentage),"INFO")

def log_to_ui(message, category='info'):

    
    flash(message, category)

    consolelog("Modul:"+category+"|","INFO", message,"INFO")

############### Bild und PDF Convertierungen ################

# Skaliert ein Bild auf die gegebene Breite und Höhe
def resize_image(image, width, height):
    consolelog("Modul:resize_image|","INFO",str(width)+"x"+str(height),"INFO")
    return image.resize((width, height), Image.LANCZOS)

def convert_to_buegelperlen(image, palette):
    pixels = np.array(image)
    new_pixels = np.apply_along_axis(lambda pixel: find_nearest_color(pixel, palette), 2, pixels)
    return Image.fromarray(new_pixels.astype('uint8'))

def compress_image(image_path, quality=85):
    with Image.open(image_path) as img:
        compressed_path = image_path.replace('.png', '_compressed.jpg')
        img = img.convert("RGB")  # PNG kann einen Alpha-Kanal haben, den wir entfernen müssen
        img.save(compressed_path, "JPEG", quality=quality)
    return compressed_path

# Erstellt eine PDF-Datei mit Compressed PNG , Titel  und Bead Count
def create_pdf(png_path, pdf_path, seitentitel, bild_breite_cm, bild_hoehe_cm, ppcm):
        # Profiling starten
    if Profiling==True:
        pr = cProfile.Profile()
        pr.enable()
    try:
        consolelog("Modul:create_pdf|","INFO",pdf_path,"INFO")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_line_width(0.1)  # Setze die Linienbreite für den Rahmen
        pdf.rect(10, 10, 190, 267)  # (x, y, Breite, Höhe) - Dies setzt einen Rahmen 10 mm vom Rand
        
        # Titel hinzufügen
        pdf.set_font("Arial", size=20)
        pdf.cell(200, 10, txt=seitentitel, ln=True, align='C')
        
        # Bildgröße und Anzahl Perlen hinzufügen
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Bildgröße: {bild_breite_cm} x {bild_hoehe_cm} cm", ln=True, align='C')
        
        consolelog("Modul:create_pdf|","INFO","Lade Vorlage in PDF-Engine!","INFO")
        # Bild hinzufügen und Größe anpassen
        image = Image.open(png_path)
        img_width, img_height = image.size

        # Bildabmessungen in Zentimetern berechnen
        img_width_cm = round(bild_breite_cm/ ppcm)
        img_height_cm = round(bild_hoehe_cm / ppcm)

        consolelog("Modul:create_pdf|","INFO","Zähle Perlen","INFO")

        # Gesamtzahl der Perlen berechnen
        total_perlen = (img_width_cm) * (img_height_cm)
        pdf.cell(200, 10, txt=f"Gesamtzahl der Perlen: {total_perlen}", ln=True, align='C')

        consolelog("Modul:create_pdf|","INFO",f"Gesamtzahl der Perlen: {total_perlen}","INFO")
        # Berechnung des maximalen Bereichs innerhalb des Rahmens
        max_width = 185  # 210 - 2*10 mm Rahmen - 5 mm Abstand zum Rahmen
        max_height = 297 - 10 - 10 - 50  # 297 - 10 mm oben - 10 mm unten - 30 mm für Titel und Text
        
        # Berechnung des Skalierungsfaktors, um das Bild innerhalb des Rahmens anzupassen
        scale = min(max_width / img_width, max_height / img_height)
        
        # Neue Bildabmessungen
        new_width = img_width * scale
        new_height = img_height * scale

        consolelog("Modul:create_pdf|","INFO","Komprimiere Grafiken","INFO")
        compressed_image_path = compress_image(png_path)
        # Berechnung der Positionen, um das Bild zu zentrieren
        x_pos = (210 - new_width) / 2  # Zentriert horizontal auf der A4-Seite (210 mm Breite)
        y_pos = 40 + (max_height - new_height) / 2  # Vertikal zentriert innerhalb des verfügbaren Bereichs

        # Bild einfügen
                # Bild einfügen

        consolelog("Modul:create_pdf|","INFO","Füge Perlen-Grafik in PDF ein!","INFO")

        pdf.image(compressed_image_path, x=x_pos, y=y_pos, w=new_width, h=new_height) 
        
        consolelog("Modul:create_pdf|","INFO","Speichere PDF als "+pdf_path,"INFO")
        
        pdf.output(pdf_path)

        consolelog("Modul:create_pdf|","INFO","PDF "+pdf_path+" wurde gespeichert.","INFO")
    finally:
        # Profiling beenden
        if Profiling==True:
            pr.disable()
            
##################################################################################################################################


##################### Perlen Converter ###########################################################################################
# Wandelt das Bild in Bügelperlen um, indem die Farben angepasst werden
# Findet die nächstgelegene Farbe in der Palette für einen gegebenen Pixel
def find_nearest_color(pixel, palette):
    palette = np.array(palette)
    distances = np.sqrt(np.sum((palette - pixel) ** 2, axis=1))
    return tuple(palette[np.argmin(distances)])

# Startseite der Anwendung
@app.route('/')
def index():
    consolelog("Modul:Designer|","Lade Designer...","INFO")
    return render_template('index.html')


# Verarbeitet das Hochladen eines Bildes und die Erstellung der Vorlage

@app.route('/upload', methods=['POST'])
def upload_image():
    consolelog("Modul:Designer|","Starte Perlen-Converter","INFO")
    task_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    update_progress(task_id, 'Started', 0)
    log_to_ui("Starte PerlenKonverter", "info")    
    try:
        breite_cm = float(request.form.get('breite_cm', 0))
        hoehe_cm = float(request.form.get('hoehe_cm', 0))
        perlen_groesse = request.form.get('perlen_groesse')
        platte_x = int(request.form.get('platte_x', 29))
        platte_y = int(request.form.get('platte_y', 29))
        abstand = float(request.form.get('abstand', 10))
        mode = request.form.get('mode', 'normal')
        originalfarben = 'originalfarben' in request.form
        seitentitel = request.form.get('seitentitel', 'Keine Titel')

        if perlen_groesse == 'mini':
            perlen_groesse_mm = 5
        elif perlen_groesse == 'midi':
            perlen_groesse_mm = 8
        elif perlen_groesse == 'maxi':
            perlen_groesse_mm = 10
        else:
            log_to_ui("Ungültige Größe der Bügelperlen. Verwenden Sie Mini, Midi oder Maxi.", 'error')
            return index()

        if 'file' not in request.files or request.files['file'].filename == '':
            log_to_ui("Keine Datei ausgewählt", 'error')
            return index()

        file = request.files['file']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = secure_filename(f"{timestamp}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(filepath)

        if not os.path.exists(filepath):
            log_to_ui("Fehler beim Speichern der Datei.", 'error')
            return index()

        log_to_ui(f"Bild erfolgreich hochgeladen und gespeichert als: {filepath}")

        original_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{timestamp}.png")
        original_bild = Image.open(filepath).convert('RGBA')
        update_progress(task_id, 'Lade Bild', 1)
        if mode == "Grayscale":
            original_bild = original_bild.convert('L').convert('RGBA')

        original_bild.save(original_image_path, 'PNG')

        breite_in_perlen = round(breite_cm * 10 / perlen_groesse_mm)
        hoehe_in_perlen = round(hoehe_cm * 10 / perlen_groesse_mm)

        skaliertes_bild = resize_image(original_bild, breite_in_perlen, hoehe_in_perlen)
        update_progress(task_id, 'Processing', 25)
        if originalfarben:
            vorlage_bild = skaliertes_bild
        else:
            selected_color=request.form.get('farbpalette',"Standard")
            print(selected_color)
            farb_palette = erstelle_farbpalette(selected_color) ## Farbpalette wählen
            farb_palette_array = [np.array(color, dtype=np.float32) for color in farb_palette]
            vorlage_bild = convert_to_buegelperlen(skaliertes_bild, farb_palette_array)
        update_progress(task_id, 'Processing', 25)
        svg_filename = f"{timestamp}_vorlage.svg"
        svg_path = os.path.join(app.config['OUTPUT_FOLDER'], svg_filename)
        png_filename = f"{timestamp}_vorlage.png"
        png_path = os.path.join(app.config['OUTPUT_FOLDER'], png_filename)

        perlen_durchmesser = perlen_groesse_mm / 10.0
        fig_width = breite_in_perlen * perlen_durchmesser
        fig_height = hoehe_cm

        additional_width = (breite_in_perlen // platte_x) * (abstand / 10.0)
        additional_height = (hoehe_in_perlen // platte_y) * (abstand / 10.0)

        fig = Figure(figsize=(fig_width + additional_width, fig_height + additional_height), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_aspect('equal')
        ax.axis('off')
        fig.patch.set_facecolor('none')

        pixel_array = np.array(vorlage_bild)

        for i in range(pixel_array.shape[0]):
           
            for j in range(pixel_array.shape[1]):
                # Aktuelle Position in linearem Index
                current_pixel_index = i * pixel_array.shape[1] + j

                total_pixels = pixel_array.shape[0] * pixel_array.shape[1]
                # Fortschritt in Prozent berechnen

                progress = (current_pixel_index / total_pixels) * 100
                log_to_ui("Perle an Position: {} | {} | {}x{} | Fortschritt: {:.2f}%".format(i, j, pixel_array.shape[0], pixel_array.shape[1], progress),"Progress")
                color = pixel_array[i, j] / 255.0
                alpha = color[3]  # Alpha-Wert des Pixels
                if alpha > 0:  # Nur Pixel mit Alpha-Wert > 0 zeichnen
                    x_position = j * perlen_durchmesser + (j // platte_x) * (abstand / 10.0)
                    y_position = fig_height - (i * perlen_durchmesser) - (i // platte_y) * (abstand / 10.0)
                    circle = Circle((x_position, y_position), perlen_durchmesser / 2, facecolor=color, edgecolor='black', linewidth=0.5)
                    ax.add_artist(circle)

        ax.set_xlim(-perlen_durchmesser / 2, fig_width + additional_width + perlen_durchmesser / 2)
        ax.set_ylim(-perlen_durchmesser / 2, fig_height + additional_height + perlen_durchmesser / 2)

        fig.tight_layout(pad=0)

        # SVG-Datei erstellen
        canvas = FigureCanvasSVG(fig)
        output = BytesIO()
        canvas.print_svg(output)
        output.seek(0)
        with open(svg_path, 'wb') as f:
            f.write(output.getvalue())

        print("SVG-Vorlage erstellt!")

        # PNG-Datei erstellen
        fig.savefig(png_path, format='png', dpi=100, bbox_inches='tight', pad_inches=0)
        print("PNG-Vorlage erstellt!")

        # Zähle die Farben
        pixel_array = np.array(vorlage_bild)
        color_counts = {}
        for i in range(pixel_array.shape[0]):
            for j in range(pixel_array.shape[1]):
                color = tuple(pixel_array[i, j])
                if color in color_counts:
                    color_counts[color] += 1
                else:
                    color_counts[color] = 1

        pdf_filename = f"{timestamp}_vorlage.pdf"
        pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], pdf_filename)
        create_pdf(png_path, pdf_path, seitentitel, breite_cm, hoehe_cm, 0.5)
        return render_template('index.html', preview_image=png_filename,seitentitel=seitentitel, task_id=task_id) 
        # PDF-Datei erstellen

        
    except Exception as e:
        update_progress(task_id, 'Error', 0)
        log_to_ui(f"Fehler: {e}", 'error')
        consolelog("Modul:Upload|","WARNING",f"Fehler: {e}", 'error',"WARNING")
        return index()

    finally:
      consolelog("Modul:Upload|","INFO","Fertig!","INFO")
         
        
# Bereitstellung der Vorschau-Bilder
@app.route('/preview_image/<filename>')
def preview_image(filename):
    try:
        consolelog("Modul:Designer|","WARNING","Stelle Vorschaubild bereit!","INFO")
        return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename))
    except:
        consolelog("Modul:Designer|","DANGER","Fehler beim Bereitstellen der Grafik","INFO")
@app.route('/progress/<task_id>')
def get_progress(task_id):
    try:
        consolelog("Modul:Designer|","WARNING","Übermittel Vorschritt an WebUI","INFO")
        return jsonify(progress.get(task_id, {'status': 'unknown', 'percentage': 0}))
    except:
        consolelog("Modul:Designer|","DANGER","Fehler beim Progressabruf!","INFO")
# Anwendung starten

def run_flask():
    # Flask-Server aufbauen
    server = make_server('0.0.0.0', PORT, app)
    # Starte den Flask-Server
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        # Behandle das Abbruchsignal (Ctrl+C)
        server.shutdown()
    finally:
        print('Flask-Server beendet.')

def open_browser():
    # Warte, bis der Flask-Server vollständig gestartet ist
    time.sleep(1)
    webbrowser.open('http://localhost:'+str(PORT))  # Verwende die URL mit dem SSL-Port

def signal_handler(sig, frame):
    print('Abbruchsignal empfangen, beende...')
    stop_event.set()  # Setze das Event, um die Threads zu beenden
    sys.exit(0)

if __name__ == '__main__':
    # Registriere das Signal-Handler für Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)  # Handle SIGTERM (nützlich für Terminierungssignale)

    # Starte den Flask-Server in einem separaten Thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Öffne den Webbrowser
    open_browser()

    # Warten, bis das Stop-Event gesetzt wird (d.h. Ctrl+C wird gedrückt)
    stop_event.wait()  # Dies blockiert bis stop_event gesetzt wird

    # Sicherstellen, dass der Flask-Thread beendet ist
    flask_thread.join()
    print('Programm beendet.')

    