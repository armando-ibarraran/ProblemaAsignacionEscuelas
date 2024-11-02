import numpy as np
from scipy.optimize import linprog



# ====================================================================================================
# Variables de descicion
# ====================================================================================================

# Van implicitas en el programa, pero son de la forma
#   x_{jk}     numero de estudiantes que iran a i grado desde el area j a la escuela k
# con j=1,2,...,6   k=1,2,3

# Para trabajar con el indexado-0 que se usa en python, pensaremos que i=0,1,2   j=0,...,5   k=0,1,2
# Podemos transformar estos indices a la version analitica con las siguientes funciones
analyticI = lambda x: x+6
analyticJ = lambda x: x+1
analyticK = lambda x: x+1

# Definimos cardinalidad de los conjuntos en que viven nuestros indices
cardI = 3 
cardJ = 6
cardK = 3

# Como linprog pide un vector de costos en una sola dimension, 
# Para nuestras variables de decision, pensaremos en un vector de la forma [x11, x12, x13, x21, ..., x63]

# Definimos la dimension de este vector 1D
dimVars1D = cardJ * cardK
# Funcion para obtener indice del vector 1D
def indice(j, k):
    ind = j*cardK + k  
    return ind



# ====================================================================================================
# Variables auxiliares
# ====================================================================================================

# Costos del camion del area j a la escuela k
# j = renglon, k = columna
# Tomamos los costos de los arreglos inviables como -1 
costCam = np.array([
    [300, 0, 700],
    [-1, 400, 500],
    [600, 300, 200],
    [200, 500, -1],
    [0, -1, 400],
    [500, 300, 0]
])

# Numero de espacios disponibles en escuela k
# k = indice
espDisp = np.array([900, 1100, 1000])

# Porcentaje de alumnos de grado i en area j
# i = renglon, j = columna
porcAlum = np.array([
    [32, 37, 30, 28, 39, 34],
    [38, 28, 32, 40, 34, 28],
    [30, 35, 38, 32, 27, 38]
])

# Numero de alumnos en area j
# j = indice
numAlum = np.array([450, 600, 550, 350, 500, 450])

# ====================================================================================================
# Restricciones PPL
# ====================================================================================================

# Definimos arreglos iniciales
costos = [0]*dimVars1D
coefsDesig = [] # Coeficientes de las variables para desigualdades
valDesig = [] # Valor constante de las desigualdades
coefsIg = [] # Coeficientes de las variables para igualdades
valIg = [] # Valor constante de las igualdades

# Obtenemos vector de costos
for j in range(cardJ):
    for k in range(cardK):
        costos[indice(j,k)] = numAlum[j]*costCam[j,k]

# Obtenemos restricciones tipo i
# Si estas restricciones se imponen, el espacio factible es vacio
"""
for i in range(cardI):  # para cada i
    for k in range(cardK):   # para cada k
        # Aqui definimos cada restriccion del tipo i

        # Primera restriccion
        coefs = [0]*dimVars1D
        # Definimos los coeficientes del primer termino de la resta
        for i in range(cardI):
            for j in range(cardJ):
                coefs[indice(j,k)] = 0.3*numAlum[j]*porcAlum[i,j]
        # Actualizamos los coeficientes para segundo termino de la resta
        for j in range(cardJ):
            coefs[indice(j,k)] -= numAlum[j]*porcAlum[i,j]
        coefsDesig.append(coefs)
        valDesig.append(0)

        # Segunda restriccion
        coefs = [0]*dimVars1D
        # Definimos los coeficientes del primer termino de la resta
        for i in range(cardI):
            for j in range(cardJ):
                coefs[indice(j,k)] = -0.36*numAlum[j]*porcAlum[i,j]
        # Actualizamos los coeficientes para segundo termino de la resta
        for j in range(cardJ):
            coefs[indice(j,k)] += numAlum[j]*porcAlum[i,j]
        coefsDesig.append(coefs)
        valDesig.append(0)
"""

# Obtenemos restricciones tipo ii
for k in range(cardK):  # para cada k
    # Aqui definimos cada restriccion del tipo ii
    coefs = [0]*dimVars1D
    for i in range(cardI):
        for j in range(cardJ):
            coefs[indice(j,k)] = numAlum[j]
    coefsDesig.append(coefs)
    valDesig.append(espDisp[k])

# Obtenemos restricciones tipo iii
for j in range(cardJ):  # para cada j
    # Aqui definimos cada restriccion del tipo iii
    coefs = [0]*dimVars1D
    for k in range(cardK):
        coefs[indice(j,k)] = 1
    coefsIg.append(coefs)
    valIg.append(1)

# Obtenemos restricciones tipo iv
coefs = [0]*dimVars1D
coefs[indice(1,0)] = 1
coefsIg.append(coefs)
valIg.append(0)
coefs = [0]*dimVars1D
coefs[indice(3,2)] = 1
coefsIg.append(coefs)
valIg.append(0)
coefs = [0]*dimVars1D
coefs[indice(4,1)] = 1
coefsIg.append(coefs)
valIg.append(0)



# ====================================================================================================
# Solucion PPL
# ====================================================================================================

# Corremos el simplex
optimo = linprog(costos, A_ub=coefsDesig, b_ub=valDesig, A_eq=coefsIg, b_eq=valIg, bounds=(0,1), integrality=1)

# Imprimamos solucion optima y valor de las variables
print('\n')
print(f'Costo minimo de ${optimo.fun}\n')
print(f'Valor de las variables::')
for j in range(cardJ):
    print(f'\tIndicadoras del area {analyticJ(j)}')
    for k in range(cardK):
        print(f'\t\tx{analyticJ(j)}{analyticK(k)} = {optimo.x[indice(j,k)]} ')
print()

# Algunos datos interesantes
print('Numero de alumnos asignados por escuela:')
for k in range(cardK): 
    cant = 0.0
    for j in range(cardJ):
        cant += optimo.x[indice(j,k)]*numAlum[j]
    print(f'\tA la escuela {analyticK(k)} se le asignaron {cant} alumnos de {espDisp[k]} que podia recibir')
print()

print('Porcentaje de alumnos en cada grado por escuela:')
for k in range(cardK):
    print(f'\tPorcentajes en escuela {analyticK(k)}')
    for i in range(cardI): 
        cantAlumGradoi = 0
        for j in range(cardJ):
            cantAlumGradoi += optimo.x[indice(j,k)]*numAlum[j]*porcAlum[i,j]
        cantAlumn = 0
        for a in range(cardI):
            for j in range(cardJ):
                cantAlumn += optimo.x[indice(j,k)]*numAlum[j]*porcAlum[a,j]
        print(f'\t\tGrado {analyticI(i)}: {np.round(100*cantAlumGradoi/cantAlumn,2)}%')
print()