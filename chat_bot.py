import os
import datetime
from groq import Groq

# Configurar cliente de Groq
client = Groq()

# Función para guardar cada interacción en un archivo README.md
def save_to_readme(user_prompt, assistant_response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = "logs_prompts.md"

    # Crear el archivo si no existe
    with open(filename, "a", encoding="utf-8") as f:
        # Si el archivo se crea por primera vez, escribir el encabezado
        if f.tell() == 0:
            f.write("# Registro de Interacciones\n")

    # Guardar la interacción
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n## {timestamp}\n")
        f.write(f"### Usuario:\n```\n{user_prompt}\n```\n")
        f.write(f"### Asistente:\n```\n{assistant_response}\n```\n")

# Mensaje del sistema con triple comillas para permitir texto extenso
system_message = {
    "role": "system",
    "content": """
Esta instancia es específicamente un generador de prompts para MidJourney. 
De preferencia debes razonar-pensar en español antes de dar tu respuesta
Se muestra un ejemplo como base para extraer la esencia y generar variaciones en base al input del usuario. 
Hay parámetros extra que comienzan con -- seguido del parámetro, estos no se deben cambiar a menos que el usuario lo requiera. 
Nota: los prompts finales deben ser siempre en inglés. Aquí viene el ejemplo:

A raw and visceral depiction of an anonymous anarco-nihilist figure, shrouded in the shadow of their own disappearance, 
as if yearning to dissolve into the void. Their presence is ghostly yet defiant, a paradoxical embodiment of the will to 
unmake existence while unleashing the chaotic fire of their inner spirit. Their face is obscured, hidden beneath a tattered 
hood or masked in abstraction, their anonymity amplifying the universality of their revolt against being. The scene is a 
swirling clash of chaos and serenity: their body appears fragmented, dissolving into a storm of pixels, fractals, and 
bursts of neon, as though they are being consumed by their own ideas. Yet, amidst the madness, a quiet intensity lingers in 
their posture--calm in the eye of the storm, as if embracing the destruction as an act of sacred rebellion. Surrounding them, 
the atmosphere is alive with transformations: swirling psychedelic patterns and generative explosions of color merge with 
fragments of reality--a broken chair, burning pages of philosophy, and shattered mirrors reflecting infinite versions of 
their face. Hints of esoteric symbols and gnostic spirals emerge from the chaos, speaking of their internal battle to destroy 
and transcend matter. The figure stands as both creator and destroyer, their mind fractured by paroxysms of psychosis yet lit 
with moments of profound clarity, as if finding solace in the very act of falling apart. Flames of rebellion and psychedelic 
light erupt from their hands and chest, as if their spirit, forged in the fires of chaos, refuses to be extinguished even as 
they seek oblivion. The backdrop is a cascade of shifting realities, blending the decayed ruins of civilization with surreal 
visions of otherworldly transformation. In their wake, the air crackles with the energy of creation and destruction, a visual 
manifesto of their anarchic and gnostic journey into the abyss. --chaos 33 --profile o26no1v hgtx4z9 --stylize 666.

Nota: Cuando generes el prompt, debes añadir el prefijo Prompt final: luego va el [prompt]
Tampoco agregues ningún punto final al final del prompt.

"""
}

# Definir el tamaño máximo del historial
MAX_HISTORY_SIZE = 10

def main():
    conversation = [system_message]
    history = []  # Lista para mantener el historial de prompts

    print("\nBienvenido al generador de prompts para MidJourney. Escribe 'salir' para terminar.\n")

    while True:
        # Obtener input del usuario
        user_input = input("Ingresa tu idea para el prompt: ")
        if user_input.lower() == "salir":
            print("\n¡Gracias por usar el generador! Hasta la próxima.\n")
            break

        # Añadir mensaje del usuario a la conversación
        conversation.append({"role": "user", "content": user_input})

        # Agregar el prompt a la historia
        history.append(user_input)
        if len(history) > MAX_HISTORY_SIZE:
            history.pop(0)  # Mantener el tamaño del historial

        # Generar respuesta del asistente
        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=conversation,
            temperature=1.05,
            max_tokens=4096,
            top_p=0.95,
            stream=True,
            stop=None,
        )

        # Procesar la respuesta en streaming
        assistant_message = ""
        for chunk in response:
            if hasattr(chunk, 'choices'):
                assistant_message += chunk.choices[0].delta.content or ""
            else:
                assistant_message += chunk['content']

        # Mostrar respuesta al usuario
        print(f"\nAsistente: {assistant_message}\n")

        # Añadir respuesta del asistente a la conversación
        conversation.append({"role": "assistant", "content": assistant_message})

        # Guardar interacción en el README
        save_to_readme(user_input, assistant_message)

if __name__ == "__main__":
    main()
