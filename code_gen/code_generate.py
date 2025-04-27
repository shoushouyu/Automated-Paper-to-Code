import os
import openai
import re
import json

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def save_generated_code(file_path, code):

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(code)

def send_to_model(prompt):
    messages = [
        {"role": "user", "content": "You are a Python code implementation expert.\n\n" + prompt}
    ]
    
    try:

        response = openai.ChatCompletion.create(
            model="o1-mini",  # 或 "o1-mini"
            messages=messages,
            max_completion_tokens=8000
        )
 
        usage_info = response['usage']
        prompt_tokens = usage_info['prompt_tokens']
        completion_tokens = usage_info['completion_tokens']
        total_tokens = usage_info['total_tokens']
        print(f"Prompt tokens: {prompt_tokens}, Completion tokens: {completion_tokens}, Total tokens: {total_tokens}")
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

def generate_prompt(prompt_template, paper_content, python_file_content, whole_design):

    prompt = prompt_template.replace("{paper_content}", paper_content)
    prompt = prompt.replace("{python_file_content}", python_file_content)
    prompt = prompt.replace("{whole_design}", whole_design)
    return prompt

def extract_python_code(response):

    match = re.search(r'```python\n(.*?)\n```', response, re.DOTALL)
    if match:
        return match.group(1).strip()  
    else:
        return None

def process_files(merged_json_path, paper_path, prompt_file_path, output_directory):

    paper_content = read_file(paper_path)
    

    prompt_template = read_file(prompt_file_path)


    with open(merged_json_path, 'r', encoding='utf-8') as f:
        merged_data = json.load(f)

    merged_data_copy = merged_data.copy()


    for key, file_design_content in merged_data.items():

        if not isinstance(file_design_content, dict) or "file_name" not in file_design_content:
            print(f"Skipping {key} because 'file_name' field not found or content is not a dict.")
            continue


        output_file_path = os.path.join(output_directory, file_design_content["file_name"])


        python_file_content = json.dumps(file_design_content, ensure_ascii=False, indent=4)
        merged_data_str = json.dumps(merged_data_copy, ensure_ascii=False, indent=4)
        
        prompt = generate_prompt(prompt_template, paper_content, python_file_content, merged_data_str)
        
        write_file("/home/lzj/code_for_run/paper2code/test.py", prompt)

        
        response = send_to_model(prompt)

        if response:
           
            python_code = extract_python_code(response)

            if python_code:
                
                save_generated_code(output_file_path, python_code)
                print(f"Response for {key} saved to {output_file_path}")
                
                
                merged_data_copy[key] = python_code
            else:
                print(f"No Python code found in the response for {key}")
        else:
            print(f"Error processing {key}")


if __name__ == "__main__":

    merged_json_path = "iter_code/paper/merged_output.json"
    paper_path = "markdown_files/output_summarized_papers/paper.md"
    prompt_file_path = "prompt/code/code_gen.md"
    output_directory = "iter_code/paper/code_generate"


    process_files(merged_json_path, paper_path, prompt_file_path, output_directory)

