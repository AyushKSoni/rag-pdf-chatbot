from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.pdf_loader import build_qa_chain
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load RAG pipeline once (important)
qa_chain = build_qa_chain()








# @app.get("/")
# def home():
#     return {"message": "RAG PDF Chatbot API is running"}


# @app.get("/ask")
# def ask_question(query: str):
#     response = qa_chain.invoke({"query": query})
#     return {
#         "answer": response["result"],
#         "sources": [
#             doc.metadata.get("source", "unknown")
#             for doc in response["source_documents"]
#         ]
#     }

@app.get("/ask")
async def ask_question(query: str):  # Added 'async'
    try:
        # Use 'await' and 'ainvoke' for async execution
        response = await qa_chain.ainvoke({"query": query}) 
        
        return {
            "answer": response["result"],
            "sources": [
                doc.metadata.get("source", "unknown") 
                for doc in response["source_documents"]
            ]
        }
    except Exception as e:
        # This will show you the ACTUAL error in the Swagger response
        return {"error": str(e)}
    