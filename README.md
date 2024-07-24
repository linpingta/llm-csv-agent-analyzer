# llm-csv-agent-analyzer

## Introduction

This project sets up a framework for an LLM (Language Learning Model) agent to analyze CSV data.

## Modules

### 1. Load CSV as a DataFrame

- **dloader**: Manages all input data (the data to be analyzed).

### 2. Read Config

- **Single Query**: Reads and manages configuration settings for queries.

### 3. Load Model

- Loads the specified model to be used for analysis.

### 4. Generate Output

- Processes the data and generates the required output.

## Analyze CSV Data and Answer Questions

### 1. Prepare Tasks

- **Tasks** are business-specific concepts, such as an estate task for analyzing real estate data.

#### Task Attributes

1. **csv content**: Held by the data loader, contains the CSV content to be used as context.
2. **prompt**: Injected into the request.
3. **question**: The actual question to be answered. Supports question lists in the future.
4. **model**: The backend model corresponding to the task.

#### Differences Between Tasks

- The primary difference lies in `_preprocess_data`, i.e., the data preprocessing part.

### 2. Data Loader Preloads CSV Content

- Can be used in several ways:
  1. As prompt context.
  2. As RAG (Retrieval-Augmented Generation).

### 3. Prepare Prompt

1. **Prompt template from file**: Prepared in a file.
2. **Prompt ID**: Each template has a corresponding code.
3. **Prompt dict**: Used to fill parameters in the template.

- The three components jointly produce a real prompt. Supports using a default prompt.

### 4. Prepare Questions

- Defines a list of questions.

### 5. Models

1. The model used for backend API requests.
2. Specifies variable parameters in the configuration or uses default parameters.

## Getting Started

To use this framework, follow these steps:

1. **Load your CSV data**: Use the data loader to manage and preprocess your input data.
2. **Read and configure settings**: Define your queries and task-specific settings.
3. **Load the desired model**: Choose and load the model for your analysis.
4. **Generate output**: Process the data and produce the required output based on your tasks and questions.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](https://opensource.org/licenses/MIT) file for details.
