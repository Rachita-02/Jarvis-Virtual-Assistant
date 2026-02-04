
from groq import Groq
import os

client =Groq(api_key=os.getenv("GROQ_API_KEY"))

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a virtual assisstant named jarvis skilled in general task like alexa and gloogle cloud"},
        {"role": "user", "content": "what is coding"}
    ]
)

print(completion.choices[0].message.content)






