from docx import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Step 1: Extract QA Pairs from a Single Word Document
def extract_qa_from_docx(file_path):
    """
    Extracts question-answer pairs from a Word file with "QUESTION:" and "ANSWER:" format.
    """
    doc = Document(file_path)
    qa_pairs = []
    current_question = None

    for para in doc.paragraphs:
        text = para.text.strip()
        if text.startswith("QUESTION:"):
            current_question = text[len("QUESTION:"):].strip()  # Remove "QUESTION:" prefix
        elif text.startswith("ANSWER:") and current_question:
            answer = text[len("ANSWER:"):].strip()  # Remove "ANSWER:" prefix
            qa_pairs.append(f"QUESTION: {current_question} ANSWER: {answer}")
            current_question = None  # Reset for the next pair

    return qa_pairs

# Step 2: Extract QA Pairs from the Word Document
print("Moving to step2")
file_path = "../data/Chatbot Preprocessed Questions.docx"  
all_sections = extract_qa_from_docx(file_path)

if not all_sections:
    print("No QA pairs found in the document!")
else:
    print(f"Extracted {len(all_sections)} QA pairs.")

# Step 3: Initialize QA-Optimized Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1")

# Step 4: Create FAISS Index
faiss_index = FAISS.from_texts(
    texts=all_sections,  # Pass the extracted QA pairs
    embedding=embeddings
)

# Step 5: Save Faiss Index Locally
faiss_index.save_local("faiss_index")
print("FAISS index saved successfully!")