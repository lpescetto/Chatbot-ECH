def obtener_respuesta(client, pregunta, codigo, base):

  local_vars = {'df': base}

  exec(codigo, {}, local_vars)

  response = local_vars['response']

  mensaje = [
        {"role": "system", "content": "Eres un chatbot de la encuesta continua de hogares de Uruguay. Recibirás una pregunta de un usuario y tendrás la respuesta a la pregunta y el código de Python con el que se generó. Debes generar una respuesta amigable para el usuario donde respondes la pregunta y al final dejas el código de Python, NO en formato markdown."},
        {"role": "system", "content": "Si el codigo es 'response = 'noinfo'' significa que no hay suficiente información para responder. Contesta eso, y no escribas la línea de código."},
        {"role": "system", "content": f"La respuesta es {response}"},
        {"role": "system", "content": f"El codigo es: {codigo}"},
        {"role": "user", "content": pregunta}
    ]

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
