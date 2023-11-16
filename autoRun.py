import time
from memoryTechniques.embeddingDatabase import getEmbeddingResponse
from memoryTechniques.queueMemory import getQueueResponse
from memoryTechniques.allMessages import getAllResponse
from memoryTechniques.blockSummary import getBlockResponse
from ratePairs import getRating
from createDirectories import createDirectories

# Define the function to get a response for a given input
# def getResponse(inputText):
#     # Replace this with your implementation of generating a response
#     response = "AI response"
#     return response

createDirectories()

responseTypes = {'block': getBlockResponse, 'all': getAllResponse, 'queue': getQueueResponse, 'embed': getEmbeddingResponse}

# getResponse = responseTypes['block']

for key, value in responseTypes.items():
    folder = key + '/'
    getResponse = value


    # Read input from 'convoInput.txt' and store it in a list
    filename = 'chatGPT'

    inputList = []
    with open('input/' + filename + '.txt', 'r') as inputFile:
        inputList = inputFile.read().splitlines()

    # Initialize an empty list to store input and response pairs
    conversations = []
    ratings = []
    prompts = []
    addedRatings = {}


    totalTime = 0
    totalScore = 0

    # Process each input and get responses
    for inputText in inputList:
        startTime = time.time()
        response, prompt = getResponse(inputText)
        endTime = time.time()
        conversations.extend(["<USER>" + inputText, "<AI>" + response])

        rating = getRating(user=inputText, ai=response)
        ratings.append(rating)

        for k in rating:
            if k in addedRatings:
                addedRatings[k] += rating[k]
            else:
                addedRatings[k] = rating[k]

        prompts.append(prompt)

        totalScore += sum(rating.values())
        totalTime += (endTime - startTime)

    # Write the input and response pairs to 'convoOutput.txt'
    with open('output/' + folder + 'convo/' + filename + 'Convo.txt', 'w') as outputFile:
        for line in conversations:
            outputFile.write(line + '\n')

    with open('output/' + folder + 'rating/' + filename + 'Rating.txt', 'w') as ratingFile:
        for r in ratings:
            ratingFile.write(str(r) + '\n')

    with open('output/' + folder + 'prompt/' + filename + 'Prompt.txt', 'w') as promptFile:
        for p in prompts:
            promptFile.write(str(p) + '\n')

    with open('output/' + folder + 'summary/' + filename + 'Summary.txt', 'w') as summaryFile:
        summaryFile.write('Number of inputs: {}\n'.format(len(inputList)))
        summaryFile.write('Average Response Time: {}\n'.format(totalTime / len(inputList)))
        summaryFile.write('Average Total Score: {} of 20\n'.format(totalScore / len(inputList)))

        summaryFile.write('Total Ratings: {}\n'.format(str(addedRatings)))
        for criteria in addedRatings:
            addedRatings[criteria] /= len(inputList)

        summaryFile.write('Average Ratings: {}\n'.format(str(addedRatings)))

        # for prompt in prompts:
        #     summaryFile.write(str(line) + '\n')

    # Print input and response
    # for i in range(0, len(conversations), 2):
    #     print(conversations[i])  # USER
    #     print(conversations[i + 1])  # AI
    #     print()

    print(folder, 'Complete')

    # print("Conversations saved")
    print('Average Response Time: {}'.format(totalTime / len(inputList)))
    print('Average Response Score: {} of 20'.format(totalScore / len(inputList)))
    print()
