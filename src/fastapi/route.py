from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# Get project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

from langchain_services.chain_builder import setup_chatbot
import uvicorn
from utils.showsources import format_source_documents, should_show_sources

app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    response: str

class ChatQuery(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    sources: str = ""  # Add sources field with default empty string

# Initialize chatbot with correct data path
chatbot = setup_chatbot(data_dir=os.path.join(PROJECT_ROOT, "data"))


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat", response_model=ChatResponse)
async def chat(query: ChatQuery):
    try:
        result = chatbot.invoke({"question": query.message})
        response = result["answer"]
        
        # Format sources if available, similar to Streamlit app
        sources = ""
        if "source_documents" in result and should_show_sources(response):
            sources = format_source_documents(result.get("source_documents", []))
            
        return ChatResponse(
            response=response,
            sources=sources
        )
    except Exception as e:
        return ChatResponse(
            response=f"An error occurred: {str(e)}",
            sources=""
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

