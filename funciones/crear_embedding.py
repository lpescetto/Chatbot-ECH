# Función para crear embeddings
def generar_embedding(texto, client):
    response = client.embeddings.create(
        input = texto,
        model= "text-embedding-3-small")
    return response.data[0].embedding
