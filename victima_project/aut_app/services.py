import os
from google import genai
from dotenv import load_dotenv

# cargar .env
load_dotenv()

# API KEY
API_KEY = os.getenv("GOOGLE_API_KEY")

# cliente Gemini
client = genai.Client(api_key=API_KEY)


PREGUNTAS_FRECUENTES = [
    "¿Cómo consultar si soy beneficiario?",
    "¿Por qué mi consulta no muestra resultados?",
    "¿Qué programas de ayuda existen actualmente?"
]


def consultar_chatbot_victimas(
        pregunta_usuario,
        historial=None
):

    pregunta = pregunta_usuario.lower()

    if "beneficiario" in pregunta:
        return (
            "Para consultar si eres beneficiario, "
            "ingresa tu número de documento "
            "en el formulario principal."
        )

    elif "ayuda" in pregunta or "programas" in pregunta:
        return (
            "Actualmente existen apoyos como "
            "ayuda humanitaria, reparación integral, "
            "acompañamiento psicosocial y programas "
            "de vivienda según el caso."
        )

    elif "hola" in pregunta:
        return (
            "Hola 👋 Soy IVON, tu asistente virtual. "
            "¿En qué puedo ayudarte?"
        )

    else:
        return (
            "No tengo información exacta sobre eso. "
            "Por favor intenta reformular tu pregunta."
        )