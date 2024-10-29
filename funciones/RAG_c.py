def aplica_ponderador(client, codigo):

    mensaje = [
        {"role": "system", "content": "Eres un Analista de datos experto en la encuesta continua de hogares de Uruguay. Recibirás código de Python para calcular un estadístico en la tabla de datos, debes modificarlo para aplicar los ponderadores al código. Los ponderadores están en la variable 'W_SEM', y se debe multiplicar a cada individuo por su ponderador y luego dividir el resultado entre la suma de los ponderadores según el filtro que se haya hecho."},
        {"role": "system", "content": "Solo devuelve la variable response con el codigo modificado en pandas, NUNCA en markdown. si la variable response tiene un str con 'noinfo' no lo modifiques."},
        {"role": "user", "content": codigo}
    ]

    # Llamar al cliente de chat y generar la respuesta
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=mensaje,
        temperature=0,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
  )

    respuesta = response.choices[0].message.content

    return respuesta
