import cv2

# Funktion zum Zeichnen einer Box um die Kanten
def draw_box(image, bbox, color=(0, 255, 0), thickness=4):
    x, y, w, h = bbox
    cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)

# Funktion zum Zeichnen des Mittelpunkts
def draw_center(image, center, color=(0, 0, 255), radius=5):
    cv2.circle(image, center, radius, color, 20)

# Funktion zum Zeichnen der Achse
def draw_axis(image, point1, point2, color=(255, 0, 0), thickness=3):
    cv2.line(image, point1, point2, color, thickness)

# Funktion zur Berechnung des Mittelpunkts und Zeichnen der Box und Achse
def mittelpunkt(image_path):
    print(image_path)

    # Laden des Bildes
    image = cv2.imread(image_path)

    # Konvertieren in Graustufenbild
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Anwenden der Canny-Kantenerkennung
    edges = cv2.Canny(gray, 20, 150)
    cv2.imwrite("edge.jpg", edges)

    # Suchen der Konturen im Bild
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Ermitteln der äußersten Koordinaten aller Boxen, die eine Mindestgröße überschreiten
    min_size = 100  # Mindestgröße für eine Box
    x_coords = []
    y_coords = []
    widths = []
    heights = []
    for contour in contours:
        # Berechnen der Begrenzungsbox um die Kontur
        x, y, w, h = cv2.boundingRect(contour)
        if w > min_size and h > min_size:
            x_coords.append(x)
            y_coords.append(y)
            widths.append(w)
            heights.append(h)

    # Ermitteln der größten umfassenden Box
    if x_coords and y_coords and widths and heights:
        x_min = min(x_coords)
        y_min = min(y_coords)
        x_max = max(x_coords) + max(widths)
        y_max = max(y_coords) + max(heights)
        bbox = (x_min, y_min, x_max - x_min, y_max - y_min)

        # Zeichnen der umfassenden Box
        draw_box(image, bbox)

        # Ermitteln der Mittelpunkt der Box
        center = (x_min + int((x_max - x_min) / 2), y_min + int((y_max - y_min) / 2))

        # Zeichnen des Mittelpunkts in Rot
        draw_center(image, center)

        # Ermitteln der Längsachse
        if x_max - x_min > y_max - y_min:
            # Längsachse verläuft horizontal
            point1 = (x_min, center[1])
            point2 = (x_max, center[1])
            print("horizontal")
        else:
            # Längsachse verläuft vertikal
            point1 = (center[0], y_min)
            point2 = (center[0], y_max)
            print("vertikal")

        # Zeichnen der Längsachse in Blau
        draw_axis(image, point1, point2)

    # Speichern des Bildes mit der gezeichneten Box und Achse
    cv2.imwrite('box15.jpg', image)
    try:
        print(center)   
        print("\n")
    except:
        print("Error no center value")


# Aufruf der Funktion mit dem Pfad zum Bild


mittelpunkt('rohr (14).jpg')
