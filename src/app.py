import streamlit as st
from langchain_services.chain_builder import setup_chatbot

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = setup_chatbot()
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def format_source_documents(source_docs):
    """Format source documents into a clickable link"""
    if not source_docs or len(source_docs) == 0:
        return ""
    
    # Get the most relevant source (first one)
    doc = source_docs[0]
    
    if hasattr(doc, 'metadata') and 'source' in doc.metadata:
        # Extract only the filename without the path
        filename = doc.metadata['source'].split('\\')[-1]
        # Create a relative path for the link
        file_path = f"data/{filename}"
        return f'Read More Here: <a href="{file_path}" target="_blank"> {filename}</a>'
    
    return ""

def should_show_sources(response):
    """
    Determine if sources should be shown based on the response content
    """
    greeting_patterns = [
        "@atcmarket.com",
        "hey", "hi", "hello", 
        "bye", "goodbye", "thanks", "thank you",
        "good morning", "good afternoon", "good evening", "good night",
        "how can i assist you", "customer assistant at atcmarket"
    ]
    
    response_lower = response.lower()
    return not any(pattern in response_lower for pattern in greeting_patterns)

def main():
    """Main function to run the Streamlit web interface"""
    st.set_page_config(
        page_title="ATC Market Assistant",
        page_icon="🏪",
        layout="centered"
    )

    st.header("🏪 ATC Market Assistant")
    initialize_session_state()

    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if (message["role"] == "assistant" and 
                "sources" in message and 
                message["sources"] and 
                should_show_sources(message["content"])):
                st.markdown(message["sources"], unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("How can I help you today?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get chatbot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.chatbot.invoke({"question": prompt})
                    response = result["answer"]
                    sources = format_source_documents(result.get("source_documents", []))
                    
                    st.markdown(response)
                    if sources and should_show_sources(response):
                        st.markdown(sources, unsafe_allow_html=True)
                    
                    # Save message with sources
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response,
                        "sources": sources if should_show_sources(response) else ""
                    })
                except Exception as e:
                    error_message = f"An error occurred. Please try again or contact support. Error: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_message
                    })

if __name__ == "__main__":
    main()