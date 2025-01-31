from docx import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# Extract QA Pairs from a Word file with "QUESTION:" and "ANSWER:" format.
def extract_qa_from_docx(file_path):
    doc = Document(file_path)
    qa_pairs = []
    current_question = None
    current_answer = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if text.startswith("QUESTION:"):
            if current_question and current_answer:
                qa_pairs.append(f"QUESTION: {current_question} ANSWER: {' '.join(current_answer)}")
            current_question = text[len("QUESTION:"):].strip()
            current_answer = []
        elif text.startswith("ANSWER:"):
            if current_question:
                current_answer.append(text[len("ANSWER:"):].strip())
            else:
                current_answer = [text[len("ANSWER:"):].strip()]
        else:
            if current_answer:
                current_answer.append(text)

    if current_question and current_answer:
        qa_pairs.append(f"QUESTION: {current_question} ANSWER: {' '.join(current_answer)}")
        
    return qa_pairs

# Extract QA pairs from the Word document.
file_path = "../data/Chatbot Preprocessed Questions.docx"  
all_sections = extract_qa_from_docx(file_path)

if not all_sections:
    print("No QA pairs found in the document!")
else:
    print(f"Extracted {len(all_sections)} QA pairs.")

# Initialize QA-Optimized Embeddings.
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1")

# Create FAISS Index for the combined QA pairs.
faiss_index = FAISS.from_texts(
    texts=all_sections,  # Pass the extracted QA pairs
    embedding=embeddings
)

# Save FAISS Index locally.
faiss_index.save_local("faiss_index")
print("FAISS index saved successfully!")
