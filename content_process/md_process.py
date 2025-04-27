import openai
import re
import os

OPTIMIZED_PROMPT = """
We need to use CIFAR-10 dataset and PFNet18 model.
You are an **information extractor**. Your goal is to find any content about:

1. **Code Implementation** (e.g., algorithms, pseudocode, data flow, architectures, code snippets),  
2. **Experiment Settings** (e.g., hyperparameters, datasets, metrics, evaluation methods, or tables specifying parameters),  

---

### Pre-Extraction Guidelines
1. **Source Restriction**: Only extract text **verbatim** from the **paragraph** provided (you may read the entire paper for context but do not quote from other sections).  
2. **Exclusions**: Omit any text about related work, theoretical proofs, citations of other works, result/ablation analyses, feature visualizations, or computational analyses even they are related to code implementation(You can infer from the paragragh's title).

---

### Extraction Rules
1. **Relevance**: Include text **exactly** as it appears if it covers:
   - Implementation details (algorithms, architecture, code snippets),
   - Experiment settings (hyperparameters, dataset names/properties, evaluation metrics, parameter tables),
   - The main problem statement.
2. **Verbatim and Complete**: Copy all relevant passages **in full**, without paraphrasing or truncating.  
3. **Tables**: If there is table data in the paragraph, extract it line by line, preserving the original format.  
4. **Non-Relevant Content**: Exclude anything else (e.g., background theory, unrelated mentions).  
5. **If No Relevant Content**: Output `"no relevant content"`.

---

### Output Format
- Provide **one continuous block** of extracted text (verbatim).
- If necessary, add separate, clearly labeled notes **after** that block to clarify or interpret.

---

### Objective
Extract and present all relevant details on **implementation**, **experiment settings**, or the **main problem statement** from the **paragraph**. Do not modify or shorten the quoted material.

---

**paper content**:
{content}

**paragraph**:
{paragraph}
"""



def read_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def split_paragraphs_by_markdown(content):

    paragraphs = re.split(r'(?=\n#{1,6}\s*)', content)  
    return [p.strip() for p in paragraphs if p.strip()] 


def extract_paragraph_title(paragraph):
    match = re.match(r'^(#{1,6})\s*(.*\S)', paragraph.strip())  
    if match:
        return match.group(0).strip()  
    return "Unknown Title"


def clean_paragraph_content(paragraph, max_tokens=8000, temperature=0):
    system_content = """
You are a text cleaner and extractor. Your task is to clean and extract information from a paragraph of text, adhering to the following rules:

### Tasks:
1. **Image Markdown Syntax:**
   - Identify any image markdown syntax (e.g., `![caption](url)`).
   - Extract the **caption or description** that immediately follows the image syntax.
   - Remove the image link and markdown syntax while keeping the extracted caption.

2. **Table Content:**
   - Retain all tables (e.g., HTML or Markdown table structures) in their original form.
   - Ensure table formatting is preserved and readable.

3. **Text Cleanup:**
   - Remove unnecessary spaces, broken lines, or redundant formatting.
   - Correct spelling and grammar errors to ensure readability.
   - Retain all symbolic or mathematical expressions, converting them into a consistent LaTeX format if necessary (e.g., `$f(\\cdot)$` should become `\\( f(\\cdot) \\)`).

4. **Output Format:**
   - Provide the cleaned paragraph, extracted captions, and preserved tables in Markdown format.
   - Maintain separate sections for the **cleaned text**, **image captions**, and **tables**.

### Example Input:
- Paragraph:
    ```
    ![Example Image](example.com/image.png)
    > **Picture description**: This is a helpful figure with explanatory text.
    This is a sample text with an image above. Table 3: Dataset details and hyperparameters:
    <html><body><table><tr><td>Header1</td><td>Header2</td></tr><tr><td>Data1</td><td>Data2</td></tr></table></body></html>
    Another line with a formula $f(x) = ax^2 + bx + c$.
    ```

### Example Output:

- **Cleaned Text:**
    ```
    This is a sample text with an image above. 
    Another line with a formula \\( f(x) = ax^2 + bx + c \\).
    > **Picture description**: This is a helpful figure with explanatory text.
    ```

- **Extracted Captions:**
    ```
    Example Image
    ```

- **Tables:**
    ```
    Table 3: Dataset details and hyperparameters:
    <html><body><table><tr><td>Header1</td><td>Header2</td></tr><tr><td>Data1</td><td>Data2</td></tr></table></body></html>
    ```

### Notes:
- Do not summarize or interpret the content; focus solely on cleaning and formatting.
- Ensure mathematical and tabular content is preserved exactly as provided.
- Return all output sections in Markdown format.

### Paragraph to Process:
    """



    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": paragraph}
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )
    
    usage_info = response['usage']
    prompt_tokens = usage_info['prompt_tokens']
    completion_tokens = usage_info['completion_tokens']
    total_tokens = usage_info['total_tokens']
    print(f"Prompt tokens: {prompt_tokens}, Completion tokens: {completion_tokens}, Total tokens: {total_tokens}")
    cleaned_paragraph = response['choices'][0]['message']['content']
    return cleaned_paragraph


def extract_implementation_details(paragraph, entire_paper_content,
                                  max_tokens=8000, temperature=0):


    system_content = OPTIMIZED_PROMPT.replace("{content}", entire_paper_content)\
                                     .replace("{paragraph}", paragraph)
    
    response = openai.ChatCompletion.create(
        model="o1-mini",
        messages=[
            {"role": "user", "content": system_content},
           
        ],
        max_completion_tokens=12000
    )
    '''

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": paragraph}
        ],
        max_tokens=max_tokens,
        temperature=0
    )
    '''
    
    usage_info = response['usage']
    prompt_tokens = usage_info['prompt_tokens']
    completion_tokens = usage_info['completion_tokens']
    total_tokens = usage_info['total_tokens']
    print(f"Prompt tokens: {prompt_tokens}, Completion tokens: {completion_tokens}, Total tokens: {total_tokens}")
    return response['choices'][0]['message']['content']


def append_to_md_file(output_path, paragraph_title, content):
    with open(output_path, 'a', encoding='utf-8') as file:
        
        file.write(f"{paragraph_title}\n")
        file.write(f"{content}\n\n")


def process_paragraphs(entire_paper_content, output_path):
    paragraphs = split_paragraphs_by_markdown(entire_paper_content)
    i = 0
    for paragraph in paragraphs:
        paragraph_title = extract_paragraph_title(paragraph)
        print(f"Processing paragraph: {paragraph_title[:50]}...")

        
        if paragraph_title.lower() == "## abstract":
            
            cleaned_paragraph = clean_paragraph_content(paragraph)
            append_to_md_file(output_path, "", paragraph)
            continue
        
        
        cleaned_paragraph = clean_paragraph_content(paragraph)
        cleaned_paragraph = paragraph_title + cleaned_paragraph

        
        extracted_content = extract_implementation_details(
            cleaned_paragraph,
            entire_paper_content
        )

        if i == 0:
            append_to_md_file(output_path, "", paragraph_title)
            i += 1
        
        elif extracted_content.lower().strip() != "no relevant content" and extracted_content.lower().strip() != '"no relevant content"':
            append_to_md_file(output_path, paragraph_title, extracted_content)
        
        


def main(input_md_folder, output_md_folder):
   
    os.makedirs(output_md_folder, exist_ok=True)

    for filename in os.listdir(input_md_folder):
        if filename.endswith("paper.md"):
            input_md_path = os.path.join(input_md_folder, filename)
            paper_name = os.path.splitext(filename)[0]
            output_md_path = os.path.join(output_md_folder, f"{paper_name}_summarized.md")

            
            entire_paper_content = read_md_file(input_md_path)

            
            process_paragraphs(entire_paper_content, output_md_path)


if __name__ == "__main__":
    input_md_folder = "markdown_files/"
    output_md_folder = "markdown_files/"
    main(input_md_folder, output_md_folder)
