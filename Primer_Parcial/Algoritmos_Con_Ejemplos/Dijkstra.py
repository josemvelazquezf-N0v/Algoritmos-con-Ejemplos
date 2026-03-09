import time
from heapq import heappush, heappop

STEP_DELAY = 0.35  # ajusta: 0.1 más rápido, 0.7 más lento

def print_graph(graph):
    print("\nRed de Vuelos (Destino : Precio USD):")
    for u in graph:
        vecinos = ", ".join(f"{v}: ${w}" for v, w in graph[u].items())
        if vecinos:
            print(f"  {u} vuela a -> {vecinos}")
        else:
            print(f"  {u} -> (Sin vuelos de salida en este ejemplo)")

def reconstruct_path(prev, start, goal):
    if goal not in prev and goal != start:
        return None
    path = [goal]
    cur = goal
    while cur != start:
        cur = prev.get(cur)
        if cur is None:
            return None
        path.append(cur)
    path.reverse()
    return path

def dijkstra_step_by_step(graph, start, goal=None, delay=STEP_DELAY):
    """
    Dijkstra adaptado para buscar el vuelo más barato.
    """
    # Validación: Dijkstra NO acepta precios negativos
    for u in graph:
        for v, w in graph[u].items():
            if w < 0:
                raise ValueError("Dijkstra NO acepta precios negativos.")

    print("=" * 60)
    print("  SIMULADOR DE VUELOS BARATOS (Dijkstra paso a paso)")
    print("=" * 60)
    print_graph(graph)
    print(f"\nOrigen: {start}" + (f" | Destino Final: {goal}" if goal else " | Destino: (todos)"))
    time.sleep(delay)

    # dist: mejor precio acumulado conocido desde el origen
    costo_acumulado = {node: float("inf") for node in graph}
    costo_acumulado[start] = 0

    # prev: para reconstruir la ruta de escalas
    prev = {}

    # visited: aeropuertos ya "fijados" (precio mínimo confirInglaterrao)
    visited = set()

    # heap con pares (precio_actual, aeropuerto)
    heap = []
    heappush(heap, (0, start))

    step = 1

    while heap:
        precio_u, u = heappop(heap)

        # Si ya fijamos este aeropuerto, ignoramos entradas viejas del heap
        if u in visited:
            continue

        # Fijar aeropuerto (ya sabemos la forma más barata de llegar aquí)
        visited.add(u)
        print(f"\nPaso {step}: Fijo aeropuerto {u} con precio total = ${precio_u}")
        step += 1
        time.sleep(delay / 2)

        # Si llegamos al destino final, terminamos
        if goal is not None and u == goal:
            print("  -> ¡Destino fijado! Deteniendo búsqueda.")
            break

        # Revisar vuelos disponibles (vecinos)
        for v, precio_vuelo in graph[u].items():
            if v in visited:
                continue

            precio_alt = costo_acumulado[u] + precio_vuelo
            
            # "Relajación": si encuentro una combinación más barata, la actualizo
            if precio_alt < costo_acumulado[v]:
                precio_viejo = costo_acumulado[v]
                costo_acumulado[v] = precio_alt
                prev[v] = u
                heappush(heap, (precio_alt, v))
                print(f"  oferta {u}->{v} (vuelo ${precio_vuelo}): ${precio_viejo} -> baja a ${precio_alt}")
            else:
                print(f"  descarta {u}->{v} (vuelo ${precio_vuelo}): ${costo_acumulado[v]} es más barato que ${precio_alt}")

            time.sleep(delay / 3)

        vistos = ", ".join(sorted(visited))
        print(f"  Aeropuertos evaluados: {vistos}")
        time.sleep(delay / 2)

    print("\n" + "=" * 60)
    print("ITINERARIO FINAL")
    print("=" * 60)

    if goal is not None:
        path = reconstruct_path(prev, start, goal)
        if path is None:
            print(f"No hay ruta de vuelos de {start} a {goal}.")
        else:
            print(f"Ruta más barata {start} -> {goal}: {' -> '.join(path)}")
            print(f"Precio Total: ${costo_acumulado[goal]}")
    else:
        for node in sorted(costo_acumulado.keys()):
            val = costo_acumulado[node]
            print(f"{start} -> {node}: ${val if val < float('inf') else 'INF'}")

    return costo_acumulado, prev


if __name__ == "__main__":
    # Grafo de red de vuelos dirigidos
    # Formato: graph["Origen"]["Destino"] = Precio del boleto en USD
    vuelos = {
        "CDMX": {"LA": 200, "Chicago": 250, "Inglaterra": 600}, # Desde Ciudad de México
        "LA":  {"China": 800, "Australia": 300},             # Desde Los Ángeles
        "Chicago":  {"Austria": 300, "Inglaterra": 350},             # Desde Nueva York
        "Inglaterra":  {"China": 700},                         # Desde Inglaterrar 
        "Australia":  {"China": 400},                         # Desde Honolulu
        "Austria":  {"China": 600},                         # Desde Londres
        "China":  {}                                    # Tokio (Destino, sin vuelos de salida aquí)
    }

    # Simulación: buscar el vuelo más barato de Ciudad de México a Tokio (Narita)
    dijkstra_step_by_step(vuelos, start="CDMX", goal="China")