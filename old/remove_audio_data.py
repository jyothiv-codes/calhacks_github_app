import re
import json

def remove_data_key_from_file(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()  # Read the entire content of the file

    # Regular expression to match `'data': <value>` patterns
    cleaned_content = re.sub(r"'data':\s*'[^']*'", '', content)

    # Optionally, remove any trailing commas left behind by the removal
    cleaned_content = re.sub(r",\s*}", '}', cleaned_content)

    with open(output_file, 'w') as file:
        file.write(cleaned_content)  # Write the modified content to a new file

    print(f"Cleaned content saved to {output_file}")

# Usage
input_file = 'audio_responses_log.txt'   # Replace with the path to your input file
output_file = 'audio_responses_cleaned.txt' # Replace with the desired output file path

remove_data_key_from_file(input_file, output_file)
