with open("testGauge1", "rb") as f:
    data = f.read()

binary = ''.join(format(byte, '08b') for byte in data)
print(binary)