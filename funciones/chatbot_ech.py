from funciones.crear_embedding import generar_embedding
from funciones.RAG_ab import obtener_codigo_py
from funciones.RAG_c import aplica_ponderador
from funciones.RAG_d import obtener_respuesta

def chatbot_ech(client, pregunta, diccionario, base):

    codigo = obtener_codigo_py(client, pregunta)

    codigo_ponderado = aplica_ponderador(client, codigo)

    respuesta = obtener_respuesta(client, pregunta, codigo_ponderado, base)

    return respuesta