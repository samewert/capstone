import time
from embeddingDatabase import getResponse

# Define the function to get a response for a given input
# def getResponse(inputText):
#     # Replace this with your implementation of generating a response
#     response = "AI response"
#     return response

# Read input from 'convoInput.txt' and store it in a list
filename = 'studentConvo'

inputList = []
with open('convos/' + filename + '.txt', 'r') as inputFile:
    inputList = inputFile.read().splitlines()

# Initialize an empty list to store input and response pairs
conversations = []


totalTime = 0

# Process each input and get responses
for inputText in inputList:
    startTime = time.time()
    response = getResponse(inputText)
    endTime = time.time()
    conversations.extend([inputText, response])

    totalTime += (endTime - startTime)

# Write the input and response pairs to 'convoOutput.txt'
with open('output/' + filename + 'Output.txt', 'w') as outputFile:
    for line in conversations:
        outputFile.write(line + '\n')

# Print input and response
for i in range(0, len(conversations), 2):
    print("User:", conversations[i])
    print("AI:", conversations[i + 1])
    print()

print("Conversations saved in 'convoOutput.txt'")
print('Average Response Time: {}'.format(totalTime / len(inputList)))
