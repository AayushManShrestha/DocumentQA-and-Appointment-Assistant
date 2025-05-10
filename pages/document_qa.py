import streamlit as st
from langchain_core.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool
from langchain_core.messages import AIMessage, HumanMessage

from utils.document_processor import process_documents
from config.llm import llm

# Helper: Initialize session state
def initialize_state():
    if "qa_messages" not in st.session_state:
        st.session_state.qa_messages = []
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "last_uploaded_files" not in st.session_state:
        st.session_state.last_uploaded_files = []  # Track uploaded files to avoid reprocessing

# UI for document uploading
def document_qa_ui():
    with st.sidebar:
        st.subheader("Upload your documents")
        files = st.file_uploader("Select PDF, DOCX, or TXT files", type=["pdf", "docx", "txt"], accept_multiple_files=True)

        # Only process files if not already processed or if new files are uploaded
        if files:
            # Convert file names to a list to detect change
            uploaded_names = sorted([f.name for f in files])

            # Check if files are new or different from the last uploaded set
            if st.session_state.last_uploaded_files != uploaded_names:
                with st.spinner("Processing documents..."):
                    st.session_state.vector_store = process_documents(files)
                    st.session_state.last_uploaded_files = uploaded_names  # Update last uploaded files
                    st.success("Documents processed successfully!")

# Helper: Creates the document QA tool when vector store is ready
def get_tools():
    if st.session_state.vector_store:
        doc_tool = create_retriever_tool(
            st.session_state.vector_store.as_retriever(),
            name="document_qa",
            description="Answer questions based on uploaded documents."
        )
        return [doc_tool]
    return []

def main():
    st.title("Document Assistant")

    # Initialize states
    initialize_state()

    # Show uploader
    document_qa_ui()

    # Get tools if documents are processed
    tools = get_tools()

    # Exit early if tools not ready
    if not tools:
        st.info("Please upload documents to start asking questions.")
        return

    # Prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that answers questions from uploaded documents."),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad")
    ])

    # Set up agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)

    # Show chat history
    for msg in st.session_state.qa_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask me anything about the uploaded documents...")
    if user_input:
        st.session_state.qa_messages.append({"role": "user", "content": user_input})
        try:
            response = executor.invoke({"input": user_input})
            st.session_state.qa_messages.append({"role": "assistant", "content": response["output"]})
        except Exception as e:
            st.session_state.qa_messages.append({"role": "assistant", "content": f"Something went wrong: {e}"})

        st.rerun()


if __name__ == "__main__":
    main()