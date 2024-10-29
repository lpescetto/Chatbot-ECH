# Chatbot-ECH
Repositorio creado para el trabajo final del curso IA con Python. 

El proyecto consiste en desarrollar un chatbot que haga consultas a la ECH de Uruguay, utilizando el diccionario de variables y modelos de embedding y NLP de OpenAI.

En esta versión piloto las consultas se hacen a la base de la implantación de la ECH 2024, utilizando los ponderadores semestrales.

A continuación se describe el proceso de creación y uso del chatbot:

1. El primer paso consiste en tomar el diccionario de variables original de la ECH (archivo 'json_ech.json') y extraer los nombres de las variables y sus respectivas preguntas, y generarles embeddings
solo a las preguntas para luego darle al modelo como diccionario de variables aquellas que más se parezcan a la consulta hecha por el usuario. Este proceso se hace en Pre-procesamiento.ipynb y el resultado
es el archivo 'variables_ech_emb.json'.

3. El segundo paso consiste en crear un RAG que a partir del diccionario de variables pueda responder a consultas del usuario acerca de la ECH. Este proceso se hace en varias partes:  
   a. Se toma la consulta del usuario y se la compara con las preguntas de la ECH utilizando la distancia del coseno entre los embeddings. Se conservan las 30 preguntas más parecidas.  
   b. Se le solicita a un modelo de NLP un código de Python que haga los filtros y cálculos necesarios para obtener la respuesta a la consulta del usuario. Para eso se le brinda un 
   diccionario con las 30 preguntas seleccionadas anteriormente, además se le da información extra, como los nombres y estructura de variables indispensables: departamento, sexo, edad.  
   c. Una vez obtenido el código de Python, se utiliza un nuevo modelo de NLP para que lo modifique incorporando los ponderadores semestrales de la ECH.  
   d. Por último, se corre el código de Python y se genera una respuesta para el usuario con la información por la cual consultó, y el código que se utilizó para obtenerla.  

Algunos ejemplos de consultas que el chatbot es capaz de responder correctamente:

- ¿Cuál es la edad promedio de las mujeres de Durazno?
- ¿Cuántas personas hay en promedio en los hogares de Montevideo?
- ¿Qué porcentaje de Maldonado saber leer y escribir?
- ¿Qué porcentaje de personas tienen un ingreso superior a $30000?
- ¿Cuál es la diferencia entre el ingreso promedio de Montevideo y Artigas?

El chatbot se puede utilizar en el notebook 'chatbot.ipynb'.
