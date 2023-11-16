import google.generativeai as palm

bardKey = 'AIzaSyAD17YvlKd1b0gYirNd7Ta-gTxYok76A3U'

palm.configure(api_key=bardKey)

models = [m for m in palm.list_models() if 'embedText' in m.supported_generation_methods]
embedModel = models[0]

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
textModel = models[0]

defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 1024,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":4},{"category":"HARM_CATEGORY_TOXICITY","threshold":4},{"category":"HARM_CATEGORY_VIOLENCE","threshold":4},{"category":"HARM_CATEGORY_SEXUAL","threshold":4},{"category":"HARM_CATEGORY_MEDICAL","threshold":4},{"category":"HARM_CATEGORY_DANGEROUS","threshold":4}],
}

messages = []

def make_prompt(query):
  prompt = ("""You are a talkative chatbot that incorporates previous chat history into your response when appropriate.
       USER INPUT: '{query}'
       CHAT HISTORY: '{messages}'

       ANSWER: """).format(query=query, messages=messages, model=textModel)

  return prompt

def getAllResponse(userInput):
  prompt = make_prompt(userInput)
  # print(prompt)
  answer = palm.generate_text(**defaults, prompt=prompt)
  response = answer.candidates[0]['output']
  messages.append('<USER>' + userInput)
  messages.append('<BOT>' + response)
  return response, prompt
