import pandas as pd

performanceTable = pd.DataFrame([])

run = {'technique': 'j', 'topic': 'test', 'dialog length': 8,
       'average input size': 8}

addedRatings = {'a':3, 'b':5}

run.update(addedRatings)

runPanda = pd.DataFrame([run])

performanceTable = pd.concat([performanceTable, runPanda], ignore_index=True)
print(performanceTable)
