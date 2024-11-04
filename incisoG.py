import incisosABC
import numpy as np



# ====================================================================================================
# Variables auxiliares
# ====================================================================================================
# Define la probabilidad de que una persona sufra un siniestro (por 1, 1.5 y 2 millas) en un año y el costo de este
p = [0.01,0.02,0.025]
c = 1000
# Define las matrices de costos de camiones correspondientes a cada problema (es lo unico que cambia entre cada inciso)
costosCam = [np.array([
    [300, 0, 700],
    [-1, 400, 500],
    [600, 300, 200],
    [200, 500, -1],
    [0, -1, 400],
    [500, 300, 0]
]), np.array([
    [300, 0, 700],
    [-1, 400, 500],
    [600, 300, 0],
    [0, 500, -1],
    [0, -1, 400],
    [500, 300, 0]
]), np.array([
    [0, 0, 700],
    [-1, 400, 500],
    [600, 0, 0],
    [0, 500, -1],
    [0, -1, 400],
    [500, 0, 0]
])]
# Define las caardinalidades, dimensiones y funciones auxiliares (iguales a las de incisosABC)
analyticI = lambda x: x+6
analyticJ = lambda x: x+1
analyticK = lambda x: x+1
cardI = 3
cardJ = 6
cardK = 3
dimVars1D = cardI * cardJ * cardK
def indice(i, j, k):
    ind = i*cardJ*cardK + j*cardK + k  
    return ind

# Define un tensor para representar las probabilidades de un siniestro al ir del area j a la escuela k por inciso s
# Para trabajar el indexado-0 de python consideramos que los incisos son 0,1,2 en vez de 1,3,4
probs = np.zeros((cardJ, cardK, 3))
for j in range(cardJ):
    for k in range(cardK):
        for s in range(3):
            if costosCam[0][j, k] == 0 :    # Primera condición
                probs[j, k, s] = p[0]  
            if s > 0 and costosCam[1][j, k] == 0 and costosCam[0][j, k] != 0: # Segunda condición
                probs[j, k, s] = p[1]  
            if s > 1 and costosCam[2][j, k] == 0 and costosCam[1][j, k] != 0 and costosCam[0][j, k] != 0:   # Tercera condición
                probs[j, k, s] = p[2] 




# ====================================================================================================
# Calcular costo de siniestros para c), e), f)
# ====================================================================================================
# Obten las soluciones de los problemas pasados
sols = [incisosABC.sol(costCam, False) for costCam in costosCam]
# Calcula el numero esperado de siniestros por cada inciso
numSinis = [0,0,0]
for i in range(cardI):
    for j in range(cardJ):
        for k in range(cardK):
            for s in range(3):
                numSinis[s] += probs[j,k,s]*sols[s].x[indice(i,j,k)] if costosCam[s][j,k]==0 else 0
# Calcula los costos de esos siniestros
costoSinis = [c*numSini for numSini in numSinis]
# Imprime informacion
print()
print("Costos esperados por siniestros")
print("                                          c)          e)           f)")
print("-------------------------------------------------------------------------")
print(f"Numero esperado de siniestros:     {numSinis[0]:>10.2f}   {numSinis[1]:>10.2f}   {numSinis[2]:>10.2f}")
print(f"Costos esperados por siniestros:   {costoSinis[0]:>10.2f}   {costoSinis[1]:>10.2f}   {costoSinis[2]:>10.2f}")
print()



# ====================================================================================================
# Minimizacion de costos considerando siniestros
# ====================================================================================================
# Ahora, supongamos que nos interesa minimizar costos, tomando en cuenta los camiones y los siniestros
# Para esto, a la antigua funcion objetivo, le sumamos el costo esperado de siniestros

# Definimos los costos de la nueva funcion objetivo
costosTot = [0,0,0]
costosTotSinis = [0,0,0]
for s in range(3):
    costos = [0]*dimVars1D
    for i in range(cardI): 
        for j in range(cardJ):
            for k in range(cardK):
                costos[indice(i,j,k)] = costosCam[s][j,k]
                costos[indice(i,j,k)] += probs[j,k,s]*c if costosCam[s][j,k]==0 else 0
    costosTot[s] =incisosABC.sol(costosCam[s], False).fun
    costosTotSinis[s] = incisosABC.sol(costosCam[s], False, costos).fun
# Imprimimos la info
print()
print('Minimizando costos tomando en cuenta el costo de los siniestros')
print("                                          c)          e)           f)")
print("-------------------------------------------------------------------------")
print(f"Costos totales sin siniestros:     ${costosTot[0]:>10.2f}   ${costosTot[1]:>10.2f}   ${costosTot[2]:>10.2f}")
print(f"Costos totales con siniestros:     ${costosTotSinis[0]:>10.2f}   ${costosTotSinis[1]:>10.2f}   ${costosTotSinis[2]:>10.2f}")
print()