# ATC Market Assistant Chatbot

A conversational AI assistant built with Streamlit and LangChain that helps customers with queries about ATC Market.

## 🌟 Features

- Interactive chat interface using Streamlit
- Context-aware responses using LangChain
- PDF document processing and retrieval
- Vector-based semantic search using FAISS
- Error handling and graceful fallbacks

## 🛠️ Technologies Used

- Python 3.x
- Streamlit
- LangChain
- FAISS
- Groq LLM
- HuggingFace Embeddings
- PyPDF2

## ⚙️ Installation

1. Clone the repository:

2. Create and activate a virtual environment:
```bash
python -m venv venv
# For Windows
venv\Scripts\activate
# For Unix/MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add:
```env
GROQ_API_KEY=your_groq_api_key_here
```

## 🚀 Running the Application

Using Make:
```bash
make run
```

Or manually:
```bash
cd src
streamlit run app.py
```

To run without any warning: 
```
streamlit run app.py --server.fileWatcherType=none
```

## 📁 Project Structure

```
ATC-Chatbot/
├── data/                   # PDF documents
├── src/
│   ├── langchain_services/
│   │   ├── chain_builder.py
│   │   ├── document_loader.py
│   │   └── embeddings.py
│   ├── utils/
│   │   └── constants.py
│   ├── app.py             # Streamlit interface
│   └── main.py            # CLI interface
├── requirements.txt
├── .env
└── README.md
```

## 💡 Usage

1. Place your PDF documents in the `data/` directory
2. Start the application
3. Access the web interface at `http://localhost:8501`
4. Start chatting with the assistant!
