import cv2
import numpy as np

def detect_tube_direction(image_path):
    # Bild laden
    image = cv2.imread(image_path)

    # Bild in Graustufen konvertieren
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Kantenbildung mit Canny-Algorithmus
    edges = cv2.Canny(gray, 50, 150)

    # Linien mit Hough-Transformation finden
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    # Steigung der Linien berechnen
    slopes = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y2 - y1) / (x2 - x1)
        slopes.append(slope)

    # Durchschnittliche Steigung berechnen
    avg_slope = np.mean(slopes)

    # Richtung des Rohrs bestimmen
    direction = None
    if avg_slope > 0.5:
        direction = "Oben"
    elif avg_slope < -0.5:
        direction = "Unten"
    elif avg_slope > -0.5 and avg_slope < 0.5:
        if avg_slope > 0:
            direction = "Rechts"
        else:
            direction = "Links"

    # Richtung ausgeben
    if direction:
        print("Richtung des Rohrs:", direction)
    else:
        print("Richtung des Rohrs konnte nicht ermittelt werden.")

# Beispielaufruf
detect_tube_direction("bild3.jpg")
