import random
from Trayecto import Trayecto,MatrizTrayectos

def generar_individuo(n):
    individuo = list(range(n))
    random.shuffle(individuo)
    return individuo

def calcular_fitness(individuo, matriz):
    distancia_total = 0
    for i in range(len(individuo)):
        distancia_total += matriz[individuo[i-1]][individuo[i]]
    return distancia_total

def seleccion_por_torneo(poblacion, fitnesses, k=3):
    seleccionados = random.sample(list(zip(poblacion, fitnesses)), k)
    return min(seleccionados, key=lambda x: x[1])[0]

def crossover_de_ciclo(padre1, padre2):
    size = len(padre1)
    hijo = [-1] * size
    ciclo = 0
    while -1 in hijo:
        if ciclo % 2 == 0:
            current_index = hijo.index(-1)
            value = padre1[current_index]
            while hijo[current_index] == -1:
                hijo[current_index] = padre1[current_index]
                current_index = padre2.index(value)
                value = padre1[current_index]
        else:
            current_index = hijo.index(-1)
            value = padre2[current_index]
            while hijo[current_index] == -1:
                hijo[current_index] = padre2[current_index]
                current_index = padre1.index(value)
                value = padre2[current_index]
        ciclo += 1
    return hijo

def crossover_ordenado(padre1, padre2):
    size = len(padre1)
    hijo = [-1]*size
    start, end = sorted(random.sample(range(size), 2))
    hijo[start:end] = padre1[start:end]
    fill_index = end % size
    for city in padre2:
        if city not in hijo:
            hijo[fill_index] = city
            fill_index = (fill_index + 1) % size
    return hijo

def crossover_hibrido(padre1, padre2):
    if random.random() > 0.5:
        return crossover_de_ciclo(padre1, padre2)
    else:
        return crossover_ordenado(padre1, padre2)

def mutacion_intercambio(individuo):
    a, b = random.sample(range(len(individuo)), 2)
    individuo[a], individuo[b] = individuo[b], individuo[a]

def two_opt(individuo, matriz):
    mejor = individuo[:]
    mejor_distancia = calcular_fitness(mejor, matriz)
    for i in range(1, len(individuo) - 1):
        for j in range(i + 1, len(individuo)):
            if j - i == 1:
                continue
            nuevo_individuo = individuo[:]
            nuevo_individuo[i:j] = reversed(individuo[i:j])
            nueva_distancia = calcular_fitness(nuevo_individuo, matriz)
            if nueva_distancia < mejor_distancia:
                mejor = nuevo_individuo[:]
                mejor_distancia = nueva_distancia
    return mejor, mejor_distancia

def algoritmo_genetico(matriz, tam_poblacion=100, generaciones=1000, p_mutacion=0.2, tasa_elitismo=0.1, prob_2opt=0.3):
    poblacion = [generar_individuo(len(matriz)) for _ in range(tam_poblacion)]
    num_elitismo = int(tam_poblacion * tasa_elitismo)

    for gen in range(generaciones):
        fitnesses = [calcular_fitness(ind, matriz) for ind in poblacion]
        nueva_poblacion = [ind for ind, fit in sorted(zip(poblacion, fitnesses), key=lambda x: x[1])[:num_elitismo]]
        
        while len(nueva_poblacion) < tam_poblacion:
            padre1 = seleccion_por_torneo(poblacion, fitnesses)
            padre2 = seleccion_por_torneo(poblacion, fitnesses)
            hijo = crossover_hibrido(padre1, padre2)
            if random.random() < p_mutacion:
                mutacion_intercambio(hijo)
            if random.random() < prob_2opt:  # Aplicar 2-opt con cierta probabilidad
                hijo, _ = two_opt(hijo, matriz)
            nueva_poblacion.append(hijo)
        
        poblacion = nueva_poblacion

    fitnesses = [calcular_fitness(ind, matriz) for ind in poblacion]
    mejor_individuo = min(zip(poblacion, fitnesses), key=lambda x: x[1])[0]
    return mejor_individuo, min(fitnesses)

# Ejecución del Algoritmo Genético
if __name__ == '__main__':
    mt = MatrizTrayectos()
    mt.crear_matriz_distancias()
    #mt.mostrar_matriz_distancias()
    matriz_distancias = mt.get_matriz()

    mejor_ruta, mejor_distancia = algoritmo_genetico(matriz_distancias)
    
    print(f"Mejor distancia encontrada por AG: {mejor_distancia:.2f}")
