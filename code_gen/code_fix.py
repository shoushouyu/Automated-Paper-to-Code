import os
import openai
import re
import json
import subprocess
from typing import Dict, List

def read_file(file_path):
    # Function to read file content with UTF-8 encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    # Function to write content to a file with UTF-8 encoding
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def extract_python_code(response):
    # Function to extract Python code between ```python``` code blocks
    match = re.search(r'```python\n(.*?)\n```', response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None

def run_main_py(target_directory):
    # Function to run main.py in the specified directory using CUDA device 2
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "2"
    process = subprocess.Popen(
        ["python", "main.py"],
        cwd=target_directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )
    stdout, stderr = process.communicate()
    return stdout, stderr, process.returncode

def run_fix_script(code_str, script_path="test.py"):
    # Function to write fix code to a temporary file and run it via subprocess
    write_file(script_path, code_str)
    process = subprocess.Popen(
        ["python", script_path],
        cwd="iter_code/paper/code_generate",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    return stdout, stderr, process.returncode

if __name__ == "__main__":
    # Set working directory and file path
    target_directory = "iter_code/paper/code_generate"
    action_code_path = os.path.join(target_directory, "main.py")

    # Read the summarized paper content
    paper_summary_path = "markdown_files/output_summarized_papers/paper.md"
    paper_summary_content = read_file(paper_summary_path)

    iteration = 0
    while True:
        iteration += 1
        print(f"--- Iteration {iteration} ---")

        # Run main.py
        stdout, stderr, returncode = run_main_py(target_directory)
        result = stdout + "\n" + stderr
        print("Execution result:", result)

        # If <code_done> is found, stop the loop
        if "<code_done>" in result:
            print("Code executed successfully. Stopping.")
            break

        # If execution fails, collect current .py and .json files
        current_files_info = []
        for root, dirs, files in os.walk(target_directory):
            for file in files:
                if file.endswith(".py") or file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    content = read_file(file_path)
                    relative_path = os.path.relpath(file_path, target_directory)
                    current_files_info.append(f"File: {relative_path}\nContent:\n{content}")
        current_context = "Here are the current files (including .py and .json):\n\n" + "\n\n".join(current_files_info)

        # Construct the error message and prompt
        error_msg = (
            f"The code execution encountered issues:\n{result}\n\n"
            "Please provide updated Python code that addresses the identified errors and ensures the program "
            "executes successfully without performance or functional anomalies.\n\n"
            "## Task Requirements\n"
            "### 1. **Identify and Fix Issues**\n"
            "- **Error Analysis:**\n"
            "  - Analyze the code thoroughly to identify all execution errors.\n"
            "  - Provide detailed explanations for each identified issue and the rationale for the proposed fixes.\n"
            "### 2. **Dimension and Compatibility Fixes**\n"
            "- Provide step-by-step explanations for resolving tensor dimension mismatches.\n"
            "- Include examples to clarify adjustments required for compatible operations.\n"
            "  Example:\n"
            "  - If encountering:\n"
            "    RuntimeError: mat1 and mat2 shapes cannot be multiplied (64x12544 and 4096x100),\n"
            "    detail how to reshape, transpose, or otherwise adjust tensors to resolve the issue.\n\n"
            "### 3. **File Modifications**\n"
            "- Define a write_to_file(path_to_file_to_be_changed, content) function to handle all file updates.\n"
            "- Use this function for every file modification, ensuring the full updated content is written to the file.\n\n"
            "### 4. **Code Formatting Requirements**\n"
            "- Enclose the entire response in a python code block.\n"
            "- Use single-line comments for all documentation and explanations.\n"
            "  Example:\n"
            "  python\n"
            "  # Correct way to provide multiline explanations\n"
            "  # Each line starts with `#` to ensure clarity and proper formatting.\n"
            "\n\n"
            "Your solution will be executed in a shell environment to test and validate the code updates. "
            "If you think the code has been executed successfully, your answer should be 'success'.\n"
            "Ensure the final implementation is functional, handles errors gracefully, "
            "and resolves any abnormal performance outcomes."
        )

        # Combine the paper summary content into the user prompt
        # so the model knows these codes are generated based on the paper
        paper_context = (
            "Below is a summary of the paper content:\n\n"
            f"{paper_summary_content}\n\n"
            "Please consider this summary when providing fixes and explanations:\n"
        )

        # Construct messages for the OpenAI ChatCompletion call
        messages = [
            {
                "role": "user",
                "content": (
                    "You are a Python code expert. You have access to a code execution environment. "
                    "Follow the user's instructions and help them fix and execute the provided code until it runs successfully.\n\n"
                    + paper_context
                    + current_context
                    + "\n\n"
                    + error_msg
                )
            }
        ]
        write_file("test_1.py", messages[0]['content'])

        # Request updated code from the model
        response = None
        try:
            # Example call to an OpenAI model
            response = openai.ChatCompletion.create(
                model="o3-mini",  # or "o1-mini", etc.
                messages=messages,
                max_completion_tokens=12000
            )
            usage_info = response['usage']
            prompt_tokens = usage_info['prompt_tokens']
            completion_tokens = usage_info['completion_tokens']
            total_tokens = usage_info['total_tokens']
            print(f"Prompt tokens: {prompt_tokens}, Completion tokens: {completion_tokens}, Total tokens: {total_tokens}")

            response_content = response['choices'][0]['message']['content']
            write_file("test_1.py", json.dumps(response_content))

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            break

        # Extract the Python code from the response
        fix_code = extract_python_code(response_content)
        if fix_code is None:
            print("No python code block found in assistant response. Stopping.")
            break

        # Execute the fix code
        print("Executing fix code...")
        fix_stdout, fix_stderr, fix_returncode = run_fix_script(fix_code)
        print("Fix result stdout:", fix_stdout)
        print("Fix result stderr:", fix_stderr)

    print("Loop ended.")
