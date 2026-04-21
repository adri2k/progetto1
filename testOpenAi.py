## Test inferenza su openai 

import openai
import os
import dotenv

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_APIKEY")

response = openai.ChatCompletion.create(
  model="gpt-5.4",
  messages=[
    {"role": "user", "content": "Raccontami una barzelletta."}
  ]
)

print(response.choices[0].message['content'])
