import os

from langchain_community import embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate


def build_qa_chain():

    # Load PDF
    loader = PyPDFLoader("uploads/DA_2026_Syllabus.pdf")
    documents = loader.load()

    print(f"Loaded {len(documents)} pages")

    # Split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Chunks Created = {len(chunks)}")

    # Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # Vector DB
    # vectorStore = FAISS.from_documents(chunks, embeddings)
    # print("Vector Store Created")
    # retriever = vectorStore.as_retriever(search_kwargs={"k": 3})

    # vectorStore.save_local("faiss_index")
    # import os
    # if os.path.exists("faiss_index"):
    #     print("Loading existing FAISS index...")
    #     # Add the flag here:
    #     vectorStore = FAISS.load_local(
    #         "faiss_index", 
    #         embeddings, 
    #         allow_dangerous_deserialization=True
    #     )
    # else:
    #     print("Creating new FAISS index...")
    #     vectorStore = FAISS.from_documents(chunks, embeddings)
    #     vectorStore.save_local("faiss_index")
    
    
    
    
    # Check if index exists
    if os.path.exists("faiss_index"):
        print("Loading existing FAISS index...")
        vectorStore = FAISS.load_local(
            "faiss_index",
            embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        print("Creating new FAISS index...")
        vectorStore = FAISS.from_documents(chunks, embeddings)
        vectorStore.save_local("faiss_index")

    # NOW create retriever (after vectorStore is final)
    retriever = vectorStore.as_retriever(search_kwargs={"k": 3})
    
    # LLM
    llm = Ollama(model="llama3")
    
    # prompt template
    prompt_template = """
    You are a helpful assistant answering questions from a PDF document.

    Use only the provided context to answer.

    If the answer is not present in the context, say:
    "I could not find that information in the PDF."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    # RAG chain
    query_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    #     chain_type_kwargs={
    #     "prompt": prompt
    # }
    )

    return query_chain