import json
import os
import openai

def read_json(file_path):

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(file_path, data):

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def call_model_to_update(merged_content_str, current_key, current_value, prompt_template_path):

    prompt_template = read_file(prompt_template_path)

    user_prompt = prompt_template.replace("{merged_content}", merged_content_str) \
                                 .replace("{current_key}", current_key) \
                                 .replace("{current_value}", json.dumps(current_value, ensure_ascii=False, indent=4))
    
    write_file("class_design/user_prompt.md", user_prompt)

    messages = [
        {"role": "system", "content": "You are a Python code reviewer who ensures the correctness of file design JSON."},
        {"role": "user", "content": user_prompt}
    ]

    try:

        response = openai.ChatCompletion.create(
            model="gpt-4o", 
            messages=messages,
            max_tokens=15000,
            temperature=0.0
        )

        usage_info = response['usage']
        prompt_tokens = usage_info['prompt_tokens']
        completion_tokens = usage_info['completion_tokens']
        total_tokens = usage_info['total_tokens']
        print(f"Prompt tokens: {prompt_tokens}, Completion tokens: {completion_tokens}, Total tokens: {total_tokens}")
        updated_content_str = response['choices'][0]['message']['content'].strip()

    
        write_file("class_design/updated_content.md", updated_content_str)


        updated_content_str = updated_content_str.replace("```json", "")
        updated_content_str = updated_content_str.replace("```", "")

        updated_content_str = updated_content_str.strip()


        if updated_content_str.startswith("[") and updated_content_str.endswith("]"):

            updated_content_str = updated_content_str[1:-1].strip()

        updated_content = json.loads(updated_content_str)

        return updated_content

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for {current_key}: {e}. Skipping update.")
        return current_value 
    except Exception as e:
        print(f"Error calling model for {current_key}: {e}")
        return current_value 

def process_merged_output(merged_json_path, prompt_template_path):


    merged_data = read_json(merged_json_path)

    keys = list(merged_data.keys())

    for key in keys:
        current_value = merged_data[key]


        merged_content_str = json.dumps(merged_data, ensure_ascii=False, indent=4)


        updated_value = call_model_to_update(merged_content_str, key, current_value, prompt_template_path)

        merged_data[key] = updated_value


        write_json(merged_json_path, merged_data)

        print(f"Updated content for {key} saved.")

if __name__ == "__main__":

    merged_output_path = "merged_output.json"  
    prompt_template_path = "last_modified.md"  


    process_merged_output(merged_output_path, prompt_template_path)
