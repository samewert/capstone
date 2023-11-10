import time
# from embeddingDatabase import getResponse
from queueMemory import getResponse

# Define the function to get a response for a given input
# def getResponse(inputText):
#     # Replace this with your implementation of generating a response
#     response = "AI response"
#     return response

# Initialize an empty list to store input and response pairs
conversations = []

totalTime = 0

try:
    while True:
        userInput = input("You: ")
        if userInput.lower() == 'q':
            break
        startTime = time.time()
        response = getResponse(userInput)
        endTime = time.time()
        totalTime += (endTime - startTime)
        print(f"Bot: {response}")

        conversations.extend([userInput, response])

except KeyboardInterrupt:
    print('\nSaved')
    print('Average Response Time: {}'.format(totalTime / (len(conversations) / 2.0)))

    # filename = 'manual1'
    filename = 'queueTest'

    # Write the input and response pairs to 'convoOutput.txt'
    with open('output/manual/' + filename + 'Output.txt', 'w') as outputFile:
        for line in conversations:
            outputFile.write(line + '\n')
