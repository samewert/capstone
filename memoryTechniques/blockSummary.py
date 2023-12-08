messages = []

import google.generativeai as palm

bardKey = 'AIzaSyBr6QwSp3NuJ4j_rYBWKHJ13dytTTa9g8c'
palm.configure(api_key=bardKey)

models = [m for m in palm.list_models() if 'embedText' in m.supported_generation_methods]
embedModel = models[0]

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
textModel = models[0]

defaults = {
  # 'model': 'models/text-bison-001',
  'temperature': 0,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 1024,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":4},{"category":"HARM_CATEGORY_TOXICITY","threshold":4},{"category":"HARM_CATEGORY_VIOLENCE","threshold":4},{"category":"HARM_CATEGORY_SEXUAL","threshold":4},{"category":"HARM_CATEGORY_MEDICAL","threshold":4},{"category":"HARM_CATEGORY_DANGEROUS","threshold":4}],
}

memory = []
messages = []

def initializeBlock():
    global memory
    global messages
    memory = []
    messages = []

# Be an AI chatbot. Read in the messages and memory. Create your response accordingly.

def make_prompt(input):
  prompt = ("""You are a talkative chatbot that incorporates memory and previous chat history into your response when appropriate.
  USER INPUT: '{input}'
  MEMORY: '{memory}'
  CHAT HISTORY: '{messages}'

  ANSWER: """).format(messages=messages, memory=memory, input=input)
  return prompt

def getBlockResponse(userInput):
  prompt = make_prompt(userInput)
  # print(prompt)
  answer = palm.generate_text(**defaults, prompt=prompt, model=textModel)
  response = answer.candidates[0]['output']

  messages.append("<USER>" + userInput)
  messages.append("<AI>" + response)

  if len(messages) > 5:
      blockPrompt = summaryPrompt()
      summary = palm.generate_text(**defaults, prompt=blockPrompt)
      memory.append(summary.candidates[0]['output'])
      # messages = []
      # del messages[:4]
      del messages[:6]

  return response, prompt

def summaryPrompt():
    prompt = f"""Summarize these messages in a concise way.
    
    MESSAGES: {messages}
    
    SUMMARY: """
    return prompt

# how to organize these blocks? I can start making summaries of summaries
# how to measure memory