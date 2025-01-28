import os
import sys

# Set the working directory paths
current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)


from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage, HumanMessage
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from services.langchain_service import chat_prompt, model
import streamlit as st

# Cache the embeddings and FAISS index to load them only once
@st.cache_resource
def load_embeddings_and_index():
    print("Loading FAISS...")
    # Load embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1")
    # Load FAISS index
    faiss_index = FAISS.load_local("../vectorDB/faiss_index", embeddings, allow_dangerous_deserialization=True)
    return embeddings, faiss_index

# Load embeddings and FAISS index
embeddings, faiss_index = load_embeddings_and_index()

# Initialize Streamlit app
st.title("Your Assistant")

# Initialize LangChain memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to display chat messages in real-time
def display_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Display existing chat history on app rerun
display_chat()

# User query input
if user_query := st.chat_input("Ask"):
    # Add user message to LangChain memory
    st.session_state.memory.chat_memory.add_user_message(user_query)

    # Add user query to chat history for display
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Immediately display the user's message
    with st.chat_message("user"):
        st.markdown(user_query)

    # Perform similarity search with FAISS
    results = faiss_index.similarity_search(user_query, k=10)
    context = "\n".join([result.page_content for result in results])

    # Prepare input for the model
    system_message = f"Information you need to answer is:\n{context}\n"
    user_message = f"User query was: {user_query}"

    # Add assistant's context to memory
    st.session_state.memory.chat_memory.add_ai_message(system_message)

    # Generate a response using the model
    with st.chat_message("assistant"):
        response_container = st.empty()  # Placeholder for streaming response
        full_response = ""

        for chunk in model.stream(chat_prompt.format(messages=st.session_state.memory.chat_memory.messages)):
            full_response += chunk.content
            response_container.markdown(full_response)  # Update streamed content

    # Add assistant response to LangChain memory
    st.session_state.memory.chat_memory.add_ai_message(full_response)

    # Add assistant response to chat history for display
    st.session_state.messages.append({"role": "assistant", "content": full_response})
