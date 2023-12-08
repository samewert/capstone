import pandas as pd
import matplotlib.pyplot as plt
import os

# Replace 'your_data.csv' with the actual file path or DataFrame variable
file_path = 'output/performanceTable.csv'
df = pd.read_csv(file_path)

# Replace 'input_1' with the specific technique you are interested in
topic = 'input_1'

# Filter the DataFrame for the specific technique
filtered_df = df[df['topic'] == topic]

# Define a dictionary to map each technique to a color
technique_colors = {
    'all': 'red',
    'queue': 'blue',
    'block': 'green',
    'embed': 'purple'
}

# Create a scatter plot with color-coded techniques
# plt.figure(figsize=(10, 6))
for technique, color in technique_colors.items():
    subset_df = filtered_df[filtered_df['technique'] == technique]
    plt.scatter(subset_df['average input size'], subset_df['average response time'], label=technique, color=color, alpha=0.5)

# Add labels and title
plt.xlabel('Average Input Size')
plt.ylabel('Average Response Time')
plt.title(f'Average Input Size vs Average Response Time (Topic: {topic})')  # Removed "Scatter Plot:"

# Add legend
plt.legend(title='Technique')

# Create 'graphs' folder if it doesn't exist
output_folder = 'graphs'
os.makedirs(output_folder, exist_ok=True)

# Save the plot to the 'graphs' folder
output_filename = f"{topic}_average_input_size_vs_response_time.png"
output_path = os.path.join(output_folder, output_filename)
plt.savefig(output_path)

# Display the plot
plt.show()
