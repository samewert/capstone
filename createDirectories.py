import os

def createDirectories():
    # Define the main directory name
    main_directory = 'output'

    # Define the subdirectories
    subdirectories = ['all', 'block', 'embed', 'queue']

    # Create the main directory
    os.makedirs(main_directory, exist_ok=True)

    # Create subdirectories within the main directory
    for subdirectory in subdirectories:
        subdirectory_path = os.path.join(main_directory, subdirectory)
        os.makedirs(subdirectory_path, exist_ok=True)

        # Create sub-subdirectories within each subdirectory
        subsubdirectories = ['convo', 'rating', 'prompt', 'summary']
        for subsubdirectory in subsubdirectories:
            subsubdirectory_path = os.path.join(subdirectory_path, subsubdirectory)
            os.makedirs(subsubdirectory_path, exist_ok=True)

    print("Directory structure created successfully.")