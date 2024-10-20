import re
import json
import pandas as pd

def parse_messages_from_file(input_file):
    # Read the entire content from the input file
    with open(input_file, 'r') as f:
        raw_data = f.read()

    # Enhanced regex pattern to capture more complex JSON structures
    pattern = re.compile(r'(\d+\.\d+)\s+-\s+Received message:\s+({.*?})(?=\d+\.\d+\s+-|$)', re.DOTALL)

    # Find all matches of the pattern
    matches = pattern.findall(raw_data)

    # List to store structured data
    structured_data = []

    # Loop through matches and parse JSON content
    for timestamp, message_json in matches:
        try:
            # Convert the string message to a valid JSON object
            message_dict = json.loads(message_json.replace("'", '"'))
            # Add the timestamp as a separate field
            message_dict['timestamp'] = float(timestamp)
            # Store the structured data
            structured_data.append(message_dict)
        except json.JSONDecodeError as e:
            print(f"Skipping a message due to JSON decoding error: {e}")

    return structured_data

def save_to_csv_and_json(structured_data, csv_file, json_file):
    # Convert the structured data to a DataFrame
    df = pd.DataFrame(structured_data)

    # Save the DataFrame to CSV for SingleStore
    df.to_csv(csv_file, index=False)

    # Save the DataFrame to JSON for ChromaDB
    df.to_json(json_file, orient='records', indent=4)

    print(f"Data saved to {csv_file} and {json_file}")

# Main execution
if __name__ == "__main__":
    input_file = 'audio_responses_cleaned.txt'  # Replace with your .txt file path
    csv_file = 'structured_data.csv'
    json_file = 'structured_data.json'

    # Parse messages from the input file
    structured_data = parse_messages_from_file(input_file)

    # Save the structured data
    save_to_csv_and_json(structured_data, csv_file, json_file)
