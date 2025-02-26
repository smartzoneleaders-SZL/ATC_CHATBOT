from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

def load_documents(directory_path):
    """
    Load PDF documents from the specified directory
    
    Args:
        directory_path (str): Path to directory containing PDF files
    
    Returns:
        list: List of loaded Document objects
    """
    loader = DirectoryLoader(
        directory_path,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    return loader.load()

def split_documents(documents):
    """
    Split documents into smaller chunks
    
    Args:
        documents (list): List of Document objects
    
    Returns:
        list: List of text chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_documents(documents)