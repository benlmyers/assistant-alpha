### Welcome to Assistant (alpha version)

The mission of Assistant is to reduce interactions between humans and services offered by third parties via API.

Assistant takes in a text input (e.g. "Summarize my most recent emails") and completes the task to the best of its ability.

### Index

User Request: The request a user makes, as text.
Subdivision: Simplify input into a Task collection
Task: An action that can completed in a single call or action by an AI or API.
External Task: A task that requires an API.
Internal Task: A task that can be completed by an AI.
Context: Necessary data for an internal task.
Prompt: Action requested for the AI using context.
Result: Data returned from a task.

### Algorithm

Input -> Subdivision -> Output (List<Task>)

For each Task:

if External Task: Requisition -> Request Preparation -> Interpret Response -> Output (Result)
if Internal Task: Action Formation -> Call AI -> Output (Result)