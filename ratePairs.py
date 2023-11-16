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

# messages = []


def rate1_prompt(user, ai):
    prompt = (
    """Rate the AI's reponse to the USER on a scale of 1 to 5 on the categories of mirroring, specificity, response-relatedness, and question-asking.
    
    USER: '{user}'
    AI: '{ai}'
    
    Display each score as category:score and separate each category with a ,
    
    """).format(user=user, ai=ai)

    return prompt

def rate2_prompt(query):
    prompt = ("""Create a score to rate how these 2 pairs compare based on repetition, specificity, response-relatedness, and question-asking.

    Pair 1:
    "Hello. Where were you last night?"
    "I was studying for an exam"
    
    Pair 2:
    "Hello. Where were you last night?"
    "My favorite color is blue."
           """).format(query=query)

    return prompt


def getRating(user, ai):
    prompt = rate1_prompt(user, ai)
    # print(prompt)
    answer = palm.generate_text(**defaults, prompt=prompt)
    response = answer.candidates[0]['output']
    # messages.append('<USER>' + userInput)
    # messages.append('<BOT>' + response)
    stats = response.split(', ')
    dictionary = {}
    for stat in stats:
        key, value = stat.split(': ')
        dictionary[key] = int(value)

    return dictionary



# stats = getRating(user="Hello. My girlfriend broke up with me", ai="Hi. I'm sorry to hear your girlfriend broke up with you. How are you feeling?")
#
# print(stats)
