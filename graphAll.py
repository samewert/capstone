import pandas as pd
import matplotlib.pyplot as plt
import os

# Replace 'your_data.csv' with the actual file path or DataFrame variable
file_path = 'output/performanceTable.csv'
df = pd.read_csv(file_path)

# Define a dictionary to map each technique to a color
technique_colors = {
    'all': 'red',
    'queue': 'blue',
    'block': 'green',
    'embed': 'purple'
}

# Create a scatter plot with color-coded techniques
# plt.figure(figsize=(10, 6))

# plt.ylim(3, 5)
plt.ylim(1, 4)
# plt.ylim(2, 4)

for technique, color in technique_colors.items():
    subset_df = df[df['technique'] == technique]
    # plt.plot(subset_df['average input size'], subset_df['average response time'], label=technique, color=color, alpha=0.5)

    # plt.scatter(subset_df['dialog length'], subset_df['average total score'], label=technique, color=color, alpha=0.5)

    plt.bar(technique, (subset_df['average response time'].mean()), color=color)
    # plt.bar(technique, (subset_df['average total score'].mean() - subset_df['question-asking'].mean())/3, color=color)


    print(technique)
    print('Average Response Time:', subset_df['average response time'].mean())
    print('Average Total Score (out of 20):', subset_df['average total score'].mean())
    print('Mirroring:', subset_df['mirroring'].mean())
    print('Specificity:', subset_df['specificity'].mean())
    print('Response-Relatedness:', subset_df['response-relatedness'].mean())
    print('Question-asking:', subset_df['question-asking'].mean())

    print('Total:', subset_df['mirroring'].mean() + subset_df['specificity'].mean() + subset_df['response-relatedness'].mean() + subset_df['question-asking'].mean())
    print('Total w/o q-a:',
          subset_df['mirroring'].mean() + subset_df['specificity'].mean() + subset_df['response-relatedness'].mean())

# Add labels and title
# plt.xlabel('Average Input Size')
plt.xlabel('Technique')
# plt.ylabel('Average Total Score')
plt.ylabel('Average Response Time')
# plt.title('Average Input Size vs Average Response Time (All Data)')
# plt.title('Dialog Length vs Average Total Score (All Data)')
plt.title('Average Response Time')


# Add legend

# plt.legend(title='Technique')

# Create 'graphs' folder if it doesn't exist
output_folder = 'graphs'
os.makedirs(output_folder, exist_ok=True)

# Save the plot to the 'graphs' folder
output_filename = "all_data_average_input_size_vs_response_time.png"
output_path = os.path.join(output_folder, output_filename)
plt.savefig(output_path)

# Display the plot
plt.show()
