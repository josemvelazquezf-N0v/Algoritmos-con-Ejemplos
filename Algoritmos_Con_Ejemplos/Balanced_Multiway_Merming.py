import random

# Generar matrículas de estudiantes (simula los exámenes recibidos sin orden)
n = 20
examenes = [random.randint(1000, 9999) for _ in range(n)]

print(" PILA ORIGINAL (Exámenes entregados al azar):")
print(examenes)
print("-" * 60)

# ---------------------------------------------------------
# FASE 1: Crear "Runs" (Pilas pequeñas ordenadas en el piso)
# ---------------------------------------------------------
# El tamaño del escritorio (RAM) solo permite ordenar 4 exámenes a la vez
espacio_escritorio = 4 
pilas_en_piso = []

for i in range(0, n, espacio_escritorio):
    # El profesor toma un bonche que quepa en su escritorio
    bonche = examenes[i:i + espacio_escritorio]
    bonche.sort() # Los ordena rápidamente a mano
    pilas_en_piso.append(bonche) # Los deja como una pila ordenada en el piso

print("  FASE 1: Pilas pequeñas creadas en el piso (cada una está ordenada internamente)")
for idx, pila in enumerate(pilas_en_piso):
    print(f"  Pila {idx + 1}: {pila}")
print("-" * 60)

# ---------------------------------------------------------
# FASE 2: Balanced Multiway Merging (Fusión K-way)
# ---------------------------------------------------------
k = 3  # El profesor puede mirar y comparar 3 pilas a la vez sin confundirse
pasada = 1

# Mientras haya más de una pila en el piso, seguimos fusionando
while len(pilas_en_piso) > 1:
    print(f"\n PASADA {pasada}: Juntando de {k} en {k} pilas (Pilas totales actuales: {len(pilas_en_piso)})")
    nuevas_pilas = []
    i = 0
    
    while i < len(pilas_en_piso):
        # El profesor agarra hasta K pilas del piso
        grupo_de_pilas = pilas_en_piso[i:i + k]
        
        # Índices para saber qué examen estamos viendo en la parte de arriba de cada pila
        indices = [0] * len(grupo_de_pilas)
        pila_fusionada = []
        
        while True:
            matricula_minima = None
            indice_pila_ganadora = -1
            
            # Miramos el examen de hasta arriba de las pilas que estamos comparando
            for idx in range(len(grupo_de_pilas)):
                if indices[idx] < len(grupo_de_pilas[idx]):
                    matricula_actual = grupo_de_pilas[idx][indices[idx]]
                    
                    if matricula_minima is None or matricula_actual < matricula_minima:
                        matricula_minima = matricula_actual
                        indice_pila_ganadora = idx
                        
            # Si todas las pilas de este grupo ya se vaciaron, terminamos esta fusión
            if indice_pila_ganadora == -1:
                break
                
            # Pasamos el examen con la matrícula más baja a la nueva pila fusionada
            pila_fusionada.append(matricula_minima)
            indices[indice_pila_ganadora] += 1 # Avanzamos a la siguiente hoja de esa pila
            
        nuevas_pilas.append(pila_fusionada)
        print(f"  -> Se fusionaron las pilas {i} a {i+len(grupo_de_pilas)-1}. Nueva pila tiene {len(pila_fusionada)} exámenes.")
        i += k
        
    pilas_en_piso = nuevas_pilas
    pasada += 1

# ---------------------------------------------------------
# RESULTADO FINAL
# ---------------------------------------------------------
examenes_ordenados = pilas_en_piso[0] if pilas_en_piso else []
print("\n" + "=" * 60)
print(" RESULTADO FINAL (Una sola pila ordenada para entregar a la escuela):")
print(examenes_ordenados)
print("=" * 60)