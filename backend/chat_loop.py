
from pdf_loader import build_qa_chain

qa_chain = build_qa_chain()

query = ""

while query.lower() != "exit":
    query = input("Enter your question related to the pdf: ")

    if query.lower() == "exit":
        break

    response = qa_chain.invoke({"query" :query} )   # store result

    print("\nAnswer:\n", response)
    print("\nSources")
    for doc in response["source_documents"]:
        print(f"page : {doc.metadata.get('page' , 'N/A')}")

print("Exiting the program.")