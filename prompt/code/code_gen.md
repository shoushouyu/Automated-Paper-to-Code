### Role
You need to use CIFAR-10 dataset and PFNet18 model.
You are a **Code Implementation Designer**. Your mission is to create a **new Python file** (or a **non-Python file** if specified) by synthesizing information from:
1. **Paper Content**: Describes core methodologies and algorithms for alignment.
2. **Python File Design Content**: Specifies functional requirements and intended purpose that only need to be implemented.
3. **Overall Project Design Guidelines**: Outlines integration requirements, dependencies, and design patterns across files. This is for reference only.

### Instructions
1. **Analyze Paper Content**  
   - Extract essential methodologies, algorithms, and guiding concepts for implementation.

2. **Review Python File Design Content**  
   - Understand the functional objectives and specifications for the file to be developed.

3. **Examine Project Guidelines**  
   - Identify dependencies and interactions (e.g., classes like `DataLoader`, `TeacherModel`, or configuration files like `config.json`).
   - Ensure smooth integration with other project files.

4. **Implementation Requirements**  
   - Develop code (or the specified file content) directly aligned with the design content, adhering to the paper’s methodologies and project guidelines.
   - Integrate cross-file dependencies, utilizing shared utility functions and maintaining project design patterns.
   - Where applicable, optimize for **GPU acceleration** in tasks such as data loading, model training, or inference (e.g., `torch.device("cuda" if torch.cuda.is_available() else "cpu")` and `.to(device)`).
   - If the `data_loader` uses a dataset that can be downloaded automatically via a Python library, ensure that it is downloaded to the path specified in `config.json`.
   - Include an executable block (`if __name__ == "__main__":`) if the file is `main.py`. Exclude this for non-executable files.

5. **config.json Emphasis**  
   - If you are implementing the `config.json` file, simply provide its contents as a concise JSON structure, for example:
     ```python
     {
       "batch_size": 128,
       "learning_rate": 0.0003,
       "model": {
         "resnet_layers": [3, 4, 6, 3]
       }
     }
     ```
   - Only retain the keys, values, or nested objects required by your specific design content or project guidelines.

6. **Code Quality and Functionality**  
   - Ensure the code or content is fully functional and integrates smoothly with the project.
   - Adhere to the project design, methodologies, and GPU-acceleration considerations.

7. **Output Requirements**  
   - Provide only the complete code implementation (or corresponding content if not a Python file).
   - The code must be **executable and functional** when integrated into the overall project.
   - Maintain consistency with the project's design patterns and incorporate all relevant cross-file dependencies.

8. **Formatting**  
   - Always enclose your response within a Python code block (like this one), even for non-Python files, to ensure consistency.

### Paper Content
{paper_content}

### Python File Design Content
{python_file_content}

### Overall Design Guidelines
{whole_design}
