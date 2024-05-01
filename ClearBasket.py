def clear_file(file_path):
    try:
        # Open the file in write mode ('w') to clear its contents
        with open(file_path, 'w') as file:
            file.truncate(0)  # Truncate the file to remove its contents
        print(f"The file '{file_path}' has been cleared.")
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Provide the path to the file you want to clear
file_path = 'Logs/GenerateBasket.txt'  # Replace with your file path

clear_file(file_path)
