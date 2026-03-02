import time
from collections import deque

STEP_DELAY = 0.5  # Para ver paso a paso cómo piensa el algoritmo

def buscar_conexion_bfs(red_social, inicio, objetivo):
    print("=" * 60)
    print(f" BUSCANDO CONEXIÓN: {inicio} -> {objetivo}")
    print("=" * 60)
    time.sleep(STEP_DELAY)

    # La "cola" (Queue) es el corazón de BFS. El primero en entrar es el primero en salir.
    # Guardamos tuplas con: (Persona_actual, Grado_de_separacion, Camino_recorrido)
    cola = deque([(inicio, 0, [inicio])])
    
    # Set de personas que ya revisamos para no entrar en bucles infinitos (ej. Tú revisas a Carlos y Carlos te revisa a ti)
    visitados = set([inicio])

    grado_actual = 0

    while cola:
        persona, grado, camino = cola.popleft()

        # Solo para imprimir bonito en consola cuando cambiamos de nivel de contactos
        if grado > grado_actual:
            print(f"\n---  Pasando a los contactos de {grado}º grado ---")
            grado_actual = grado
            time.sleep(STEP_DELAY)

        print(f"Revisando perfil de: {persona} (Grado {grado})")
        time.sleep(STEP_DELAY / 2)

        # ¿Es la persona que buscamos?
        if persona == objetivo:
            print("\n" + "=" * 60)
            print(f" ¡CONEXIÓN ENCONTRADA EN {grado} GRADOS DE SEPARACIÓN!")
            print(f"Ruta de presentación: {' -> '.join(camino)}")
            print("=" * 60)
            return camino

        # Si no es, agregamos a TODOS sus contactos a la fila de espera (cola)
        contactos = red_social.get(persona, [])
        for contacto in contactos:
            if contacto not in visitados:
                visitados.add(contacto)
                # Los añadimos al final de la cola, un grado más lejos
                cola.append((contacto, grado + 1, camino + [contacto]))

    # Si la cola se vacía y no la encontramos
    print(f"\n Fin de la red. No hay conexión entre {inicio} y {objetivo}.")
    return None

if __name__ == "__main__":
    # Diccionario que simula nuestra base de datos de la red social
    # Clave: Persona, Valor: Lista de sus amigos directos
    linkedin_simulado = {
        "Tú": ["Carlos", "María", "Luis"],
        "Carlos": ["Tú", "Jorge", "Elena"],
        "María": ["Tú", "Sofía"],
        "Luis": ["Tú", "Pedro"],
        "Jorge": ["Carlos", "Miguel"],
        "Elena": ["Carlos", "Directora Ana"], # ¡Elena conoce a la Directora!
        "Sofía": ["María", "Diego"],
        "Pedro": ["Luis"],
        "Miguel": ["Jorge"],
        "Diego": ["Sofía", "Directora Ana"],  # Diego también la conoce
        "Directora Ana": ["Elena", "Diego"]
    }

    # Ejecutar la simulación
    buscar_conexion_bfs(linkedin_simulado, inicio="Tú", objetivo="Directora Ana")