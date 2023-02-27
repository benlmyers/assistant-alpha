## Welcome to Assistant (alpha version)

The mission of Assistant is to reduce interactions between humans and services offered by third parties via API.

Assistant takes in a text input (e.g. "Summarize my most recent emails") and completes the task to the best of its ability.

## ⚡️ Quick Start

## 🧠 Training Models

Assistant uses a combination of machine learning and natural language processing to complete tasks. To train the models, we need to provide a large amount of data.

### Step 1: Create Training Data 

To create data, first enable Training Mode. You can enable Training Mode with the following steps:

1. Run **main.py**.
2. Enter 'M' to enter the Menu.
3. Enter 'T' to enable Training Mode.
4. Press ENTER to continue.

When Training Mode is enabled, you'll see console output starting with '[TRAIN]'. This means that you can now create training data.




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