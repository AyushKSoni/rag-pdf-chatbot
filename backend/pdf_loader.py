from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama


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
    vectorStore = FAISS.from_documents(chunks, embeddings)
    print("Vector Store Created")

    retriever = vectorStore.as_retriever(search_kwargs={"k": 3})

    # LLM
    llm = Ollama(model="llama3")

    # RAG chain
    query_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )

    return query_chain