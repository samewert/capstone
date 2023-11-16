import google.generativeai as palm
import numpy as np
import pandas as pd
import chromadb
from chromadb.api.types import Documents, Embeddings

bardKey = 'AIzaSyAD17YvlKd1b0gYirNd7Ta-gTxYok76A3U'

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

DOCUMENT1 = "Bob is 6' tall"
DOCUMENT2 = "Joe has blonde hair"
DOCUMENT3 = "Bill is awesome"

def embedFunction(texts: Documents) -> Embeddings:
    # Embed the documents using any supported method
    return [palm.generate_embeddings(model=embedModel, text=text)['embedding'] for text in texts]

# def createChromaDb(documents, name):
#
#     # chromaClient = chromadb.PersistentClient(path='db')
#     db = chromaClient.create_collection(name=name, embedding_function=embedFunction)
#     # for i,d in enumerate(documents):
#     #     db.add(documents=d,ids=str(i))
#     return db

user = 'user1'

chromaClient = chromadb.Client()
# chromaClient = chromadb.PersistentClient()
# chromaClient.reset()

# print(chromaClient.get_collection(name=user).peek())

if len(chromaClient.list_collections()) < 1:
    chromaClient.create_collection(name=user, embedding_function=embedFunction)



# id = 0

# Set up the DB
# db = createChromaDb([DOCUMENT1, DOCUMENT2, DOCUMENT3], "user1")
# db = createChromaDb([], 'user1')

def addDocument(query, collectionName):
    embedding = palm.generate_embeddings(model=embedModel, text=query)['embedding']
    id = chromaClient.get_collection(collectionName).count()
    chromaClient.get_collection(collectionName).add(ids=str(id), embeddings=embedding, documents=query)

def get_relevant_passage(query, collectionName):
    embedding = palm.generate_embeddings(model=embedModel, text=query)['embedding']
    passage = chromaClient.get_collection(collectionName).query(query_embeddings=embedding, n_results=3)['documents']
    return passage[0]
    # if len(passage[0]) == 0:
    #     return ''
    # return passage[0][0]

def make_prompt(query, relevant_passage):
    prompt = ("""You are a talkative chatbot that incorporates previous chat history into your response when appropriate.
     USER INPUT: '{query}'
     CHAT HISTORY: '{relevant_passage}'
     
     ANSWER: """).format(query=query, relevant_passage=relevant_passage)

    return prompt

def getEmbeddingResponse(query):
    cleanedQuery = query.replace("'", "").replace('"', "").replace("\n", " ")
    passage = get_relevant_passage(cleanedQuery, user)
    prompt = make_prompt(cleanedQuery, passage)
    # print(prompt)
    # print(textModel)
    answer = palm.generate_text(**defaults, prompt=prompt, model=textModel)
    response = answer.candidates[0]['output']

    addDocument(cleanedQuery, user)
    # TODO how to include for user input and ai response? Combine them into the same line? separate documents?

    return response, prompt


# temperature = 0.65
# query = 'Where does Bill live?'
# print(getResponse(textModel, query, db, temperature))




## Manual Vector Database

# texts = [DOCUMENT1, DOCUMENT2, DOCUMENT3]
#
# db = pd.DataFrame(texts)
# db.columns = ['Text']
# print(db)
#
# def embed_fn(text):
#     return palm.generate_embeddings(model=embedModel, text=text)['embedding']
#
# db['Embeddings'] = db['Text'].apply(embed_fn)
# print(db)
#
# query = "Who is Joe?"
#
# def find_best_passage(query, db):
#     """
#     Compute the distances between the query and each document in the dataframe
#     using the dot product.
#     """
#     query_embedding = palm.generate_embeddings(model=embedModel, text=query)
#     dot_products = np.dot(np.stack(db['Embeddings']), query_embedding['embedding'])
#     idx = np.argmax(dot_products)
#     return db.iloc[idx]['Text']  # Return text from index with max value
#
# passage = find_best_passage(query, db)
# print(passage)

# prompt = make_prompt(query, passage)
# print(prompt)
#
# temperature = 0.5
# answer = palm.generate_text(prompt=prompt,
#                             model=textModel,
#                             candidate_count=3,
#                             temperature=temperature,
#                             max_output_tokens=1000)
#
# for i, candidate in enumerate(answer.candidates):
#   print(f"Candidate {i}: {candidate['output']}\n")





