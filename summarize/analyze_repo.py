import os
import csv

def analyze_codebase(start_path='.'):
    folder_info = {}
    specific_folders = ['model', 'data_loader', 'train', 'scripts']

    for dirpath, dirnames, filenames in os.walk(start_path):
  
        py_files = [f for f in filenames if f.endswith('.py')]
        
        if py_files:  
            relative_path = os.path.relpath(dirpath, start_path)
            folder_info[relative_path] = {
                'py_file_count': len(py_files),
                'py_files': py_files
            }
            
            
            folder_name = os.path.basename(dirpath)
            if folder_name in specific_folders:
                print(f'Directory: {relative_path}')
                print(f'    Number of .py files: {len(py_files)}')
                for file in py_files:
                    print(f'        File: {file}')
                print()

    return folder_info

def save_analysis_to_csv(analysis_data, output_csv_path):
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Directory', 'Number of .py files', 'Files']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for folder, info in analysis_data.items():
            writer.writerow({
                'Directory': folder,
                'Number of .py files': info['py_file_count'],
                'Files': ', '.join(info['py_files'])
            })

def analyze_github_repos(repos_root, output_dir):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    
    github_folders = [f for f in os.listdir(repos_root) if os.path.isdir(os.path.join(repos_root, f))]

    for repo_folder in github_folders:
        repo_path = os.path.join(repos_root, repo_folder)
        print(f"Analyzing GitHub repo: {repo_folder}")
        
        
        analysis_data = analyze_codebase(repo_path)
        
        
        output_csv_path = os.path.join(output_dir, f"{repo_folder}_analysis.csv")
        save_analysis_to_csv(analysis_data, output_csv_path)

        print(f"Analysis for {repo_folder} saved to {output_csv_path}")


if __name__ == "__main__":
    
    repos_root = 'downloaded_github_repos'
    output_dir = 'analysis_results'

  
    analyze_github_repos(repos_root, output_dir)
