import cv2
import numpy as np

def finde_rohr_position(foto, rohr):
    # Lade das Foto und das Rohrbild
    foto = cv2.imread(foto)
    rohr = cv2.imread(rohr)

    # Konvertiere das Foto und das Rohrbild in Graustufen
    foto_gray = cv2.cvtColor(foto, cv2.COLOR_BGR2GRAY)
    rohr_gray = cv2.cvtColor(rohr, cv2.COLOR_BGR2GRAY)

    # Führe eine Objekterkennung durch
    resultat = cv2.matchTemplate(foto_gray, rohr_gray, cv2.TM_CCOEFF)
    _, _, min_loc, _ = cv2.minMaxLoc(resultat)

    # Extrahiere die Position des Rohrs
    x, y = min_loc
    rohr_hoehe, rohr_breite = rohr_gray.shape

    # Berechne die Mitte des Rohrs
    rohr_mitte_x = x + rohr_breite // 2
    rohr_mitte_y = y + rohr_hoehe // 2

    # Berechne die Ausrichtung des Rohrs
    schwellenwert = 100
    _, binarisiertes_foto = cv2.threshold(foto_gray, schwellenwert, 255, cv2.THRESH_BINARY_INV)
    konturen, _ = cv2.findContours(binarisiertes_foto, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rohr_kontur = None

    for kontur in konturen:
        (x_kontur, y_kontur, breite_kontur, hoehe_kontur) = cv2.boundingRect(kontur)
        if x <= x_kontur <= x + rohr_breite and y <= y_kontur <= y + rohr_hoehe:
            rohr_kontur = kontur
            break

    # Bestimme die Ausrichtung des Rohrs (in Grad)
    ausrichtung = 0
    if rohr_kontur is not None:
        (x_kontur, y_kontur, breite_kontur, hoehe_kontur) = cv2.boundingRect(rohr_kontur)
        moment = cv2.moments(rohr_kontur)
        if moment["m00"] != 0:
            schwerpunkt_x = int(moment["m10"] / moment["m00"])
            schwerpunkt_y = int(moment["m01"] / moment["m00"])
            ausrichtung = np.degrees(np.arctan2(schwerpunkt_y - y_kontur - hoehe_kontur // 2, schwerpunkt_x - x_kontur - breite_kontur // 2))
            if ausrichtung < 0:
                ausrichtung += 360

    return rohr_mitte_x, rohr_mitte_y, ausrichtung

def markiere_rohrposition(bild, rohr_position):
    rohr_mitte_x, rohr_mitte_y, ausrichtung = rohr_position

    # Lade das Bild
    bild = cv2.imread(bild)

    # Setze einen roten Punkt an der Rohrposition
    roter_punkt = (0, 0, 255)  # Rot (BGR-Farbformat)
    cv2.circle(bild, (rohr_mitte_x, rohr_mitte_y), 5, roter_punkt, 100)

    # Zeige das Bild mit markierter Rohrposition an
    cv2.imwrite("Bild_mit_markierter_Rohrposition.jpg", bild)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

# Beispielaufruf
rohr_position = finde_rohr_position('foto.jpg', 'rohr.jpg')
markiere_rohrposition("foto.jpg", rohr_position)
print("Die Position des Rohrs ist:", rohr_position)


# BSP x-koordinate -> mitte des Bauteils liegt 2825 Pixel von der linken kante entfernt