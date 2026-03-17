from pdf_loader import build_qa_chain

qa_chain = build_qa_chain()

query = ""

while query.lower() != "exit":
    query = input("Enter your question related to the pdf: ")

    if query.lower() == "exit":
        break

    response = qa_chain.run(query)   # store result

    print("\nAnswer:\n", response)

print("Exiting the program.")