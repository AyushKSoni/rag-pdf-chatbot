from langchain_community.document_loaders import PyPDFLoader

# Load the PDF
loader = PyPDFLoader("uploads/DA_2026_Syllabus.pdf")

documents = loader.load()

print(f"Loaded {len(documents)} pages")

# print first 500 characters
# print(documents[0].page_content[:1000])

# splitting into chunks of 1000 characters with 200 characters overlap
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 200
)
chunks = text_splitter.split_documents(documents)
print(f"Chunks Created = {len(chunks)}")

# print(chunks[0].page_content[:1000])

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

#CRATING EMBEDDINGS
embeddings = HuggingFaceEmbeddings(model_name="All-MiniLM-L6-v2")

#create vector database
vectorStore = FAISS.from_documents(chunks,embeddings)

print("Vector Store Created")

retriever = vectorStore.as_retriever(search_kwargs={"k":3})


#asks question and retrieves relevant chunks
query ="Probability and Statistics"

#retreive relevent chunks
results = retriever.get_relevant_documents(query)

print("Top Relevant Chunks:\n ")
for i ,doc in enumerate(results):
    print(f"Chunk {i+1}:")
    print("---------")
    # :\n{doc.page_content[:500]}\n")

from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

#create RAG chain 
query_chain  = RetrievalQA.from_chain_type(llm=llm,
                                            retriever=retriever)

#asks questions
query ="What's document about"
response = query_chain.run(query)

print("Response:\n")
print(response)