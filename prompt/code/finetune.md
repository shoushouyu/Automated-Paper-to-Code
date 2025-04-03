Please read and modify the provided main.py file so that it integrates Ray Tune for tuning the learning rate hyperparameter. The requirements are as follows:

1) Use Ray Tune
- Import necessary modules (for example, ray, ray.tune, and a scheduler such as ASHAScheduler).
- Define a training function (for instance, train_with_tune) that Ray Tune will call for each hyperparameter trial. This function should train the model and return results.

2) Only tune learning_rate
- Set a search space, for example:
search_space = {"lr": tune.loguniform(1e-5, 1e-2)}

3) Report metrics in dictionary form
- To avoid the error "TypeError: report() got an unexpected keyword argument 'accuracy'", you must report metrics with tune.report({"accuracy": accuracy})
- Do not use tune.report(accuracy=accuracy)

4) Specify metric and mode only in tune.run or the scheduler
- In ASHAScheduler, only keep options like max_t, grace_period, reduction_factor, etc., without specifying metric="accuracy" or mode="max".
- In tune.run, set metric="accuracy" and mode="max" so that Ray knows which metric to maximize.

5) Final output
- After searching completes, print the best learning rate (best_lr) and then retrain the model with it.
- Print the final test accuracy (final_accuracy) corresponding to this best learning rate in a format such as:
Best hyperparameters found: lr=...
Final Test Accuracy: ...

Please preserve the existing data-loading and model (EntropyAwareGNN, GCNLayer, etc.) logic in main.py, and only add or modify code where necessary to accomplish the hyperparameter tuning with Ray Tune. Make sure the modified code can run successfully and print both the best_lr and the final_accuracy. Then provide the complete updated main.py file as an example.

Then, provide the complete updated main.py file inside a fenced Python code block. You do not need to make changes to the evaluation file.

### Content of main.py file:
{template}

### Content of the corresponding evaluation file:
{evaluate}
