import os
import openai

def analyze_function_content(file_content):

    prompt = f"""Analyze the following Python file content. For each global function (not inside any class), your answer only provide:
1. Function name.
2. Specific implementation details of the function.

Do not analyze any classes or functions defined within classes.If there is no global function in file content, your answer should be None.

Python file content:
{file_content}
"""


    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0.0
    )
    
    return response['choices'][0]['message']['content']

def process_python_file(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    
    if "def " in file_content:
        
        result = analyze_function_content(file_content)
        return result
    else:
        return None

def analyze_functions_in_repo(repo_path, repo_name, output_file):

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, repo_path)  
                full_path = f"{repo_name}/{relative_path}" 
                print(f"Analyzing file: {full_path}")
                
          
                analysis_result = process_python_file(file_path)
                
                if analysis_result and analysis_result.split()[0] != "None":  
                    output_file.write(f"File: {full_path}\n")  
                    output_file.write(f"Analysis:\n{analysis_result}\n\n")
                else:
                    pass
                    #output_file.write(f"File: {full_path} contains no functions.\n\n")



def analyze_functions_in_results(results_folder, repos_root, output_dir):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for result_file in os.listdir(results_folder):
        if result_file.endswith('_class_analysis.txt'):
            result_file_path = os.path.join(results_folder, result_file)
            repo_folder_name = result_file.split('_')[0]  
            repo_path = os.path.join(repos_root, repo_folder_name)

            if os.path.exists(repo_path):
                output_file_path = os.path.join(output_dir, f"{repo_folder_name}_function_analysis.txt")
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(f"Function analysis for repository: {repo_folder_name}\n\n")
                    
                    
                    analyze_functions_in_repo(repo_path, repo_folder_name, output_file)
                
                print(f"Analysis for repository {repo_folder_name} saved to {output_file_path}")
            else:
                print(f"Repository folder {repo_folder_name} not found in {repos_root}")



if __name__ == "__main__":
    results_folder = 'class_analysis_results_1'
    repos_root = 'downloaded_github_repos'
    output_dir = 'function_analysis_results'
    
    analyze_functions_in_results(results_folder, repos_root, output_dir)
