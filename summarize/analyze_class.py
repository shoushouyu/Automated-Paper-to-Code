import os
import openai


def analyze_class_content(file_content):

    prompt = f"""Analyze the following Python file content. For each class, provide:
1. Class name.
2. Specific implementation details of the class.

If there are no classes, skip the analysis.

Python file content:
{file_content}
"""


    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.2
    )
    
    return response['choices'][0]['message']['content']

def process_python_file(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    
    if "class " in file_content:
        
        result = analyze_class_content(file_content)
        return result
    else:
        return None

def analyze_classes_in_repos(repos_root, output_dir):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for repo in os.listdir(repos_root):
        repo_path = os.path.join(repos_root, repo)
        if os.path.isdir(repo_path):
            analysis_file_path = os.path.join(output_dir, f"{repo}_class_analysis.txt")
            with open(analysis_file_path, 'w', encoding='utf-8') as analysis_file:
                analysis_file.write(f"Analysis results for repository: {repo}\n\n")
                
                for root, dirs, files in os.walk(repo_path):
                    for file in files:
                        if file.endswith('.py'):
                            file_path = os.path.join(root, file)
                            relative_path = os.path.relpath(file_path, repos_root)  
                            print(f"Analyzing file: {relative_path}")
                            
                            
                            analysis_result = process_python_file(file_path)
                            
                            if analysis_result:
                               
                                analysis_file.write(f"File: {relative_path}\n")  
                                analysis_file.write(f"Analysis:\n{analysis_result}\n\n")
                
                print(f"Analysis for repository {repo} saved to {analysis_file_path}")



if __name__ == "__main__":
    repos_root = 'downloaded_github_repos'
    output_dir = 'class_analysis_results_1'
    
    analyze_classes_in_repos(repos_root, output_dir)
