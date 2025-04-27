import json
import openai  
import os
import re


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_to_txt_file(output_path, content):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)


def save_data(json_file_path, data):
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def generate_design_from_json(json_file_path, design_file_path, output_directory):

    
    with open(design_file_path, 'r', encoding='utf-8') as f:
        class_design = json.load(f)

    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    
    i = 1

    
    for key, details in data.items():
        
        content = read_file("markdown_files/output_summarized_papers/paper.md")
        

        
        user_prompt = read_file("prompt/design/class_design.md")

 
        details_str = json.dumps(details, ensure_ascii=False)
        data_str = json.dumps(data, ensure_ascii=False)

    
        user_prompt = user_prompt.replace("{current_file}", details_str).replace("{file_design}", data_str).replace("{content}", content)


        messages = [
            {"role": "user", "content": user_prompt}
        ]
    
        try:
            
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=6000,
                temperature=0.0
            )
            usage_info = response['usage']
            prompt_tokens = usage_info['prompt_tokens']
            completion_tokens = usage_info['completion_tokens']
            total_tokens = usage_info['total_tokens']
            print(f"Prompt tokens: {prompt_tokens}, Completion tokens: {completion_tokens}, Total tokens: {total_tokens}")           
        except Exception as e:
            print(f"Error generating code for {key}: {e}")
            continue

    
        generated_code = response['choices'][0]['message']['content']

       
        try:
            
            updated_details = json.loads(generated_code)
            data[key] = updated_details
        except json.JSONDecodeError:
            data[key]['implementation'] = generated_code

        
        base_name, extension = os.path.splitext(key)
        output_file_path = f"{output_directory}/{base_name}_{i}{extension}"

      
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
  
            output_file.write(generated_code)
          
        print(f"Generated code saved to {output_file_path}")

        
        i += 1

        
        save_data(json_file_path, data)

    


generate_design_from_json(
    "markdown_files/step_markdown/paper/optimized_code_structure_step3.json",
    "markdown_files/step_markdown/paper/optimized_code_structure_step3.json",
    "iter_code/paper/design_generated"
)
