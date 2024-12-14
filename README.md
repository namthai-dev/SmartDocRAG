# SmartDocRAG

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
