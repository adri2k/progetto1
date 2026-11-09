## Test inferenza su openai

import openai
import os
import dotenv

dotenv.load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_APIKEY"))

response = client.chat.completions.create(
  model="gpt-5.4",
  messages=[
    {"role": "user", "content": "Raccontami una barzelletta breve"}
  ]
)

# Stampa la risposta generata da OpenAI
print(response.choices[0].message.content)

# Stampami i token usati 
print(f"Token usati: {response.usage.total_tokens}")
