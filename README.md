# SmartDocRAG

This project integrates Llama 3 with LlamaIndex and Streamlit to build a Retrieval-Augmented Generation (RAG) system. The goal is to enhance Llama 3's ability to generate accurate and context-aware responses by incorporating external knowledge through a robust retrieval mechanism.

### Key Features

- Knowledge Retrieval with LlamaIndex
  LlamaIndex serves as the backbone for indexing and retrieving relevant information from structured and unstructured data sources. It ensures the model is provided with precise context to generate accurate and informed responses.

- Advanced Generation with Llama 3
  By combining retrieved context with user queries, Llama 3 delivers high-quality, contextually enriched answers. Careful prompt engineering ensures seamless integration between the retrieval and generation components.

- Interactive UI with Streamlit
  A sleek and intuitive interface built with Streamlit allows users to input queries, view results, and analyze retrieved documents. The interface prioritizes usability and responsiveness for an enhanced user experience.

### How It Works

- Data Indexing:
  Use LlamaIndex to preprocess and index your data. The system supports various data formats, making it adaptable to different datasets.

- Retrieval and Augmentation:
  For each user query, LlamaIndex retrieves the most relevant data, which is then passed to Llama 3 for contextual understanding.

- Interactive Querying:
  Streamlit provides a front-end interface where users can interact with the system, submit queries, and receive insightful responses augmented by retrieved knowledge.

## Prerequisites

- Python 3.10 or higher

## Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/namthai-dev/SmartDocRAG.git
```

### Step 2: Navigate to the project directory

```bash
cd SmartDocRAG
```

## Installation

### Step 1: Install the required packages

```bash
pip install -r requirements.txt
```

### Step 2: Setup Ollama

Follow the instruction [here](https://github.com/ollama/ollama) to install Ollama

```bash
ollama pull llama3.2:1b
```

### Step 3: Run the main notebook (Optional)

```bash
jupyter nbconvert --to notebook --execute main.ipynb
```

## Run Streamlit App

### Step 1: Install Streamlit

```bash
pip install streamlit
```

### Step 2: Run the Streamlit App

```bash
streamlit run app.py
```

## Output

### Screenshots

![image](https://github.com/user-attachments/assets/3e5dc98f-6d3f-4c4e-9ab4-d4b45c8efcd6)

![image](https://github.com/user-attachments/assets/e42aff8a-d1b5-47a8-9189-89ade7bf8c94)

### Demo

https://github.com/user-attachments/assets/a6ad1781-4bc1-431a-b519-52b41e3a7de9
