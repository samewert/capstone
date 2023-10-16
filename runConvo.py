# Define the function to get a response for a given input
def getResponse(inputText):
    # Replace this with your implementation of generating a response
    response = "AI response"
    return response

# Read input from 'convoInput.txt' and store it in a list
inputList = []
with open('convos/convoInput.txt', 'r') as inputFile:
    inputList = inputFile.read().splitlines()

# Initialize an empty list to store input and response pairs
conversations = []

# Process each input and get responses
for inputText in inputList:
    response = getResponse(inputText)
    conversations.extend([inputText, response])

# Write the input and response pairs to 'convoOutput.txt'
with open('output/convoOutput.txt', 'w') as outputFile:
    for line in conversations:
        outputFile.write(line + '\n')

# Print input and response
for i in range(0, len(conversations), 2):
    print("User:", conversations[i])
    print("AI:", conversations[i + 1])
    print()

print("Conversations saved in 'convoOutput.txt'")
