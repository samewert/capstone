import openai

openai.api_key = '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'

completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])
print(completion.choices[0].message.content)


