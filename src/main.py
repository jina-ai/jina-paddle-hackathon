from jina import Executor, requests, DocumentArray, Document, Deployment


class MyExecutor(Executor):
    @requests
    def foo(self, docs, **kwargs):
        for d in docs:
            d.text = 'hello world'


with Deployment(uses=MyExecutor) as dep:
    response_docs = dep.post(
        on='/', inputs=DocumentArray([Document(text='hello')]))
    print(f'Text: {response_docs[0].text}')
