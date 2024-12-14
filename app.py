import os
import base64
import gc
import uuid
import tempfile

from IPython.display import Markdown, display
import streamlit as st
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.core import PromptTemplate
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, ServiceContext, SimpleDirectoryReader

# Session State Initialization
if "id" not in st.session_state:
    st.session_state.id = uuid.uuid4()
    st.session_state.file_cache = {}
    st.session_state.messages = []
    st.session_state.context = None

session_id = st.session_state.id


# LLM Initialization
@st.cache_resource
def load_llm():
    """Load the Llama model with specified parameters."""
    return Ollama(model="llama3.2:1b", request_timeout=360.0)


# Reset Chat
def reset_chat():
    """Clear the chat history and context."""
    st.session_state.messages = []
    st.session_state.context = None
    gc.collect()


# Display PDF Preview
def display_pdf(file):
    """Embed and display a PDF file in Streamlit."""
    st.markdown("### PDF Preview")
    base64_pdf = base64.b64encode(file.read()).decode("utf-8")
    pdf_display = f"""<iframe src="data:application/pdf;base64,{base64_pdf}" 
                      width="100%" height="100%" type="application/pdf" 
                      style="height:100vh;"></iframe>"""
    st.markdown(pdf_display, unsafe_allow_html=True)


# File Handling and Indexing
def process_uploaded_file(uploaded_file):
    """Handle the uploaded file, process it and create an index."""
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        file_key = f"{session_id}-{uploaded_file.name}"
        st.write("Indexing your document...")

        if file_key not in st.session_state.get("file_cache", {}):
            loader = SimpleDirectoryReader(
                input_dir=temp_dir, required_exts=[".pdf"], recursive=True
            )
            docs = loader.load_data()

            llm = load_llm()
            embed_model = HuggingFaceEmbedding(
                model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                trust_remote_code=True,
            )

            Settings.embed_model = embed_model
            index = VectorStoreIndex.from_documents(docs, show_progress=True)

            Settings.llm = llm
            query_engine = index.as_query_engine(streaming=True)

            qa_prompt_tmpl = PromptTemplate(
                "Context information is below.\n"
                "---------------------\n"
                "{context_str}\n"
                "---------------------\n"
                "Given the context information above I want you to think step by step to answer the query in a crisp manner, "
                "incase you don't know the answer say 'I don't know!'.\n"
                "Query: {query_str}\n"
                "Answer: "
            )

            query_engine.update_prompts(
                {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
            )

            st.session_state.file_cache[file_key] = query_engine
        else:
            query_engine = st.session_state.file_cache[file_key]

        st.success("Ready to Chat!")
        display_pdf(uploaded_file)
        return query_engine


# Sidebar UI
with st.sidebar:
    st.header("Add Your Documents!")
    uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf")

    if uploaded_file:
        try:
            query_engine = process_uploaded_file(uploaded_file)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.stop()

# Main UI Layout
col1, col2 = st.columns([6, 1])

with col1:
    st.header("Chat with Docs using Llama-3")

with col2:
    st.button("Clear ↺", on_click=reset_chat)

# Chat Display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("What's up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        streaming_response = query_engine.query(prompt)
        for chunk in streaming_response.response_gen:
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
