import os
import openai

def analyze_file(file_content):

    prompt = f"""As a code summarizer, your task is to summarize the functionality and detailed implementation of the following Python file. The goal is to explain how this file works, including key steps and logic, so that others can reproduce its functionality. Focus on describing the workflow, the roles of key components, and how they come together to achieve the file's purpose.

Python file content:
{file_content}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.0
    )

    return response['choices'][0]['message']['content']


def process_python_file(file_path, repo_name, output_file):

    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    analysis_result = analyze_file(file_content)
    
   
    relative_path = os.path.relpath(file_path, repo_name)

    
    output_file.write(f"File: {relative_path}\n")
    output_file.write(f"Analysis:\n{analysis_result}\n\n")

    
    return analysis_result


def contains_python_files(folder_path):

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                return True
    return False


def recursive_analyze_folder(folder_path, repo_name, output_file):

    folder_analysis = []
    py_file_analysis = []

   
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if file.endswith('.py'):
            relative_path = os.path.relpath(file_path, repo_name) 
            print(f"Analyzing file: {relative_path}")
            
            
            analysis_result = process_python_file(file_path, repo_name, output_file)
            py_file_analysis.append(f"File: {relative_path}\nPurpose:\n{analysis_result}\n\n")

   
    for dir_name in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, dir_name)
        if os.path.isdir(subfolder_path) and contains_python_files(subfolder_path):  
            subfolder_analysis = recursive_analyze_folder(subfolder_path, repo_name, output_file)
            if subfolder_analysis:
                relative_subfolder_path = os.path.relpath(subfolder_path, repo_name)  
                py_file_analysis.append(f"Folder: {relative_subfolder_path}\nSummary:\n{subfolder_analysis}\n\n")
    
    
    if py_file_analysis:
        folder_prompt = " ".join(py_file_analysis)
        folder_summary = summarize_folder(folder_prompt)
        
        
        relative_folder_path = os.path.relpath(folder_path, repo_name)
        
        
        output_file.write(f"Folder: {relative_folder_path}\nSummary:\n{folder_summary}\n\n")
        folder_analysis.append(f"Folder: {relative_folder_path}\nSummary:\n{folder_summary}\n\n")

    return " ".join(folder_analysis)


def summarize_folder(content):

    prompt = f"""A brief but complete explanation of what this folder does is provided by the description of the subfolders and.py files under this folder.

Content:
{content}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.0
    )

    return response['choices'][0]['message']['content']


def analyze_repo(repo_path, repo_name, output_dir):

    output_file_path = os.path.join(output_dir, f"{repo_name}_analysis.txt")
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f"Repository analysis for: {repo_name}\n\n")
        folder_summary = recursive_analyze_folder(repo_path, repo_name, output_file)
        if folder_summary:
            output_file.write(f"Final Repository Summary:\n{folder_summary}\n")


def analyze_all_repos(results_folder, repos_root, output_dir):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    
    for result_file in os.listdir(results_folder):
        if result_file.endswith('_class_analysis.txt'):
            repo_folder_name = result_file.split('_')[0] 
            repo_path = os.path.join(repos_root, repo_folder_name)

            
            if os.path.exists(repo_path) and contains_python_files(repo_path):
                analyze_repo(repo_path, repo_folder_name, output_dir)
                print(f"Analysis for repository {repo_folder_name} saved.")
            else:
                print(f"Repository folder {repo_folder_name} not found or contains no Python files in {repos_root}")



if __name__ == "__main__":
    results_folder = 'class_analysis_results_1'
    repos_root = 'downloaded_github_repos'
    output_dir = 'repo_analysis_results'
    
    analyze_all_repos(results_folder, repos_root, output_dir)
