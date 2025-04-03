### Task Instructions
You need to use CIFAR-10 dataset and PFNet18 model.

You are tasked with optimizing the implementation of a given file design in **current_file**. Your role is to refine and enhance the existing design based on the overall repository structure **file_design** and the provided paper content **content**. The optimization should be grounded in the theoretical framework of the paper, with an emphasis on aligning the implementation with the methodologies described in the relevant sections. 

**You must keep the original class or function names in `current_file`, but you are allowed to modify parameter types, add or remove parameters, or alter return values as needed** to ensure a proper implementation that aligns with the paper’s methodology.

The optimization should focus on the following aspects:

1. **Class Attributes**:
   - Add or remove attributes based on their relevance and necessity as per the paper.
   - For attributes with fixed values, determine those values explicitly from the paper. If not directly provided, propose reasonable defaults based on the paper’s content and overall design context.
   - Ensure that any attributes mentioned in relevant sections of the paper (e.g., Section 3 Setup) are correctly integrated into the class.

2. **Class Methods**:
   - Provide a detailed explanation of each method, including its purpose, functionality, and how it aligns with the methodologies described in the paper.
   - Include step-by-step implementation details, explicitly referencing the relevant paper sections (e.g., "as described in Section 4.1") to ensure clarity and adherence to the proposed methods.
   - Incorporate all relevant formulas and definitions from the paper that influence method implementation.
   - **Adjust method parameters or return values** when necessary to maintain consistency with the paper’s proposed design while preserving the original method names.

3. **Functions**:
   - Similar to class methods, refine functions by specifying the exact data types for their parameters.
   - Provide detailed step-by-step descriptions of how each function should be implemented, ensuring they follow the principles outlined in the paper.
   - Include references to relevant sections or formulas from the paper to clarify the rationale behind each function's design.
   - **Make necessary modifications to function parameters or return values** if it improves adherence to the paper's methodologies.

4. **Parameter Values (if no classes or functions are present)**:
   - Identify and supplement any parameter values within the file based on the paper’s specifications.
   - Ensure that all parameters are clearly defined with appropriate default values or constraints as described in the paper.
   - Reference the relevant sections of the paper that dictate these parameter values to maintain alignment with the theoretical framework.

5. **Data Loading with Data Download**:
   - If the design in `current_file` involves data loading, include a data downloading procedure as part of the implementation step.
   - This procedure should reference any relevant instructions or packages necessary to retrieve and prepare the dataset for use within the file.

Ensure that the optimized implementation is not only practical and well-structured, but also thoroughly aligned with the theoretical foundations described in the paper. Every step of the implementation must trace back to the content in the paper, especially in sections such as "Section 3: Setup" or "Section 4: Methodology", and these references should be clearly stated within the implementation.

---

Your output format should be consistent with the Example File Design with Detailed Implementation Steps section and don't add anything extraneous.

### Example File Design with Detailed Implementation Steps(not for config.json)

```json
{
  "file_name": "models/neural_network.py",
  "implementation": "Defines a simple feedforward neural network class and utility functions for training and evaluating the network on generic data, based on the methodologies described in Section 3. The network is designed for regression tasks and uses a ReLU activation function as outlined in the paper.",
  "dependencies": {
    "imports": [
      "torch",
      "torch.nn as nn",
      "torch.optim as optim",
      "numpy as np"
    ]
  },
  "classes_and_functions": [
    {
      "class_name": "SimpleNN",
      "purpose": "Implements a simple feedforward neural network for regression tasks as described in Section 3.2 of the paper, where the model's architecture is defined by the input, hidden, and output layers.",
      "attributes": {
        "input_dim": "Dimension of the input features, as defined in Section 3.2. It should match the number of features in the input data. This attribute is critical and must remain as defined in the paper.",
        "hidden_dim": "Number of units in the hidden layer, determined based on the experimental setup described in Section 3.2, typically set to 64. This is an essential attribute and must remain.",
        "output_dim": "Dimension of the output predictions, which corresponds to the regression target variable. Set to 1 for scalar regression tasks. This is needed and cannot be removed.",
        "layers": "Sequential container for the network layers, including input, hidden, and output layers, based on the architecture presented in the paper. This attribute remains the same.",
        "dropout_rate": "Dropout rate for regularization, added based on empirical results from Section 4.2 to avoid overfitting. This attribute was added to the class for better generalization.",
        "activation_function": "Activation function to use between layers, default to ReLU as specified in the paper. Optional attribute added to provide flexibility in the network design."
      },
      "methods": [
        {
          "name": "__init__",
          "purpose": "Initializes the network architecture with input, hidden, and output layers as per the design specified in Section 3.2 of the paper. The addition of dropout regularization is implemented.",
          "parameters": {
            "input_dim": "Number of input features, derived from the dataset (as described in Section 3.2). This remains unchanged.",
            "hidden_dim": "Number of units in the hidden layer, suggested to be 64 based on experiments in the paper. No change here.",
            "output_dim": "Number of output features, usually 1 for regression tasks, as defined in the paper. This remains.",
            "dropout_rate": "Dropout rate for regularization, added as a new parameter based on the paper's suggestion for avoiding overfitting. Typically set to 0.2 as suggested in Section 4.2."
          },
          "return": "None",
          "implementation_steps": [
            "1. Call the parent class nn.Module's __init__ method to initialize the base class, as outlined in Section 3.2.",
            "2. Define the input layer using nn.Linear, where input_dim and hidden_dim are the parameters. This corresponds to the first layer in the architecture described in Section 3.2, with the equation: $z_1 = W_1 x + b_1$.",
            "3. Define the hidden layer using nn.Linear, where hidden_dim and output_dim are the parameters. The hidden layer transforms the feature representation, as detailed in the paper, with the equation: $z_2 = W_2 h_1 + b_2$.",
            "4. Apply nn.ReLU as the activation function after the input layer, introducing non-linearity as stated in Section 3.2. The activation function is: $h_1 = ReLU(z_1)$.",
            "5. Apply dropout regularization to the hidden layer using nn.Dropout with the specified dropout_rate (typically 0.2 as described in Section 4.2) to prevent overfitting. The dropout operation is: $h_2 = Dropout(h_1)$.",
            "6. Store the layers (input, hidden, and output) in a Sequential container, which facilitates the flow of data through the network as shown in Figure 1 of the paper."
          ]
        },
        {
          "name": "forward",
          "purpose": "Performs a forward pass through the network, as outlined in the forward propagation section of the paper (Section 3.3).",
          "parameters": {
            "x": "Input tensor of shape (batch_size, input_dim), representing a batch of input data."
          },
          "return": "Output tensor of shape (batch_size, output_dim), representing the predictions of the model.",
          "implementation_steps": [
            "1. Apply the first layer (input layer) to the input tensor 'x'. This step maps the input features to the hidden layer, using the equation: $h_1 = ReLU(W_1 x + b_1)$.",
            "2. Apply ReLU activation to the output of the first layer, introducing non-linearity as described in Section 3.2.",
            "3. Apply dropout regularization to the output of the first layer using dropout_rate, which is 0.2 by default: $h_2 = Dropout(h_1)$.",
            "4. Apply the second layer (hidden layer) transformation: $y = W_2 h_2 + b_2$.",
            "5. Return the final output of the second layer as the prediction, as per the network architecture described in the paper."
          ]
        }
      ]
    },
    {
      "function_name": "train_model",
      "purpose": "Trains the neural network on a given dataset. The training procedure follows the steps outlined in Section 4.1 of the paper, where gradient descent is used for optimization. The optimizer is Adam, and the batch size is 32 as suggested in the paper.",
      "parameters": {
        "model": "Instance of SimpleNN to be trained, based on the architecture specified in the paper.",
        "data_loader": "DataLoader providing batches of training data, typically split into batches of 32 as suggested in Section 4.1.",
        "criterion": "Loss function used for training, typically Mean Squared Error (MSE) for regression tasks, as stated in Section 4.1.",
        "optimizer": "Optimizer for updating model parameters, commonly Adam optimizer as per the paper's recommendation.",
        "epochs": "Number of training epochs, typically set to 50 based on the experimental setup in the paper."
      },
      "return": "Trained model instance, which can be used for evaluation or inference.",
      "implementation_steps": [
        "1. Set the model to training mode using model.train() to enable training-specific behaviors like dropout, as explained in Section 4.1.",
        "2. Loop over the specified number of epochs. In each epoch, the entire dataset will be processed once.",
        "3. Inside each epoch, iterate over the data_loader to get batches of data, where each batch contains 'batch_size' samples.",
        "4. For each batch, zero the gradients of the optimizer using optimizer.zero_grad(), which clears old gradients from the previous step.",
        "5. Perform a forward pass through the model to get predictions for the current batch, following the forward propagation process: $h_1 = ReLU(W_1 x + b_1)$ and $y = W_2 h_2 + b_2$.",
        "6. Compute the loss by passing the predictions and true labels through the criterion (e.g., MSE). The loss function is defined as: $L = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$.",
        "7. Backpropagate the loss by calling loss.backward(), which computes the gradients of the model's parameters.",
        "8. Update the model parameters by calling optimizer.step(), which adjusts the parameters in the direction that reduces the loss.",
        "9. Optionally, track the loss or other metrics for each epoch for performance monitoring, as suggested in Section 4.1."
      ]
    }
  ]
}
```

**current file to refer**:
{current_file}

**file design to refer**:
{file_design}

**content to refer**:
{content}

