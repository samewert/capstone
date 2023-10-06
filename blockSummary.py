"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as palm

bardKey = 'AIzaSyAD17YvlKd1b0gYirNd7Ta-gTxYok76A3U'

palm.configure(api_key=bardKey)

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

def getResponse(prompt):
  response = palm.generate_text(
    **defaults,
    prompt=prompt
  )
  return response


def responsePrompt(text, messages, memory):
  prompt = f"""You are a genius. Read the memory and messages. Guide the user towards an answer but don't give them one directly.
  
  Messages: {messages}
  
  Memory: {memory}
  
  User Input: {text}
  
  Response: """
  return prompt

def summaryPrompt(messages):
  prompt = f"""Summarize these messages in a concise way.
  
  Messages: {messages}
  
  Summary: """
  return prompt

messages = []
memory = []

convoIndex = 1

while convoIndex < 20:
  print(convoIndex)

  text = input()

  prompt = responsePrompt(text, messages, memory)
  messages.append(text)

  response = getResponse(prompt)

  print(response.result)

  messages.append(response.result)

  if convoIndex % 5 == 0:
    prompt = summaryPrompt(messages)
    response = getResponse(prompt)
    memory.append(response.result)

    messages = []

  convoIndex += 1
  print("Memory: {}".format(memory))
  print("Messages: {}".format(memory))

# how to organize these blocks? I can start making summaries of summaries
# how to measure memory