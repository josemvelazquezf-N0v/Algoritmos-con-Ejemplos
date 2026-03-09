import json
import random

# 1. Cargar el archivo JSON
def cargar_datos():
    with open('BaseDeDatos.json', 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

# 2. Lógica de respuesta
def buscar_respuesta(mensaje_usuario, datos):
    mensaje_usuario = mensaje_usuario.lower() # Convertir a minúsculas para comparar
    
    for intencion in datos['intenciones']:
        for patron in intencion['patrones']:
            if patron in mensaje_usuario: # Si la palabra clave está en el mensaje
                return random.choice(intencion['respuestas'])

    nueva_respuesta(mensaje_usuario, datos) # Si no se encuentra una respuesta, se agrega al JSON

# 3. Agregar nueva respuesta al JSON
def nueva_respuesta(mensaje_usuario, datos):
    respuestaBot("Lo siento, no entiendo. ¿Puedes enseñarme? Dime que respuesta debería dar.")
    mensaje_respuesta = input("Tú (respuesta para el bot): ")
    nueva_intencion = {
        "patrones": [mensaje_usuario],
        "respuestas": [mensaje_respuesta]
    }
    datos['intenciones'].append(nueva_intencion)
    
    with open('BaseDeDatos.json', 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
    
    return "Aprendido: " + mensaje_usuario


# 4. Bucle del chat
def chat():
    datos = cargar_datos()
    print("¡Bot activo! (Escribe 'salir' para terminar)")
    
    while True:
        usuario = input("Tú: ")
        if usuario.lower() == 'salir':
            break
            
        respuesta = buscar_respuesta(usuario, datos)
        respuestaBot(respuesta)

def respuestaBot(respuesta):
    print(f"Bot: {respuesta}")


if __name__ == "__main__":
    chat()