import numpy as np
from scipy.optimize import linprog

def sol(costCam = None, printEnabled=True, costos=None):

    # ====================================================================================================
    # Variables de descicion
    # ====================================================================================================

    # Van implicitas en el programa, pero son de la forma
    #   x_{ijk}     numero de estudiantes que iran a i grado desde el area j a la escuela k
    # con i=6,7,8  j=1,2,...,6   k=1,2,3

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
    # Para nuestras variables de decision, pensaremos en un vector de la forma [x611, x612, x613, x621, ..., x663, x711, ..., x863]

    # Definimos la dimension de este vector 1D
    dimVars1D = cardI * cardJ * cardK
    # Funcion para obtener indice del vector 1D
    def indice(i, j, k):
        ind = i*cardJ*cardK + j*cardK + k  
        return ind



    # ====================================================================================================
    # Variables auxiliares
    # ====================================================================================================

    # Costos del camion del area j a la escuela k
    # j = renglon, k = columna
    # Tomamos los costos de los arreglos inviables como -1 
    if costCam is None: # Esto es agregado para poder correr los incisos e y f
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

    # Numero de alumnos de grado i en area j
    # i = renglon, j = columna
    alum = np.array([
        [144, 222, 165, 98, 195, 153],
        [171, 168, 176, 140, 170, 126],
        [135, 210, 209, 112, 135, 171]
    ])


    # ====================================================================================================
    # Restricciones PPL
    # ====================================================================================================

    # Definimos arreglos iniciales
    coefsDesig = [] # Coeficientes de las variables para desigualdades
    valDesig = [] # Valor constante de las desigualdades
    coefsIg = [] # Coeficientes de las variables para igualdades
    valIg = [] # Valor constante de las igualdades

    # Obtenemos vector de costos
    if costos is None:
        costos = [0]*dimVars1D
        for i in range(cardI): 
            for j in range(cardJ):
                for k in range(cardK):
                    costos[indice(i,j,k)] = costCam[j,k]

    # Obtenemos restricciones tipo i
    for i in range(cardI):  # para cada i
        for k in range(cardK):   # para cada k
            # Aqui definimos cada restriccion del tipo i

            # Primera restriccion
            coefs = [0]*dimVars1D
            # Definimos los coeficientes del primer termino de la resta
            for i in range(cardI):
                for j in range(cardJ):
                    coefs[indice(i,j,k)] = 0.3
            # Actualizamos los coeficientes para segundo termino de la resta
            for j in range(cardJ):
                coefs[indice(i,j,k)] -= 1
            coefsDesig.append(coefs)
            valDesig.append(0)

            # Segunda restriccion
            coefs = [0]*dimVars1D
            # Definimos los coeficientes del primer termino de la resta
            for i in range(cardI):
                for j in range(cardJ):
                    coefs[indice(i,j,k)] = -0.36
            # Actualizamos los coeficientes para segundo termino de la resta
            for j in range(cardJ):
                coefs[indice(i,j,k)] += 1
            coefsDesig.append(coefs)
            valDesig.append(0)

    # Obtenemos restricciones tipo ii
    for k in range(cardK):  # para cada k
        # Aqui definimos cada restriccion del tipo ii
        coefs = [0]*dimVars1D
        for i in range(cardI):
            for j in range(cardJ):
                coefs[indice(i,j,k)] = 1
        coefsDesig.append(coefs)
        valDesig.append(espDisp[k])

    # Obtenemos restricciones tipo iii
    for i in range(cardI):  # para cada i
        for j in range(cardJ):  # para cada j
            # Aqui definimos cada restriccion del tipo iii
            coefs = [0]*dimVars1D
            for k in range(cardK):
                coefs[indice(i,j,k)] = 1
            coefsIg.append(coefs)
            valIg.append(alum[i,j])

    # Obtenemos restricciones tipo iv
    for i in range(cardI):  # para cada i
        # Aqui definimos cada restriccion del tipo iv de 3 en 3
        coefs = [0]*dimVars1D
        coefs[indice(i,1,0)] = 1
        coefsIg.append(coefs)
        valIg.append(0)

        coefs = [0]*dimVars1D
        coefs[indice(i,3,2)] = 1
        coefsIg.append(coefs)
        valIg.append(0)
        
        coefs = [0]*dimVars1D
        coefs[indice(i,4,1)] = 1
        coefsIg.append(coefs)
        valIg.append(0)



    # ====================================================================================================
    # Solucion PPL
    # ====================================================================================================

    # Corremos el simplex
    optimo = linprog(costos, A_ub=coefsDesig, b_ub=valDesig, A_eq=coefsIg, b_eq=valIg, integrality=1)
    if printEnabled:
        # Imprimamos solucion optima y valor de las variables
        print('\n')
        print(f'Costo minimo de ${optimo.fun}\n')
        print(f'Valor de las variables:')
        for j in range(cardJ):
            print(f'\tAsignados del area {analyticJ(j)}')
            for i in range(cardI):
                print(f'\t\tDel grado {analyticI(i)}')
                for k in range(cardK):
                    print(f'\t\t\tx{analyticI(i)}{analyticJ(j)}{analyticK(k)} = {np.round(np.abs(optimo.x[indice(i,j,k)]))} \t a la escuela {analyticK(k)}')  
                    # se redondea y calcula del valor absoluto de la variable para ajustar errores de precision computacionales, 
                    # pero esto no afecta el resultado, ya que dentro de las restricciones se exige que las variables sean enteros no negativos
        print()

        # Algunos datos interesantes
        print('Numero de alumnos asignados por escuela:')
        for k in range(cardK): 
            numAlum = 0
            for i in range(cardI):
                for j in range(cardJ):
                    numAlum += optimo.x[indice(i,j,k)]
            print(f'\tA la escuela {analyticK(k)} se le asignaron {numAlum} alumnos de {espDisp[k]} que podia recibir')
        print()

        print('Porcentaje de alumnos en cada grado por escuela:')
        for k in range(cardK):
            print(f'\tPorcentajes en escuela {analyticK(k)}')
            for i in range(cardI): 
                cantAlumGradoi = 0
                for j in range(cardJ):
                    cantAlumGradoi += optimo.x[indice(i,j,k)]
                cantAlumn = 0
                for a in range(cardI):
                    for j in range(cardJ):
                        cantAlumn += optimo.x[indice(a,j,k)]
                print(f'\t\tGrado {analyticI(i)}: {np.round(100*cantAlumGradoi/cantAlumn,2)}%')
        print()
    return optimo

if __name__ == "__main__":
    sol()