import json
import random

class mensajes:

    def __init__(self):
        self.mensajes = ""
    mensaje_actual = ""
    mensaje_backup = ""


# 1. Cargar el archivo JSON
def cargar_datos():
    with open('BaseDeDatos.json', 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

# 2. Lógica de respuesta
def buscar_respuesta(lista_mensajes, datos):
    mensaje_usuario = lista_mensajes.mensaje_actual.lower() # Convertir a minúsculas para comparar

    if mensaje_usuario == "quiero otra respuesta":
        return nueva_respuesta(lista_mensajes.mensaje_backup, datos)

    for intencion in datos['intenciones']:
        for patron in intencion['patrones']:
            if patron in mensaje_usuario: # Si la palabra clave está en el mensaje
                return random.choice(intencion['respuestas'])
    respuestaBot("Lo siento, no entiendo. ¿Puedes enseñarme? Dime que respuesta debería dar.")
    nueva_respuesta(mensaje_usuario, datos) # Si no se encuentra una respuesta, se agrega al JSON
    return "He aprendido algo nuevo gracias a ti."

# 3. Agregar nueva respuesta al JSON
def nueva_respuesta(mensaje_usuario, datos):
    for intencion in datos['intenciones']:
        if mensaje_usuario in intencion['patrones']:
            respuestaBot("Ya conozco ese mensaje, pero ¿qué respuesta quieres que dé?")
            mensaje_respuesta = input("Tú (respuesta para el bot): ")
            intencion['respuestas'].append(mensaje_respuesta)
            with open('BaseDeDatos.json', 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return "Respuesta actualizada: " + mensaje_usuario
    
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
    lista_mensajes = mensajes()
    print("¡Bot activo! (Escribe 'salir' para terminar)")
    
    while True:
        lista_mensajes.mensaje_actual = input("Tú: ").lower() # Actualizar el mensaje actual
        if lista_mensajes.mensaje_actual.lower() == 'salir':
            break
            
        respuesta = buscar_respuesta(lista_mensajes, datos)
        respuestaBot(respuesta)
        if lista_mensajes.mensaje_actual.lower() != "quiero otra respuesta": # Solo actualizar el backup si no se está pidiendo una nueva respuesta
            lista_mensajes.mensaje_backup = lista_mensajes.mensaje_actual # Guardar el mensaje del usuario para la función de nueva respuesta

def respuestaBot(respuesta):
    print(f"Bot: {respuesta}")


if __name__ == "__main__":
    chat()