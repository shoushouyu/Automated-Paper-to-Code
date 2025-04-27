import os
import json
import openai
import re
import io
import tokenize
from volcenginesdkarkruntime import Ark

def write_file(file_path, content):

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def read_files_from_dir(root_dir, extensions=(".py", ".json")):

    file_contents = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(extensions):
                full_path = os.path.join(dirpath, filename)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    file_contents[full_path] = content
                except Exception as e:
                    print(f"read file {full_path} error: {e}")
    return file_contents

def read_markdown_file(md_file_path):

    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"read file {md_file_path} error: {e}")
        return ""



def construct_prompt(paper_content, files_content):


    file_contents_str = ""
    for path, content in files_content.items():
        file_contents_str += f"file_path: {path}\ncontent:\n{content}\n{'-'*60}\n"

    prompt = f"""Please evaluate whether the following file content correctly implements the requirements outlined in the paper. In particular, carefully assess the internal implementation concerning model design, loss function design, and model updating. If any issues are found in the file content, please return the corrected complete code for the corresponding file. The output must follow the format: filename + file content, and it should be enclosed within a Python code block.

Paper content:
{'='*80}
{paper_content}
{'='*80}

File content:
{'='*80}
{file_contents_str}
{'='*80}
"""

    return prompt

def remove_comments_and_docstrings(source):

    io_obj = io.BytesIO(source.encode('utf-8'))
    output_tokens = []
    prev_toktype = tokenize.INDENT
    try:
        for token in tokenize.tokenize(io_obj.readline):
            token_type = token.type
            token_string = token.string
        
            if token_type == tokenize.COMMENT:
                continue
            
            if token_type == tokenize.STRING and prev_toktype in (tokenize.INDENT, tokenize.NEWLINE):
                if token_string.startswith('"""') or token_string.startswith("'''"):
                    continue
            output_tokens.append(token)
            prev_toktype = token_type
    except tokenize.TokenError:
       
        return source
    new_source = tokenize.untokenize(output_tokens).decode('utf-8')
    return new_source

if __name__ == "__main__":
    
    code_dir = "iter_code/paper/code_generate"
    paper_md_path = "markdown_files/output_summarized_papers/paper.md"
    
    

    files_content = read_files_from_dir(code_dir, extensions=(".py", ".json"))
    

    for file_path, content in files_content.items():
        if file_path.endswith('.py'):
            #files_content[file_path] = remove_comments_and_docstrings(content)
            files_content[file_path] = content
    

    paper_content = read_markdown_file(paper_md_path)
    

    prompt_text = construct_prompt(paper_content, files_content)
    

    write_file("test.py", prompt_text)
    

    messages = [
        {
            "role": "user",
            "content": prompt_text
        }
    ]

    response = openai.ChatCompletion.create(
        model="o1-mini",  
        messages=messages,
        max_completion_tokens=16000
    )

    
    usage_info = response['usage']
    prompt_tokens = usage_info['prompt_tokens']
    completion_tokens = usage_info['completion_tokens']
    total_tokens = usage_info['total_tokens']
    print(f"Prompt tokens: {prompt_tokens}, Completion tokens: {completion_tokens}, Total tokens: {total_tokens}")

    response_content = response['choices'][0]['message']['content']
    write_file("test_1.py", json.dumps(response_content))
