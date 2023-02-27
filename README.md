## Welcome to Assistant (alpha version)

The mission of Assistant is to reduce interactions between humans and services offered by third parties via API.

Assistant takes in a text input (e.g. "Summarize my most recent emails") and completes the task to the best of its ability.

## ⚡️ Quick Start

## 🧠 Training Models

Assistant uses a combination of machine learning and natural language processing to complete tasks. To train the models, we need to provide a large amount of data.

### Step 1: Collect Training Data 

To create data, first enable Training Mode. You can enable Training Mode with the following steps:

1. Run **main.py**.
2. Enter 'M' to enter the Menu.
3. Enter 'T' to enable Training Mode.
4. Press ENTER to continue.

When Training Mode is enabled, you'll see console output starting with '[TRAIN]'. This means that you can now create training data.

When the Assistant is in Training Mode, it well tell you about it's current completion. 

- If it looks correct, enter 'Y' to confirm.
- If it looks incorrect, enter 'N' to reject and fix it yourself.

Data is recorded and saved to a file called `training_elements.json`. This file is used to hold data and correct completions used to generate training data.

### Step 2: Generate Training Data

To generate training data for OpenAI, follow these steps:

1. Run **main.py**.
2. Enter 'M' to enter the Menu.
3. Enter 'G' to generate training data.

This will generate a file called `training_data.json` using information from `training_elements.json`. This file is used to train the OpenAI model.

> **Tip**: If you only want to generate training data for specific processes, add/remove processes in `generate_training_data.py`'s `processes` list.'

### Step 3: Upload and Fine-Tune a Model

The last step is to upload the training data to OpenAI and fine-tune a model. To do this, follow these steps:

1. Run **main.py**.
2. Enter 'M' to enter the Menu.
3. Enter 'F' to fine-tune the models using the training data from Step 2.

This will automatically upload the training data to OpenAI and fine-tune the base models as specified in `pretrained_models.json`. The fine-tuned models will be added to that file, as well.

When a model is fine-tuned, it may take some time to complete. Be aware of this when attempting to immediately use the model (the Assistant may return unknown errors).

## Index

User Request: The request a user makes, as text.
Subdivision: Simplify input into a Task collection
Task: An action that can completed in a single call or action by an AI or API.
External Task: A task that requires an API.
Internal Task: A task that can be completed by an AI.
Context: Necessary data for an internal task.
Prompt: Action requested for the AI using context.
Result: Data returned from a task.

## Algorithm

Input -> Subdivision -> Output (List<Task>)

For each Task:

if External Task: Requisition -> Request Preparation -> Interpret Response -> Output (Result)
if Internal Task: Action Formation -> Call AI -> Output (Result)