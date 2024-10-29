import json
import numpy as np
import os

from funciones.crear_embedding import generar_embedding

# Función para obtener código de Python
def obtener_codigo_py(client, pregunta, k=30):

    # Cargar los embeddings y los textos desde el archivo JSON
    with open('variables_ech_emb.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extraer embeddings y preguntas
    embeddings = [item['Question_vector'] for item in data]
    preguntas = [item['Question'] for item in data]
    ids = [item['ID'] for item in data]
    
    # Generar el embedding para la pregunta del usuario
    pregunta_embedding = generar_embedding(pregunta, client)

    # Convertir los embeddings almacenados y la pregunta en arrays de NumPy
    embeddings_array = np.vstack(embeddings)
    pregunta_embedding_array = np.array(pregunta_embedding)

    # Calcular la similitud coseno entre la pregunta y los embeddings almacenados
    dot_product = np.dot(embeddings_array, pregunta_embedding_array)
    norm_embeddings = np.linalg.norm(embeddings_array, axis=1)
    norm_pregunta = np.linalg.norm(pregunta_embedding_array)
    similitudes = dot_product / (norm_embeddings * norm_pregunta)

    # Obtener los índices de las preguntas más similares
    indices_top_k = np.argsort(similitudes)[-k:][::-1]

    # Obtener los IDs de los elementos más relevantes
    ids_relevantes = [ids[i] for i in indices_top_k]

    # Filtrar el JSON para incluir solo los elementos relevantes (campos Variable Name y Question)
    elementos_relevantes = [
        {key: value for key, value in item.items() if key not in ['ID', 'Question_vector']} 
        for item in data if item['ID'] in [ids[i] for i in indices_top_k]
    ]

    # Convertir los elementos relevantes en formato JSON para el contexto
    contexto = "\n".join([json.dumps(item) for item in elementos_relevantes])

    # Construir el mensaje con el contexto incluido
    mensaje = [
        {"role": "system", "content": "Eres un programador experto en la encuesta continua de hogares de Uruguay. A partir de una consulta de un usuario, debes devolver el código necesario para extraer la información relevante de la tabla."},
        {"role": "system", "content": "Genera únicamente el código en pandas que debo ejecutar para obtener la respuesta en crudo, NUNCA en formato Markdown. Siempre debes almacenar la respuesta en una variable llamada 'response'. Intenta que response siempre sea un solo número pero incluyendo todas las variables correspondientes."},
        {"role": "system", "content": f"Aquí tienes algunos fragmentos del diccionario de variables de la tabla en formato JSON. Usa solo variables que estén en el campo 'Variable Name':\n{contexto}. Si te preguntan por algo que no se encuentra en el contexto, guarda 'noinfo' en la variable 'response'."},
        {"role": "system", "content": "Recuerda: Los nombres de los departamentos de Uruguay están en la variable 'nom_dpto' con mayúsculas al comienzo de cada palabra excepto la letra y; y tildes. La variable sexo es 'e26' (hombre = 1, mujer = 2), edad es 'e27', y el ingreso es 'PT1'"},
        {"role": "user", "content": pregunta}
    ]

    # Llamar al cliente de chat y generar la respuesta
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Cambiado a un modelo de chat compatible
        messages=mensaje,
        temperature=0,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    # Acceder al contenido del mensaje y retornarlo
    respuesta = response.choices[0].message.content

    return respuesta

