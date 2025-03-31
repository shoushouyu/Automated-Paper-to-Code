# Task Instructions
You need to use CIFAR-10 dataset and PFNet18 model.

You are a **code structure generator**. Your task is to design a **modular GitHub repository structure** based on the content of the following paper. Use the provided template, which summarizes repository structures from several papers, as a reference to guide your design. This template will help create a clear and organized separation of functionalities.

---

## 1. Generate the GitHub Repository Structure and Describe Each File
Create a **modular** repository structure that reflects the **key functionalities** of the paper:

1. **Data Processing Files** (e.g., `data_loader.py`):  
   - Clearly state which dataset(s) or data source(s) the paper uses, **and include a mandatory download step** if the dataset is not found locally. Do not simply load from a local file path without verifying the dataset is available; ensure reproducibility by specifying the full download approach (e.g., from a URL, a Python library, or a script).  
   - Explain **how** you will process the data after downloading (e.g., splitting into train/test, applying normalization, data augmentation, or converting formats).  
   - Reference the paper’s description of data preparation and processing steps, including the exact title/section where these are mentioned.

2. **Model Architecture Files** (e.g., `model.py`):
   - Describe the model structure precisely (e.g., layer configuration, activation functions, skip connections) based on the paper’s sections detailing the architecture.
   - Indicate if you create multiple model files (e.g., for variations in architecture) and why, referencing the exact paper sections or subsections.

3. **Training-Related Files** (e.g., `train.py`, `losses.py`):
   - Outline how training is conducted (optimizers, custom loss functions, hyperparameters) and which specific parts of the paper they implement.
   - Reference any mention of batch sizes, learning rates, or specialized training loops from the paper.  
   - If different training strategies are mentioned in separate sections, include them here or split them into multiple files.

4. **Model Evaluation Files** (e.g., `evaluation.py`):
   - Specify **exact** evaluation metrics and procedures (e.g., accuracy, precision, recall, F1). 
   - Note how the results tie back to the relevant sections of the paper, including any visualizations or analysis steps.

5. **Config Files** (e.g., `config.json`):
   - List all parameters (paths, hyperparameters, environment variables) mentioned in the paper and how they will be stored/loaded.
   - Explain how these configurations are accessed by other modules.

6. **Main File** (e.g., `main.py`):
   - Illustrate how all components integrate (data loading, model instantiation, training, evaluation).
   - Mandatory Requirement: In the main file, you must clearly document the entire workflow of the paper—explain step by step how the system works according to the paper’s “System Overview” or conceptual framework.
   - Clarify any command-line interfaces, pipeline setups, or orchestrations that follow the paper’s overall “System Overview” or conceptual framework.

You are forbidden to design utils/helpers.py, requirements.txt or README.md.
---

### Detailing Each File’s Implementation
For **every file** in the repository, provide:

1. **File Name**: A concise, descriptive name (e.g., `data/loader.py`, `train/optimizer.py`).
2. **Implementation**:
   - **Exact Reference**: Which sections of the paper (e.g., “Section 4.1 Data Preparation,” “Section 3.2 Model Architecture”) does this file implement? Include relevant headings or titles verbatim.
   - **Functionality**:
     - **Data Files**: Include any dataset source from Python libraries (e.g., `torchvision.datasets.CIFAR10`), and **the exact transformations** (e.g., “loading from the library, applying random rotations, splitting 80/20, normalizing pixel values”). **Emphasize a required download routine** if the dataset is not already present.
     - **Model Files**: Describe each layer, how they connect, any hyperparameters or architectures referenced (e.g., hidden units, dropout rates).  
     - **Training Files**: Clarify how gradients are computed, mention the optimizer (e.g., Adam, SGD), loss functions, and relevant hyperparameters.  
     - **Evaluation Files**: List the metrics, how they are calculated, and any specialized test procedures.  
   - **Dependencies**:  
     - **Inter-file Dependencies**: For instance, how does `train.py` use the model from `core_model.py` and the data from `data_loader.py`?  
     - **Data Flow**: Indicate how data, parameters, or objects move from one file to another.  
   - **Reasoning**:
     - Describe briefly why you chose this file design (e.g., “We separate data loading for clarity and reusability across multiple experiments.”).  

> Ensure the **Implementation** section is direct and precise. For example, if the paper states “We use the CIFAR-10 dataset and apply a random crop of 32×32 followed by normalization,” then in the `loader.py` file’s Implementation, explicitly mention these steps **including the mandatory download step**.

---

## 2. Handling Specific Content
- **Exclude non-implementation sections**: Do not include files for content such as ablation studies or formal proofs that do not require direct coding. Focus on methodologies, experiments, models, and other technical aspects that translate into actionable code.

---

## 3. Final Check
- **Review all extracted titles**: Confirm each required implementable section from the paper is addressed.  
- **Ensure clarity**: Each file must serve a distinct purpose. If any section overlaps, state clearly how responsibilities are divided or shared.

---

## 4. Expected Output Format
Your final output should be a **JSON-like structure** (or a similarly structured response) containing:
1. **"Extracted Titles"**: List of all headings found in the paper starting with `#`.
2. **"Workflow"**: A structured outline detailing the necessary steps for implementing a complete code solution based on the paper. This should describe the sequence of actions required, such as data preprocessing, model architecture design, training procedures, evaluation methods, and any additional components needed to fully realize the paper's proposed approach.
3. **Repository Files**: A section for each file, using a key like `"data/loader.py"` or `"models/model.py"`, followed by its **Implementation** describing the details noted above.

Please ensure:
- **Implementation** thoroughly explains **which data** is used and **how** it’s processed (for data files), or the **model structure** (for model files), or the **training** and **evaluation** methods for the respective files.
- Any **dependencies** or **shared functionalities** between files are clearly stated.
- **Crucially, for data files, ensure you demonstrate a mandatory downloading process** rather than reading directly from a local path if the data is not already present.

---

### Template to Refer to:
{template}

### Paper Content:
{content}

**Design Order** (recommended):
1. **Data Processing Files**
2. **Model Architecture Files**
3. **Training-Related Files**
4. **Model Evaluation Files**
5. **Config Files**
6. **Main File**

---

By following these guidelines, you will produce a comprehensive, modular, and well-documented GitHub repository design that aligns with the paper’s content and methodology.
