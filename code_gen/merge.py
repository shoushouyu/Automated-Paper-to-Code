import os
import json
import re

def clean_json_content(content):
    """
    Cleans the JSON content by removing comments (e.g., lines starting with //).
    """
    # Remove single-line comments (e.g., // comment)
    cleaned_content = re.sub(r'//.*', '', content)
    # Optionally remove multi-line comments (e.g., /* comment */)
    cleaned_content = re.sub(r'/\*.*?\*/', '', cleaned_content, flags=re.DOTALL)
    return cleaned_content

def extract_json_from_file(file_path):
    """
    Extracts JSON content enclosed in ```json ... ``` from a given file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    json_blocks = []
    inside_json = False
    current_json = ""
    
    for line in content.splitlines():
        if line.strip() == "```json":
            inside_json = True
            current_json = ""
        elif line.strip() == "```" and inside_json:
            inside_json = False
            try:
                # Clean JSON content before parsing
                cleaned_json = clean_json_content(current_json)
                json_data = json.loads(cleaned_json)
                json_blocks.append(json_data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {file_path}: {e}. Skipping this block.")
        elif inside_json:
            current_json += line + "\n"
    
    return json_blocks

def extract_and_merge_json(directory, output_file):
    """
    Extracts JSON content from all .py files in the directory and merges into one JSON file
    with file names as keys and their corresponding JSON content as values.
    """
    merged_json = {}
    files_with_order = []

    for root, _, files in os.walk(directory):
        for file_name in files:
            
            if file_name.endswith((".py", ".json")):
      
                match = re.search(r'_(\d+)\.(py|json)$', file_name)
                if match:
                    file_order = int(match.group(1))  
                    file_path = os.path.join(root, file_name)  
                    files_with_order.append((file_order, file_path, file_name))

    # Sort files based on their numeric order
    files_with_order.sort(key=lambda x: x[0])

    # Process files in sorted order
    for _, file_path, file_name in files_with_order:
        extracted_json = extract_json_from_file(file_path)
        # Add the extracted content to the merged JSON dictionary
        merged_json[file_name] = extracted_json

    # Write the merged JSON to the output file
    with open(output_file, 'w', encoding='utf-8') as out_file:
        json.dump(merged_json, out_file, indent=4, ensure_ascii=False)
    print(f"Merged JSON written to {output_file}")

if __name__ == "__main__":
    # Directory containing the .py files
    input_directory = "iter_code/paper/design_generated"
    output_json_file = "iter_code/paper/merged_output.json"
    
    # Extract and merge JSON
    extract_and_merge_json(input_directory, output_json_file)
