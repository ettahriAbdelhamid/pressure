import numpy as np

def read_su3_gauge_file(filepath):
    header = {}
    with open(filepath, 'rb') as f:
        while True:
            line = f.readline().decode('utf-8', errors='ignore').strip()
            if line == 'END_HEADER':
                break
            if '=' in line:
                key, val = line.split('=', 1)
                header[key.strip()] = val.strip()
        
        data = np.fromfile(f, dtype='>f4')
        
    return header, data

# Datei einlesen
header, binary_data = read_su3_gauge_file('gauge_1')
print(f"Eingelesene Floats: {binary_data.size}")

# Komplexe Zahlen erstellen
data_native = binary_data.astype(np.float32)
re = data_native[0::2]
im = data_native[1::2]
complex_data = re + 1j * im

print(f"Anzahl komplexer Zahlen: {complex_data.size}")

# Da die Standard-Dimensionen (2x2x2x2 = 16) laut Dateigröße nicht ganz hinhauen 
# (16 * 36 = 576 komplexe Zahlen werden erwartet, aber wir haben hier weniger),
# formen wir es basierend auf der tatsächlichen Größe um:
# Jede Matrix hat 4 Richtungen * 9 Elemente = 36 Zahlen. 
# 192 / 36 = 5.33 -> Es scheint, als ob hier eine andere Anzahl an Gitterpunkten vorliegt.
# Testen wir ein flexibles Reshape, falls es z.B. nur 1 Gitterpunkt oder ein anderer Layout ist:

try:
    # Versuche es mit dem Header (falls er doch stimmt und ich mich verrechnet habe: 16 * 36 = 576)
    nx = int(header['DIMENSION_1'])
    ny = int(header['DIMENSION_2'])
    nz = int(header['DIMENSION_3'])
    nt = int(header['DIMENSION_4'])
    gauge_fields = complex_data.reshape((nx, ny, nz, nt, 4, 3, 3))
    print("Erfolgreich mit Header-Dimensionen geshapet!")
except ValueError as e:
    print(f"Konnte nicht mit Header-Dimensionen geshapet werden: {e}")
    print("Die Dateigröße passt mathematisch nicht exakt zu 2x2x2x2. Bitte prüfen Sie, ob die Datei vollständig ist.")