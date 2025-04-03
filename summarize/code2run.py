import os
import openai


analysis_results_path = 'analysis_results'
repo_analysis_results_path = 'repo_analysis_results'
class_analysis_results_path = 'class_analysis_results_1'
function_analysis_results_path = 'function_analysis_results'
output_dir = 'repo_summaries'

def read_analysis_file(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_paper_repo_structure(paper_id):

    paper_structure_path = os.path.join(analysis_results_path, f"{paper_id}_analysis.csv")
    if os.path.exists(paper_structure_path):
        return read_analysis_file(paper_structure_path)
    else:
        return f"No structure information found for paper: {paper_id}"

def extract_py_file_flow(paper_id):

    paper_repo_flow_path = os.path.join(repo_analysis_results_path, f"{paper_id}_analysis.txt")
    if os.path.exists(paper_repo_flow_path):
        return read_analysis_file(paper_repo_flow_path)
    else:
        return f"No repo analysis found for paper: {paper_id}"

def extract_class_analysis(paper_id):

    paper_class_analysis_path = os.path.join(class_analysis_results_path, f"{paper_id}_class_analysis.txt")
    if os.path.exists(paper_class_analysis_path):
        return read_analysis_file(paper_class_analysis_path)
    else:
        return f"No class analysis found for paper: {paper_id}"

def extract_function_analysis(paper_id):

    paper_function_analysis_path = os.path.join(function_analysis_results_path, f"{paper_id}_function_analysis.txt")
    if os.path.exists(paper_function_analysis_path):
        return read_analysis_file(paper_function_analysis_path)
    else:
        return f"No function analysis found for paper: {paper_id}"

def call_gpt_summary(paper_info):

    prompt = f"Based on the following information from a paper, summarize the process of constructing a repository from four aspect: repository statistic pattern, repository construction, class and function abstraction, components interaction. You are able to summarize other features:\n\n{paper_info}"
    
 
    if len(prompt) > 200000: 
        prompt = prompt[:200000]

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.2
    )
    
    return response['choices'][0]['message']['content']

def call_gpt_summary_all(paper_info):
   
    prompt = f"I am now a student who has to write code for a thesis. According to the repository summary of the following ten papers, the overall process of building a repository for a new paper is summarized:\n\n{paper_info}"
    
    
    if len(prompt) > 200000:  
        prompt = prompt[:200000]

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.2
    )
    
    return response['choices'][0]['message']['content']

def save_summary_to_file(paper_id, summary, final=False):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    file_name = f"{paper_id}_summary.txt" if not final else "final_summary.txt"
    file_path = os.path.join(output_dir, file_name)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(summary)

def summarize_repo_construction():
    
    paper_ids = [file.split('_')[0] for file in os.listdir(analysis_results_path) if file.endswith('_analysis.csv')]
    all_paper_info = []

    print("Gathering information to summarize each paper's repo construction process...\n")
    
    for paper_id in paper_ids:
        paper_info = f"### Paper: {paper_id} ###\n"
        
        
        structure_info = extract_paper_repo_structure(paper_id)
        paper_info += "1. Repository Structure:\n" + structure_info + "\n"
        
        
        repo_flow_info = extract_py_file_flow(paper_id)
        paper_info += "2. Purpose and Flow of .py files:\n" + repo_flow_info + "\n"
        
        
        class_info = extract_class_analysis(paper_id)
        paper_info += "3. Class Analysis:\n" + class_info + "\n"
        
        
        function_info = extract_function_analysis(paper_id)
        paper_info += "4. Function Analysis:\n" + function_info + "\n"
        
        
        print(f"Summarizing repo construction process for paper: {paper_id}...\n")
        paper_summary = call_gpt_summary(paper_info)
        all_paper_info.append(paper_summary)

        
        save_summary_to_file(paper_id, paper_summary)

    
    combined_info = "\n".join(all_paper_info)

   
    print("Summarizing the overall process of constructing a repository for all papers...\n")
    final_summary = call_gpt_summary_all(combined_info)
    
    
    save_summary_to_file("combined", final_summary, final=True)
    
    print("### Final Summary of Repo Construction Process ###\n")
    print(final_summary)


if __name__ == "__main__":
    summarize_repo_construction()
