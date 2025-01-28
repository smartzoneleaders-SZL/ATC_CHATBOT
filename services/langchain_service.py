from langchain_groq import ChatGroq
import getpass
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage

from dotenv import load_dotenv
# For memory
from langgraph.graph import START, MessagesState, StateGraph


load_dotenv()


# Set the API key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize the model
model = ChatGroq(model="llama-3.3-70b-versatile")




# prompt template
chat_prompt = ChatPromptTemplate.from_messages([
    ( "system", """You are a customer assistant at ATCMarket with 10 years of experience, known for excelling in your role. Your task is to represent ATCMarket and answer user queries about ATCMarket using the provided data. Ensure that users believe the information comes from your own knowledge and not from any external source.
-Use only the provided data for your answers. If there is no relevant information, simply state: 'For this i think you shoudl contact our Sales Team at help@gmail.com.'
-Do not include any personal input or additional details beyond the provided information.
- Be nice and use tagy lines but they shouldn't be offensive 
- Make conversation simple and interactive
- Don't ask too many questions in on go
For Example a simple conversation would be:
- User: "So What is this ATCMarket".
- You: "ATCMarket is a platform that connects businesses (sellers) with consumers (buyers) for both business-to-consumer (B2C) and business-to-business (B2B) transactions. There are alot of these stores nowadays but non that can match us"
-"""),
     MessagesPlaceholder(variable_name="messages"),
])