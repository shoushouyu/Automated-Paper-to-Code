You are tasked with converting a markdown-formatted document into a JSON format, preserving all details without any reduction. The content should be output in the following structure:

1. **File Name**: The name of the file being described.
2. **Implementation**: A detailed description of the primary implementation goals of the file, reflecting any adjustments made based on utility files.
3. **Dependencies**:
   - **Imports**: A list of classes or functions imported from other files, specifying the file names.
4. **Classes and Functions**:
   - **Class** (if applicable):
     - **Purpose**: The main function or purpose of the class.
     - **Attributes**: Key attributes, describing their roles with names consistent with the paper.
     - **Methods**: Main methods with descriptions of their functionalities, using names consistent with the paper.
   - **Function** (if applicable):
     - **Purpose**: Describes the purpose of the function.
     - **Parameters**: Key parameters for the function, maintaining consistency with the paper's naming conventions.
     - **Return**: For functions, specify the return values.
5. **Content**:

Ensure that all information from the markdown is preserved and presented in JSON format.

For example, if the markdown contains details for a file `data/loader.py`, the output should look like this:

{
  "data/loader.py": {
    "implementation": "Handles data loading and preprocessing, including Poisson disk sampling and patch generation.",
    "dependencies": {
      "imports": [
        "from utils.helpers import add_gaussian_noise"
      ]
    },
    "classes_and_functions": [
      {
        "class_name": "DataLoader",
        "purpose": "Handles loading and preprocessing of point cloud datasets.",
        "attributes": {
          "data_path": "Path to the dataset.",
          "batch_size": "Number of samples per batch.",
          "poisson_disk_radius": "Radius for Poisson disk sampling.",
          "patch_size": "Number of points per patch.",
          "dataset": "Loaded dataset.",
          "data_loader": "Iterator over the dataset."
        },
        "methods": [
          {
            "name": "__init__",
            "purpose": "Initializes the data loader.",
            "parameters": {
              "data_path": "Path to the dataset.",
              "batch_size": "Number of samples per batch.",
              "poisson_disk_radius": "Radius for Poisson disk sampling.",
              "patch_size": "Number of points per patch."
            },
            "return": "None"
          },
          {
            "name": "load_data",
            "purpose": "Loads data from the specified path.",
            "parameters": {},
            "return": "None"
          }
        ]
      },
      {
        "function_name": "add_gaussian_noise",
        "purpose": "Adds Gaussian noise to a point cloud.",
        "parameters": {
          "point_cloud": "Input point cloud.",
          "noise_level": "Noise level."
        },
        "return": "Noisy point cloud."
      }
    ]
  }
}

- Only include content related to the file design.
- If no classes or functions are defined, include empty arrays (`[]`) for those fields.
- Ensure the output is strictly in JSON format without any explanation or extra content.

### markdown-formatted document:
{md_content}
