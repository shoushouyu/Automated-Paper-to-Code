import openai
import json


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_to_txt_file(output_path, content):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)

def generate_code_framework(template, content):

    
    prompt = read_file('prompt/design/code_framework.md')
    

    
    prompt = prompt.replace("{template}", template).replace("{content}", content)

    
 
    response = openai.ChatCompletion.create(
        model="gpt-4o",  
        messages=[
            {"role": "system", "content": "You need to use ResNet-18 without pretrained and CIFAR10 dataset."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=3000,
        temperature=0.0
    )
    
    usage_info = response['usage']
    prompt_tokens = usage_info['prompt_tokens']
    completion_tokens = usage_info['completion_tokens']
    total_tokens = usage_info['total_tokens']
    print(f"Prompt tokens: {prompt_tokens}, Completion tokens: {completion_tokens}, Total tokens: {total_tokens}")

    
    return response['choices'][0]['message']['content']


def framework_refinement_step1(content, code_structure):

    
    prompt = read_file('prompt/design/overall_design.md')

   
    prompt = prompt.replace("{content}", content).replace("{code_structure}", code_structure)
    

    
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=6000,
        temperature=0.0
    )
    
    usage_info = response['usage']
    prompt_tokens = usage_info['prompt_tokens']
    completion_tokens = usage_info['completion_tokens']
    total_tokens = usage_info['total_tokens']
    print(f"Prompt tokens: {prompt_tokens}, Completion tokens: {completion_tokens}, Total tokens: {total_tokens}")

    
    return response['choices'][0]['message']['content']



def framework_refinement_step3(code_structure):

    
    prompt = read_file('prompt/design/import.md')

    
    prompt = prompt.replace("{code_structure}", code_structure)

   
    
    response = openai.ChatCompletion.create(
        model="gpt-4o", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=6000,
        temperature=0.0
    )
    
    usage_info = response['usage']
    prompt_tokens = usage_info['prompt_tokens']
    completion_tokens = usage_info['completion_tokens']
    total_tokens = usage_info['total_tokens']
    print(f"Prompt tokens: {prompt_tokens}, Completion tokens: {completion_tokens}, Total tokens: {total_tokens}")

   
    return response['choices'][0]['message']['content']

def trans_md_json(md_path):

    
    md_content = read_file(md_path)

    
    prompt = read_file('prompt/design/trans_md_json.md')

   
    prompt = prompt.replace("{md_content}", md_content)

    
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=6000,
        temperature=0.0
    )
    
    usage_info = response['usage']
    prompt_tokens = usage_info['prompt_tokens']
    completion_tokens = usage_info['completion_tokens']
    total_tokens = usage_info['total_tokens']
    print(f"Prompt tokens: {prompt_tokens}, Completion tokens: {completion_tokens}, Total tokens: {total_tokens}")

    return response['choices'][0]['message']['content']




def main():
    
    template_path = 'prompt/design/repo_template.txt'
    content_path = 'markdown_files/paper.md'
    output_path = 'markdown_files/step_markdown/paper'
    
    template = read_file(template_path)
    content = read_file(content_path)

    
    initial_code_structure = generate_code_framework(template, content)
    write_to_txt_file(output_path + '/code_structure.md', initial_code_structure)
    
    
    initial_code_structure = read_file(output_path + '/code_structure.md')
    
    
    optimized_code_structure_step1 = framework_refinement_step1(content, initial_code_structure)
    write_to_txt_file(output_path + '/optimized_code_structure_step1.md', optimized_code_structure_step1)

   
    optimized_code_structure_step1 = read_file(output_path + '/optimized_code_structure_step1.md')

    optimized_code_structure_step3 = framework_refinement_step3(optimized_code_structure_step1)
    write_to_txt_file(output_path + '/optimized_code_structure_step3.md', optimized_code_structure_step3)
    
    md_path = 'data/markdown_files/step_markdown/2411.18388/optimized_code_structure_step3.md'
    json_output = trans_md_json(md_path)
    write_to_txt_file(output_path + '/optimized_code_structure_step3.json', json_output)

if __name__ == "__main__":
    main()
