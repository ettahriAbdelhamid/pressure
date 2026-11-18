import numpy as np
import sys

def read_header_and_data(path):
    header = {}
    with open(path, "rb") as f:
        while True:
            line = f.readline().decode("utf-8", errors="ignore").strip()
            if line == "END_HEADER":
                break
            if "=" in line:
                key, val = line.split("=", 1)
                header[key.strip()] = val.strip()

        data = np.fromfile(f, dtype=">f4")
    return header, data

def packed_link_to_su3(v):
    # v has 6 complex entries
    a = np.array([v[0], v[1], v[2]], dtype=np.complex128)
    b = np.array([v[3], v[4], v[5]], dtype=np.complex128)

    # For this vacuum file, this reconstructs the identity matrix
    c = np.cross(a, b)
    U = np.column_stack([a, b, c])
    return U

def packed_link_to_su3_REAL(v):
    # v has 6 complex entries
    a = np.array([v[0], v[1], v[2]])
    b = np.array([v[3], v[4], v[5]])

    # For this vacuum file, this reconstructs the identity matrix
    c = np.cross(a, b)
    U = np.column_stack([a, b, c])
    return U

def packed_link_to_su3_REAL_SINGLEARRAY(v):
    # v has 6 complex entries
    a = np.array([v[0], v[1], v[2]])
    b = np.array([v[3], v[4], v[5]])

    # For this vacuum file, this reconstructs the identity matrix
    c = np.cross(a, b)
    U = np.append(np.append(a, b), c)
    
    if np.allclose(U, [1, 0, 0, 0, 1, 0, 0, 0, 1]):
        return 1
    elif np.allclose(U, [0, 0, 0, 0, 0, 0, 0, 0, 0]):
        return 0
    return U

myfile=sys.argv[1]
newSize=int(sys.argv[2])

header, data = read_header_and_data(myfile)

xSize=newSize
ySize=newSize
zSize=newSize
tSize=2


print(header)

# Convert interleaved real/imag floats into complex numbers
z = data[0::2]

links = z.reshape(xSize, ySize, zSize, tSize, 4, 6)
# Reshape into (x,y,z,t,mu,6)
print("=============================================")
print("REAL")
print("=============================================")

for t in range(tSize):
    for z in range(zSize):
        for y in range(ySize):
            for x in range(xSize):
                print(f"\nsite ({x},{y},{z},{t})", end="")
                for mu in range(4):
                    U = packed_link_to_su3_REAL_SINGLEARRAY(links[x, y, z, t, mu])
                    print(f"{mu}->", end=" ")
                    print(f"{U}; ", end="")
                print()


# Convert interleaved real/imag floats into complex numbers
z =data[1::2]
links = z.reshape(xSize, ySize, zSize, tSize, 4, 6)

# Reshape into (x,y,z,t,mu,6)cd /home/aettahri/simQcd/data/latticegrow && python3 readBinAsMat.py | head -n 60cd /home/aettahri/simQcd/data/latticegrow && python3 readBinAsMat.py | head -n 60

print("=============================================")
print("IMAGINARY")
print("=============================================")

for t in range(tSize):
    for z in range(zSize):
        for y in range(ySize):
            for x in range(xSize):
                print(f"\nsite ({x},{y},{z},{t})", end="")
                for mu in range(4):
                    U = packed_link_to_su3_REAL_SINGLEARRAY(links[x, y, z, t, mu])
                    print(f"{mu}->", end=" ")
                    print(f"{U}; ", end="")
                print()