from jina import Client, Document, DocumentArray

ppmap = {
    "http": 12345,
    "grpc": 12344,
    "websocket": 12346
}

print("=====================Test calling=====================")

for protocol in ppmap:
    c = Client(port=ppmap[protocol], protocol=protocol)
    response_docs = c.post(on='/', inputs=DocumentArray(
        [Document(text='你好！')]))
    print(f"Test {protocol}:", response_docs[0].text)

print("======================Plato chat======================")

docs = DocumentArray([])
while True:
    docs.append(Document(text=input("我: ")))
    response_docs = c.post(on='/', inputs=docs)
    docs.append(response_docs[0])
    print("Plato: ", response_docs[0].text)
