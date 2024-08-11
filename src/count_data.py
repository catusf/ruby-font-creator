import json

# Path to the JSON file
json_file_path = 'src/data.json'

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Calculate the number of keys (number of dictionaries in the list)
num_keys = len(data)

# Create a set of 'codepoint'
codepoint_set = {item['codepoint'] for item in data}

# Output the results
print(f"Number of keys: {num_keys}")
print(f"Set of codepoints: {len(codepoint_set)}")
