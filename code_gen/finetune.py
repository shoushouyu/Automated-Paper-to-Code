import openai
import re

def read_file(path: str) -> str:
    """Utility function to read text content from a file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_python_code(text: str) -> str:
    """
    Find the first fenced Python code block in the text.
    Example fence:
    python ...
    
    Returns the code (string) inside the fence or an empty string if not found.
    """
    pattern = r"```python(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def main():
    try:
  
        prompt_text = read_file("prompt/code/finetune.md")
        
       
        original_main_py = read_file("iter_code/paper/code_generate/main.py")
        original_eval_py = read_file("code_generate/evaluation/evaluate.py")
        
 
        full_prompt = prompt_text.replace("{template}", original_main_py).replace("{evaluate}", original_eval_py)
        print(full_prompt)
        

        response = openai.ChatCompletion.create(
            model="o1-mini",  # or "gpt-4o" if that's your custom model name
            messages=[{"role": "user", "content": full_prompt}],
            max_completion_tokens=8000
        )
        
        print(response)
     
        response_text = response["choices"][0]["message"]["content"]
        #print(response_text)
        
       
        new_main_py_code = extract_python_code(response_text)
        
       
        if new_main_py_code:
            with open("iter_code/paper/code_generate/main.py", "w", encoding="utf-8") as f:
                f.write(new_main_py_code)
            print("main.py has been updated successfully.")
        else:
            print("No Python code block found in the model's response. main.py was not changed.")
    
    except openai.error.OpenAIError as e:
        print(f"Error calling OpenAI API: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
