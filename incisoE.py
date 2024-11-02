import incisosABC
import numpy as np

# Costos que valian $200 en c), valen 0 ahora
costCam = np.array([
    [300, 0, 700],
    [-1, 400, 500],
    [600, 300, 0],
    [0, 500, -1],
    [0, -1, 400],
    [500, 300, 0]
])

incisosABC.sol(costCam)