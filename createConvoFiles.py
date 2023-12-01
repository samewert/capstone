import os

file_path = 'JOY chats.txt'
output_file_counter = 1
messages = []
output_folder = 'input'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Opening the file in read mode
with open(file_path, 'r') as file:
    for line in file:
        cleaned_line = line.strip()

        # Skip blank or empty lines
        if not cleaned_line:
            continue

        # Convert the lines to lowercase for case-insensitive comparison
        lower_line = cleaned_line.lower()

        if lower_line.startswith("student:"):
            # Remove the "Student:" prefix and add to messages
            messages.append(cleaned_line[len("student:"):].strip())
        elif lower_line.startswith("joy:"):
            pass
        else:
            # Save the line to the output file if messages is not empty
            if messages:
                output_file_path = os.path.join(output_folder, f'input_{output_file_counter}.txt')
                with open(output_file_path, 'a') as output_file:
                    for message in messages:
                        output_file.write(message + '\n')
                    # output_file.write(cleaned_line + '\n')

                # Increment the output file counter
                output_file_counter += 1

                # Empty the messages list
                messages = []
