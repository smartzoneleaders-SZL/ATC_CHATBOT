from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.memory import ConversationBufferMemory
from .document_loader import load_documents, split_documents
from .embeddings import create_vector_store
from utils.constants import SYSTEM_PROMPT

def setup_chatbot():
    """
    Initialize the chatbot with necessary components
    
    Returns:
        ConversationalRetrievalChain: Configured chatbot chain
    """
    documents = load_documents("./data")
    chunks = split_documents(documents)
    vector_store = create_vector_store(chunks)
    
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "Based on the following information: {context}\n\nQuestion: {question}"),
    ])
    
    condense_question_prompt = PromptTemplate.from_template(
        """Given the following conversation and a follow-up input, rephrase the follow-up input to be a standalone question ONLY if it's a question. 
        If it's a greeting or statement, return it as-is.
        
        Chat History:
        {chat_history}
        
        Follow-Up Input: {question}
        Standalone input:"""
    )
    
    llm = ChatGroq(
        temperature=0.3,
        model_name="llama-3.1-8b-instant",
        max_tokens=200
    )
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
        k=2
    )
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": chat_prompt},
        condense_question_prompt=condense_question_prompt,
        return_source_documents=True,
        verbose=True
    )
    
    return chain