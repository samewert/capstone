import numpy as np
import google.generativeai as palm

bardKey = 'AIzaSyBRD-JtiPLXXPvpH9HPyfFaxxRAbW5B-NE'

palm.configure(api_key=bardKey)

# for model in palm.list_models():
#     if 'embedText' in model.supported_generation_methods:
#         print(model.name)


x = 'cat and dot'

close = 'I failed an exam'

far = 'I won the lottery'

model = 'models/embedding-gecko-001'

embeddingX = palm.generate_embeddings(model=model, text=x)
embeddingClose = palm.generate_embeddings(model=model, text=close)
embeddingFar = palm.generate_embeddings(model=model, text=far)

print(embeddingX)
print(embeddingClose)
print(embeddingFar)


similarMeasure = np.dot(embeddingX['embedding'], embeddingClose['embedding'])
print(similarMeasure)

farMeasure = np.dot(embeddingX['embedding'], embeddingFar['embedding'])
print(farMeasure)

# 0 means less similar
# 1 means more similar