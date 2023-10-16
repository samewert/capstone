import google.generativeai as palm
import textwrap
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
  'model': 'models/text-bison-001',
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

def embed_function(texts: Documents) -> Embeddings:
    # Embed the documents using any supported method
    return [palm.generate_embeddings(model=embedModel, text=text)['embedding'] for text in texts]

def create_chroma_db(documents, name):
    chroma_client = chromadb.Client()
    db = chroma_client.create_collection(name=name, embedding_function=embed_function)
    for i,d in enumerate(documents):
        db.add(documents=d,ids=str(i))
    return db

# Set up the DB
db = create_chroma_db([DOCUMENT1, DOCUMENT2, DOCUMENT3], "googlecardb")


print(pd.DataFrame(db.peek(1)))


#
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
#
# def make_prompt(query, relevant_passage):
#     escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
#     prompt = textwrap.dedent("""You are a helpful and informative bot that answers questions using text from the reference passage included below. \
#      Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
#      However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
#      strike a friendly and converstional tone. \
#      If the passage is irrelevant to the answer, you may ignore it.
#      QUESTION: '{query}'
#      PASSAGE: '{relevant_passage}'
#
#        ANSWER:
#      """).format(query=query, relevant_passage=escaped)
#
#     return prompt
#
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





