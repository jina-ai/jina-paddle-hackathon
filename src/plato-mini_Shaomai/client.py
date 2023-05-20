from jina import Client, DocumentArray, Document

docs = DocumentArray([])
while True:
    docs.append(Document(text=input("我：")))
    c = Client(port=12347)
    response_docs = c.post(on="/generate", inputs=docs)
    docs.append(response_docs[0])
    print("Plato: ", response_docs[0].text)
