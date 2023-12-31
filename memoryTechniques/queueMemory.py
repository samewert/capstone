import google.generativeai as palm
from collections import deque

bardKey = 'AIzaSyA44l27TAC60NpOM04q4NCfpXg2wE5sBrk'

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

queueLen = 3
queue = deque(maxlen=queueLen)

def initializeQueue():
    global queue
    queue = deque(maxlen=queueLen)

def make_prompt(input):
    prompt = ("""You are a talkative chatbot that incorporates previous chat history into your response when appropriate.
     USER INPUT: '{input}'
     CHAT HISTORY: '{queue}'

     ANSWER: """).format(input=input, queue=list(queue))

    return prompt

def getQueueResponse(userInput):
    prompt = make_prompt(userInput)
    # print(prompt)
    answer = palm.generate_text(**defaults, prompt=prompt, model=textModel)
    response = answer.candidates[0]['output']
    # if len(queue) == queueLen:
    #     queue.remove()
    #     queue.remove()
    queue.append('<USER> ' + userInput)
    queue.append('<Bot> ' + response)

    return response, prompt
