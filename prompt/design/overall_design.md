### Optimized Task Instructions
You need to use Cora dataset and download it from Planetoid.
You are a Python class and function designer. Your task is to create modular, purpose-driven designs for each Python file (e.g., `xx.py`) in the proposed repository structure.
 **Each design should be directly aligned with the specific sections of the paper referenced in the provided file implementation details** to ensure that the implementation accurately reflects the theoretical concepts, algorithms, and methodologies outlined in the paper. The primary goal is to ensure the complete and accurate representation of the functionality described in the paper, without over-simplifying or introducing redundancy. The focus should be on achieving a comprehensive design that captures all necessary details and is ready to be implemented in code.

---

### Initial Steps

1. **Review Paper Content and File Implementation Details**: Start by carefully examining the relevant paper sections directly referenced in each file's implementation details. This review will guide your design of each class and function, ensuring they align with the paper’s requirements and fully capture the intended functionality of the repository structure.

2. **Objective**: Design each class and function to be clear, modular, and sufficiently complete to represent the functionality of each file. The goal is to achieve a comprehensive design that reflects the concepts, algorithms, and methodologies outlined in the paper, without excessive detail or oversimplification.

3. **Modular Design**: Organize the classes and functions into logical, purpose-driven modules. Ensure that each class and function serves a specific purpose, contributing directly to the overall functionality of the file. Avoid splitting functionality unnecessarily across multiple files, especially when it pertains to single-module components. If any class or function is intended to be reusable across multiple modules, it should be designed to be easily portable without requiring excessive dependencies.

---

### **Design Classes and Functions for Each File**

- **Reference to Paper Content**: Each class and function should be directly derived from the specified sections of the paper (e.g., "4.3 Network Architecture" or "4.1 Dual Mapping Formulation") to ensure accurate representation of the methodologies. Do not introduce functionality or assumptions that are not explicitly detailed in the paper.

- **Primary Classes and Functions**: For each file, design the core classes and functions required to implement the main functionality, as outlined in the file's implementation notes and the relevant sections of the paper.

- **Supporting Classes or Functions**: Include additional classes or functions for subcomponents or auxiliary tasks, ensuring modularity and clarity. Reuse code where applicable by grouping similar functionalities in utility functions or base classes shared across files.

- **Purpose, Attributes, and Methods**: For each class, clearly define its purpose, key attributes, and essential methods. Ensure that each class and function serves a distinct role, and avoid combining unrelated functionalities within a single class or function.

Note that you don't need to design any classes or functions for the config.json file, but you do need to give its contents.
---

### Expected Output Format

For each file, provide the following structure:

1. **File Name**

2. **Implementation**: Briefly describe the primary implementation goals of the file, as extracted from the code structure.

3. **Classes and Functions** (as required by the file's implementation):

   - **Primary Class Name** (if the implementation requires a class)

     - **Purpose**: Briefly describe the primary function or purpose of the class.
     - **Attributes**: List and describe key attributes, specifying their roles. **Use names consistent with those used in the original paper to enhance interpretability.**
     - **Methods**: List the main methods with a short description of each method's functionality. **Method names should also be consistent with the terminology used in the paper.**

   - **Supporting Class Name** (if applicable)

     - **Purpose**: Describe the purpose of the supporting class.
     - **Attributes**: List key attributes, maintaining consistency with paper naming.
     - **Methods**: List the main methods with descriptions of each method's functionality, using names consistent with the paper.

   - **Function Name** (if the implementation requires a function)

     - **Purpose**: Describe the purpose of the function.
     - **Parameters**: List parameters and briefly describe each. **Use parameter names consistent with those in the paper.**
     - **Return**: Specify what the function returns.

---

### Reference example

**"Workflow"**: A structured outline extracted from code_structure.

### Design of `data_manager.py`

1. **File Name**: `data_manager.py`

2. **Implementation**:  
   Manages data loading and preprocessing based on "2.1. Data Preprocessing" from the paper. The dataset (e.g., CIFAR-10) is loaded, filtered, normalized, and augmented as instructed by the paper, then organized into batches for training.  
   **Important**: The design of `data_manager.py` requires that the dataset **must not** be loaded directly from `file_path` if it does not already exist. Instead, a download step is mandatory to ensure data availability and reproducibility.

3. **Classes and Functions**:

   - **Class: DataManager**  
     - **Purpose**:  
       Download and load the dataset (e.g., CIFAR-10) using the most appropriate method (URL, library, or script), apply any filtering criteria, normalize features according to the paper’s specified statistics, perform augmentations (e.g., random horizontal flips, crops) as described, and provide data in batches for training.
       
     - **Attributes**:  
       - `data_source` (str): The source of the dataset, which could be a URL, a Python library (e.g., `torchvision`, `tensorflow_datasets`), or a custom script.  
       - `data_path` (str): Local path to store the downloaded dataset or retrieve the existing dataset.  
       - `batch_size` (int): The batch size stated in the paper.  
       - `mean` (tuple): Mean values per channel from the paper’s stated statistics.  
       - `std` (tuple): Standard deviations per channel as given by the paper.  
       - `augmentation_policy` (dict): Augmentation methods (e.g., `{"random_flip": True}`) per the paper’s instructions.  
       - `dataset`: The fully preprocessed dataset ready for training.  
       - `data_loader`: An iterator providing batches according to the paper’s training pipeline.

     - **Methods**:  
       - `__init__(self, data_source, data_path, batch_size, mean, std, augmentation_policy)`: Initializes parameters as stated in the paper.  
       - `download_data(self)`:  
         Ensures the dataset is downloaded as the first step in the pipeline:  
         - If `data_source` is a URL, downloads the dataset and saves it in `data_path`.  
         - If `data_source` is a Python library (e.g., `torchvision.datasets`), uses the library’s API to download and store the dataset.  
         - If `data_source` is a custom script, executes the script to fetch and save the data.  
         Ensures the dataset is correctly saved and extracted.  
       - `load_data(self)`: Loads the dataset from `data_path` or the library API, applies any paper-specified filters or splits.  
       - `normalize(self)`: Normalizes images using `(image - mean)/std` as per the paper’s formula.  
       - `augment_data(self)`: Applies augmentations exactly as described in the paper.  
       - `create_data_loader(self)`: Creates the data loader for batch processing as the paper prescribes (e.g., shuffle, batch size).

---

### Design of `model_architecture.py`

1. **File Name**: `model_architecture.py`

2. **Implementation**:  
   Defines the primary neural network architecture according to "3.2 Model Framework". If the paper describes a series of convolutional and fully connected layers with certain activation functions and initialization strategies, implement them precisely.

3. **Classes and Functions**:

   - **Class: BasicModel**  
     - **Purpose**:  
       Construct the model using the exact layer configuration, activation functions, and initialization routines described in the paper’s "3.2 Model Framework."
       
     - **Attributes**:  
       - `layers` (list): The layer configurations (e.g., [Conv2D(64), Conv2D(128), FC(256)]) as stated in the paper.  
       - `activation_function` (callable): The activation (e.g., ReLU) specified in the paper.  
       - `input_size` (int): Input dimension as given by the paper.  
       - `output_size` (int): Output dimension (e.g., number of classes) stated in the paper.  
       - `model`: The assembled model structure reflecting the paper’s specified architecture.

     - **Methods**:  
       - `__init__(self, input_size, output_size, layers_config, activation_function)`: Initializes model parameters from the paper’s instructions.  
       - `build_model(self)`: Constructs the layers and connections as detailed in the paper’s model framework.  
       - `forward(self, x)`: Defines the forward pass according to the paper’s computational flow.  
       - `save(self, file_path)`: Saves model parameters, if the paper states a method for persistence.  
       - `load(self, file_path)`: Loads model parameters, adhering to the paper’s approach for model restoration.

---

### Design of `evaluation.py`

1. **File Name**: `evaluation.py`

2. **Implementation**:  
   Implements evaluation metrics and evaluation procedures based on "4.4 Performance Metrics" in the paper. This includes functions to compute metrics like F1 score and ROC AUC, and a function to evaluate the model with these metrics.

3. **Classes and Functions**:

   - **Function: calculate_f1_score(predictions, ground_truth)**  
     - **Purpose**: Compute the F1 score exactly as defined by the paper’s evaluation criteria.  
     - **Parameters**:  
       - `predictions` (array-like): Predicted labels.  
       - `ground_truth` (array-like): True labels.  
     - **Return**: (float) The computed F1 score.

   - **Function: calculate_roc_auc(predictions, ground_truth)**  
     - **Purpose**: Compute the ROC AUC score following the paper’s prescribed evaluation process.  
     - **Parameters**:  
       - `predictions` (array-like): Predicted probabilities.  
       - `ground_truth` (array-like): True labels.  
     - **Return**: (float) The computed ROC AUC score.

   - **Function: evaluate_model(model, data_loader)**  
     - **Purpose**: Evaluate the trained model on the provided data and calculate metrics as stated in the paper.  
     - **Parameters**:  
       - `model`: The trained model instance.  
       - `data_loader`: DataLoader providing evaluation data as per the paper.  
     - **Return**: (dict) A dictionary containing the computed metrics (e.g., `{"f1_score": ..., "roc_auc": ...}`).

---

### Design of `main.py`

1. **File Name**: `main.py`

2. **Implementation**:  
   Coordinates the entire workflow outlined in "1. Application Setup" of the paper, including loading configuration settings, initializing data and model components, running training for the specified number of epochs, and evaluating the model, returning or printing results as described by the paper.

3. **Classes and Functions**:

   - **Function: main(config)**  
     - **Purpose**: Orchestrate the full application flow as per the paper’s instructions: load config, prepare data, build the model, train for the specified epochs, and evaluate the model, reporting metrics.  
     - **Parameters**:  
       - `config` (dict): Configuration settings loaded as the paper states.  
     - **Return**: None (may print or save results as indicated by the paper).

   - **Function: load_config(file_path)**  
     - **Purpose**: Load configuration settings (batch size, learning rate, number of epochs, data path) from a specified file as the paper directs.  
     - **Parameters**:  
       - `file_path` (str): Path to the configuration file.  
     - **Return**: (dict) Dictionary of configuration settings.

---

### Final Instructions

Design each file in the specified order, ensuring that all classes and functions within each file are purpose-driven, modularly designed, and aligned with the file’s implementation needs. **Reference the specific paper sections in `code_structure` for each class and function to ensure comprehensive coverage**.

### code_structure

{code_structure}

### Paper Content

{content}
