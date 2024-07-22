standardfarben = [
        # Standard Farben
        (0, 0, 0, 255),           # Schwarz
        (255, 255, 255, 255),     # Weiß
        (255, 224, 189, 255),     # Hautfarbe
        (165, 42, 42, 255),       # Braun
        (255, 228, 196, 255),     # Beige

        # Blau-Töne
        (135, 206, 250, 255),     # Himmelblau
        (173, 216, 230, 255),     # Babyblau
        (0, 0, 255, 255),         # Königsblau
        (0, 0, 139, 255),         # Dunkelblau
        (64, 224, 208, 255),      # Türkisblau

        # Rot-Töne
        (255, 192, 203, 255),     # Rosa
        (255, 36, 0, 255),        # Zinnoberrot
        (255, 0, 0, 255),         # Rot
        (139, 0, 0, 255),         # Dunkelrot

        # Gelb-Töne
        (255, 255, 224, 255),     # Zitronengelb
        (255, 255, 179, 255),     # Helles Gelb
        (255, 255, 0, 255),       # Gelb
        (255, 215, 0, 255),       # Goldgelb
        (255, 204, 0, 255),       # Senfgelb
        (255, 255, 102, 255),     # Maisgelb
        (255, 221, 51, 255),      # Honiggelb
        (255, 223, 128, 255),     # Gelbgold
        (255, 250, 205, 255),     # Buttergelb
        (255, 245, 150, 255),     # Creme

        # Grün-Töne
        (144, 238, 144, 255),     # Hellgrün
        (152, 251, 152, 255),     # Mintgrün
        (128, 128, 0, 255),       # Olivgrün
        (124, 252, 0, 255),       # Grasgrün
        (80, 200, 120, 255),      # Smaragdgrün
        (0, 128, 0, 255),         # Tannengrün
        (0, 100, 0, 255),         # Dunkelgrün
        (50, 205, 50, 255),       # Limettengrün
        (0, 128, 128, 255),       # Flaschengrün
        (0, 255, 255, 255),       # Seetanggrün

        # Grau-Töne
        (211, 211, 211, 255),     # Hellgrau
        (169, 169, 169, 255),     # Grau
        (105, 105, 105, 255),     # Dunkelgrau
        (112, 128, 144, 255),     # Schiefergrau
        (0, 0, 0, 255),           # Anthrazit

        # Rosa-Violett-Töne
        (255, 182, 193, 255),     # Blassrosa
        (255, 105, 180, 255),     # Rosa
        (255, 20, 147, 255),      # Hot Pink
        (255, 0, 255, 255),       # Magenta
        (255, 0, 255, 255),       # Fuchsia
        (230, 230, 250, 255),     # Lavendel
        (128, 0, 128, 255),       # Lila
        (186, 85, 211, 255),      # Violett
        (218, 112, 214, 255),     # Orchidee
        (147, 112, 219, 255),     # Mittelviolett
    
    ]

Pastelfarben = [
        # Pastell Farben
        (0, 0, 0, 255),           # Schwarz
        (255, 255, 255, 255),     # Weiß
        (255, 224, 189, 255),     # Hautfarbe
        (165, 42, 42, 255),       # Braun
        (255, 228, 196, 255),     # Beige
        (255, 182, 193, 255),     # Pastellrosa
        (255, 255, 204, 255),     # Pastellgelb
        (204, 255, 204, 255),     # Pastellgrün
        (204, 229, 255, 255),     # Pastellblau
        (255, 224, 178, 255),     # Pastellorange
        (230, 190, 255, 255),     # Pastelllila
        (255, 218, 185, 255),     # Pastellpeach
        (198, 255, 218, 255),     # Pastellmint

    ]
SpezialFarben =[
        # Spezial Farben
        (0, 0, 0, 255),           # Schwarz
        (255, 255, 255, 255),     # Weiß
        (255, 215, 0, 255),       # Gold
        (192, 192, 192, 255),     # Silber
        (255, 105, 180, 255)      # Glitzer (als Näherung, da echtes Glitzer nicht darstellbar ist)
]
NeonFarben=[
         # Neon Farben
        (0, 0, 0, 255),           # Schwarz
        (255, 255, 255, 255),     # Weiß
        (255, 20, 147, 255),      # Neonpink
        (0, 255, 0, 255),         # Neongrün
        (255, 69, 0, 255),        # Neonorange
        (0, 191, 255, 255),       # Neonblau
]

def erstelle_farbpalette(palette="Standard"):
    if palette == "Standard":
        neuePalette = standardfarben
    elif palette == "Pastel":
        neuePalette = Pastelfarben
    elif palette == "Mega":
        neuePalette = standardfarben + Pastelfarben + NeonFarben + SpezialFarben
    else:
        neuePalette = []  # Standardmäßig leere Liste, wenn die Palette nicht erkannt wird
    return neuePalette
    
