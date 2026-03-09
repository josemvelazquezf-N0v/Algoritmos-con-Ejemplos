import random
import time

# Generar lista de paquetes (simula los paquetes a ordenar por cercanía)
n = 10
# Cada elemento es ["ID del paquete", distancia_en_km]
arr = [[f"Paquete-{i+1}", random.randint(1, 50)] for i in range(n)]

print(" RUTA ORIGINAL (Desordenada):")
for p in arr:
    print(f"  {p[0]}: {p[1]} km")
print("-" * 40)

# Selection Sort (ordenamiento por selección) - inline, sin funciones
comparisons = 0
swaps = 0

print(" Iniciando carga del camión (del más cercano al más lejano)...\n")

for i in range(len(arr) - 1):
    # asumir que el paquete más cercano está en la posición i
    min_idx = i
    
    # buscar el paquete realmente más cercano en la porción de paquetes aún no ordenados
    for j in range(i + 1, len(arr)):
        comparisons += 1
        # Comparamos la distancia en km (que está en la posición 1 de nuestra sub-lista)
        if arr[j][1] < arr[min_idx][1]:
            min_idx = j
            
    # si el más cercano no está ya en la posición i, el operador los intercambia
    if min_idx != i:
        # Intercambio de los paquetes en la lista
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        swaps += 1
        print(f" Movimiento: Poniendo el {arr[i][0]} ({arr[i][1]}km) en la posición {i+1}")
        
    # comentario: después de cada iteración, arr[0..i] está ordenado
    # (los paquetes más cercanos ya están asegurados al inicio del camión)
    time.sleep(0.5)

print("-" * 40)
print(" RUTA ORDENADA (Lista para el repartidor):")
for p in arr:
    print(f"  {p[0]}: {p[1]} km")
print("-" * 40)
print(f" Estadísticas logísticas -> Comparaciones visuales: {comparisons} | Paquetes movidos (swaps): {swaps}")