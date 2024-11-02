import incisosABC
import numpy as np

# Costos que valian $300 en e), valen 0 ahora
costCam = np.array([
    [0, 0, 700],
    [-1, 400, 500],
    [600, 0, 0],
    [0, 500, -1],
    [0, -1, 400],
    [500, 0, 0]
])

incisosABC.sol(costCam)